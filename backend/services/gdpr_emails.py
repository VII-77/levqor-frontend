"""
GDPR Opt-out Confirmation Emails
Sends confirmation when users object to data processing.
"""

import logging
import os

log = logging.getLogger("levqor.gdpr")


def send_optout_confirmation(user_email, user_name, scopes_applied):
    """
    Send confirmation email when user opts out of data processing.
    
    Args:
        user_email: User's email address
        user_name: User's name (or None)
        scopes_applied: List of scopes opted out (e.g. ['marketing', 'profiling'])
    """
    from billing.dunning_emails import send_billing_email
    
    name = user_name or "there"
    base_url = os.environ.get("NEXTAUTH_URL", "https://levqor.ai")
    
    # Format scopes for readability
    scope_descriptions = {
        'marketing': 'marketing emails and communications',
        'profiling': 'profiling and personalized recommendations',
        'automation': 'automated workflow triggers',
        'analytics': 'analytics tracking'
    }
    
    scope_list = [scope_descriptions.get(s, s) for s in scopes_applied]
    
    if len(scope_list) == 1:
        scope_text = scope_list[0]
    elif len(scope_list) == 2:
        scope_text = f"{scope_list[0]} and {scope_list[1]}"
    else:
        scope_text = ", ".join(scope_list[:-1]) + f", and {scope_list[-1]}"
    
    subject = "Your Levqor privacy preferences have been updated"
    
    body = f"""Hi {name},

We've received and processed your request to object to certain data processing activities.

You have opted out of:
{scope_text}

What this means:
• If you opted out of marketing: You will no longer receive promotional emails (you'll still receive important transactional emails about your account)
• If you opted out of profiling: We will not use your data for personalized recommendations or AI-driven suggestions
• If you opted out of automation: Background automated workflows for suggestions will be disabled (your manually triggered workflows will continue)
• If you opted out of analytics: We will not track your usage for analytics purposes

Your preferences take effect immediately and will be applied across our entire platform.

You can change your privacy preferences at any time by visiting:
{base_url}/privacy-tools/opt-out

If you have questions about your privacy rights or data processing, please contact our Data Protection Officer at:
privacy@levqor.ai

Best regards,
The Levqor Team

---
This is a transactional email about your privacy preferences at levqor.ai
You are receiving this because you updated your GDPR objection settings
"""
    
    # This is a transactional email confirming their opt-out, so always send it
    send_billing_email(user_email, subject, body, is_transactional=True)
    log.info(f"[GDPR] Sent opt-out confirmation to {user_email} for scopes: {', '.join(scopes_applied)}")
