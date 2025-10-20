#!/usr/bin/env python3
"""Phase 95: Security Scan - Automated Security Auditing"""
import os, sys, json
from datetime import datetime

def run_security_scan():
    """Run automated security scan"""
    try:
        findings = []
        
        # Check for sensitive files
        sensitive_patterns = ['.env', 'secrets', 'private_key']
        for pattern in sensitive_patterns:
            if os.path.exists(pattern):
                findings.append({
                    "severity": "low",
                    "issue": f"Sensitive file detected: {pattern}",
                    "recommendation": "Ensure file is in .gitignore"
                })
        
        # Check RBAC
        if not os.path.exists('data/rbac_users.json'):
            findings.append({
                "severity": "medium",
                "issue": "RBAC not initialized",
                "recommendation": "Run rbac_system.py to initialize"
            })
        
        result = {
            "ok": True,
            "ts": datetime.utcnow().isoformat() + "Z",
            "findings": len(findings),
            "critical": sum(1 for f in findings if f['severity'] == 'critical'),
            "high": sum(1 for f in findings if f['severity'] == 'high'),
            "medium": sum(1 for f in findings if f['severity'] == 'medium'),
            "low": sum(1 for f in findings if f['severity'] == 'low'),
            "details": findings
        }
        
        os.makedirs('logs', exist_ok=True)
        with open('logs/security_scan.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        return result
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = run_security_scan()
    print(json.dumps(result, indent=2))
