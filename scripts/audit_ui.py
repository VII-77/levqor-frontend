#!/usr/bin/env python3
"""
Phase 60: Audit UI
Read-only audit log viewer API
"""
import os
import sys
import json
import glob

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def get_latest_audit():
    """Get latest audit report"""
    try:
        # Find latest audit file
        audit_files = sorted(glob.glob("backups/audit/audit_*.json"))
        
        if not audit_files:
            return {
                "ok": True,
                "entries": 0,
                "file": None,
                "message": "No audit files found"
            }
        
        latest_file = audit_files[-1]
        
        # Load audit data
        with open(latest_file, 'r') as f:
            data = json.load(f)
        
        # Count entries
        if isinstance(data, list):
            entry_count = len(data)
        elif isinstance(data, dict):
            entry_count = data.get('entries', len(data.get('items', [])))
        else:
            entry_count = 1
        
        return {
            "ok": True,
            "entries": entry_count,
            "file": latest_file,
            "data": data if entry_count < 100 else None  # Don't return large datasets
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def get_audit_summary():
    """Get summary of all audit files"""
    try:
        audit_files = sorted(glob.glob("backups/audit/audit_*.json"))
        
        summary = {
            "total_files": len(audit_files),
            "files": []
        }
        
        for filepath in audit_files[-10:]:  # Last 10 files
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                if isinstance(data, list):
                    entry_count = len(data)
                else:
                    entry_count = data.get('entries', 0)
                
                summary['files'].append({
                    "file": os.path.basename(filepath),
                    "entries": entry_count,
                    "size_kb": os.path.getsize(filepath) / 1024
                })
            except:
                continue
        
        return {"ok": True, "summary": summary}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    # Test both functions
    print("Latest Audit:")
    print(json.dumps(get_latest_audit(), indent=2))
    print("\nAudit Summary:")
    print(json.dumps(get_audit_summary(), indent=2))
