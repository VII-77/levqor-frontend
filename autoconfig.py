#!/usr/bin/env python3
"""
EchoPilot Auto-Configuration Script
Automatically configures payment and client management systems
"""

import os
import json

print("=" * 80)
print("⚙️  EchoPilot Auto-Configuration")
print("=" * 80)
print()

def check_env(var_name):
    value = os.environ.get(var_name)
    if value:
        print(f"✅ {var_name}: Configured")
        return True
    else:
        print(f"❌ {var_name}: Not set")
        return False

print("📋 Current Configuration Status:")
print()

print("🔐 Core System (Required):")
core_vars = [
    "AI_INTEGRATIONS_OPENAI_API_KEY",
    "AI_INTEGRATIONS_OPENAI_BASE_URL",
    "AUTOMATION_QUEUE_DB_ID",
    "AUTOMATION_LOG_DB_ID",
    "JOB_LOG_DB_ID"
]

core_complete = all(check_env(v) for v in core_vars)
print()

print("📧 Alert System (Required for notifications):")
alert_vars = [
    "ALERT_TO",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID"
]

alert_complete = all(check_env(v) for v in alert_vars)
print()

print("💰 Payment System (Optional - activate one):")
stripe_key = check_env("STRIPE_SECRET_KEY")
stripe_webhook = check_env("STRIPE_WEBHOOK_SECRET")
print()
paypal_id = check_env("PAYPAL_CLIENT_ID")
paypal_sec = check_env("PAYPAL_SECRET")
paypal_live = check_env("PAYPAL_LIVE")
payment_complete = (stripe_key and stripe_webhook) or (paypal_id and paypal_sec)
print()

print("💼 Client Management System (Optional):")
client_db = check_env("NOTION_CLIENT_DB_ID")
default_rate = check_env("DEFAULT_RATE_USD_PER_MIN")
client_complete = client_db
print()

print("📊 Live Diagnostics (Optional):")
status_db = check_env("NOTION_STATUS_DB_ID")
print()

print("=" * 80)
print("📈 Configuration Summary")
print("=" * 80)
print()

systems = [
    ("Core System", core_complete, True),
    ("Alert System", alert_complete, True),
    ("Payment System", payment_complete, False),
    ("Client Management", client_complete, False),
    ("Live Diagnostics", status_db, False)
]

for name, complete, required in systems:
    if complete:
        status = "✅ Active"
    elif required:
        status = "❌ Missing (Required)"
    else:
        status = "⚠️  Not configured (Optional)"
    
    print(f"{status}: {name}")

print()
print("=" * 80)
print("📝 Next Steps")
print("=" * 80)
print()

if not core_complete:
    print("❌ Core system incomplete - add missing environment variables")
elif not alert_complete:
    print("⚠️  Alert system incomplete - notifications won't work")
elif not payment_complete:
    print("💡 To activate payments, add one of:")
    print("   • Stripe: STRIPE_SECRET_KEY + STRIPE_WEBHOOK_SECRET")
    print("   • PayPal: PAYPAL_CLIENT_ID + PAYPAL_SECRET + PAYPAL_LIVE")
elif not client_complete:
    print("💡 To activate client management:")
    print("   1. Create 'EchoPilot Clients' database in Notion")
    print("   2. Add NOTION_CLIENT_DB_ID to environment")
    print("   3. (Optional) Set DEFAULT_RATE_USD_PER_MIN")
else:
    print("✨ All systems fully configured!")
    print()
    print("🚀 Your EchoPilot bot is production-ready with:")
    print("   • 60-second Notion polling")
    print("   • GPT-4o AI processing")
    print("   • 80% QA threshold")
    print("   • Auto-operator monitoring")
    print("   • Payment integration")
    print("   • Client management")
    print("   • Revenue tracking")
    print("   • Invoice generation & delivery")

print()

if core_complete:
    print("📖 Documentation:")
    print("   • PAYMENT_SYSTEM_GUIDE.md - Payment setup instructions")
    print("   • CLIENT_SYSTEM_GUIDE.md - Client billing instructions")
    print("   • Run: python test_integration.py - Test all systems")
    print()
    print("🔗 Production URLs:")
    print("   • App: https://Echopilotai.replit.app")
    print("   • Health: https://Echopilotai.replit.app/health")
    print("   • Auto-Operator: https://Echopilotai.replit.app/ops-report")
    print("   • Stripe Webhook: https://Echopilotai.replit.app/webhook/stripe")
    print("   • PayPal Webhook: https://Echopilotai.replit.app/webhook/paypal")

print()
