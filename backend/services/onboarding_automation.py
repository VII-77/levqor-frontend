"""
Onboarding Automation
Orchestrates email flows and notifications for new DFY orders
"""

import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def handle_new_order(order, customer_name=''):
    """
    Main automation orchestrator for new orders
    
    Called immediately after Stripe checkout completes.
    Sends confirmation emails and internal notifications.
    
    Args:
        order: DFYOrder model instance
        customer_name: Customer's name from checkout
    """
    logger.info(f"onboarding.start order_id={order.id} email={order.customer_email}")
    
    # Send payment confirmation
    send_payment_confirmation_email(order, customer_name)
    
    # Send intake request
    send_intake_request_email(order, customer_name)
    
    # Notify internal team
    notify_internal_new_order(order, customer_name)
    
    logger.info(f"onboarding.complete order_id={order.id}")


def send_payment_confirmation_email(order, customer_name=''):
    """Send payment received confirmation"""
    from backend.utils.resend_sender import send_template_email
    
    data = {
        'name': customer_name or 'there',
        'tier': order.tier,
        'order_id': order.id
    }
    
    success = send_template_email('dfy_welcome', order.customer_email, data)
    
    if success:
        logger.info(f"onboarding.confirmation_sent order_id={order.id}")
    else:
        logger.error(f"onboarding.confirmation_failed order_id={order.id}")
    
    return success


def send_intake_request_email(order, customer_name=''):
    """Send intake form request"""
    from backend.utils.resend_sender import send_email_via_resend
    
    subject = "Next step: Tell us about your automation needs"
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2>Hi {customer_name or 'there'},</h2>
        
        <p>Thanks for choosing Levqor! Your order is confirmed.</p>
        
        <p><strong>What happens next:</strong></p>
        <ol>
            <li>Fill out our quick intake form (5 minutes)</li>
            <li>We'll schedule a kickoff call within 24 hours</li>
            <li>We'll build your automation</li>
            <li>You'll receive your completed workflow</li>
        </ol>
        
        <p style="text-align: center; margin: 30px 0;">
            <a href="https://levqor.ai/intake?order_id={order.id}" 
               style="background: #10b981; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold;">
                Fill Out Intake Form
            </a>
        </p>
        
        <p>Questions? Just reply to this email.</p>
        
        <p>Best,<br>The Levqor Team</p>
    </body>
    </html>
    """
    
    success = send_email_via_resend(order.customer_email, subject, html_body)
    
    if success:
        logger.info(f"onboarding.intake_request_sent order_id={order.id}")
    else:
        logger.error(f"onboarding.intake_request_failed order_id={order.id}")
    
    return success


def send_intake_reminder_email(order, customer_name=''):
    """Send reminder if intake form not submitted after 48 hours"""
    from backend.utils.resend_sender import send_email_via_resend
    
    subject = "Reminder: Complete your intake form"
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2>Hi {customer_name or 'there'},</h2>
        
        <p>We noticed you haven't filled out your intake form yet.</p>
        
        <p>We're ready to start building your automation, but we need a few details from you first.</p>
        
        <p style="text-align: center; margin: 30px 0;">
            <a href="https://levqor.ai/intake?order_id={order.id}" 
               style="background: #10b981; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold;">
                Complete Intake Form Now
            </a>
        </p>
        
        <p>Need help? Reply to this email or book a call: https://levqor.ai/call</p>
        
        <p>Best,<br>The Levqor Team</p>
    </body>
    </html>
    """
    
    return send_email_via_resend(order.customer_email, subject, html_body)


def send_handover_email(order, customer_name='', package_url=''):
    """Send delivery notification with download link"""
    from backend.utils.resend_sender import send_template_email
    
    data = {
        'name': customer_name or 'there',
        'tier': order.tier,
        'package_url': package_url or order.final_package_url or '[Contact support]',
        'support_days': '7' if 'STARTER' in order.tier else '30'
    }
    
    success = send_template_email('dfy_delivery', order.customer_email, data)
    
    if success:
        logger.info(f"onboarding.handover_sent order_id={order.id}")
    else:
        logger.error(f"onboarding.handover_failed order_id={order.id}")
    
    return success


def send_upsell_email(order, customer_name=''):
    """Send upsell email 7 days after delivery"""
    from backend.utils.resend_sender import send_email_via_resend
    
    subject = "How's your automation working?"
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2>Hi {customer_name or 'there'},</h2>
        
        <p>Hope your automation is running smoothly!</p>
        
        <p>Quick question: Need help with any other workflows?</p>
        
        <p><strong>Popular next steps:</strong></p>
        <ul>
            <li>Add more workflows (Professional or Enterprise tiers)</li>
            <li>Upgrade to a subscription for ongoing automation</li>
            <li>Add priority support for faster response times</li>
        </ul>
        
        <p style="text-align: center; margin: 30px 0;">
            <a href="https://levqor.ai/pricing" 
               style="background: #10b981; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold;">
                View Plans
            </a>
        </p>
        
        <p>Questions? Just reply to this email.</p>
        
        <p>Best,<br>The Levqor Team</p>
    </body>
    </html>
    """
    
    return send_email_via_resend(order.customer_email, subject, html_body)


def notify_internal_new_order(order, customer_name=''):
    """Send Telegram notification to internal team"""
    from backend.utils.telegram_helper import send_telegram_notification
    
    message = f"""
🎉 NEW ORDER RECEIVED!

Order ID: #{order.id}
Customer: {customer_name} ({order.customer_email})
Tier: {order.tier}
Status: {order.status}
Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

Action needed: Monitor intake form submission
    """.strip()
    
    send_telegram_notification(message)
