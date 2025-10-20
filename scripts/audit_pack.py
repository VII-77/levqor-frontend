#!/usr/bin/env python3
"""
Audit Pack - Phase 38
SOC-lite compliance with hash chain audit trail
"""
import os
import hashlib
import json
import glob
from datetime import datetime

def generate_audit_chain():
    """Generate cryptographic hash chain for audit compliance"""
    chain = []
    
    # Process all log files
    for log_file in sorted(glob.glob("logs/*.log")):
        try:
            with open(log_file, "r") as f:
                for line in f:
                    # Hash each log line
                    line_hash = hashlib.sha256(line.encode()).hexdigest()
                    chain.append(line_hash)
        except Exception as e:
            # Log errors but continue
            error_hash = hashlib.sha256(f"ERROR:{log_file}:{str(e)}".encode()).hexdigest()
            chain.append(error_hash)
    
    # Generate root hash from chain
    chain_combined = "".join(chain)
    root_hash = hashlib.sha256(chain_combined.encode()).hexdigest()
    
    audit_report = {
        "root_hash": root_hash,
        "entry_count": len(chain),
        "ts": datetime.utcnow().isoformat() + "Z",
        "audit_version": "1.0",
        "compliance": ["SOC-lite", "audit-trail"]
    }
    
    # Save audit report
    os.makedirs("backups/audit", exist_ok=True)
    audit_filename = f"backups/audit/audit_{datetime.utcnow().strftime('%Y%m%d')}.json"
    
    with open(audit_filename, "w") as f:
        json.dump(audit_report, f, indent=2)
    
    return {
        "ok": True,
        "audit_file": audit_filename,
        "hash_root": root_hash,
        "entries": len(chain),
        "ts": audit_report["ts"]
    }

if __name__ == "__main__":
    result = generate_audit_chain()
    print(json.dumps(result, indent=2))
