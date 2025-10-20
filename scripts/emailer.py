#!/usr/bin/env python3
"""
Phase 52: SMTP Email System
Sends receipts and alert notifications
Dry-run safe if SMTP credentials not configured
"""
import os
import sys
import json
import smtplib
from email.message import EmailMessage
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def send_email(to, subject, body, html_body=None):
    """
    Send email via SMTP
    Returns dry_run=True if SMTP not configured
    """
    try:
        # Check for SMTP configuration
        smtp_host = os.getenv('SMTP_HOST', '')
        smtp_user = os.getenv('SMTP_USER', '')
        smtp_pass = os.getenv('SMTP_PASS', '')
        smtp_port = int(os.getenv('SMTP_PORT', '465'))
        smtp_from = os.getenv('SMTP_FROM', 'ops@echopilot.ai')
        
        # Dry run if not configured
        if not all([smtp_host, smtp_user, smtp_pass]):
            return {
                "ok": True,
                "dry_run": True,
                "message": "SMTP not configured - email not sent"
            }
        
        # Create message
        msg = EmailMessage()
        msg['From'] = smtp_from
        msg['To'] = to
        msg['Subject'] = subject
        msg.set_content(body)
        
        # Add HTML version if provided
        if html_body:
            msg.add_alternative(html_body, subtype='html')
        
        # Send via SMTP
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        
        # Log success
        log_entry = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "event": "email_sent",
            "to": to,
            "subject": subject,
            "status": "sent"
        }
        
        os.makedirs('logs', exist_ok=True)
        with open('logs/emails.ndjson', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return {
            "ok": True,
            "dry_run": False,
            "sent_to": to,
            "subject": subject
        }
    
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "dry_run": False
        }

def send_payment_receipt(email, amount, currency, payment_id):
    """Send payment receipt email"""
    subject = f"Payment Receipt - ${amount:.2f} {currency.upper()}"
    
    body = f"""Thank you for your payment!

Payment Details:
- Amount: ${amount:.2f} {currency.upper()}
- Payment ID: {payment_id}
- Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

Questions? Reply to this email.

- The EchoPilot Team
"""
    
    html_body = f"""
    <html>
    <body style="font-family: sans-serif;">
        <h2>Thank you for your payment!</h2>
        <h3>Payment Details</h3>
        <ul>
            <li><strong>Amount:</strong> ${amount:.2f} {currency.upper()}</li>
            <li><strong>Payment ID:</strong> {payment_id}</li>
            <li><strong>Date:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</li>
        </ul>
        <p>Questions? Reply to this email.</p>
        <p><em>- The EchoPilot Team</em></p>
    </body>
    </html>
    """
    
    return send_email(email, subject, body, html_body)

if __name__ == "__main__":
    # Test email
    result = send_email(
        "test@example.com",
        "EchoPilot Test Email",
        "This is a test email from EchoPilot."
    )
    print(json.dumps(result, indent=2))
