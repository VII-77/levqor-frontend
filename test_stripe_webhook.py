"""
Stripe Webhook Live Test Script
Simulates a Stripe checkout.session.completed event with proper signature
"""

import requests
import json
import time
import hashlib
import hmac
import os

# Configuration
WEBHOOK_URL = "http://localhost:8000/api/webhooks/stripe/checkout-completed"
WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

# Sample checkout session completed event
def create_test_event():
    """Create a realistic checkout.session.completed event"""
    timestamp = int(time.time())
    
    event = {
        "id": f"evt_test_{timestamp}",
        "object": "event",
        "api_version": "2023-10-16",
        "created": timestamp,
        "data": {
            "object": {
                "id": f"cs_test_{timestamp}",
                "object": "checkout.session",
                "amount_total": 9900,  # £99.00 in pence
                "currency": "gbp",
                "customer": f"cus_test_{timestamp}",
                "customer_email": "test@levqor.ai",
                "customer_details": {
                    "email": "test@levqor.ai",
                    "name": "Test Customer"
                },
                "metadata": {
                    "mode": "dfy",
                    "plan": "starter",
                    "source": "webhook_test"
                },
                "payment_status": "paid",
                "status": "complete"
            }
        },
        "livemode": False,
        "pending_webhooks": 1,
        "request": {
            "id": None,
            "idempotency_key": None
        },
        "type": "checkout.session.completed"
    }
    
    return event


def generate_stripe_signature(payload, secret):
    """Generate Stripe signature for webhook verification"""
    timestamp = int(time.time())
    payload_str = json.dumps(payload, separators=(',', ':'))
    
    # Create the signed payload
    signed_payload = f"{timestamp}.{payload_str}"
    
    # Generate signature
    signature = hmac.new(
        secret.encode('utf-8'),
        signed_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Return Stripe-Signature header format
    return f"t={timestamp},v1={signature}"


def test_webhook():
    """Test the webhook endpoint with a simulated event"""
    print("=" * 70)
    print("STRIPE WEBHOOK LIVE TEST")
    print("=" * 70)
    print()
    
    # Check webhook secret
    if not WEBHOOK_SECRET:
        print("❌ ERROR: STRIPE_WEBHOOK_SECRET not found in environment")
        return False
    
    print(f"✓ Webhook URL: {WEBHOOK_URL}")
    print(f"✓ Webhook Secret: {'*' * 10}{WEBHOOK_SECRET[-4:]}")
    print()
    
    # Create test event
    event = create_test_event()
    print("📦 Test Event Created:")
    print(f"   - Type: {event['type']}")
    print(f"   - Customer Email: {event['data']['object']['customer_email']}")
    print(f"   - Amount: £{event['data']['object']['amount_total'] / 100:.2f}")
    print(f"   - Plan: {event['data']['object']['metadata']['plan'].upper()}")
    print(f"   - Mode: {event['data']['object']['metadata']['mode'].upper()}")
    print()
    
    # Generate signature
    signature = generate_stripe_signature(event, WEBHOOK_SECRET)
    
    # Send webhook request
    print("🚀 Sending webhook request...")
    payload = json.dumps(event, separators=(',', ':'))
    
    headers = {
        "Content-Type": "application/json",
        "Stripe-Signature": signature
    }
    
    try:
        response = requests.post(WEBHOOK_URL, data=payload, headers=headers)
        
        print(f"📬 Response Status: {response.status_code}")
        print()
        
        if response.status_code == 200:
            data = response.json()
            print("✅ WEBHOOK ACCEPTED")
            print(f"   Response: {json.dumps(data, indent=2)}")
            
            if data.get("ok"):
                order_id = data.get("order_id")
                tier = data.get("tier")
                print()
                print("=" * 70)
                print("SUCCESS!")
                print("=" * 70)
                print(f"✓ Signature verified")
                print(f"✓ DFYOrder created: ID={order_id}, Tier={tier}")
                print(f"✓ Automation triggered: {data.get('status')}")
                return True
        else:
            print(f"❌ WEBHOOK REJECTED")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def verify_order_created():
    """Query database to verify order was created"""
    print()
    print("=" * 70)
    print("STEP 6: VERIFYING ORDER IN DATABASE")
    print("=" * 70)
    
    try:
        # Import models
        import sys
        sys.path.insert(0, '/home/runner/workspace')
        
        from app import app, db
        from backend.models.sales_models import DFYOrder
        
        with app.app_context():
            # Get all orders
            orders = DFYOrder.query.order_by(DFYOrder.created_at.desc()).limit(5).all()
            
            print(f"\n📋 Recent DFY Orders (last 5):")
            print()
            
            if orders:
                for order in orders:
                    print(f"   Order #{order.id}")
                    print(f"   └─ Email: {order.customer_email}")
                    print(f"   └─ Tier: {order.tier}")
                    print(f"   └─ Status: {order.status}")
                    print(f"   └─ Created: {order.created_at}")
                    print()
                
                latest = orders[0]
                if "test@levqor.ai" in latest.customer_email:
                    print("✅ TEST ORDER FOUND IN DATABASE!")
                    print(f"   Order ID: {latest.id}")
                    print(f"   Tier: {latest.tier}")
                    print(f"   Status: {latest.status}")
                    return True
                else:
                    print("⚠️  Latest order doesn't match test email")
            else:
                print("   (No orders found)")
                
    except Exception as e:
        print(f"❌ Database query error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return False


if __name__ == "__main__":
    # Run webhook test
    webhook_success = test_webhook()
    
    # Verify in database
    if webhook_success:
        time.sleep(1)  # Give DB a moment to commit
        verify_order_created()
    
    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
