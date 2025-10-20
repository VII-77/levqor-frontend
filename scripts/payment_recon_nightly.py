#!/usr/bin/env python3
"""
Phase 67: Nightly Payment Reconciliation
Backs up daily payment reconciliation data
"""
import os
import sys
import json
import shutil
from datetime import datetime, date

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def backup_payment_recon():
    """Backup payment reconciliation data"""
    try:
        today = date.today().isoformat()
        src = "logs/payout_recon.json"
        
        # Create backup directory
        os.makedirs("backups/payouts", exist_ok=True)
        dst = f"backups/payouts/payout_recon_{today}.json"
        
        # Copy if source exists
        backed_up = False
        if os.path.exists(src):
            shutil.copy2(src, dst)
            backed_up = True
        
        result = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "ok": backed_up,
            "src": src,
            "dst": dst if backed_up else None,
            "exists": os.path.exists(dst) if backed_up else False
        }
        
        # Log the backup
        os.makedirs("logs", exist_ok=True)
        with open("logs/payment_recon_nightly.log", "a") as f:
            f.write(json.dumps(result) + "\n")
        
        return result
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = backup_payment_recon()
    print(json.dumps(result, indent=2))
