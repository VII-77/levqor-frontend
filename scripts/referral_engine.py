#!/usr/bin/env python3
"""
Referral Engine - Phase 37
Growth engine with referral code generation and tracking
"""
import uuid
import json
import os
from datetime import datetime

def generate_referral_code():
    """Generate unique referral code"""
    code = "EP-" + uuid.uuid4().hex[:6].upper()
    
    record = {
        "code": code,
        "created": datetime.utcnow().isoformat() + "Z",
        "uses": 0,
        "revenue": 0.0
    }
    
    # Log to referrals file
    os.makedirs("logs", exist_ok=True)
    with open("logs/referrals.log", "a") as f:
        f.write(json.dumps(record) + "\n")
    
    share_url = f"https://echopilotai.replit.app/?ref={code}"
    
    return {
        "referral_code": code,
        "share_url": share_url,
        "created": record["created"]
    }

def track_referral_use(code, revenue=0.0):
    """Track when a referral code is used"""
    record = {
        "code": code,
        "used": datetime.utcnow().isoformat() + "Z",
        "revenue": revenue,
        "action": "use"
    }
    
    os.makedirs("logs", exist_ok=True)
    with open("logs/referrals.log", "a") as f:
        f.write(json.dumps(record) + "\n")
    
    return {"ok": True, "code": code}

def get_referral_stats(code):
    """Get statistics for a referral code"""
    if not os.path.exists("logs/referrals.log"):
        return {"ok": False, "error": "No referral data"}
    
    uses = 0
    total_revenue = 0.0
    created = None
    
    with open("logs/referrals.log", "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("code") == code:
                    if entry.get("action") == "use":
                        uses += 1
                        total_revenue += entry.get("revenue", 0.0)
                    elif "created" in entry and not created:
                        created = entry["created"]
            except:
                continue
    
    return {
        "ok": True,
        "code": code,
        "uses": uses,
        "revenue": round(total_revenue, 2),
        "created": created
    }

if __name__ == "__main__":
    result = generate_referral_code()
    print(json.dumps(result, indent=2))
