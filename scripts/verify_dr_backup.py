#!/usr/bin/env python3
"""
DR Backup Verification Script
Tests disaster recovery backup integrity and restore capability
"""
import os
import sys
import json
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path

def find_latest_backup():
    """Find the most recent DR backup"""
    backup_dir = Path("backups/dr")
    if not backup_dir.exists():
        return None
    
    backups = sorted(backup_dir.glob("dr_backup_*.tar.gz"), reverse=True)
    return backups[0] if backups else None

def verify_backup_integrity(backup_path):
    """Verify backup file integrity"""
    results = []
    
    # Test 1: File exists and is readable
    if not backup_path.exists():
        return {"ok": False, "error": "Backup file not found"}
    
    results.append({
        "test": "file_exists",
        "status": "PASS",
        "size_mb": round(backup_path.stat().st_size / 1024 / 1024, 2)
    })
    
    # Test 2: Archive is valid
    try:
        with tarfile.open(backup_path, 'r:gz') as tar:
            members = tar.getmembers()
            results.append({
                "test": "archive_valid",
                "status": "PASS",
                "file_count": len(members)
            })
    except Exception as e:
        results.append({
            "test": "archive_valid",
            "status": "FAIL",
            "error": str(e)
        })
        return {"ok": False, "tests": results}
    
    # Test 3: Required directories present
    required_dirs = ['logs/', 'data/', 'configs/']
    found_dirs = set()
    
    with tarfile.open(backup_path, 'r:gz') as tar:
        for member in tar.getmembers():
            for required_dir in required_dirs:
                if member.name.startswith(required_dir):
                    found_dirs.add(required_dir)
    
    missing_dirs = set(required_dirs) - found_dirs
    
    if missing_dirs:
        results.append({
            "test": "required_directories",
            "status": "WARN",
            "missing": list(missing_dirs),
            "found": list(found_dirs)
        })
    else:
        results.append({
            "test": "required_directories",
            "status": "PASS",
            "directories": list(found_dirs)
        })
    
    # Test 4: Dry-run extract
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            with tarfile.open(backup_path, 'r:gz') as tar:
                # Extract first 5 files as a test
                members = tar.getmembers()[:5]
                tar.extractall(path=temp_dir, members=members)
                
                results.append({
                    "test": "dry_run_extract",
                    "status": "PASS",
                    "extracted_files": len(members)
                })
    except Exception as e:
        results.append({
            "test": "dry_run_extract",
            "status": "FAIL",
            "error": str(e)
        })
        return {"ok": False, "tests": results}
    
    # Test 5: Critical files check
    critical_files = [
        'logs/scheduler.log',
        'logs/slo_report.json',
        'logs/production_alerts.ndjson'
    ]
    
    with tarfile.open(backup_path, 'r:gz') as tar:
        archive_files = [m.name for m in tar.getmembers()]
        found_critical = [f for f in critical_files if f in archive_files]
        
        results.append({
            "test": "critical_files",
            "status": "INFO",
            "found": found_critical,
            "total_critical": len(critical_files)
        })
    
    # Overall assessment
    failures = sum(1 for r in results if r.get('status') == 'FAIL')
    warnings = sum(1 for r in results if r.get('status') == 'WARN')
    
    return {
        "ok": failures == 0,
        "backup_path": str(backup_path),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "tests": results,
        "summary": {
            "total_tests": len(results),
            "passed": sum(1 for r in results if r.get('status') == 'PASS'),
            "warnings": warnings,
            "failures": failures,
            "status": "PASS" if failures == 0 else "FAIL"
        }
    }

def main():
    """Run DR backup verification"""
    print("=== DR Backup Verification ===\n")
    
    # Find latest backup
    latest_backup = find_latest_backup()
    
    if not latest_backup:
        result = {
            "ok": False,
            "error": "No DR backups found",
            "help": "Run: python3 scripts/dr_backups.py"
        }
        print(json.dumps(result, indent=2))
        return 1
    
    print(f"Testing backup: {latest_backup}\n")
    
    # Verify backup
    verification = verify_backup_integrity(latest_backup)
    
    # Print results
    print(json.dumps(verification, indent=2))
    
    # Log verification
    os.makedirs('logs', exist_ok=True)
    with open('logs/dr_verification.ndjson', 'a') as f:
        f.write(json.dumps(verification) + '\n')
    
    # Exit code based on result
    return 0 if verification['ok'] else 1

if __name__ == "__main__":
    sys.exit(main())
