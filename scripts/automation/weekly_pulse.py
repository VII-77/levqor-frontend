#!/usr/bin/env python3
"""
Weekly Pulse Summary
Collects: uptime %, spend $, sign-ups, churn
Sends to Notion and email
Runs every Friday
"""
import os
import sys
import requests
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from server.notion_helper import NotionHelper, notion_title, notion_number, notion_rich_text, notion_date

def get_expansion_metrics():
    """Collect expansion product metrics"""
    metrics = {
        "integrity_runs": 0,
        "template_sales": 0.0,
        "api_revenue": 0.0,
        "white_label_inquiries": 0,
    }
    
    try:
        # Count Integrity Pack runs from Notion (if configured)
        notion_integrity_db = os.getenv("NOTION_INTEGRITY_DB_ID", "").strip()
        if notion_integrity_db:
            # TODO: Query Notion for integrity runs count (when DB is set up)
            pass
        
        # Get Template Pack sales from Stripe
        stripe_key = os.getenv("STRIPE_SECRET_KEY", "").strip()
        if stripe_key:
            try:
                headers = {"Authorization": f"Bearer {stripe_key}"}
                
                # Get charges for template packs (filter by metadata or description)
                week_ago = int((datetime.utcnow() - timedelta(days=7)).timestamp())
                params = {"created[gte]": week_ago, "limit": 100}
                
                response = requests.get(
                    "https://api.stripe.com/v1/charges",
                    headers=headers,
                    params=params,
                )
                
                if response.status_code == 200:
                    data = response.json()
                    charges = data.get("data", [])
                    
                    # Filter for template pack purchases (by description or metadata)
                    template_charges = [
                        c for c in charges 
                        if c.get("paid") and "template" in c.get("description", "").lower()
                    ]
                    metrics["template_sales"] = sum(c["amount"] for c in template_charges) / 100
                    
                    # Filter for API tier charges
                    api_charges = [
                        c for c in charges 
                        if c.get("paid") and "api" in c.get("description", "").lower()
                    ]
                    metrics["api_revenue"] = sum(c["amount"] for c in api_charges) / 100
                    
            except Exception as e:
                print(f"⚠️  Stripe expansion metrics error: {str(e)}")
        
        # Count white-label inquiries from Notion (if configured)
        notion_leads_db = os.getenv("NOTION_AGENCY_LEADS_DB_ID", "").strip()
        if notion_leads_db:
            # TODO: Query Notion for agency leads count (when DB is set up)
            pass
            
    except Exception as e:
        print(f"⚠️  Expansion metrics error: {str(e)}")
    
    return metrics

def collect_pulse_data():
    """Collect weekly pulse metrics"""
    try:
        # Get uptime from metrics
        metrics_response = requests.get("https://api.levqor.ai/public/metrics", timeout=10)
        uptime_7d = 0.0
        
        if metrics_response.status_code == 200:
            metrics = metrics_response.json()
            uptime_7d = metrics.get("uptime_rolling_7d", 0.0)
        
        # Get expansion metrics
        expansion = get_expansion_metrics()
        
        # TODO: Get actual user metrics from database
        pulse = {
            "week_ending": datetime.utcnow().date().isoformat(),
            "uptime_percent": uptime_7d,
            "total_spend": 0.0,  # Sum of Replit + Vercel
            "revenue": 0.0,  # From Stripe
            "new_signups": 0,  # From users table
            "churn_count": 0,  # Cancelled subscriptions
            "active_users": 0,  # From sessions/activity
            # Expansion metrics
            "integrity_runs": expansion["integrity_runs"],
            "template_sales": expansion["template_sales"],
            "api_revenue": expansion["api_revenue"],
            "white_label_inquiries": expansion["white_label_inquiries"],
        }
        
        return pulse
        
    except Exception as e:
        print(f"❌ Pulse collection error: {str(e)}")
        return None

def generate_summary(pulse):
    """Generate human-readable summary"""
    if not pulse:
        return "Failed to collect pulse data"
    
    expansion_total = (
        pulse['template_sales'] + 
        pulse['api_revenue']
    )
    
    summary = f"""
📊 LEVQOR WEEKLY PULSE
Week ending: {pulse['week_ending']}

🟢 UPTIME
  • 7-day rolling: {pulse['uptime_percent']:.2f}%

💰 FINANCIAL
  • Total spend: ${pulse['total_spend']:.2f}
  • Revenue: ${pulse['revenue']:.2f}
  • Net: ${pulse['revenue'] - pulse['total_spend']:.2f}

👥 USERS
  • New sign-ups: {pulse['new_signups']}
  • Churn: {pulse['churn_count']}
  • Active users: {pulse['active_users']}

🚀 EXPANSION PRODUCTS
  • Integrity runs: {pulse['integrity_runs']}
  • Template sales: ${pulse['template_sales']:.2f}
  • API revenue: ${pulse['api_revenue']:.2f}
  • White-label inquiries: {pulse['white_label_inquiries']}
  • Total expansion: ${expansion_total:.2f}
"""
    return summary

def send_to_notion(pulse, summary):
    """Log pulse to Notion database"""
    print(summary)
    
    db_id = os.getenv("NOTION_PULSE_DB_ID", "").strip()
    
    if not db_id:
        print("ℹ️  NOTION_PULSE_DB_ID not configured, skipping Notion logging")
        print("   Add your database ID to Secrets to enable Notion integration")
        return
    
    try:
        notion = NotionHelper()
        
        net_profit = pulse['revenue'] - pulse['total_spend']
        
        properties = {
            "Week Ending": notion_title(pulse['week_ending']),
            "Uptime": notion_number(pulse['uptime_percent']),
            "Revenue": notion_number(pulse['revenue']),
            "Active Users": notion_number(pulse['active_users']),
            "Churn": notion_number(pulse['churn_count']),
            "Net": notion_number(net_profit),
            "Summary": notion_rich_text(summary),
        }
        
        notion.create_page(db_id, properties)
        print("✅ Pulse logged to Notion")
        
    except Exception as e:
        print(f"⚠️  Notion logging failed: {str(e)}")
        print("   Pulse collection completed, but not logged to Notion")

def send_email_summary(summary):
    """Send pulse summary via email using Resend"""
    receiving_email = os.getenv("RECEIVING_EMAIL", "").strip()
    resend_api_key = os.getenv("RESEND_API_KEY", "").strip()
    
    if not receiving_email or not resend_api_key:
        print("ℹ️  Email not configured (RECEIVING_EMAIL or RESEND_API_KEY missing)")
        return
    
    try:
        import requests
        
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {resend_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "from": "Levqor Pulse <noreply@levqor.ai>",
            "to": [receiving_email],
            "subject": f"📊 Weekly Pulse - {datetime.utcnow().strftime('%B %d, %Y')}",
            "html": f"<pre>{summary}</pre>"
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print("✅ Email summary sent via Resend")
        else:
            print(f"⚠️  Email send failed: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️  Email send error: {str(e)}")

if __name__ == "__main__":
    print(f"📈 Weekly Pulse Collection - {datetime.utcnow().isoformat()}")
    
    pulse = collect_pulse_data()
    summary = generate_summary(pulse)
    
    if pulse:
        send_to_notion(pulse, summary)
        send_email_summary(summary)
        print("✅ Weekly pulse complete")
        exit(0)
    else:
        print("❌ Pulse collection failed")
        exit(1)
