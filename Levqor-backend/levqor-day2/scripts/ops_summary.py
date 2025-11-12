#!/usr/bin/env python3
"""
Levqor Ops Summary - Automated operational reporting
Sends daily/weekly summary emails with system metrics, health, and cost tracking.
"""
import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta
from time import time

try:
    import requests
except ImportError:
    print("Error: requests library not installed. Run: pip install requests")
    sys.exit(1)

BACKEND_URL = os.getenv("BACKEND_URL", "https://api.levqor.ai")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RECEIVING_EMAIL = os.getenv("RECEIVING_EMAIL", "ops@levqor.ai")
DB_PATH = os.getenv("SQLITE_PATH", "levqor.db")

def get_system_metrics():
    """Fetch system health and operational metrics"""
    metrics = {
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": None,
        "health": None,
        "queue": None,
        "billing": None,
        "error": None
    }
    
    try:
        resp = requests.get(f"{BACKEND_URL}/ops/uptime", timeout=10)
        if resp.status_code == 200:
            metrics["uptime"] = resp.json()
    except Exception as e:
        metrics["error"] = f"Uptime fetch failed: {str(e)}"
    
    try:
        resp = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if resp.status_code == 200:
            metrics["health"] = resp.json()
    except Exception as e:
        if not metrics["error"]:
            metrics["error"] = f"Health fetch failed: {str(e)}"
    
    try:
        resp = requests.get(f"{BACKEND_URL}/ops/queue_health", timeout=10)
        if resp.status_code == 200:
            metrics["queue"] = resp.json()
    except Exception:
        pass
    
    try:
        resp = requests.get(f"{BACKEND_URL}/billing/health", timeout=10)
        if resp.status_code == 200:
            metrics["billing"] = resp.json()
    except Exception:
        pass
    
    return metrics

def get_db_stats():
    """Get database statistics"""
    stats = {
        "total_users": 0,
        "new_users_7d": 0,
        "db_size_mb": 0
    }
    
    try:
        if os.path.exists(DB_PATH):
            stats["db_size_mb"] = round(os.path.getsize(DB_PATH) / 1024 / 1024, 2)
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM users")
            stats["total_users"] = cursor.fetchone()[0]
            
            seven_days_ago = time() - (7 * 24 * 60 * 60)
            cursor.execute("SELECT COUNT(*) FROM users WHERE created_at >= ?", (seven_days_ago,))
            stats["new_users_7d"] = cursor.fetchone()[0]
            
            conn.close()
    except Exception as e:
        stats["error"] = str(e)
    
    return stats

def format_html_report(metrics, db_stats, report_type="daily"):
    """Generate HTML email report"""
    status_emoji = "🟢" if metrics.get("health", {}).get("ok") else "🔴"
    uptime_data = metrics.get("uptime", {})
    queue_data = metrics.get("queue", {})
    billing_data = metrics.get("billing", {})
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
        .content {{ padding: 30px; }}
        .metric-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0; }}
        .metric {{ background: #f8f9fa; padding: 15px; border-radius: 6px; border-left: 3px solid #667eea; }}
        .metric-label {{ font-size: 12px; color: #6c757d; text-transform: uppercase; letter-spacing: 0.5px; }}
        .metric-value {{ font-size: 24px; font-weight: 600; margin-top: 5px; color: #212529; }}
        .status-ok {{ color: #28a745; }}
        .status-warn {{ color: #ffc107; }}
        .status-error {{ color: #dc3545; }}
        .section {{ margin: 25px 0; }}
        .section-title {{ font-size: 16px; font-weight: 600; margin-bottom: 15px; color: #495057; border-bottom: 2px solid #e9ecef; padding-bottom: 8px; }}
        .quick-links {{ background: #f8f9fa; padding: 20px; border-radius: 6px; }}
        .quick-links a {{ display: inline-block; margin: 5px 10px 5px 0; padding: 8px 16px; background: white; border: 1px solid #dee2e6; border-radius: 4px; text-decoration: none; color: #495057; font-size: 13px; }}
        .quick-links a:hover {{ background: #667eea; color: white; border-color: #667eea; }}
        .footer {{ background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #6c757d; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{status_emoji} Levqor {report_type.title()} Ops Report</h1>
            <p>{metrics['timestamp']}</p>
        </div>
        
        <div class="content">
            <div class="section">
                <div class="section-title">System Health</div>
                <div class="metric-grid">
                    <div class="metric">
                        <div class="metric-label">Status</div>
                        <div class="metric-value status-{'ok' if uptime_data.get('status') == 'operational' else 'error'}">
                            {uptime_data.get('status', 'unknown').upper()}
                        </div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Version</div>
                        <div class="metric-value">{uptime_data.get('version', 'N/A')}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">API Service</div>
                        <div class="metric-value status-{'ok' if uptime_data.get('services', {}).get('api') == 'operational' else 'error'}">
                            {uptime_data.get('services', {}).get('api', 'unknown').upper()}
                        </div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Database</div>
                        <div class="metric-value status-{'ok' if uptime_data.get('services', {}).get('database') == 'operational' else 'error'}">
                            {uptime_data.get('services', {}).get('database', 'unknown').upper()}
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">User Metrics</div>
                <div class="metric-grid">
                    <div class="metric">
                        <div class="metric-label">Total Users</div>
                        <div class="metric-value">{db_stats.get('total_users', 0):,}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">New Users (7d)</div>
                        <div class="metric-value">{db_stats.get('new_users_7d', 0):,}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Database Size</div>
                        <div class="metric-value">{db_stats.get('db_size_mb', 0)} MB</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Queue Depth</div>
                        <div class="metric-value">{queue_data.get('depth', 0)}</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">Billing & Infrastructure</div>
                <div class="metric-grid">
                    <div class="metric">
                        <div class="metric-label">Stripe Status</div>
                        <div class="metric-value status-{'ok' if billing_data.get('stripe') else 'warn'}">
                            {'ACTIVE' if billing_data.get('stripe') else 'N/A'}
                        </div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Available Features</div>
                        <div class="metric-value">{len(billing_data.get('available', []))}</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">Quick Links</div>
                <div class="quick-links">
                    <a href="{BACKEND_URL}/ops/uptime" target="_blank">Backend Uptime</a>
                    <a href="{BACKEND_URL}/ops/queue_health" target="_blank">Queue Health</a>
                    <a href="{BACKEND_URL}/billing/health" target="_blank">Billing Status</a>
                    <a href="https://dashboard.stripe.com" target="_blank">Stripe Dashboard</a>
                    <a href="https://resend.com/emails" target="_blank">Resend Logs</a>
                    <a href="https://github.com/{os.getenv('GITHUB_REPO', 'levqor/levqor')}/actions" target="_blank">GitHub Actions</a>
                </div>
            </div>
        </div>
        
        <div class="footer">
            Generated by Levqor Ops Summary • {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}
        </div>
    </div>
</body>
</html>
"""
    return html

def send_email_report(html_content, report_type="daily"):
    """Send email via Resend"""
    if not RESEND_API_KEY:
        print("Error: RESEND_API_KEY not set. Cannot send email.")
        return False
    
    subject = f"Levqor {report_type.title()} Ops Report - {datetime.utcnow().strftime('%Y-%m-%d')}"
    
    payload = {
        "from": "Levqor Ops <ops@levqor.ai>",
        "to": [RECEIVING_EMAIL],
        "subject": subject,
        "html": html_content
    }
    
    try:
        resp = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=10
        )
        
        if resp.status_code == 200:
            print(f"✅ Email sent successfully to {RECEIVING_EMAIL}")
            return True
        else:
            print(f"❌ Email failed: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        print(f"❌ Email error: {str(e)}")
        return False

def main():
    """Main execution"""
    import argparse
    parser = argparse.ArgumentParser(description="Levqor Ops Summary Reporter")
    parser.add_argument("--type", choices=["daily", "weekly"], default="daily", help="Report type")
    parser.add_argument("--no-email", action="store_true", help="Don't send email, just print to stdout")
    args = parser.parse_args()
    
    print(f"🔍 Gathering {args.type} operational metrics...")
    
    metrics = get_system_metrics()
    db_stats = get_db_stats()
    
    if metrics.get("error"):
        print(f"⚠️  Warning: {metrics['error']}")
    
    html_report = format_html_report(metrics, db_stats, args.type)
    
    if args.no_email:
        print("\n" + "="*60)
        print("HTML REPORT (preview)")
        print("="*60)
        print(f"System Status: {metrics.get('uptime', {}).get('status', 'unknown')}")
        print(f"Total Users: {db_stats.get('total_users', 0)}")
        print(f"New Users (7d): {db_stats.get('new_users_7d', 0)}")
        print(f"Database Size: {db_stats.get('db_size_mb', 0)} MB")
        print("="*60)
    else:
        send_email_report(html_report, args.type)
    
    print(f"✅ {args.type.title()} ops summary complete!")

if __name__ == "__main__":
    main()
