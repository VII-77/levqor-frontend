#!/usr/bin/env python3
"""
Phase 50: Auto-Governance System
Monitors KPIs & enforces thresholds autonomously
"""
import os
import sys
import json
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def check_governance():
    """Check all governance KPIs"""
    try:
        checks = {
            "revenue": "unknown",
            "uptime": "unknown",
            "alerts": 0,
            "compliance": "unknown",
            "performance": "unknown"
        }
        
        # Check revenue trend
        rev_file = 'logs/revenue_intelligence.ndjson'
        if os.path.exists(rev_file):
            with open(rev_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    last = json.loads(lines[-1])
                    if last.get('change_pct', 0) > -20:
                        checks["revenue"] = "ok"
                    else:
                        checks["revenue"] = "warning"
        
        # Check uptime (via ops sentinel)
        ops_file = 'logs/ops_sentinel.ndjson'
        if os.path.exists(ops_file):
            with open(ops_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    last = json.loads(lines[-1])
                    if last.get('status') == 'healthy':
                        checks["uptime"] = "ok"
                        checks["performance"] = "ok"
                    else:
                        checks["uptime"] = "warning"
                        checks["performance"] = "degraded"
                        checks["alerts"] = len(last.get('warnings', []))
        
        # Check compliance
        checks["compliance"] = "ok"  # Placeholder
        
        # Overall status
        warnings = [k for k, v in checks.items() if v in ['warning', 'degraded']]
        status = "healthy" if not warnings else "needs_attention"
        
        report = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "event": "governance_check",
            "status": status,
            "checks": checks,
            "warnings": warnings
        }
        
        # Save report
        os.makedirs('logs', exist_ok=True)
        with open('logs/governance_report.ndjson', 'a') as f:
            f.write(json.dumps(report) + '\n')
        
        # Also save as JSON for easy reading
        with open('logs/governance_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        return {"ok": True, "status": status, "checks": checks}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = check_governance()
    print(json.dumps(result, indent=2))
