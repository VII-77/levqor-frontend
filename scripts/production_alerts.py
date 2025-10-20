#!/usr/bin/env python3
"""
Production Alert Monitor
Monitors critical metrics and sends alerts for:
- Webhook failures (>3 in 5min)
- Payment error rate (>5%/hour)
- Revenue dips (>30% day-over-day)
"""
import os
import sys
import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from bot import config
from bot.notion_api import NotionClientWrapper

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

def send_alert(title, message, severity="WARNING"):
    """Send Telegram alert"""
    emoji = {"CRITICAL": "🔴", "WARNING": "⚠️", "INFO": "ℹ️"}.get(severity, "📊")
    text = f"{emoji} *{title}*\n\n{message}\n\n_Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC_"
    
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"},
                timeout=10
            )
        except:
            pass
    
    print(json.dumps({
        "ts": datetime.utcnow().isoformat() + "Z",
        "event": "alert",
        "severity": severity,
        "title": title,
        "message": message
    }))

def check_webhook_failures():
    """Alert if >3 webhook failures in last 5 minutes"""
    ops_monitor_id = os.getenv('NOTION_OPS_MONITOR_DB_ID', '')
    
    if not ops_monitor_id:
        return 0
    
    notion = NotionClientWrapper()
    cutoff_time = datetime.utcnow() - timedelta(minutes=5)
    
    try:
        results = notion.notion.databases.query(
            database_id=ops_monitor_id,
            filter={
                "and": [
                    {"property": "Event Type", "select": {"equals": "webhook_failure"}},
                    {"property": "Created", "date": {"after": cutoff_time.isoformat()}}
                ]
            }
        )
        
        failure_count = len(results.get('results', []))
        
        if failure_count > 3:
            send_alert(
                "Webhook Failures Detected",
                f"⚠️ {failure_count} webhook failures in last 5 minutes\n"
                f"Threshold: >3 failures\n"
                f"Action: Check Stripe webhook logs",
                severity="CRITICAL"
            )
            return failure_count
    except:
        pass
    
    return 0

def check_payment_errors():
    """Alert if >5% payment error rate in last hour"""
    job_log_id = os.getenv('JOB_LOG_DB_ID', '')
    
    if not job_log_id:
        return 0
    
    notion = NotionClientWrapper()
    cutoff_time = datetime.utcnow() - timedelta(hours=1)
    
    try:
        # Get all payment attempts in last hour
        results = notion.notion.databases.query(
            database_id=job_log_id,
            filter={
                "and": [
                    {"property": "Created", "date": {"after": cutoff_time.isoformat()}},
                    {"property": "Payment Status", "select": {"is_not_empty": True}}
                ]
            }
        )
        
        total = 0
        errors = 0
        
        for page in results.get('results', []):
            props = page.get('properties', {})
            status = props.get('Payment Status', {}).get('select', {}).get('name', '')
            
            if status in ['Pending', 'Paid', 'Failed', 'Refunded']:
                total += 1
                if status == 'Failed':
                    errors += 1
        
        if total > 0:
            error_rate = (errors / total) * 100
            
            if error_rate > 5:
                send_alert(
                    "High Payment Error Rate",
                    f"⚠️ Payment errors: {errors}/{total} ({error_rate:.1f}%)\n"
                    f"Threshold: >5% errors\n"
                    f"Action: Check Stripe logs and API status",
                    severity="CRITICAL"
                )
                return error_rate
    except:
        pass
    
    return 0

def check_revenue_dip():
    """Alert if >30% revenue drop day-over-day"""
    finance_db_id = os.getenv('NOTION_FINANCE_DB_ID', '')
    
    if not finance_db_id:
        return 0
    
    notion = NotionClientWrapper()
    
    try:
        # Get last 2 days of revenue
        results = notion.notion.databases.query(
            database_id=finance_db_id,
            sorts=[{"property": "Date", "direction": "descending"}],
            page_size=2
        )
        
        pages = results.get('results', [])
        
        if len(pages) >= 2:
            today_rev = pages[0].get('properties', {}).get('Revenue USD', {}).get('number', 0)
            yesterday_rev = pages[1].get('properties', {}).get('Revenue USD', {}).get('number', 0)
            
            if yesterday_rev > 0:
                change_pct = ((today_rev - yesterday_rev) / yesterday_rev) * 100
                
                if change_pct < -30:
                    send_alert(
                        "Revenue Dip Detected",
                        f"⚠️ Revenue dropped {abs(change_pct):.1f}%\n"
                        f"Today: ${today_rev:.2f}\n"
                        f"Yesterday: ${yesterday_rev:.2f}\n"
                        f"Threshold: >30% drop\n"
                        f"Action: Review active jobs and client activity",
                        severity="WARNING"
                    )
                    return change_pct
    except:
        pass
    
    return 0

def main():
    print(json.dumps({
        "ts": datetime.utcnow().isoformat() + "Z",
        "event": "production_alerts_start"
    }))
    
    # Run all checks
    webhook_failures = check_webhook_failures()
    payment_error_rate = check_payment_errors()
    revenue_change = check_revenue_dip()
    
    print(json.dumps({
        "ts": datetime.utcnow().isoformat() + "Z",
        "event": "production_alerts_complete",
        "webhook_failures": webhook_failures,
        "payment_error_rate": payment_error_rate,
        "revenue_change": revenue_change
    }))

if __name__ == "__main__":
    main()
