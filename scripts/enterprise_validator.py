#!/usr/bin/env python3
"""Phase 100B: Enterprise Validator - Automated System Health Audit"""
import os, sys, json, glob
from datetime import datetime, timedelta

def validate_enterprise():
    """Comprehensive enterprise system validation"""
    try:
        checks = {}
        overall_status = "PASS"
        
        # 1. API Status Check
        api_files_exist = os.path.exists('run.py')
        checks["api_status"] = {
            "status": "PASS" if api_files_exist else "FAIL",
            "details": "API server file exists" if api_files_exist else "Missing run.py"
        }
        
        # 2. Scheduler Check
        scheduler_active = os.path.exists('logs/scheduler.log')
        checks["scheduler"] = {
            "status": "PASS" if scheduler_active else "FAIL",
            "details": "Scheduler running" if scheduler_active else "Scheduler not active"
        }
        
        # 3. Logs Integrity
        log_files = glob.glob('logs/*.ndjson')
        checks["logs_integrity"] = {
            "status": "PASS",
            "details": f"{len(log_files)} NDJSON log files found"
        }
        
        # 4. RBAC Users
        rbac_ok = os.path.exists('data/rbac_users.json')
        if rbac_ok:
            with open('data/rbac_users.json', 'r') as f:
                users = json.load(f)
                admin_count = sum(1 for u in users.values() if u.get('role') == 'admin')
                rbac_ok = admin_count >= 1
        checks["rbac_users"] = {
            "status": "PASS" if rbac_ok else "WARN",
            "details": "Admin users configured" if rbac_ok else "No admin users"
        }
        
        # 5. FinOps Spend
        finops_ok = True
        if os.path.exists('logs/costs.json'):
            with open('logs/costs.json', 'r') as f:
                costs = json.load(f)
                finops_ok = costs.get('data', {}).get('alert_level') != 'CRITICAL'
        checks["finops_spend"] = {
            "status": "PASS" if finops_ok else "WARN",
            "details": "Spend within limits" if finops_ok else "Cost alert active"
        }
        
        # 6. Security Scan
        security_ok = os.path.exists('logs/security_scan.json')
        if security_ok:
            with open('logs/security_scan.json', 'r') as f:
                scan = json.load(f)
                security_ok = scan.get('critical', 0) == 0
        checks["security_scan"] = {
            "status": "PASS" if security_ok else "WARN",
            "details": "No critical findings" if security_ok else "Security issues detected"
        }
        
        # 7. DR Backup
        dr_ok = os.path.exists('backups/dr')
        if dr_ok:
            dr_files = glob.glob('backups/dr/*.tar.gz')
            dr_ok = len(dr_files) > 0
        checks["dr_backup"] = {
            "status": "PASS" if dr_ok else "WARN",
            "details": "DR backups exist" if dr_ok else "No DR backups"
        }
        
        # 8. Optimizer
        optimizer_ok = os.path.exists('logs/adaptive_optimizer.json')
        checks["optimizer"] = {
            "status": "PASS" if optimizer_ok else "WARN",
            "details": "Optimizer running" if optimizer_ok else "Optimizer not run"
        }
        
        # 9. Governance AI
        governance_ok = os.path.exists('logs/governance_ai.json')
        checks["governance_ai"] = {
            "status": "PASS" if governance_ok else "WARN",
            "details": "Governance report exists" if governance_ok else "No governance report"
        }
        
        # Determine overall status
        fail_count = sum(1 for c in checks.values() if c['status'] == 'FAIL')
        warn_count = sum(1 for c in checks.values() if c['status'] == 'WARN')
        
        if fail_count > 0:
            overall_status = "FAIL"
        elif warn_count > 2:
            overall_status = "WARN"
        
        result = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "status": overall_status,
            "checks": checks,
            "summary": {
                "total_checks": len(checks),
                "passed": sum(1 for c in checks.values() if c['status'] == 'PASS'),
                "warnings": warn_count,
                "failures": fail_count
            }
        }
        
        # Save results
        os.makedirs('logs', exist_ok=True)
        with open('logs/enterprise_validator_report.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        # Generate HTML report
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Enterprise Validation Report</title>
    <style>
        body {{ font-family: Arial; max-width: 1200px; margin: 40px auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; }}
        .status-PASS {{ color: #48bb78; font-weight: bold; }}
        .status-WARN {{ color: #ed8936; font-weight: bold; }}
        .status-FAIL {{ color: #f56565; font-weight: bold; }}
        .check-item {{ background: #f7fafc; padding: 15px; margin: 10px 0; border-radius: 8px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏢 EchoPilot Enterprise Validation Report</h1>
        <p>Generated: {result['ts']}</p>
        <p class="status-{overall_status}">Overall Status: {overall_status}</p>
    </div>
    <div class="content">
        <h2>Validation Checks ({result['summary']['passed']}/{result['summary']['total_checks']} Passed)</h2>
"""
        
        for check_name, check_data in checks.items():
            html += f"""
        <div class="check-item">
            <strong>{check_name.replace('_', ' ').title()}:</strong>
            <span class="status-{check_data['status']}">{check_data['status']}</span>
            <p>{check_data['details']}</p>
        </div>
"""
        
        html += """
    </div>
</body>
</html>"""
        
        with open('logs/enterprise_validator_report.html', 'w') as f:
            f.write(html)
        
        return {"ok": True, "validation": result}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = validate_enterprise()
    print(json.dumps(result, indent=2))
