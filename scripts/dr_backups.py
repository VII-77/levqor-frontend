#!/usr/bin/env python3
"""Phase 83: DR Backups - Disaster Recovery Backup System"""
import os, sys, json, tarfile, shutil
from datetime import datetime
from pathlib import Path

DR_BACKUP_BUCKET = os.getenv('DR_BACKUP_BUCKET', 'echopilot-backups')

def create_dr_backup():
    """Create comprehensive DR backup"""
    try:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_name = f"dr_backup_{timestamp}.tar.gz"
        backup_path = Path(f"backups/dr/{backup_name}")
        
        os.makedirs(backup_path.parent, exist_ok=True)
        
        # Create compressed backup
        with tarfile.open(backup_path, "w:gz") as tar:
            for item in ['logs', 'data', 'configs', 'backups/payouts', 'backups/daily']:
                if os.path.exists(item):
                    tar.add(item)
        
        size_bytes = backup_path.stat().st_size
        
        result = {
            "ok": True,
            "ts": datetime.utcnow().isoformat() + "Z",
            "backup": str(backup_path),
            "size_bytes": size_bytes,
            "size_mb": round(size_bytes / 1024 / 1024, 2),
            "bucket": DR_BACKUP_BUCKET
        }
        
        # Log DR backup
        os.makedirs('logs', exist_ok=True)
        with open('logs/dr_backups.ndjson', 'a') as f:
            f.write(json.dumps(result) + '\n')
        
        return result
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = create_dr_backup()
    print(json.dumps(result, indent=2))
