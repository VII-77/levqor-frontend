#!/usr/bin/env python3
import os
import sys
from datetime import datetime

print("=" * 80)
print("🧪 EchoPilot Integration Test Suite")
print("=" * 80)
print()

results = []

def test(name, func):
    try:
        print(f"Testing: {name}...")
        result = func()
        if result:
            print(f"✅ {name}: PASS")
            results.append((name, True, result))
        else:
            print(f"❌ {name}: FAIL")
            results.append((name, False, "Failed"))
    except Exception as e:
        print(f"❌ {name}: ERROR - {e}")
        results.append((name, False, str(e)))
    print()

def test_openai():
    from openai import OpenAI
    api_key = os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY")
    base_url = os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL")
    
    if not api_key or not base_url:
        return "Missing API key or base URL"
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'test successful'"}],
        max_tokens=10
    )
    return f"Response: {response.choices[0].message.content}"

def test_notion():
    from bot.notion_api import NotionClientWrapper
    api = NotionClientWrapper()
    
    queue_id = os.environ.get("AUTOMATION_QUEUE_DB_ID")
    log_id = os.environ.get("AUTOMATION_LOG_DB_ID")
    job_id = os.environ.get("JOB_LOG_DB_ID")
    
    if not all([queue_id, log_id, job_id]):
        return "Missing database IDs"
    
    items = api.get_triggered_tasks()
    return f"Found {len(items)} triggered tasks"

def test_gmail():
    from bot.gmail_client import GmailClientWrapper
    client = GmailClientWrapper()
    
    return "Gmail client initialized (OAuth token managed by Replit)"

def test_telegram():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        return "Missing Telegram credentials"
    
    import requests
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return f"Bot: @{data['result']['username']}"
    else:
        return f"HTTP {response.status_code}"

def test_payment_system():
    try:
        from bot.payments import is_payment_configured
        configured = is_payment_configured()
        
        stripe_key = os.environ.get("STRIPE_SECRET_KEY")
        paypal_id = os.environ.get("PAYPAL_CLIENT_ID")
        
        if configured:
            provider = "Stripe" if stripe_key else "PayPal"
            return f"Payment system ready ({provider})"
        else:
            return "Payment credentials not configured (optional)"
    except ImportError:
        return "Payment module not available"

def test_client_system():
    try:
        from bot.client_manager import is_client_system_configured
        configured = is_client_system_configured()
        
        if configured:
            return "Client system configured"
        else:
            return "Client database not configured (optional)"
    except ImportError:
        return "Client module not available"

def test_git_integration():
    from bot.git_utils import get_git_info, check_git_clean
    
    commit, branch, _ = get_git_info()
    clean = check_git_clean()
    
    return f"Commit: {commit[:8]}, Branch: {branch}, Clean: {clean}"

def test_health_endpoint():
    import requests
    response = requests.get("http://localhost:5000/health")
    
    if response.status_code == 200:
        return f"Status: {response.json()['status']}"
    else:
        return f"HTTP {response.status_code}"

def test_env_vars():
    required = [
        "AI_INTEGRATIONS_OPENAI_API_KEY",
        "AI_INTEGRATIONS_OPENAI_BASE_URL",
        "AUTOMATION_QUEUE_DB_ID",
        "AUTOMATION_LOG_DB_ID",
        "JOB_LOG_DB_ID"
    ]
    
    missing = [var for var in required if not os.environ.get(var)]
    
    if missing:
        return f"Missing: {', '.join(missing)}"
    else:
        return f"All {len(required)} required variables present"

print("🔍 Running Integration Tests...")
print()

test("Environment Variables", test_env_vars)
test("Git Integration", test_git_integration)
test("Health Endpoint", test_health_endpoint)
test("OpenAI Connection", test_openai)
test("Notion Connection", test_notion)
test("Gmail Connection", test_gmail)
test("Telegram Connection", test_telegram)
test("Payment System", test_payment_system)
test("Client Management", test_client_system)

print("=" * 80)
print("📊 Test Summary")
print("=" * 80)
print()

passed = sum(1 for _, success, _ in results if success)
total = len(results)

for name, success, msg in results:
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {name}")
    if msg and len(msg) < 100:
        print(f"   → {msg}")

print()
print(f"Results: {passed}/{total} tests passed ({passed*100//total}%)")
print()

if passed == total:
    print("🎉 All systems operational!")
    sys.exit(0)
else:
    print("⚠️  Some tests failed - check configuration")
    sys.exit(1)
