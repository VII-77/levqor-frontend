"""
DSAR Email Notifications
Sends data export ZIP files as email attachments using Resend
"""
import os
import requests
import base64
from datetime import datetime


def send_export_as_attachment(user_email, user_name, zip_bytes, filename, reference_id):
    """
    Send data export ZIP file directly as email attachment
    
    Args:
        user_email: Recipient email address
        user_name: User's name (for personalization)
        zip_bytes: Binary ZIP file content
        filename: Export filename (e.g., "levqor-dsar-user-123-20241114.zip")
        reference_id: DSAR reference ID for user's records
    
    Returns:
        dict: Result with 'ok' status and optional 'error'
    """
    
    resend_api_key = os.getenv("RESEND_API_KEY")
    if not resend_api_key:
        return {"ok": False, "error": "RESEND_API_KEY not configured"}
    
    from_email = os.getenv("AUTH_FROM_EMAIL", "no-reply@levqor.ai")
    
    # Base64 encode the ZIP file for email attachment
    zip_base64 = base64.b64encode(zip_bytes).decode('utf-8')
    
    # HTML email content
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
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
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
        .greeting {{
            font-size: 16px;
            margin-bottom: 24px;
            color: #cbd5e1;
        }}
        .message {{
            font-size: 15px;
            line-height: 1.6;
            color: #cbd5e1;
            margin-bottom: 24px;
        }}
        .info-box {{
            background: #0f172a;
            border: 2px solid #10b981;
            border-radius: 8px;
            padding: 24px;
            margin: 24px 0;
        }}
        .info-label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #94a3b8;
            margin-bottom: 8px;
        }}
        .info-value {{
            font-size: 16px;
            font-weight: 600;
            color: #10b981;
            font-family: 'Courier New', monospace;
        }}
        .warning-box {{
            background: #7f1d1d;
            border-left: 4px solid #dc2626;
            padding: 16px;
            border-radius: 4px;
            margin: 24px 0;
        }}
        .warning-box p {{
            margin: 0;
            font-size: 14px;
            color: #fca5a5;
        }}
        .footer {{
            background: #0f172a;
            padding: 24px;
            text-align: center;
            font-size: 12px;
            color: #64748b;
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
            <h1>🔒 Your Levqor Data Export (GDPR/UK-GDPR)</h1>
        </div>
        
        <div class="content">
            <div class="greeting">
                Hi {user_name or "there"},
            </div>
            
            <div class="message">
                Your data export request has been processed. Your personal data export is attached to this email as a ZIP file.
            </div>
            
            <div class="info-box">
                <div class="info-label">Attachment</div>
                <div class="info-value">{filename}</div>
                <div style="margin-top: 12px; color: #94a3b8; font-size: 13px;">
                    Contains: User profile, workflows, API keys, partnerships, audit logs, and all personal data we hold.
                </div>
            </div>
            
            <div class="info-box">
                <div class="info-label">Reference ID</div>
                <div class="info-value">{reference_id}</div>
                <div style="margin-top: 12px; color: #94a3b8; font-size: 13px;">
                    Keep this reference for your records if you need to contact us about this export.
                </div>
            </div>
            
            <div class="message">
                <strong>What's inside your export:</strong>
            </div>
            
            <ul style="color: #cbd5e1; line-height: 1.8;">
                <li><strong>user_data.json</strong> - Complete JSON export of all your data</li>
                <li><strong>*.csv files</strong> - Human-readable CSV exports by category</li>
                <li>User profile, workflows, API keys, partnerships, and audit logs</li>
                <li>Marketing consent records and terms acceptance history</li>
            </ul>
            
            <div class="warning-box">
                <p><strong>⚠️ Security Notice</strong></p>
                <p>This file contains your personal data. Store it securely and do not share it publicly. Delete it when no longer needed.</p>
            </div>
            
            <div class="warning-box">
                <p><strong>⚠️ Did not request this?</strong> If you did not request a data export, contact privacy@levqor.ai immediately. Your account may be compromised.</p>
            </div>
        </div>
        
        <div class="footer">
            <p>Levqor Data Export System • Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}</p>
            <p>
                <a href="https://www.levqor.ai/privacy">Privacy Policy</a> • 
                <a href="https://www.levqor.ai/gdpr">GDPR Compliance</a> • 
                <a href="mailto:privacy@levqor.ai">Contact Privacy Team</a>
            </p>
            <p style="margin-top: 16px;">
                This email was sent to {user_email} in response to your data export request under UK GDPR/EU GDPR Article 15 (Right of Access).
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    # Plain text fallback
    text_content = f"""
Your Levqor Data Export (GDPR/UK-GDPR)

Hi {user_name or "there"},

Your data export request has been processed. Your personal data export is attached to this email as: {filename}

Reference ID: {reference_id}

What's inside:
- user_data.json - Complete JSON export
- *.csv files - CSV exports by category
- User profile, workflows, API keys, partnerships, audit logs

SECURITY NOTICE: This file contains your personal data. Store it securely and do not share it publicly.

If you did not request this, contact privacy@levqor.ai immediately.

---
Levqor Data Export System
Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}

Privacy: https://www.levqor.ai/privacy
Contact: privacy@levqor.ai
"""
    
    # Send via Resend API with attachment
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
                "subject": "🔒 Your Levqor data export (GDPR/UK-GDPR)",
                "html": html_content,
                "text": text_content,
                "attachments": [
                    {
                        "filename": filename,
                        "content": zip_base64
                    }
                ]
            },
            timeout=30  # Increased timeout for larger files
        )
        
        if response.status_code in (200, 201):
            return {"ok": True, "message_id": response.json().get("id")}
        else:
            return {
                "ok": False,
                "error": f"Resend API error: {response.status_code}",
                "details": response.text
            }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}


# Keep legacy function for backwards compatibility
def send_export_ready_email(user_email, user_name, download_token, otp):
    """
    Send email with download link and OTP to user
    
    Args:
        user_email: Recipient email address
        user_name: User's name (for personalization)
        download_token: Secure download token
        otp: One-time passcode (6 digits)
    
    Returns:
        dict: Result with 'ok' status and optional 'error'
    """
    
    resend_api_key = os.getenv("RESEND_API_KEY")
    if not resend_api_key:
        return {"ok": False, "error": "RESEND_API_KEY not configured"}
    
    from_email = os.getenv("AUTH_FROM_EMAIL", "no-reply@levqor.ai")
    base_url = os.getenv("BASE_URL", "https://www.levqor.ai")
    
    download_url = f"{base_url}/data-export/download?token={download_token}"
    
    # Format OTP for readability
    otp_formatted = f"{otp[:3]} {otp[3:]}"
    
    # HTML email content
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
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
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
        .greeting {{
            font-size: 16px;
            margin-bottom: 24px;
            color: #cbd5e1;
        }}
        .message {{
            font-size: 15px;
            line-height: 1.6;
            color: #cbd5e1;
            margin-bottom: 24px;
        }}
        .otp-box {{
            background: #0f172a;
            border: 2px solid #10b981;
            border-radius: 8px;
            padding: 24px;
            text-align: center;
            margin: 24px 0;
        }}
        .otp-label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #94a3b8;
            margin-bottom: 8px;
        }}
        .otp-code {{
            font-size: 32px;
            font-weight: 700;
            letter-spacing: 4px;
            color: #10b981;
            font-family: 'Courier New', monospace;
        }}
        .button-container {{
            text-align: center;
            margin: 32px 0;
        }}
        .button {{
            display: inline-block;
            padding: 16px 32px;
            background: #10b981;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 16px;
        }}
        .button:hover {{
            background: #059669;
        }}
        .warning-box {{
            background: #7f1d1d;
            border-left: 4px solid #dc2626;
            padding: 16px;
            border-radius: 4px;
            margin: 24px 0;
        }}
        .warning-box p {{
            margin: 0;
            font-size: 14px;
            color: #fca5a5;
        }}
        .footer {{
            background: #0f172a;
            padding: 24px;
            text-align: center;
            font-size: 12px;
            color: #64748b;
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
            <h1>🔒 Your Levqor Data Export is Ready</h1>
        </div>
        
        <div class="content">
            <div class="greeting">
                Hi {user_name or "there"},
            </div>
            
            <div class="message">
                Your data export request has been processed. To download your personal data from Levqor, you'll need both the download link and your one-time passcode below.
            </div>
            
            <div class="otp-box">
                <div class="otp-label">Your One-Time Passcode</div>
                <div class="otp-code">{otp_formatted}</div>
            </div>
            
            <div class="button-container">
                <a href="{download_url}" class="button">Download My Data →</a>
            </div>
            
            <div class="message">
                <strong>Important Security Information:</strong>
            </div>
            
            <ul style="color: #cbd5e1; line-height: 1.8;">
                <li><strong>OTP valid for 15 minutes</strong> from when this email was sent</li>
                <li><strong>Download link valid for 24 hours</strong></li>
                <li>One-time use only - code expires after successful download</li>
                <li>Your export contains personal data - keep it secure</li>
            </ul>
            
            <div class="warning-box">
                <p><strong>⚠️ Did not request this?</strong> If you did not request a data export, contact privacy@levqor.ai immediately. Your account may be compromised.</p>
            </div>
            
            <div class="message" style="margin-top: 32px; font-size: 13px; color: #94a3b8;">
                Alternative method: If the button doesn't work, copy and paste this URL into your browser:<br>
                <code style="background: #0f172a; padding: 8px; border-radius: 4px; display: inline-block; margin-top: 8px; word-break: break-all;">{download_url}</code>
            </div>
        </div>
        
        <div class="footer">
            <p>Levqor Data Export System • Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}</p>
            <p>
                <a href="https://www.levqor.ai/privacy">Privacy Policy</a> • 
                <a href="https://www.levqor.ai/gdpr">GDPR Compliance</a> • 
                <a href="mailto:privacy@levqor.ai">Contact Privacy Team</a>
            </p>
            <p style="margin-top: 16px;">
                This email was sent to {user_email} in response to your data export request under UK GDPR/EU GDPR Article 15 (Right of Access).
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    # Plain text fallback
    text_content = f"""
Your Levqor Data Export is Ready

Hi {user_name or "there"},

Your data export request has been processed. To download your personal data:

1. Visit this link: {download_url}
2. Enter your one-time passcode: {otp_formatted}

Important:
- OTP valid for 15 minutes
- Download link valid for 24 hours  
- One-time use only

If you did not request this, contact privacy@levqor.ai immediately.

---
Levqor Data Export System
Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}

Privacy: https://www.levqor.ai/privacy
Contact: privacy@levqor.ai
"""
    
    # Send via Resend API
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
                "subject": "🔒 Your Levqor data export is ready",
                "html": html_content,
                "text": text_content
            },
            timeout=10
        )
        
        if response.status_code in (200, 201):
            return {"ok": True, "message_id": response.json().get("id")}
        else:
            return {
                "ok": False,
                "error": f"Resend API error: {response.status_code}",
                "details": response.text
            }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}
