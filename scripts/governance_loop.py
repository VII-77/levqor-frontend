#!/usr/bin/env python3
"""
Governance Loop - Continuous SLO and KPI governance (every 15 min)
Compares targets vs actuals, triggers alerts on breach > 10%
"""
import json
import os
import requests
from datetime import datetime, timezone
from pathlib import Path

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

def read_json(filepath):
    """Read JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return None

def send_telegram_alert(message):
    """Send Telegram alert"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    
    try:
        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except:
        return False

def check_slo_compliance():
    """Check SLO compliance"""
    slo_report = read_json('logs/slo_report.json')
    if not slo_report:
        return {
            "status": "UNKNOWN",
            "breaches": [],
            "breach_severity": 0,
            "note": "SLO report not available"
        }
    
    overall_status = slo_report.get('overall_status', 'UNKNOWN')
    breaches = slo_report.get('breaches', [])
    
    # Calculate breach severity (how far from target)
    breach_severity = 0
    slos = slo_report.get('slos', {})
    
    if 'availability' in breaches:
        actual = slos.get('availability', {}).get('actual_pct', 100)
        target = slos.get('availability', {}).get('target_pct', 99.9)
        breach_severity = max(breach_severity, ((target - actual) / target) * 100)
    
    if 'p95_latency' in breaches:
        actual = slos.get('p95_latency', {}).get('actual_ms', 0)
        target = slos.get('p95_latency', {}).get('target_ms', 400)
        if actual > target:
            breach_severity = max(breach_severity, ((actual - target) / target) * 100)
    
    if 'webhook_success' in breaches:
        actual = slos.get('webhook_success', {}).get('actual_pct', 100)
        target = slos.get('webhook_success', {}).get('target_pct', 99)
        breach_severity = max(breach_severity, ((target - actual) / target) * 100)
    
    return {
        "status": overall_status,
        "breaches": breaches,
        "breach_severity": round(breach_severity, 2),
        "slos": slos
    }

def check_finance_health():
    """Check finance health"""
    try:
        with open('logs/finance.ndjson', 'r') as f:
            lines = f.readlines()[-50:]
        
        failed_payments = sum(1 for line in lines if 'payment_failed' in line)
        total_payments = sum(1 for line in lines if 'payment_' in line)
        
        failure_rate = (failed_payments / total_payments * 100) if total_payments > 0 else 0
        
        return {
            "status": "OK" if failure_rate < 5 else "WARN",
            "failure_rate_pct": round(failure_rate, 2),
            "failed_payments": failed_payments,
            "total_payments": total_payments
        }
    except:
        return {"status": "UNKNOWN", "note": "Finance data not available"}

def calculate_compliance_index():
    """Calculate overall compliance index (0-100)"""
    score = 100
    
    # SLO compliance (-20 per breach)
    slo = check_slo_compliance()
    score -= len(slo['breaches']) * 20
    
    # Breach severity (-10 if > 10%)
    if slo['breach_severity'] > 10:
        score -= 10
    
    # Finance health (-15 if payment failure rate > 5%)
    finance = check_finance_health()
    if finance.get('failure_rate_pct', 0) > 5:
        score -= 15
    
    # Security alerts (-5 if > 10 alerts/hour)
    try:
        with open('logs/production_alerts.ndjson', 'r') as f:
            recent_alerts = len(f.readlines()[-10:])
        if recent_alerts > 10:
            score -= 5
    except:
        pass
    
    return max(0, min(100, score))

def run_governance_loop():
    """Run governance loop check"""
    governance_ts = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    print(f"[{governance_ts}] Running governance loop...")
    
    # Check SLO compliance
    slo = check_slo_compliance()
    finance = check_finance_health()
    compliance_index = calculate_compliance_index()
    
    # Determine overall status
    if slo['breach_severity'] > 10 or compliance_index < 70:
        overall_status = "BREACH"
    elif compliance_index < 85:
        overall_status = "WARN"
    else:
        overall_status = "OK"
    
    # Build governance entry
    governance_entry = {
        "ts": governance_ts,
        "status": overall_status,
        "compliance_index": compliance_index,
        "slo": slo,
        "finance": finance,
        "okr_status": {
            "availability": "✅" if 'availability' not in slo['breaches'] else "❌",
            "latency": "✅" if 'p95_latency' not in slo['breaches'] else "❌",
            "webhooks": "✅" if 'webhook_success' not in slo['breaches'] else "❌",
            "payments": "✅" if finance.get('failure_rate_pct', 0) < 5 else "❌"
        }
    }
    
    # Write to log
    os.makedirs('logs', exist_ok=True)
    with open('logs/governance_loop.ndjson', 'a') as f:
        f.write(json.dumps(governance_entry) + '\n')
    
    print(f"   Status: {overall_status}")
    print(f"   Compliance Index: {compliance_index}/100")
    print(f"   SLO Breaches: {len(slo['breaches'])}")
    
    # Send Telegram alert if breach > 10%
    if slo['breach_severity'] > 10:
        message = f"""🚨 *GOVERNANCE ALERT*

Status: {overall_status}
Compliance Index: {compliance_index}/100
Breach Severity: {slo['breach_severity']}%

Breaches: {', '.join(slo['breaches']) or 'None'}

Immediate review required!
"""
        sent = send_telegram_alert(message)
        print(f"   🚨 Telegram alert {'sent' if sent else 'failed'}")
        governance_entry["telegram_alert_sent"] = sent
    
    return governance_entry

if __name__ == '__main__':
    result = run_governance_loop()
    print(json.dumps(result, indent=2))
