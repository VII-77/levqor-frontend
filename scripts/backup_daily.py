#!/usr/bin/env python3
"""
Phase 70: Daily Backup System
Creates compressed archives of logs and important data
"""
import os
import sys
import json
import tarfile
from datetime import datetime, date

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def create_daily_backup():
    """Create daily backup archive"""
    try:
        today = date.today().isoformat()
        
        # Create backup directory
        os.makedirs("backups/daily", exist_ok=True)
        archive_path = f"backups/daily/backup_{today}.tar.gz"
        
        # Create tar.gz archive
        with tarfile.open(archive_path, "w:gz") as tar:
            # Add logs directory
            if os.path.exists("logs"):
                tar.add("logs", arcname="logs")
            
            # Add configs directory
            if os.path.exists("configs"):
                tar.add("configs", arcname="configs")
            
            # Add payout backups
            if os.path.exists("backups/payouts"):
                tar.add("backups/payouts", arcname="backups/payouts")
        
        # Get archive size
        size_bytes = os.path.getsize(archive_path)
        size_mb = size_bytes / (1024 * 1024)
        
        result = {
            "ok": True,
            "ts": datetime.utcnow().isoformat() + "Z",
            "archive": archive_path,
            "size_bytes": size_bytes,
            "size_mb": round(size_mb, 2)
        }
        
        # Log backup creation
        os.makedirs("logs", exist_ok=True)
        with open("logs/backup_daily.log", "a") as f:
            f.write(json.dumps(result) + "\n")
        
        return result
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = create_daily_backup()
    print(json.dumps(result, indent=2))
