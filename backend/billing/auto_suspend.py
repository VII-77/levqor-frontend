"""
Auto-Suspend System for Failed Payments
Automatically suspends user access after final dunning attempt fails
"""
import logging
from datetime import datetime

log = logging.getLogger("levqor.auto_suspend")


def suspend_user_access(db_conn, user_email, stripe_customer_id, stripe_subscription_id, reason="payment_failed"):
    """
    Suspend user access to workflows and API after payment failure
    
    Args:
        db_conn: Database connection
        user_email: User's email address
        stripe_customer_id: Stripe customer ID
        stripe_subscription_id: Stripe subscription ID
        reason: Reason for suspension (default: payment_failed)
    
    Returns:
        dict: {'ok': bool, 'suspended': bool, 'user_id': str or None}
    """
    now_iso = datetime.utcnow().isoformat()
    
    try:
        # Get user from database
        cursor = db_conn.execute(
            "SELECT id, email, status FROM users WHERE email = ?",
            (user_email,)
        )
        user = cursor.fetchone()
        
        if not user:
            log.warning(f"auto_suspend.user_not_found email={user_email}")
            return {'ok': False, 'suspended': False, 'user_id': None}
        
        user_id, email, current_status = user
        
        # Check if already suspended
        if current_status == 'suspended':
            log.info(f"auto_suspend.already_suspended user_id={user_id} email={email}")
            return {'ok': True, 'suspended': True, 'user_id': user_id}
        
        # Update user status to suspended
        db_conn.execute(
            "UPDATE users SET status = 'suspended', suspended_at = ?, suspension_reason = ? WHERE id = ?",
            (now_iso, reason, user_id)
        )
        
        # Log suspension event
        db_conn.execute("""
            INSERT INTO billing_status_changes (
                id, user_id, stripe_customer_id, stripe_subscription_id,
                old_status, new_status, reason, changed_at, changed_by
            ) VALUES (?, ?, ?, ?, ?, 'suspended', ?, ?, 'system')
        """, (
            f"bsc_{datetime.utcnow().timestamp()}",
            user_id,
            stripe_customer_id,
            stripe_subscription_id,
            current_status or 'active',
            reason,
            now_iso
        ))
        
        db_conn.commit()
        
        log.info(
            f"auto_suspend.suspended user_id={user_id} email={email} "
            f"customer={stripe_customer_id} subscription={stripe_subscription_id} "
            f"reason={reason}"
        )
        
        return {'ok': True, 'suspended': True, 'user_id': user_id}
        
    except Exception as e:
        log.error(f"auto_suspend.error email={user_email} error={str(e)}", exc_info=True)
        return {'ok': False, 'suspended': False, 'user_id': None, 'error': str(e)}


def unsuspend_user_access(db_conn, user_email, stripe_customer_id, stripe_subscription_id):
    """
    Restore user access after successful payment
    
    Args:
        db_conn: Database connection
        user_email: User's email address
        stripe_customer_id: Stripe customer ID
        stripe_subscription_id: Stripe subscription ID
    
    Returns:
        dict: {'ok': bool, 'unsuspended': bool, 'user_id': str or None}
    """
    now_iso = datetime.utcnow().isoformat()
    
    try:
        # Get user from database
        cursor = db_conn.execute(
            "SELECT id, email, status FROM users WHERE email = ?",
            (user_email,)
        )
        user = cursor.fetchone()
        
        if not user:
            log.warning(f"auto_unsuspend.user_not_found email={user_email}")
            return {'ok': False, 'unsuspended': False, 'user_id': None}
        
        user_id, email, current_status = user
        
        # Check if not suspended
        if current_status != 'suspended':
            log.info(f"auto_unsuspend.not_suspended user_id={user_id} email={email} status={current_status}")
            return {'ok': True, 'unsuspended': False, 'user_id': user_id}
        
        # Restore user status to active
        db_conn.execute(
            "UPDATE users SET status = 'active', suspended_at = NULL, suspension_reason = NULL WHERE id = ?",
            (user_id,)
        )
        
        # Log restoration event
        db_conn.execute("""
            INSERT INTO billing_status_changes (
                id, user_id, stripe_customer_id, stripe_subscription_id,
                old_status, new_status, reason, changed_at, changed_by
            ) VALUES (?, ?, ?, ?, 'suspended', 'active', 'payment_succeeded', ?, 'system')
        """, (
            f"bsc_{datetime.utcnow().timestamp()}",
            user_id,
            stripe_customer_id,
            stripe_subscription_id,
            now_iso
        ))
        
        db_conn.commit()
        
        log.info(
            f"auto_unsuspend.restored user_id={user_id} email={email} "
            f"customer={stripe_customer_id} subscription={stripe_subscription_id}"
        )
        
        return {'ok': True, 'unsuspended': True, 'user_id': user_id}
        
    except Exception as e:
        log.error(f"auto_unsuspend.error email={user_email} error={str(e)}", exc_info=True)
        return {'ok': False, 'unsuspended': False, 'user_id': None, 'error': str(e)}


def check_failed_dunning_and_suspend(db_conn):
    """
    Scheduled job: Check for dunning attempts that have all failed (Day 14 sent + failed)
    and auto-suspend those users
    
    Args:
        db_conn: Database connection
    
    Returns:
        dict: {'processed': int, 'suspended': int, 'errors': int}
    """
    log.info("auto_suspend.check_started")
    
    stats = {
        'processed': 0,
        'suspended': 0,
        'errors': 0
    }
    
    try:
        # Find subscriptions where all 3 dunning attempts have been sent
        # and the subscription is still unpaid
        cursor = db_conn.execute("""
            SELECT 
                stripe_customer_id, 
                stripe_subscription_id, 
                email,
                COUNT(*) as attempt_count,
                MAX(sent_at) as last_sent
            FROM billing_dunning_events
            WHERE status = 'sent'
            AND sent_at IS NOT NULL
            GROUP BY stripe_customer_id, stripe_subscription_id, email
            HAVING attempt_count >= 3
        """)
        
        failed_subscriptions = cursor.fetchall()
        stats['processed'] = len(failed_subscriptions)
        
        for row in failed_subscriptions:
            customer_id, subscription_id, email, attempt_count, last_sent = row
            
            log.info(
                f"auto_suspend.candidate customer={customer_id} subscription={subscription_id} "
                f"email={email} attempts={attempt_count} last_sent={last_sent}"
            )
            
            # Check if user is already suspended
            user_cursor = db_conn.execute(
                "SELECT id, status FROM users WHERE email = ?",
                (email,)
            )
            user = user_cursor.fetchone()
            
            if user and user[1] == 'suspended':
                log.info(f"auto_suspend.already_suspended email={email}")
                continue
            
            # Suspend the user
            result = suspend_user_access(
                db_conn, email, customer_id, subscription_id,
                reason="payment_failed_after_3_attempts"
            )
            
            if result['ok'] and result['suspended']:
                stats['suspended'] += 1
            else:
                stats['errors'] += 1
        
        log.info(
            f"auto_suspend.check_complete processed={stats['processed']} "
            f"suspended={stats['suspended']} errors={stats['errors']}"
        )
        
        return stats
        
    except Exception as e:
        log.error(f"auto_suspend.check_error error={str(e)}", exc_info=True)
        stats['errors'] += 1
        return stats


def send_suspension_notification(email_address, suspension_reason, billing_portal_url):
    """
    Send email notification to user when account is suspended
    
    Args:
        email_address: User's email
        suspension_reason: Why the account was suspended
        billing_portal_url: URL to billing portal to resolve issue
    
    Returns:
        bool: True if email sent successfully
    """
    import os
    import requests
    
    resend_api_key = os.environ.get('RESEND_API_KEY')
    from_email = os.environ.get('AUTH_FROM_EMAIL', 'noreply@levqor.ai')
    
    if not resend_api_key:
        log.error("auto_suspend.email_error error='RESEND_API_KEY not configured'")
        return False
    
    subject = "Levqor Account Suspended - Action Required"
    body = f"""Hi there,

We're writing to inform you that your Levqor account has been temporarily suspended due to: {suspension_reason}

Your workflows have been paused and API access has been disabled until this issue is resolved.

To restore your account:
1. Visit your billing portal: {billing_portal_url}
2. Update your payment method
3. Clear any outstanding invoices
4. Your account will be automatically restored within 15 minutes

If you believe this is an error or need assistance, please reply to this email or contact support@levqor.ai.

We're here to help get you back up and running!

Best regards,
The Levqor Team
"""
    
    try:
        response = requests.post(
            'https://api.resend.com/emails',
            headers={
                'Authorization': f'Bearer {resend_api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'from': from_email,
                'to': email_address,
                'subject': subject,
                'text': body
            },
            timeout=10
        )
        
        if response.status_code in (200, 201):
            log.info(f"auto_suspend.notification_sent to={email_address}")
            return True
        else:
            log.error(f"auto_suspend.notification_error status={response.status_code} error={response.text}")
            return False
            
    except Exception as e:
        log.error(f"auto_suspend.notification_exception error={str(e)}")
        return False
