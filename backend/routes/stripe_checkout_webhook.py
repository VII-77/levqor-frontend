"""
Stripe Checkout Webhook Handler
Handles checkout.session.completed events for DFY and Subscription purchases
"""

from flask import Blueprint, request, jsonify
import logging
import os
import stripe
from datetime import datetime

log = logging.getLogger("levqor.stripe_checkout")

stripe_checkout_bp = Blueprint('stripe_checkout', __name__, url_prefix='/api/webhooks/stripe')

# Initialize Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')


def get_db():
    """Import SQLAlchemy db from app at runtime to avoid circular imports"""
    from app import db
    return db


@stripe_checkout_bp.route('/checkout-completed', methods=['POST'])
def checkout_completed():
    """
    Handle Stripe checkout.session.completed webhook
    
    Verifies Stripe signature, extracts order data, creates DFYOrder record,
    and triggers onboarding automation.
    
    Returns:
        200: {"ok": true, "order_id": 123}
        400: {"ok": false, "error": "..."}
    """
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        # Verify Stripe signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except ValueError as e:
        log.error(f"stripe_checkout.invalid_payload error={str(e)}")
        return jsonify({"ok": False, "error": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError as e:
        log.error(f"stripe_checkout.invalid_signature error={str(e)}")
        return jsonify({"ok": False, "error": "Invalid signature"}), 400
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        try:
            return handle_checkout_session(session)
        except Exception as e:
            log.error(f"stripe_checkout.processing_error error={str(e)}", exc_info=True)
            return jsonify({"ok": False, "error": "Internal server error"}), 500
    
    # Return success for other event types
    return jsonify({"ok": True, "message": "Event received"}), 200


def handle_checkout_session(session):
    """
    Process checkout session and create order
    
    Args:
        session: Stripe checkout session object
    
    Returns:
        JSON response with order_id
    """
    # Extract data from session
    customer_email = session.get('customer_email') or session.get('customer_details', {}).get('email')
    customer_name = session.get('customer_details', {}).get('name', '')
    amount_total = session.get('amount_total', 0)
    currency = session.get('currency', 'gbp')
    
    # Get metadata for plan identification
    metadata = session.get('metadata', {})
    mode = metadata.get('mode', 'unknown')  # 'dfy' or 'subscription'
    plan = metadata.get('plan', 'unknown')  # 'starter', 'professional', 'enterprise', etc.
    term = metadata.get('term', '')  # 'monthly' or 'yearly' for subscriptions
    
    # Determine tier
    tier = f"{plan.upper()}"
    if mode == 'subscription':
        tier = f"{plan.upper()}_{term.upper()}" if term else plan.upper()
    
    log.info(
        f"stripe_checkout.session_completed "
        f"email={customer_email} mode={mode} plan={plan} "
        f"amount={amount_total} currency={currency}"
    )
    
    # Import models
    from backend.models.sales_models import DFYOrder
    
    db = get_db()
    
    # Create order record with proper error handling and rollback
    try:
        order = DFYOrder(
            customer_id=session.get('customer', ''),
            customer_email=customer_email,
            tier=tier,
            status='NEW',
            revisions_left=1,
            checklist_status='PENDING'
        )
        
        db.session.add(order)
        db.session.commit()
        
        log.info(
            f"stripe_checkout.order_created "
            f"order_id={order.id} email={customer_email} tier={tier}"
        )
    except Exception as e:
        db.session.rollback()
        log.error(
            f"stripe_checkout.database_error "
            f"email={customer_email} tier={tier} error={str(e)}",
            exc_info=True
        )
        raise
    
    # Trigger onboarding automation
    try:
        from backend.services.onboarding_automation import handle_new_order
        handle_new_order(order, customer_name)
        
        log.info(
            f"stripe_checkout.automation_triggered "
            f"order_id={order.id}"
        )
    except Exception as e:
        log.error(
            f"stripe_checkout.automation_failed "
            f"order_id={order.id} error={str(e)}", 
            exc_info=True
        )
        # Don't fail the webhook if automation fails
    
    return jsonify({
        "ok": True,
        "order_id": order.id,
        "tier": tier,
        "status": "automation_triggered"
    }), 200


@stripe_checkout_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "ok": True,
        "service": "stripe_checkout_webhook",
        "endpoint": "/api/webhooks/stripe/checkout-completed"
    }), 200
