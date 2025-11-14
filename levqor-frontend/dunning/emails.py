"""
Dunning email templates and sending logic
Progressive email sequence for payment recovery
"""
import os
import requests
from datetime import datetime


def send_dunning_email(user_email, user_name, email_type, amount_cents, currency="gbp", invoice_url=None):
    """
    Send dunning email based on failure timeline
    
    email_type: 'day0', 'day3', 'day7', 'day14'
    """
    
    resend_api_key = os.getenv("RESEND_API_KEY")
    if not resend_api_key:
        return {"ok": False, "error": "RESEND_API_KEY not configured"}
    
    from_email = os.getenv("AUTH_FROM_EMAIL", "billing@levqor.ai")
    
    amount_display = f"£{amount_cents / 100:.2f}" if currency == "gbp" else f"{amount_cents / 100:.2f} {currency.upper()}"
    
    # Email content based on type
    templates = {
        "day0": {
            "subject": "Payment retry scheduled - Levqor",
            "headline": "We'll retry your payment soon",
            "message": f"We couldn't process your payment of {amount_display}. This happens sometimes with card authorizations. We'll automatically retry in a few hours.",
            "cta": "Update Payment Method",
            "urgency": "low"
        },
        "day3": {
            "subject": "⚠️ Action needed: Update your payment method",
            "headline": "Please update your payment method",
            "message": f"We've tried processing your payment of {amount_display} several times without success. To avoid service interruption, please update your payment method.",
            "cta": "Update Payment Method Now",
            "urgency": "medium"
        },
        "day7": {
            "subject": "🚨 Final notice: Payment required to maintain service",
            "headline": "Final payment reminder",
            "message": f"Your payment of {amount_display} is now 7 days overdue. Your subscription will be paused if payment is not received within 7 days.",
            "cta": "Resolve Payment Issue",
            "urgency": "high"
        },
        "day14": {
            "subject": "Subscription paused - Levqor",
            "headline": "Your subscription has been paused",
            "message": f"Your Levqor subscription has been paused due to non-payment of {amount_display}. Your workflows are temporarily disabled. Update your payment method to restore access.",
            "cta": "Restore Subscription",
            "urgency": "critical"
        }
    }
    
    template = templates.get(email_type, templates["day0"])
    urgency_colors = {
        "low": {"bg": "#0369a1", "text": "#bae6fd"},
        "medium": {"bg": "#d97706", "text": "#fef3c7"},
        "high": {"bg": "#dc2626", "text": "#fee2e2"},
        "critical": {"bg": "#7f1d1d", "text": "#fca5a5"}
    }
    colors = urgency_colors[template["urgency"]]
    
    payment_url = invoice_url or "https://www.levqor.ai/account/billing"
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 0;
            padding: 0;
            background: #0f172a;
            color: #e2e8f0;
        }}
        .container {{
            max-width: 600px;
            margin: 40px auto;
            background: #1e293b;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        .header {{
            background: {colors["bg"]};
            padding: 32px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
            color: white;
        }}
        .content {{
            padding: 32px;
        }}
        .message {{
            font-size: 16px;
            line-height: 1.6;
            color: #cbd5e1;
            margin-bottom: 24px;
        }}
        .amount-box {{
            background: #0f172a;
            border: 2px solid {colors["bg"]};
            border-radius: 8px;
            padding: 16px;
            text-align: center;
            margin: 24px 0;
        }}
        .amount {{
            font-size: 28px;
            font-weight: 700;
            color: {colors["text"]};
        }}
        .button {{
            display: inline-block;
            padding: 16px 32px;
            background: {colors["bg"]};
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 16px;
            text-align: center;
            margin: 16px 0;
        }}
        .footer {{
            background: #0f172a;
            padding: 24px;
            text-align: center;
            font-size: 12px;
            color: #64748b;
            border-top: 1px solid #334155;
        }}
        .footer a {{
            color: #10b981;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{template["headline"]}</h1>
        </div>
        
        <div class="content">
            <p class="message">Hi {user_name or "there"},</p>
            
            <p class="message">{template["message"]}</p>
            
            <div class="amount-box">
                <div class="amount">{amount_display}</div>
                <div style="color: #94a3b8; font-size: 14px; margin-top: 8px;">Amount due</div>
            </div>
            
            <div style="text-align: center;">
                <a href="{payment_url}" class="button">{template["cta"]} →</a>
            </div>
            
            <p class="message" style="margin-top: 32px; font-size: 14px; color: #94a3b8;">
                <strong>Need help?</strong><br>
                If you're experiencing issues or have questions about this charge, please contact our billing support at billing@levqor.ai
            </p>
        </div>
        
        <div class="footer">
            <p>Levqor Billing • {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}</p>
            <p>
                <a href="https://www.levqor.ai/billing-policy">Billing Policy</a> • 
                <a href="mailto:billing@levqor.ai">Contact Billing Support</a>
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    text_content = f"""
{template["headline"]}

Hi {user_name or "there"},

{template["message"]}

Amount due: {amount_display}

{template["cta"]}: {payment_url}

Need help? Contact billing@levqor.ai

---
Levqor Billing
{datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}
"""
    
    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {resend_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "from": from_email,
                "to": [user_email],
                "subject": template["subject"],
                "html": html_content,
                "text": text_content
            },
            timeout=10
        )
        
        if response.status_code in (200, 201):
            return {"ok": True, "message_id": response.json().get("id"), "type": email_type}
        else:
            return {
                "ok": False,
                "error": f"Resend API error: {response.status_code}",
                "details": response.text
            }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}
