"""
Billing Dunning Email Templates
Sends payment failure notifications at Day 1, 7, and 14
"""

import logging
import os

log = logging.getLogger("levqor")


def get_billing_url():
    """Get billing portal URL"""
    base_url = os.environ.get("NEXTAUTH_URL", "https://levqor.ai")
    return f"{base_url}/billing"


def send_billing_email(to: str, subject: str, body: str):
    """
    Send billing email via Resend (or log if not configured)
    
    TODO: Wire up to actual Resend API when RESEND_API_KEY is configured
    """
    resend_key = os.environ.get("RESEND_API_KEY")
    
    if not resend_key:
        log.warning(f"[BILLING_EMAIL] No RESEND_API_KEY - would send to {to}")
        log.info(f"Subject: {subject}")
        log.info(f"Body:\n{body}")
        return
    
    try:
        import requests
        
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {resend_key}",
                "Content-Type": "application/json"
            },
            json={
                "from": "Levqor Billing <billing@levqor.ai>",
                "to": [to],
                "subject": subject,
                "text": body
            },
            timeout=10
        )
        
        if response.status_code == 200:
            log.info(f"[BILLING_EMAIL] Sent to {to}: {subject}")
        else:
            log.error(f"[BILLING_EMAIL] Failed to send to {to}: {response.text}")
            
    except Exception as e:
        log.error(f"[BILLING_EMAIL] Error sending to {to}: {e}")


def send_day1_notice(email: str, customer_name: str = None):
    """Day 1: Payment failed, service still active"""
    name = customer_name or "there"
    billing_url = get_billing_url()
    
    subject = "Levqor: We couldn't process your payment"
    
    body = f"""Hi {name},

We attempted to charge your payment method for your Levqor subscription, but the payment was unsuccessful.

Your service is still active, and we'll automatically retry your payment. However, to avoid any interruption, please update your billing details as soon as possible.

What you should do:
• Update your payment method: {billing_url}
• Ensure your card has sufficient funds
• Check that your card hasn't expired

Your Levqor automation workflows will continue running normally while we work to resolve this.

If you have any questions, please contact us at support@levqor.ai.

Best regards,
The Levqor Team

---
This email is about your Levqor subscription at levqor.ai
"""
    
    send_billing_email(email, subject, body)


def send_day7_notice(email: str, customer_name: str = None):
    """Day 7: Second failure, service at risk"""
    name = customer_name or "there"
    billing_url = get_billing_url()
    
    subject = "Levqor: Service at risk due to payment issue"
    
    body = f"""Hi {name},

We've attempted to charge your payment method multiple times for your Levqor subscription, but all attempts have failed.

⚠️ URGENT: Your service may be paused soon

If we don't receive payment within the next 7 days, your account will be paused and your automation workflows will stop running.

What you need to do NOW:
1. Update your payment method: {billing_url}
2. Verify your billing information is correct
3. Contact your bank if the card is being declined

Time remaining: ~7 days before service interruption

We don't want to pause your workflows! Please take action today to keep your automation running smoothly.

Need help? Contact support@levqor.ai

Best regards,
The Levqor Team

---
This email is about your Levqor subscription at levqor.ai
"""
    
    send_billing_email(email, subject, body)


def send_day14_final_notice(email: str, customer_name: str = None):
    """Day 14: Final notice before suspension"""
    name = customer_name or "there"
    billing_url = get_billing_url()
    
    subject = "Levqor: Your service will be paused"
    
    body = f"""Hi {name},

FINAL NOTICE: Despite multiple payment attempts, we have not been able to charge your payment method for your Levqor subscription.

🚨 YOUR SERVICE WILL BE PAUSED

Your account will be paused within the next 3 days, and all automation workflows will stop running. This means:

• No new workflows will be created
• Existing workflows will be paused
• API access will be suspended
• Scheduled automations will not execute

To prevent service interruption:
1. Update your payment method immediately: {billing_url}
2. Ensure payment is processed within 3 days
3. Contact us if you need assistance: support@levqor.ai

Once payment is received, your service will be restored automatically.

We value your business and want to continue serving you. Please take action today.

Best regards,
The Levqor Team

---
This email is about your Levqor subscription at levqor.ai
If you believe this is an error, please contact support@levqor.ai immediately.
"""
    
    send_billing_email(email, subject, body)


def send_account_suspended_notice(email: str, customer_name: str = None):
    """Account suspended due to repeated payment failures"""
    name = customer_name or "there"
    billing_url = get_billing_url()
    
    subject = "Levqor: Your account has been paused"
    
    body = f"""Hi {name},

Your Levqor account has been paused due to repeated payment failures.

All automation workflows have been stopped and API access has been suspended.

To restore your service:
1. Update your payment method: {billing_url}
2. Ensure payment is processed successfully
3. Your service will resume automatically once payment is received

We're here to help:
If you're experiencing billing issues or need assistance, please contact our support team at support@levqor.ai.

Best regards,
The Levqor Team

---
This email is about your Levqor subscription at levqor.ai
"""
    
    send_billing_email(email, subject, body)
