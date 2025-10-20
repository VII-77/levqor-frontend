#!/usr/bin/env python3
"""
Phase 41: Payments Command Center
- Lists latest transactions from Stripe
- Processes refunds securely
- Logs all payment events to NDJSON
"""
import os
import sys
import json
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def get_stripe_key():
    """Get Stripe API key based on mode"""
    mode = os.getenv('STRIPE_MODE', 'test')
    if mode == 'live':
        return os.getenv('STRIPE_SECRET_LIVE', '')
    return os.getenv('STRIPE_SECRET_KEY', '')

def list_payments(limit=10):
    """List recent Stripe payments"""
    try:
        import stripe
        stripe.api_key = get_stripe_key()
        
        payments = stripe.PaymentIntent.list(limit=limit)
        
        data = []
        for p in payments.data:
            data.append({
                "id": p.id,
                "amount": p.amount / 100,
                "currency": p.currency,
                "status": p.status,
                "created": datetime.fromtimestamp(p.created).isoformat()
            })
        
        return {"ok": True, "payments": data, "count": len(data)}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def refund_payment(payment_intent_id, amount=None):
    """Process refund for payment intent"""
    try:
        import stripe
        stripe.api_key = get_stripe_key()
        
        kwargs = {"payment_intent": payment_intent_id}
        if amount:
            kwargs["amount"] = int(amount * 100)  # Convert to cents
        
        refund = stripe.Refund.create(**kwargs)
        
        # Log refund
        log_entry = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "event": "refund_processed",
            "refund_id": refund.id,
            "payment_intent": payment_intent_id,
            "amount": refund.amount / 100,
            "status": refund.status
        }
        
        os.makedirs('logs', exist_ok=True)
        with open('logs/payments_live.ndjson', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return {
            "ok": True,
            "refund_id": refund.id,
            "status": refund.status,
            "amount": refund.amount / 100
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    # Test listing payments
    result = list_payments(5)
    print(json.dumps(result, indent=2))
