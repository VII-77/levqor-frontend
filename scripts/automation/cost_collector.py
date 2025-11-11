#!/usr/bin/env python3
"""
Cost Dashboard Data Collector
Pulls daily spend from Replit, Stripe, Vercel
Logs to Notion Cost Dashboard
Alerts if Replit spend > $10
"""
import os
import sys
import requests
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from server.notion_helper import NotionHelper, notion_title, notion_number, notion_checkbox, notion_date

def get_replit_usage():
    """Get Replit usage and costs (mock for now)"""
    # TODO: Implement actual Replit API when available
    return {
        "ai_spend": 0.0,
        "compute_spend": 0.0,
        "total": 0.0,
        "date": datetime.utcnow().date().isoformat(),
    }

def get_stripe_revenue():
    """Get Stripe revenue, fees, and failed payments"""
    stripe_key = os.getenv("STRIPE_SECRET_KEY")
    if not stripe_key:
        print("⚠️  Stripe key not configured")
        return {
            "revenue": 0.0,
            "fees": 0.0,
            "addon_revenue": 0.0,
            "failed_payments": 0
        }
    
    try:
        # Get charges from last 24 hours
        yesterday = int((datetime.utcnow() - timedelta(days=1)).timestamp())
        
        headers = {"Authorization": f"Bearer {stripe_key}"}
        params = {"created[gte]": yesterday, "limit": 100}
        
        response = requests.get(
            "https://api.stripe.com/v1/charges",
            headers=headers,
            params=params,
        )
        
        if response.status_code == 200:
            data = response.json()
            charges = data.get("data", [])
            
            successful = sum(c["amount"] for c in charges if c["paid"]) / 100
            failed = sum(1 for c in charges if not c["paid"])
            
            # Calculate Stripe fees (2.9% + $0.30 per transaction)
            stripe_fees = sum(
                (c["amount"] * 0.029 + 30) / 100 
                for c in charges if c["paid"]
            )
            
            # Track add-on revenue (Integrity Pack, Templates, etc.)
            addon_charges = [
                c for c in charges 
                if c.get("paid") and any(
                    keyword in c.get("description", "").lower() 
                    for keyword in ["integrity", "template", "api"]
                )
            ]
            addon_revenue = sum(c["amount"] for c in addon_charges) / 100
            
            return {
                "revenue": successful,
                "fees": stripe_fees,
                "addon_revenue": addon_revenue,
                "failed_payments": failed,
                "total_transactions": len(charges),
            }
        else:
            print(f"⚠️  Stripe API error: {response.status_code}")
            return {
                "revenue": 0.0,
                "fees": 0.0,
                "addon_revenue": 0.0,
                "failed_payments": 0
            }
            
    except Exception as e:
        print(f"❌ Stripe error: {str(e)}")
        return {
            "revenue": 0.0,
            "fees": 0.0,
            "addon_revenue": 0.0,
            "failed_payments": 0
        }

def get_vercel_usage():
    """Get Vercel build minutes and bandwidth"""
    vercel_token = os.getenv("VERCEL_TOKEN")
    if not vercel_token:
        print("⚠️  Vercel token not configured")
        return {"build_minutes": 0, "bandwidth_gb": 0.0}
    
    # TODO: Implement Vercel usage API when needed
    return {
        "build_minutes": 0,
        "bandwidth_gb": 0.0,
    }

def check_cost_alerts(data):
    """Check if any cost thresholds exceeded"""
    alerts = []
    
    replit_total = data["replit"]["total"]
    if replit_total > 10.0:
        alerts.append(f"🚨 Replit spend (${replit_total:.2f}) exceeds $10 threshold")
    
    failed_payments = data["stripe"]["failed_payments"]
    if failed_payments > 0:
        alerts.append(f"⚠️  {failed_payments} failed Stripe payment(s)")
    
    return alerts

def log_to_notion(data, alerts):
    """Log cost data to Notion dashboard"""
    # Calculate costs and margins
    total_costs = (
        data['replit']['total'] + 
        data['vercel']['bandwidth_gb'] + 
        data['stripe']['fees']
    )
    
    total_revenue = data['stripe']['revenue']
    addon_revenue = data['stripe']['addon_revenue']
    net_margin = total_revenue - total_costs
    margin_percent = (net_margin / total_revenue * 100) if total_revenue > 0 else 0
    
    print("\n📊 Cost Dashboard Summary:")
    print(f"  Replit: ${data['replit']['total']:.2f}")
    print(f"  Vercel: ${data['vercel']['bandwidth_gb']:.2f}")
    print(f"  Stripe Fees: ${data['stripe']['fees']:.2f}")
    print(f"  Total Costs: ${total_costs:.2f}")
    print(f"\n  Revenue: ${total_revenue:.2f}")
    print(f"  Add-on Revenue: ${addon_revenue:.2f}")
    print(f"  Net Margin: ${net_margin:.2f} ({margin_percent:.1f}%)")
    print(f"  Failed Payments: {data['stripe']['failed_payments']}")
    
    if alerts:
        print("\n🚨 ALERTS:")
        for alert in alerts:
            print(f"  {alert}")
    
    db_id = os.getenv("NOTION_COST_DB_ID", "").strip()
    
    if not db_id:
        print("ℹ️  NOTION_COST_DB_ID not configured, skipping Notion logging")
        print("   Add your database ID to Secrets to enable Notion integration")
        return
    
    try:
        notion = NotionHelper()
        today = datetime.utcnow().date().isoformat()
        
        properties = {
            "Date": notion_title(today),
            "Replit": notion_number(data['replit']['total']),
            "Stripe Revenue": notion_number(total_revenue),
            "Stripe Fees": notion_number(data['stripe']['fees']),
            "Add-on Revenue": notion_number(addon_revenue),
            "Vercel": notion_number(data['vercel']['bandwidth_gb']),
            "Failed Payments": notion_number(data['stripe']['failed_payments']),
            "Total Cost": notion_number(total_costs),
            "Net Margin": notion_number(net_margin),
            "Alert": notion_checkbox(len(alerts) > 0),
        }
        
        notion.create_page(db_id, properties)
        print("✅ Cost data logged to Notion")
        
    except Exception as e:
        print(f"⚠️  Notion logging failed: {str(e)}")
        print("   Cost collection completed, but not logged to Notion")

if __name__ == "__main__":
    print(f"💰 Cost Collection - {datetime.utcnow().isoformat()}")
    
    data = {
        "replit": get_replit_usage(),
        "stripe": get_stripe_revenue(),
        "vercel": get_vercel_usage(),
        "timestamp": datetime.utcnow().isoformat(),
    }
    
    alerts = check_cost_alerts(data)
    log_to_notion(data, alerts)
    
    exit_code = 1 if alerts else 0
    exit(exit_code)
