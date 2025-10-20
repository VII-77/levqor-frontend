#!/usr/bin/env python3
"""
Replica Sync - Phase 39
Multi-region data synchronization
"""
import os
import shutil
import glob
from datetime import datetime

def sync_to_replica():
    """Sync logs to replica/backup location"""
    dest = os.getenv("RAILWAY_FALLBACK_PATH", "backups/replica")
    os.makedirs(dest, exist_ok=True)
    
    synced_count = 0
    synced_files = []
    
    # Sync log files
    for log_file in glob.glob("logs/*.log"):
        try:
            shutil.copy2(log_file, dest)
            synced_count += 1
            synced_files.append(os.path.basename(log_file))
        except Exception as e:
            # Continue on error
            pass
    
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    print(f"[{timestamp}] Synced {synced_count} files → {dest}")
    
    return {
        "ok": True,
        "synced_count": synced_count,
        "destination": dest,
        "files": synced_files,
        "ts": timestamp
    }

if __name__ == "__main__":
    import json
    result = sync_to_replica()
    print(json.dumps(result, indent=2))
