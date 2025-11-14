"""
Stripe Dunning System - Payment Recovery Module
Handles automated email sequences for failed subscription payments
"""
import os
import json
import logging
from datetime import datetime, timedelta
from uuid import uuid4
import requests

from backend.billing.config import (
    DUNNING_ENABLED,
    DUNNING_SCHEDULE_DAYS,
    RESEND_API_KEY,
    FROM_EMAIL,
    BILLING_PORTAL_URL
)

log = logging.getLogger("levqor.dunning")


def compute_scheduled_time(failure_time, days_offset):
    """
    Compute when a dunning email should be scheduled
    
    Args:
        failure_time: datetime or ISO8601 string of payment failure
        days_offset: int (1, 7, or 14 days)
    
    Returns:
        ISO8601 timestamp string
    """
    if isinstance(failure_time, str):
        failure_dt = datetime.fromisoformat(failure_time.replace('Z', '+00:00'))
    else:
        failure_dt = failure_time
    
    scheduled_dt = failure_dt + timedelta(days=days_offset)
    return scheduled_dt.isoformat()


def create_dunning_events(db_conn, stripe_customer_id, stripe_subscription_id, 
                          invoice_id, email, plan, failure_time_utc):
    """
    Create dunning email events for the payment failure schedule
    
    Args:
        db_conn: SQLite database connection
        stripe_customer_id: Stripe customer ID (cus_xxx)
        stripe_subscription_id: Stripe subscription ID (sub_xxx)
        invoice_id: Stripe invoice ID (in_xxx)
        email: Customer email address
        plan: Plan name (e.g., "Growth Monthly")
        failure_time_utc: ISO8601 timestamp of payment failure
    
    Returns:
        list of created event IDs
    """
    
    # Check if events already exist for this invoice
    cursor = db_conn.execute(
        "SELECT COUNT(*) FROM billing_dunning_events WHERE invoice_id = ?",
        (invoice_id,)
    )
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        log.info(f"dunning.events_already_exist invoice_id={invoice_id} count={existing_count}")
        return []
    
    created_ids = []
    now_iso = datetime.utcnow().isoformat()
    
    for attempt_number in [1, 2, 3]:
        days_offset = DUNNING_SCHEDULE_DAYS[attempt_number - 1]
        scheduled_for = compute_scheduled_time(failure_time_utc, days_offset)
        
        event_id = str(uuid4())
        
        db_conn.execute("""
            INSERT INTO billing_dunning_events (
                id, created_at, updated_at,
                stripe_customer_id, stripe_subscription_id, invoice_id,
                email, plan, attempt_number, scheduled_for, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
        """, (
            event_id, now_iso, now_iso,
            stripe_customer_id, stripe_subscription_id, invoice_id,
            email, plan, attempt_number, scheduled_for
        ))
        
        created_ids.append(event_id)
        
        log.info(
            f"dunning.schedule_created event_id={event_id} "
            f"customer={stripe_customer_id} subscription={stripe_subscription_id} "
            f"invoice={invoice_id} attempt={attempt_number} scheduled_for={scheduled_for}"
        )
    
    db_conn.commit()
    return created_ids


def cancel_pending_dunning_events(db_conn, stripe_subscription_id):
    """
    Mark all pending dunning events as 'skipped' when subscription recovers
    
    Args:
        db_conn: SQLite database connection
        stripe_subscription_id: Stripe subscription ID that recovered
    
    Returns:
        int: number of events cancelled
    """
    now_iso = datetime.utcnow().isoformat()
    
    cursor = db_conn.execute("""
        UPDATE billing_dunning_events
        SET status = 'skipped', updated_at = ?
        WHERE stripe_subscription_id = ?
        AND status = 'pending'
        AND sent_at IS NULL
    """, (now_iso, stripe_subscription_id))
    
    count = cursor.rowcount
    db_conn.commit()
    
    log.info(
        f"dunning.cancelled_pending subscription={stripe_subscription_id} count={count}"
    )
    
    return count


def render_dunning_email(attempt_number, plan_name, amount, pause_date=None):
    """
    Load and render dunning email template
    
    Args:
        attempt_number: 1, 2, or 3
        plan_name: Subscription plan name
        amount: Formatted amount string (e.g., "£29.00")
        pause_date: Date when service will pause (for attempt 2)
    
    Returns:
        dict with 'subject' and 'body' keys
    """
    template_path = f"templates/email/dunning_{attempt_number}.txt"
    
    if not os.path.exists(template_path):
        log.error(f"dunning.template_missing path={template_path}")
        return None
    
    with open(template_path, 'r') as f:
        content = f.read()
    
    # Extract subject from first line (# Subject: ...)
    lines = content.split('\n')
    subject = lines[0].replace('# Subject:', '').strip()
    body = '\n'.join(lines[2:])  # Skip subject and blank line
    
    # Replace placeholders
    body = body.replace('{plan_name}', plan_name or 'Levqor Subscription')
    body = body.replace('{amount}', amount)
    
    if pause_date:
        body = body.replace('{pause_date}', pause_date)
    
    return {
        'subject': subject,
        'body': body
    }


def send_dunning_email(email_address, subject, body):
    """
    Send dunning email via Resend
    
    Args:
        email_address: Recipient email
        subject: Email subject line
        body: Plain text email body
    
    Returns:
        dict: {'ok': bool, 'message_id': str or None, 'error': str or None}
    """
    if not RESEND_API_KEY:
        log.error("dunning.email_error error='RESEND_API_KEY not configured'")
        return {'ok': False, 'error': 'RESEND_API_KEY not configured'}
    
    try:
        response = requests.post(
            'https://api.resend.com/emails',
            headers={
                'Authorization': f'Bearer {RESEND_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'from': FROM_EMAIL,
                'to': email_address,
                'subject': subject,
                'text': body
            },
            timeout=10
        )
        
        if response.status_code in (200, 201):
            data = response.json()
            message_id = data.get('id')
            log.info(f"dunning.email_sent to={email_address} message_id={message_id}")
            return {'ok': True, 'message_id': message_id, 'error': None}
        else:
            error_msg = response.text[:200]
            log.error(
                f"dunning.email_error to={email_address} "
                f"status={response.status_code} error={error_msg}"
            )
            return {'ok': False, 'message_id': None, 'error': error_msg}
            
    except Exception as e:
        log.error(f"dunning.email_exception to={email_address} error={str(e)}")
        return {'ok': False, 'message_id': None, 'error': str(e)}


def run_dunning_cycle(db_conn, now_utc=None):
    """
    Process all pending dunning events that are due to be sent
    
    Args:
        db_conn: SQLite database connection
        now_utc: datetime (defaults to current UTC time)
    
    Returns:
        dict with 'processed', 'sent', 'skipped', 'errors' counts
    """
    if now_utc is None:
        now_utc = datetime.utcnow()
    
    now_iso = now_utc.isoformat()
    
    log.info(f"dunning.cycle_start time={now_iso} enabled={DUNNING_ENABLED}")
    
    # Query pending events that are due
    cursor = db_conn.execute("""
        SELECT id, stripe_customer_id, stripe_subscription_id, invoice_id,
               email, plan, attempt_number, scheduled_for
        FROM billing_dunning_events
        WHERE status = 'pending'
        AND sent_at IS NULL
        AND scheduled_for <= ?
        ORDER BY scheduled_for ASC
    """, (now_iso,))
    
    events = cursor.fetchall()
    
    stats = {
        'processed': len(events),
        'sent': 0,
        'skipped': 0,
        'errors': 0
    }
    
    for row in events:
        event_id, customer_id, subscription_id, invoice_id, email, plan, attempt, scheduled = row
        
        log.info(
            f"dunning.processing event_id={event_id} customer={customer_id} "
            f"attempt={attempt} scheduled={scheduled}"
        )
        
        # Safety check: Skip if dunning is disabled
        if not DUNNING_ENABLED:
            log.info(
                f"dunning.skipped event_id={event_id} reason='DUNNING_ENABLED=False'"
            )
            stats['skipped'] += 1
            continue
        
        # Render email template
        # Calculate pause date (7 days from now for attempt 2)
        pause_date = None
        if attempt == 2:
            pause_dt = now_utc + timedelta(days=7)
            pause_date = pause_dt.strftime('%B %d, %Y')
        
        # Format amount (would come from invoice in production)
        amount = "£29.00"  # Placeholder - should fetch from Stripe invoice
        
        email_content = render_dunning_email(attempt, plan, amount, pause_date)
        
        if not email_content:
            log.error(f"dunning.template_error event_id={event_id} attempt={attempt}")
            db_conn.execute("""
                UPDATE billing_dunning_events
                SET status = 'error', error_message = 'Template not found', updated_at = ?
                WHERE id = ?
            """, (now_iso, event_id))
            stats['errors'] += 1
            continue
        
        # Send email
        result = send_dunning_email(email, email_content['subject'], email_content['body'])
        
        if result['ok']:
            db_conn.execute("""
                UPDATE billing_dunning_events
                SET status = 'sent', sent_at = ?, updated_at = ?
                WHERE id = ?
            """, (now_iso, now_iso, event_id))
            stats['sent'] += 1
            
            log.info(
                f"dunning.email_sent event_id={event_id} customer={customer_id} "
                f"attempt={attempt} message_id={result.get('message_id')}"
            )
        else:
            error_msg = result.get('error', 'Unknown error')[:500]
            db_conn.execute("""
                UPDATE billing_dunning_events
                SET status = 'error', error_message = ?, updated_at = ?
                WHERE id = ?
            """, (error_msg, now_iso, event_id))
            stats['errors'] += 1
            
            log.error(
                f"dunning.error event_id={event_id} customer={customer_id} "
                f"attempt={attempt} error={error_msg}"
            )
    
    db_conn.commit()
    
    log.info(
        f"dunning.cycle_complete processed={stats['processed']} "
        f"sent={stats['sent']} skipped={stats['skipped']} errors={stats['errors']}"
    )
    
    return stats


def handle_payment_failed(db_conn, stripe_event):
    """
    Handle invoice.payment_failed webhook event
    
    Args:
        db_conn: SQLite database connection
        stripe_event: Parsed Stripe event object
    
    Returns:
        bool: True if handled successfully
    """
    invoice = stripe_event.get('data', {}).get('object', {})
    
    customer_id = invoice.get('customer')
    subscription_id = invoice.get('subscription')
    invoice_id = invoice.get('id')
    customer_email = invoice.get('customer_email')
    amount_due = invoice.get('amount_due', 0)
    currency = invoice.get('currency', 'gbp')
    
    # Get plan name from subscription metadata (or use generic)
    plan_name = invoice.get('lines', {}).get('data', [{}])[0].get('description', 'Levqor Subscription')
    
    log.info(
        f"dunning.payment_failed customer={customer_id} subscription={subscription_id} "
        f"invoice={invoice_id} amount={amount_due} currency={currency}"
    )
    
    if not DUNNING_ENABLED:
        log.info(
            f"dunning.disabled customer={customer_id} invoice={invoice_id} "
            "message='Dunning disabled, recording payment_failed only'"
        )
        return True
    
    # Create dunning event schedule
    failure_time = datetime.utcnow().isoformat()
    
    created_events = create_dunning_events(
        db_conn, customer_id, subscription_id, invoice_id,
        customer_email, plan_name, failure_time
    )
    
    log.info(
        f"dunning.events_created customer={customer_id} invoice={invoice_id} "
        f"count={len(created_events)}"
    )
    
    return True


def handle_subscription_updated(db_conn, stripe_event):
    """
    Handle customer.subscription.updated webhook event
    
    Args:
        db_conn: SQLite database connection
        stripe_event: Parsed Stripe event object
    
    Returns:
        bool: True if handled successfully
    """
    subscription = stripe_event.get('data', {}).get('object', {})
    subscription_id = subscription.get('id')
    status = subscription.get('status')
    
    log.info(
        f"dunning.subscription_updated subscription={subscription_id} status={status}"
    )
    
    # If subscription becomes active again, cancel pending dunning emails
    if status == 'active':
        cancelled_count = cancel_pending_dunning_events(db_conn, subscription_id)
        
        if cancelled_count > 0:
            log.info(
                f"dunning.recovery subscription={subscription_id} "
                f"cancelled_emails={cancelled_count}"
            )
    
    return True
