#!/usr/bin/env python3
"""
Phase 65: Incident Autoresponder
Automated incident detection and alerting
"""
import os
import sys
import json
import time
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def send_telegram_alert(message):
    """Send Telegram alert"""
    try:
        import requests
        
        token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
        
        if not token or not chat_id:
            return {"ok": True, "dry_run": True}
        
        # Send alert
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message[:3900],  # Telegram limit
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, json=data, timeout=10)
        return {"ok": response.status_code == 200, "dry_run": False}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def scan_for_incidents():
    """Scan for incidents across multiple systems"""
    try:
        breach = False
        details = []
        
        # Check SLO breaches
        if os.path.exists('logs/slo_report.json'):
            try:
                with open('logs/slo_report.json', 'r') as f:
                    slo = json.load(f)
                
                if slo.get('breach'):
                    breach = True
                    p95 = slo.get('p95_ms', 0)
                    success = slo.get('success_rate', 1.0)
                    details.append(f"SLO breach: P95={p95:.0f}ms, Success={success:.1%}")
            except:
                pass
        
        # Check payout reconciliation issues
        if os.path.exists('logs/payout_recon.json'):
            try:
                with open('logs/payout_recon.json', 'r') as f:
                    payout = json.load(f)
                
                summary = payout.get('summary', {})
                missing = summary.get('missing_in_ledger', 0)
                mismatch = summary.get('amount_mismatch', 0)
                
                if missing > 0 or mismatch > 0:
                    breach = True
                    details.append(f"Payout issues: {missing} missing, {mismatch} mismatched")
            except:
                pass
        
        # Check ops sentinel warnings
        if os.path.exists('logs/ops_sentinel.ndjson'):
            try:
                with open('logs/ops_sentinel.ndjson', 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last = json.loads(lines[-1])
                        warnings = last.get('warnings', [])
                        
                        if warnings:
                            breach = True
                            details.append(f"System warnings: {', '.join(warnings[:3])}")
            except:
                pass
        
        # Check production alerts
        if os.path.exists('logs/production_alerts.json'):
            try:
                with open('logs/production_alerts.json', 'r') as f:
                    alerts = json.load(f)
                
                active = alerts.get('active', [])
                if active:
                    breach = True
                    details.append(f"Production alerts: {len(active)} active")
            except:
                pass
        
        # Log incident if found
        if breach:
            incident = {
                "ts": time.time(),
                "ts_iso": datetime.utcnow().isoformat() + "Z",
                "type": "incident",
                "severity": "high" if len(details) > 2 else "medium",
                "details": details
            }
            
            os.makedirs('logs', exist_ok=True)
            with open('logs/incidents.ndjson', 'a') as f:
                f.write(json.dumps(incident) + '\n')
            
            # Send alert
            alert_message = "🚨 *EchoPilot Incident Detected*\n\n" + "\n".join(f"• {d}" for d in details)
            send_telegram_alert(alert_message)
        
        return {
            "ok": True,
            "breach": breach,
            "incident_count": len(details),
            "details": details
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = scan_for_incidents()
    print(json.dumps(result, indent=2))
