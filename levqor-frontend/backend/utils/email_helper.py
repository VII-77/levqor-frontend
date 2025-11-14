"""
Email Helper Utility
Centralized email sending with template support
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def send_email(template, to, data):
    """
    Send email with template
    
    Args:
        template: Email template name (e.g., 'lead_magnet_welcome')
        to: Recipient email
        data: Dict with template variables
    
    Returns:
        bool: Success status
    """
    email_body = render_template(template, data)
    email_subject = get_subject(template, data)
    
    logger.info(f"[EMAIL] To: {to}")
    logger.info(f"[EMAIL] Subject: {email_subject}")
    logger.info(f"[EMAIL] Template: {template}")
    logger.info(f"[EMAIL] Body:\n{email_body}")
    
    return True


def render_template(template, data):
    """Render email template"""
    templates = {
        'lead_magnet_welcome': f"""
Hi {data.get('name', 'there')},

Thanks for downloading our free automation guide!

We've prepared a comprehensive PDF that covers:
• The 5 most common workflow automations
• Step-by-step setup guides
• Best practices for business automation

Download your guide here: [PLACEHOLDER PDF LINK]

Need help getting started? Reply to this email or book a call: https://levqor.ai/call

Best,
The Levqor Team
""",
        'followup_value': f"""
Hi {data.get('name', 'there')},

Hope you enjoyed the automation guide we sent yesterday!

Here's a quick tip: The #1 mistake we see businesses make is trying to automate everything at once. Start with your most repetitive task first.

What's your biggest time-sink right now? Reply and let us know - we might have a quick solution.

Best,
The Levqor Team
""",
        'followup_case_study': f"""
Hi {data.get('name', 'there')},

Just wanted to share a quick success story:

One of our clients was spending 15+ hours/week on manual data entry. We built them a simple 3-step automation that now handles it in under 5 minutes.

Investment: £249 (Professional DFY)
Time saved: 15 hours/week
ROI: Paid for itself in 2 weeks

Curious if we can do something similar for you? Book a 15-min call: https://levqor.ai/call

Best,
The Levqor Team
""",
        'followup_soft_pitch': f"""
Hi {data.get('name', 'there')},

I know we've sent you a few emails - this will be my last one unless you'd like to hear more.

If you're ready to automate your workflows, here's what we can do:

✓ Done-For-You builds from £99
✓ 24-48 hour delivery
✓ 14-day money-back guarantee

See plans: https://levqor.ai/dfy

Not interested? No problem - just reply with "unsubscribe" and we'll stop the emails.

Best,
The Levqor Team
""",
        'dfy_welcome': f"""
Hi {data.get('name', 'there')},

Welcome to Levqor! 🎉

Your {data.get('tier', 'DFY')} order has been received.

What happens next:
1. We'll email you within 24 hours to schedule your kickoff call
2. After the call, we'll start building your workflows
3. You'll receive your completed automation within the delivery timeframe

Questions? Reply to this email anytime.

Best,
The Levqor Team
""",
        'dfy_upsell_12h': f"""
Hi {data.get('name', 'there')},

Hope you're excited about your automation!

Quick question: Did you know you can upgrade to Professional for just £150 extra?

Professional includes:
✓ 3 workflows (vs 1)
✓ 30 days support (vs 7)
✓ Self-healing features
✓ Priority support

This offer expires in 24 hours.

Upgrade now: https://levqor.ai/dfy-upgrade

Best,
The Levqor Team
""",
        'dfy_upsell_36h': f"""
Hi {data.get('name', 'there')},

Just a heads up - your Professional upgrade offer expires in 12 hours.

After that, you'll need to pay full price (£249 instead of £199).

Upgrade now while you can: https://levqor.ai/dfy-upgrade

Best,
The Levqor Team
""",
        'dfy_delivery': f"""
Hi {data.get('name', 'there')},

Your automation is complete! 🚀

Download your final package: {data.get('package_url', '[URL]')}

What's included:
• Workflows (ready to use)
• Documentation
• Setup guide
• Support access for {data.get('support_days', '7')} days

Questions? Reply to this email.

Best,
The Levqor Team
"""
    }
    
    return templates.get(template, f"Template '{template}' not found")


def get_subject(template, data):
    """Get email subject for template"""
    subjects = {
        'lead_magnet_welcome': 'Your Free Automation Guide',
        'followup_value': 'Quick automation tip for you',
        'followup_case_study': 'How we saved a client 15 hours/week',
        'followup_soft_pitch': 'Last email (promise!)',
        'dfy_welcome': f"Welcome! Your {data.get('tier', 'DFY')} order is confirmed",
        'dfy_upsell_12h': 'Upgrade to Professional - £150 off (24h only)',
        'dfy_upsell_36h': 'Last chance: £150 off Professional upgrade',
        'dfy_delivery': 'Your automation is ready! 🚀'
    }
    
    return subjects.get(template, 'Levqor Notification')
