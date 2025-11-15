"""
Telegram Notification Helper
Send internal notifications to admin via Telegram bot
"""

import os
import logging
import requests

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '5932848683')  # Default admin chat ID

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_telegram_notification(message):
    """
    Send notification via Telegram
    
    Args:
        message: Text message to send
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("telegram.missing_bot_token - skipping notification")
        return False
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(
            TELEGRAM_API_URL,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info(f"telegram.sent chat_id={TELEGRAM_CHAT_ID}")
            return True
        else:
            logger.error(
                f"telegram.failed "
                f"status={response.status_code} "
                f"response={response.text}"
            )
            return False
            
    except Exception as e:
        logger.error(f"telegram.error error={str(e)}", exc_info=True)
        return False


def notify_intake_submitted(order_id, customer_email):
    """Notify when customer submits intake form"""
    message = f"""
📝 <b>INTAKE SUBMITTED</b>

Order ID: #{order_id}
Customer: {customer_email}

Action needed: Schedule kickoff call
    """.strip()
    
    return send_telegram_notification(message)


def notify_project_delivered(order_id, customer_email, tier):
    """Notify when project is marked as delivered"""
    message = f"""
🚀 <b>PROJECT DELIVERED</b>

Order ID: #{order_id}
Customer: {customer_email}
Tier: {tier}

Handover email sent.
    """.strip()
    
    return send_telegram_notification(message)
