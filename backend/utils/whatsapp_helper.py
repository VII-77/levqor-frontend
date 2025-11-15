"""
WhatsApp Notification Helper
Send notifications via WhatsApp Business API (NO-OP until configured)
"""

import os
import logging
import requests

logger = logging.getLogger(__name__)

WHATSAPP_API_URL = os.environ.get('WHATSAPP_API_URL')
WHATSAPP_ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN')
WHATSAPP_SENDER_ID = os.environ.get('WHATSAPP_SENDER_ID')


def send_whatsapp_message(phone, text):
    """
    Send WhatsApp message
    
    Args:
        phone: Phone number in international format (e.g. +447123456789)
        text: Message text to send
    
    Returns:
        bool: True if sent successfully, False if not configured or failed
    """
    if not all([WHATSAPP_API_URL, WHATSAPP_ACCESS_TOKEN, WHATSAPP_SENDER_ID]):
        logger.info("whatsapp.not_configured - skipping send")
        return False
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {
            "body": text
        }
    }
    
    try:
        response = requests.post(
            f"{WHATSAPP_API_URL}/{WHATSAPP_SENDER_ID}/messages",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            logger.info(f"whatsapp.sent to={phone}")
            return True
        else:
            logger.error(
                f"whatsapp.failed to={phone} "
                f"status={response.status_code} "
                f"response={response.text}"
            )
            return False
            
    except Exception as e:
        logger.error(f"whatsapp.error to={phone} error={str(e)}", exc_info=True)
        return False


def notify_new_ticket(email, message):
    """
    Send WhatsApp notification for new support ticket
    (NO-OP if WhatsApp not configured)
    
    Args:
        email: Customer email
        message: Ticket message preview
    
    Returns:
        bool: Success status
    """
    admin_phone = os.environ.get('WHATSAPP_ADMIN_PHONE')
    
    if not admin_phone:
        logger.info("whatsapp.admin_phone_not_configured - skipping")
        return False
    
    notification_text = f"""
🎫 NEW SUPPORT TICKET

From: {email}
Message: {message[:100]}...

Reply via dashboard or Telegram
    """.strip()
    
    return send_whatsapp_message(admin_phone, notification_text)
