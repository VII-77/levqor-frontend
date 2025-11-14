"""
Billing and dunning configuration
"""
import os

# Stripe configuration
STRIPE_API_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

# Dunning system configuration
# CRITICAL: Starts as False for safety - must be explicitly enabled
DUNNING_ENABLED = os.getenv("DUNNING_ENABLED", "false").lower() in ("true", "1", "yes")

# Dunning email schedule (days after payment failure)
DUNNING_SCHEDULE_DAYS = [1, 7, 14]

# Billing portal URL
BILLING_PORTAL_URL = os.getenv("BILLING_PORTAL_URL", "https://www.levqor.ai/billing")

# Email configuration
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
FROM_EMAIL = os.getenv("AUTH_FROM_EMAIL", "billing@levqor.ai")
