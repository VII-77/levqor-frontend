"""
Internal billing webhook endpoints
Called by frontend Stripe webhook handler after signature verification
"""
from flask import Blueprint, request, jsonify
import logging
from datetime import datetime

log = logging.getLogger("levqor.billing_webhooks")

billing_webhooks_bp = Blueprint('billing_webhooks', __name__, url_prefix='/api/internal/billing')


def get_db():
    """Import get_db from run.py at runtime to avoid circular imports"""
    from run import get_db as _get_db
    return _get_db()


def verify_internal_secret(request):
    """Verify internal API secret for secure communication"""
    import os
    expected_secret = os.environ.get('INTERNAL_API_SECRET', 'dev_secret')
    provided_secret = request.headers.get('X-Internal-Secret', '')
    
    if provided_secret != expected_secret:
        log.warning(f"billing_webhook.unauthorized_request ip={request.remote_addr}")
        return False
    return True


@billing_webhooks_bp.route('/payment-failed', methods=['POST'])
def payment_failed():
    """
    Handle invoice.payment_failed webhook from Stripe
    
    Expected JSON body:
    {
        "event": {
            "id": "in_xxx",
            "customer": "cus_xxx",
            "subscription": "sub_xxx",
            "customer_email": "user@example.com",
            "amount_due": 2900,
            "currency": "gbp",
            "lines": {...}
        }
    }
    
    Returns:
        200: {"ok": true, "events_created": 3}
        400: {"ok": false, "error": "..."}
        401: {"ok": false, "error": "unauthorized"}
    """
    if not verify_internal_secret(request):
        return jsonify({"ok": False, "error": "unauthorized"}), 401
    
    try:
        data = request.get_json() or {}
        invoice = data.get('event', {})
        
        customer_id = invoice.get('customer')
        subscription_id = invoice.get('subscription')
        invoice_id = invoice.get('id')
        customer_email = invoice.get('customer_email')
        amount_due = invoice.get('amount_due', 0)
        currency = invoice.get('currency', 'gbp')
        
        # Get plan name from line items
        lines = invoice.get('lines', {}).get('data', [])
        plan_name = lines[0].get('description', 'Levqor Subscription') if lines else 'Levqor Subscription'
        
        log.info(
            f"billing_webhook.payment_failed customer={customer_id} "
            f"subscription={subscription_id} invoice={invoice_id} "
            f"amount={amount_due} currency={currency}"
        )
        
        if not all([customer_id, subscription_id, invoice_id, customer_email]):
            return jsonify({
                "ok": False,
                "error": "Missing required fields"
            }), 400
        
        # Import dunning system
        from backend.billing.dunning import create_dunning_events, handle_payment_failed
        
        db = get_db()
        
        # Create dunning email schedule (Day 1, 7, 14)
        failure_time = datetime.utcnow().isoformat()
        
        created_events = create_dunning_events(
            db, customer_id, subscription_id, invoice_id,
            customer_email, plan_name, failure_time
        )
        
        log.info(
            f"billing_webhook.dunning_scheduled customer={customer_id} "
            f"invoice={invoice_id} events_created={len(created_events)}"
        )
        
        return jsonify({
            "ok": True,
            "events_created": len(created_events),
            "event_ids": created_events
        }), 200
        
    except Exception as e:
        log.error(f"billing_webhook.payment_failed_error error={str(e)}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


@billing_webhooks_bp.route('/payment-succeeded', methods=['POST'])
def payment_succeeded():
    """
    Handle invoice.paid webhook from Stripe
    
    Expected JSON body:
    {
        "event": {
            "id": "in_xxx",
            "customer": "cus_xxx",
            "subscription": "sub_xxx",
            "customer_email": "user@example.com"
        }
    }
    
    Returns:
        200: {"ok": true, "cancelled_events": 2}
        400: {"ok": false, "error": "..."}
        401: {"ok": false, "error": "unauthorized"}
    """
    if not verify_internal_secret(request):
        return jsonify({"ok": False, "error": "unauthorized"}), 401
    
    try:
        data = request.get_json() or {}
        invoice = data.get('event', {})
        
        customer_id = invoice.get('customer')
        subscription_id = invoice.get('subscription')
        invoice_id = invoice.get('id')
        
        log.info(
            f"billing_webhook.payment_succeeded customer={customer_id} "
            f"subscription={subscription_id} invoice={invoice_id}"
        )
        
        if not subscription_id:
            return jsonify({
                "ok": False,
                "error": "Missing subscription_id"
            }), 400
        
        # Import dunning system
        from backend.billing.dunning import cancel_pending_dunning_events
        
        db = get_db()
        
        # Cancel any pending dunning emails
        cancelled_count = cancel_pending_dunning_events(db, subscription_id)
        
        log.info(
            f"billing_webhook.dunning_cancelled customer={customer_id} "
            f"subscription={subscription_id} cancelled={cancelled_count}"
        )
        
        return jsonify({
            "ok": True,
            "cancelled_events": cancelled_count
        }), 200
        
    except Exception as e:
        log.error(f"billing_webhook.payment_succeeded_error error={str(e)}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


@billing_webhooks_bp.route('/subscription-updated', methods=['POST'])
def subscription_updated():
    """
    Handle customer.subscription.updated webhook from Stripe
    
    Expected JSON body:
    {
        "event": {
            "id": "sub_xxx",
            "customer": "cus_xxx",
            "status": "active"
        }
    }
    
    Returns:
        200: {"ok": true}
        401: {"ok": false, "error": "unauthorized"}
    """
    if not verify_internal_secret(request):
        return jsonify({"ok": False, "error": "unauthorized"}), 401
    
    try:
        data = request.get_json() or {}
        subscription = data.get('event', {})
        
        subscription_id = subscription.get('id')
        customer_id = subscription.get('customer')
        status = subscription.get('status')
        
        log.info(
            f"billing_webhook.subscription_updated subscription={subscription_id} "
            f"customer={customer_id} status={status}"
        )
        
        # If subscription becomes active, cancel pending dunning
        if status == 'active':
            from backend.billing.dunning import cancel_pending_dunning_events
            
            db = get_db()
            cancelled_count = cancel_pending_dunning_events(db, subscription_id)
            
            if cancelled_count > 0:
                log.info(
                    f"billing_webhook.recovery subscription={subscription_id} "
                    f"cancelled_emails={cancelled_count}"
                )
        
        return jsonify({"ok": True}), 200
        
    except Exception as e:
        log.error(f"billing_webhook.subscription_updated_error error={str(e)}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


@billing_webhooks_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint for internal billing webhooks"""
    return jsonify({
        "ok": True,
        "service": "billing_webhooks",
        "endpoints": [
            "/api/internal/billing/payment-failed",
            "/api/internal/billing/payment-succeeded",
            "/api/internal/billing/subscription-updated"
        ]
    }), 200
