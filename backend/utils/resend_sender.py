"""
Resend Email Sender
Real email sending using Resend API
"""

import os
import logging
import requests

logger = logging.getLogger(__name__)

RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
FROM_EMAIL = os.environ.get('AUTH_FROM_EMAIL', 'no-reply@levqor.ai')
RESEND_API_URL = "https://api.resend.com/emails"


def send_email_via_resend(to, subject, html_body):
    """
    Send email via Resend API
    
    Args:
        to: Recipient email address
        subject: Email subject line
        html_body: HTML email content
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not RESEND_API_KEY:
        logger.error("resend_sender.missing_api_key")
        return False
    
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": FROM_EMAIL,
        "to": [to],
        "subject": subject,
        "html": html_body
    }
    
    try:
        response = requests.post(
            RESEND_API_URL,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            logger.info(f"resend_sender.sent to={to} subject='{subject}'")
            return True
        else:
            logger.error(
                f"resend_sender.failed to={to} "
                f"status={response.status_code} "
                f"response={response.text}"
            )
            return False
            
    except Exception as e:
        logger.error(f"resend_sender.error to={to} error={str(e)}", exc_info=True)
        return False


def send_template_email(template_name, to, data):
    """
    Send templated email using email_helper templates
    
    Args:
        template_name: Name of email template
        to: Recipient email
        data: Dict with template variables
    
    Returns:
        bool: Success status
    """
    from backend.utils.email_helper import render_template, get_subject
    
    subject = get_subject(template_name, data)
    html_body = render_template(template_name, data)
    
    # Convert plain text to HTML
    html_body = html_body.replace('\n', '<br>')
    html_body = f"<html><body style='font-family: Arial, sans-serif;'>{html_body}</body></html>"
    
    return send_email_via_resend(to, subject, html_body)
