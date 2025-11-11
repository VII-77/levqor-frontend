"""
Alerting System for Go/No-Go Monitoring
Checks critical metrics and sends alerts
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import requests
import json

# Alert thresholds
ERROR_RATE_THRESHOLD = 0.5  # 0.5%
COST_THRESHOLD = 10.0  # $10/day
BURST_5XX_THRESHOLD = 5  # 5 errors in 1 minute

def get_db_connection():
    """Get PostgreSQL connection"""
    return psycopg2.connect(
        os.environ.get("DATABASE_URL"),
        cursor_factory=RealDictCursor
    )

def check_error_rate():
    """Check if error rate exceeds 0.5%"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    COUNT(*) as total_checks,
                    COUNT(CASE WHEN error IS NOT NULL THEN 1 END) as error_count
                FROM system_health_log
                WHERE timestamp > NOW() - INTERVAL '1 hour'
            """)
            
            row = cur.fetchone()
            
            if row and row['total_checks'] > 0:
                error_rate = (row['error_count'] / row['total_checks']) * 100
                
                if error_rate > ERROR_RATE_THRESHOLD:
                    return {
                        "alert": True,
                        "metric": "error_rate",
                        "value": error_rate,
                        "threshold": ERROR_RATE_THRESHOLD,
                        "message": f"Error rate {error_rate:.2f}% exceeds threshold {ERROR_RATE_THRESHOLD}%"
                    }
            
            return {"alert": False, "metric": "error_rate", "value": error_rate if row else 0}

def check_5xx_burst():
    """Check for 5xx error bursts (>5 errors in 1 minute)"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    COUNT(*) as error_count
                FROM system_health_log
                WHERE timestamp > NOW() - INTERVAL '1 minute'
                AND (backend >= 500 OR frontend >= 500)
            """)
            
            row = cur.fetchone()
            error_count = row['error_count'] if row else 0
            
            if error_count > BURST_5XX_THRESHOLD:
                return {
                    "alert": True,
                    "metric": "5xx_burst",
                    "value": error_count,
                    "threshold": BURST_5XX_THRESHOLD,
                    "message": f"5xx burst detected: {error_count} errors in 1 minute"
                }
            
            return {"alert": False, "metric": "5xx_burst", "value": error_count}

def check_daily_cost():
    """Check if Replit spend exceeds $10/day"""
    # This would integrate with Replit cost API or tracking
    # For now, return placeholder
    return {
        "alert": False,
        "metric": "daily_cost",
        "value": 0,
        "message": "Cost tracking pending Replit API integration"
    }

def send_alert(alert_data):
    """Send alert via configured channels (Slack, email, etc.)"""
    print(f"\n🚨 ALERT: {alert_data['message']}")
    
    # Log to database
    try:
        from modules.auto_intel.db_adapter import log_intel_action
        log_intel_action(
            action='alert_triggered',
            metadata=alert_data
        )
    except Exception as e:
        print(f"⚠️ Could not log alert: {e}")
    
    # Send to Slack if webhook configured
    slack_webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if slack_webhook:
        try:
            payload = {
                "text": f"🚨 Levqor Alert: {alert_data['message']}",
                "attachments": [{
                    "color": "danger",
                    "fields": [
                        {"title": "Metric", "value": alert_data['metric'], "short": True},
                        {"title": "Value", "value": str(alert_data['value']), "short": True},
                        {"title": "Threshold", "value": str(alert_data.get('threshold', 'N/A')), "short": True},
                    ]
                }]
            }
            requests.post(slack_webhook, json=payload, timeout=5)
            print("  ✅ Alert sent to Slack")
        except Exception as e:
            print(f"  ⚠️ Slack alert failed: {e}")

def run_alert_checks():
    """Run all alert checks"""
    print(f"\n🔔 Running alert checks at {datetime.utcnow().isoformat()}")
    
    checks = [
        check_error_rate(),
        check_5xx_burst(),
        check_daily_cost(),
    ]
    
    alerts_triggered = [check for check in checks if check.get('alert')]
    
    if alerts_triggered:
        print(f"⚠️ {len(alerts_triggered)} alert(s) triggered")
        for alert in alerts_triggered:
            send_alert(alert)
    else:
        print("✅ All checks passed - no alerts")
    
    return checks

if __name__ == "__main__":
    run_alert_checks()
