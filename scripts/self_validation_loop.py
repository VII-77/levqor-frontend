#!/usr/bin/env python3
"""
Self-Validation Loop - Continuous health monitoring
Runs all health checks and updates validation log
Triggers auto-rollback on critical failures
"""
import json
import os
import requests
import subprocess
from datetime import datetime, timezone
from pathlib import Path

DASHBOARD_KEY = os.getenv('DASHBOARD_KEY', '')
BASE_URL = 'http://localhost:5000'

def check_api_health():
    """Check API health endpoint"""
    try:
        headers = {'X-Dash-Key': DASHBOARD_KEY} if DASHBOARD_KEY else {}
        response = requests.get(f'{BASE_URL}/api/system-health', headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "OK" if data.get('status') == 'healthy' else "WARN",
                "details": data
            }
        return {"status": "FAIL", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

def check_slo_status():
    """Check SLO status"""
    try:
        if not DASHBOARD_KEY:
            return {"status": "SKIP", "error": "No DASHBOARD_KEY"}
        
        headers = {'X-Dash-Key': DASHBOARD_KEY}
        response = requests.get(f'{BASE_URL}/api/observability/slo', headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json().get('data', {})
            overall = data.get('overall_status', 'UNKNOWN')
            return {
                "status": "OK" if overall == 'OK' else "WARN",
                "overall": overall,
                "breaches": data.get('breaches', [])
            }
        elif response.status_code == 404:
            return {"status": "SKIP", "note": "SLO report not yet generated"}
        return {"status": "FAIL", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

def check_scheduler():
    """Check scheduler is running"""
    try:
        pid_file = Path('logs/scheduler.pid')
        if not pid_file.exists():
            return {"status": "FAIL", "error": "PID file missing"}
        
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        # Check if process exists
        try:
            os.kill(pid, 0)
            return {"status": "OK", "pid": pid}
        except OSError:
            return {"status": "FAIL", "error": f"Process {pid} not running"}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

def check_critical_files():
    """Check critical files exist"""
    critical_files = [
        'run.py',
        'scripts/exec_scheduler.py',
        'scripts/final_audit.py',
        'scripts/slo_guard.py',
        'scripts/production_alerts.py'
    ]
    
    missing = []
    for filepath in critical_files:
        if not os.path.exists(filepath):
            missing.append(filepath)
    
    if missing:
        return {"status": "FAIL", "missing": missing}
    return {"status": "OK", "files_checked": len(critical_files)}

def trigger_auto_rollback():
    """Trigger auto-rollback on critical failure"""
    try:
        if not DASHBOARD_KEY:
            return {"status": "SKIP", "error": "No DASHBOARD_KEY"}
        
        headers = {'X-Dash-Key': DASHBOARD_KEY}
        response = requests.post(f'{BASE_URL}/api/rollback/suggest', headers=headers, timeout=10)
        return {
            "status": "TRIGGERED",
            "response": response.status_code
        }
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

def main():
    validation_ts = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    print(f"[{validation_ts}] Running self-validation checks...")
    
    # Run all health checks
    checks = {
        "api_health": check_api_health(),
        "slo_status": check_slo_status(),
        "scheduler": check_scheduler(),
        "critical_files": check_critical_files()
    }
    
    # Determine overall status
    failures = [k for k, v in checks.items() if v.get('status') == 'FAIL']
    warnings = [k for k, v in checks.items() if v.get('status') == 'WARN']
    
    if failures:
        overall = "CRITICAL"
        print(f"   ❌ CRITICAL: {len(failures)} check(s) failed: {', '.join(failures)}")
    elif warnings:
        overall = "WARNING"
        print(f"   ⚠️  WARNING: {len(warnings)} check(s) have warnings: {', '.join(warnings)}")
    else:
        overall = "HEALTHY"
        print(f"   ✅ HEALTHY: All checks passed")
    
    # Build validation entry
    validation_entry = {
        "ts": validation_ts,
        "overall": overall,
        "checks": checks,
        "failures": failures,
        "warnings": warnings
    }
    
    # Write to validation log
    os.makedirs('logs', exist_ok=True)
    with open('logs/validation.ndjson', 'a') as f:
        f.write(json.dumps(validation_entry) + '\n')
    
    # Trigger auto-rollback if critical
    if overall == "CRITICAL" and len(failures) >= 3:
        print(f"   🚨 Triggering auto-rollback due to {len(failures)} critical failures")
        rollback_result = trigger_auto_rollback()
        validation_entry["rollback_triggered"] = rollback_result
    
    print(f"   📝 Logged to logs/validation.ndjson")
    
    return validation_entry

if __name__ == '__main__':
    result = main()
    import sys
    sys.exit(0 if result['overall'] in ['HEALTHY', 'WARNING'] else 1)
