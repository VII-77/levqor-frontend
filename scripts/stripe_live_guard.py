#!/usr/bin/env python3
"""
Stripe Live Guard - Phase 33
Safe Stripe payment handling with test/live mode toggle
"""
import os
import json
import stripe
from decimal import Decimal

def get_stripe_config():
    """Get Stripe configuration based on mode"""
    mode = os.getenv("STRIPE_MODE", "test")
    
    if mode == "live":
        api_key = os.getenv("STRIPE_SECRET_LIVE")
        webhook_secret = os.getenv("STRIPE_WEBHOOK_LIVE")
    else:
        api_key = os.getenv("STRIPE_SECRET_KEY")
        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    return {
        "mode": mode,
        "api_key": api_key,
        "webhook_secret": webhook_secret
    }

def safe_price(amount_usd):
    """Enforce minimum pricing and rounding"""
    amount = Decimal(str(amount_usd))
    minimum = Decimal("0.50")  # $0.50 minimum
    
    # Reject negative or zero amounts
    if amount <= 0:
        raise ValueError(f"Amount must be positive, got ${amount}")
    
    # Round to 2 decimal places
    amount = amount.quantize(Decimal("0.01"))
    
    # Enforce minimum
    if amount < minimum:
        amount = minimum
    
    return float(amount)

def create_invoice(amount_usd, email, description="EchoPilot Job"):
    """Create Stripe checkout session"""
    config = get_stripe_config()
    
    if not config["api_key"]:
        return {
            "ok": False,
            "error": f"Stripe API key not configured for {config['mode']} mode"
        }
    
    stripe.api_key = config["api_key"]
    
    # Validate and enforce pricing
    safe_amount = safe_price(amount_usd)
    amount_cents = int(safe_amount * 100)
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            customer_email=email,
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": amount_cents,
                    "product_data": {
                        "name": description
                    }
                },
                "quantity": 1
            }],
            success_url="https://echopilotai.replit.app/portal?success=1",
            cancel_url="https://echopilotai.replit.app/portal?cancel=1",
            metadata={
                "mode": config["mode"],
                "original_amount": str(amount_usd),
                "safe_amount": str(safe_amount)
            }
        )
        
        return {
            "ok": True,
            "mode": config["mode"],
            "invoice_link": session.url,
            "session_id": session.id,
            "amount_usd": safe_amount
        }
        
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "mode": config["mode"]
        }

def verify_webhook(payload, signature):
    """Verify Stripe webhook signature"""
    config = get_stripe_config()
    
    if not config["webhook_secret"]:
        return {"ok": False, "error": "Webhook secret not configured"}
    
    try:
        event = stripe.Webhook.construct_event(
            payload, signature, config["webhook_secret"]
        )
        return {"ok": True, "event": event}
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    # Test invoice creation
    result = create_invoice(1.00, "demo@echopilot.ai", "Test Invoice")
    print(json.dumps(result, indent=2))
