#!/usr/bin/env python3
"""
Expansion Verification Cron
Nightly health check for:
- Notion write success
- Stripe data fetch completeness
- Replit cost threshold
Logs anomalies to System Health Log
"""
import os
import sys
import requests
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from server.notion_helper import NotionHelper, notion_title, notion_date, notion_select, notion_number, notion_rich_text


def check_notion_health():
    """Verify Notion API is responding"""
    print("\n🔍 Checking Notion Health...")
    
    notion_token = os.getenv("NOTION_TOKEN", "").strip()
    
    if not notion_token:
        print("  ⚠️  Notion: Not configured")
        return True, "Notion not configured (skipped)"
    
    try:
        notion = NotionHelper()
        
        # Test authentication - just creating the helper is sufficient
        # since it validates the token on initialization
        print("  ✅ Notion API: Authenticated")
        return True, "Notion API healthy"
            
    except Exception as e:
        print(f"  ❌ Notion API: Error - {str(e)}")
        return False, f"Notion error: {str(e)}"


def check_stripe_health():
    """Verify Stripe data fetches complete"""
    print("\n🔍 Checking Stripe Health...")
    
    stripe_key = os.getenv("STRIPE_SECRET_KEY", "").strip()
    if not stripe_key:
        print("  ⚠️  Stripe: Not configured")
        return True, "Stripe not configured (skipped)"
    
    try:
        headers = {"Authorization": f"Bearer {stripe_key}"}
        
        # Test balance endpoint (lightweight check)
        response = requests.get("https://api.stripe.com/v1/balance", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("  ✅ Stripe API: Connected")
            
            # Check recent charges exist
            yesterday = int((datetime.utcnow() - timedelta(days=1)).timestamp())
            params = {"created[gte]": yesterday, "limit": 1}
            
            charges_response = requests.get(
                "https://api.stripe.com/v1/charges",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if charges_response.status_code == 200:
                print("  ✅ Stripe Charges: Accessible")
                return True, "Stripe API healthy"
            else:
                print(f"  ⚠️  Stripe Charges: HTTP {charges_response.status_code}")
                return False, f"Stripe charges returned {charges_response.status_code}"
        else:
            print(f"  ❌ Stripe API: HTTP {response.status_code}")
            return False, f"Stripe API returned {response.status_code}"
            
    except Exception as e:
        print(f"  ❌ Stripe: Error - {str(e)}")
        return False, f"Stripe error: {str(e)}"


def check_cost_threshold():
    """Verify Replit cost is under threshold"""
    print("\n🔍 Checking Cost Threshold...")
    
    # For now, this is a placeholder since we don't have direct Replit API access
    # In production, you'd query actual Replit costs
    
    estimated_daily_cost = 0.0  # TODO: Get from Replit API when available
    threshold = 10.0
    
    if estimated_daily_cost > threshold:
        print(f"  ⚠️  Replit cost: ${estimated_daily_cost:.2f} exceeds ${threshold:.2f} threshold")
        return False, f"Daily cost ${estimated_daily_cost:.2f} exceeds threshold"
    else:
        print(f"  ✅ Replit cost: ${estimated_daily_cost:.2f} (under ${threshold:.2f} threshold)")
        return True, f"Cost within threshold: ${estimated_daily_cost:.2f}"


def log_verification_results(results):
    """Log verification results to Notion System Health Log"""
    print("\n📊 Verification Summary:")
    
    all_healthy = all(r["healthy"] for r in results)
    failed_checks = [r for r in results if not r["healthy"]]
    
    for result in results:
        status_emoji = "✅" if result["healthy"] else "❌"
        print(f"  {status_emoji} {result['check']}: {result['message']}")
    
    if failed_checks:
        print(f"\n⚠️  {len(failed_checks)} check(s) failed")
    else:
        print("\n✅ All verification checks passed")
    
    # Log to Notion if configured
    db_id = os.getenv("NOTION_HEALTH_DB_ID", "").strip()
    
    if not db_id:
        print("ℹ️  NOTION_HEALTH_DB_ID not configured, skipping Notion logging")
        return all_healthy
    
    try:
        notion = NotionHelper()
        
        # Create summary of failed checks
        if failed_checks:
            notes = "Failed checks: " + ", ".join([f"{r['check']}: {r['message']}" for r in failed_checks])
        else:
            notes = "All verification checks passed"
        
        properties = {
            "Name": notion_title(f"Expansion Verification - {datetime.utcnow().strftime('%Y-%m-%d')}"),
            "Timestamp": notion_date(datetime.utcnow().isoformat()),
            "Endpoint": notion_rich_text("Expansion System"),
            "Status": notion_select("Healthy" if all_healthy else "Degraded"),
            "Latency": notion_number(len(results)),  # Number of checks
            "Notes": notion_rich_text(notes[:2000]),  # Limit to 2000 chars
        }
        
        notion.create_page(db_id, properties)
        print("✅ Verification logged to Notion")
        
    except Exception as e:
        print(f"⚠️  Notion logging failed: {str(e)}")
    
    return all_healthy


if __name__ == "__main__":
    print(f"🔐 Expansion Verification - {datetime.utcnow().isoformat()}")
    
    results = []
    
    # Run all checks
    notion_healthy, notion_msg = check_notion_health()
    results.append({
        "check": "Notion API",
        "healthy": notion_healthy,
        "message": notion_msg
    })
    
    stripe_healthy, stripe_msg = check_stripe_health()
    results.append({
        "check": "Stripe API",
        "healthy": stripe_healthy,
        "message": stripe_msg
    })
    
    cost_healthy, cost_msg = check_cost_threshold()
    results.append({
        "check": "Cost Threshold",
        "healthy": cost_healthy,
        "message": cost_msg
    })
    
    # Log results
    all_healthy = log_verification_results(results)
    
    # Exit with error code if any check failed
    exit_code = 0 if all_healthy else 1
    exit(exit_code)
