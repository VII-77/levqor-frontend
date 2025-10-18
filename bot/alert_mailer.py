import os
from bot.gmail_client import GmailClientWrapper

def send_alert(subject: str, body: str, to_email: str = None) -> bool:
    """
    Send alert email via Gmail API
    
    Args:
        subject: Email subject line
        body: Email body content
        to_email: Optional recipient (defaults to ALERT_TO env var)
    
    Returns:
        bool: True if sent successfully
    """
    try:
        gmail = GmailClientWrapper()
        recipient = to_email or os.getenv('ALERT_TO', '')
        
        if not recipient:
            print("[Alert] No recipient configured (ALERT_TO not set)")
            return False
        
        result = gmail.send_email(
            to=recipient,
            subject=subject,
            body=body
        )
        
        return result.get('ok', False)
        
    except Exception as e:
        print(f"[Alert] Failed to send email: {e}")
        return False
