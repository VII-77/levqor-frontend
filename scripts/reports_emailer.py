#!/usr/bin/env python3
"""
Phase 56: Reports Emailer
Sends daily CEO brief and metrics via email
"""
import os
import sys
import json
import glob
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def send_daily_report():
    """Send daily CEO brief and metrics via email"""
    try:
        from scripts.emailer import send_email
        
        # Get latest CEO brief
        brief_files = sorted(glob.glob("logs/exec_briefs/brief_*.json"))
        latest_brief = None
        if brief_files:
            with open(brief_files[-1], 'r') as f:
                latest_brief = json.load(f)
        
        # Get latest governance report
        governance = {}
        if os.path.exists('logs/governance_report.json'):
            with open('logs/governance_report.json', 'r') as f:
                governance = json.load(f)
        
        # Get latest observability
        observability = {}
        if os.path.exists('logs/observability.json'):
            with open('logs/observability.json', 'r') as f:
                observability = json.load(f)
        
        # Build email content
        subject = f"[EchoPilot] Daily Report - {datetime.utcnow().strftime('%Y-%m-%d')}"
        
        body_parts = [
            "EchoPilot Daily Report",
            "=" * 50,
            "",
            f"Report Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
            ""
        ]
        
        # System Health
        if observability:
            system = observability.get('system', {})
            health = observability.get('health', {})
            body_parts.extend([
                "SYSTEM HEALTH:",
                f"  Status: {health.get('overall', 'unknown')}",
                f"  CPU: {system.get('cpu_percent', 0):.1f}%",
                f"  Memory: {system.get('mem_percent', 0):.1f}%",
                f"  Disk: {system.get('disk_percent', 0):.1f}%",
                ""
            ])
        
        # Governance Status
        if governance:
            checks = governance.get('checks', {})
            body_parts.extend([
                "GOVERNANCE:",
                f"  Overall: {governance.get('status', 'unknown')}",
                f"  Revenue: {checks.get('revenue', 'unknown')}",
                f"  Uptime: {checks.get('uptime', 'unknown')}",
                f"  Compliance: {checks.get('compliance', 'unknown')}",
                ""
            ])
        
        # CEO Brief Summary
        if latest_brief:
            body_parts.extend([
                "CEO BRIEF:",
                f"  {latest_brief.get('summary', 'No summary available')[:200]}",
                ""
            ])
        
        body_parts.extend([
            "",
            "Dashboard: https://echopilotai.replit.app",
            "",
            "- EchoPilot Automation System"
        ])
        
        body = "\n".join(body_parts)
        
        # Send email
        to = os.getenv('REPORTS_TO', 'founder@echopilot.ai')
        result = send_email(to, subject, body)
        
        # Log send
        log_entry = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "event": "daily_report_sent",
            "to": to,
            "dry_run": result.get('dry_run', False)
        }
        
        os.makedirs('logs', exist_ok=True)
        with open('logs/reports_emailer.log', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return result
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = send_daily_report()
    print(json.dumps(result, indent=2))
