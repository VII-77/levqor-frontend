#!/usr/bin/env python3
"""
Data Export - Phase 35
GDPR-compliant data export and backup system
"""
import os
import json
import glob
import hashlib
from datetime import datetime
import shutil

def export_logs():
    """Export all logs with SHA256 hashes for compliance"""
    timestamp = datetime.utcnow()
    
    export_data = {
        "ts": timestamp.isoformat() + "Z",
        "export_type": "compliance",
        "files": []
    }
    
    # Hash all log files
    for log_file in glob.glob("logs/*.log"):
        try:
            with open(log_file, "rb") as f:
                content = f.read()
                file_hash = hashlib.sha256(content).hexdigest()
            
            export_data["files"].append({
                "file": log_file,
                "sha256": file_hash,
                "size_bytes": len(content)
            })
        except Exception as e:
            export_data["files"].append({
                "file": log_file,
                "error": str(e)
            })
    
    # Save export manifest
    os.makedirs("backups", exist_ok=True)
    export_filename = f"backups/export_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(export_filename, "w") as f:
        json.dump(export_data, f, indent=2)
    
    return {
        "ok": True,
        "export": export_filename,
        "count": len(export_data["files"]),
        "ts": export_data["ts"]
    }

def backup_database():
    """Backup critical data"""
    timestamp = datetime.utcnow()
    backup_dir = f"backups/backup_{timestamp.strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Copy log files
    copied = 0
    for log_file in glob.glob("logs/*.log") + glob.glob("logs/*.json"):
        try:
            shutil.copy2(log_file, backup_dir)
            copied += 1
        except:
            pass
    
    return {
        "ok": True,
        "backup_dir": backup_dir,
        "files_backed_up": copied,
        "ts": timestamp.isoformat() + "Z"
    }

if __name__ == "__main__":
    result = export_logs()
    print(json.dumps(result, indent=2))
