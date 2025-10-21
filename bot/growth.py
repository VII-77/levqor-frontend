"""
Boss Mode Phase 10: Growth Loops Foundation
Provides referral tracking and onboarding status management
"""

import os
import json
from datetime import datetime
from pathlib import Path

REFERRALS_FILE = Path("logs/referrals.json")
ONBOARDING_FILE = Path("logs/onboarding.json")

def ensure_files():
    """Ensure growth tracking files exist"""
    REFERRALS_FILE.parent.mkdir(exist_ok=True)
    if not REFERRALS_FILE.exists():
        REFERRALS_FILE.write_text("[]")
    if not ONBOARDING_FILE.exists():
        ONBOARDING_FILE.write_text("{}")

def track_referral(referrer_id: str, referee_id: str, source: str = "direct"):
    """Track a new referral"""
    ensure_files()
    
    referrals = json.loads(REFERRALS_FILE.read_text())
    referrals.append({
        "referrer_id": referrer_id,
        "referee_id": referee_id,
        "source": source,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "pending"
    })
    
    REFERRALS_FILE.write_text(json.dumps(referrals, indent=2))
    return {"ok": True, "referral_id": len(referrals)}

def get_referral_stats(user_id: str):
    """Get referral statistics for a user"""
    ensure_files()
    
    referrals = json.loads(REFERRALS_FILE.read_text())
    user_refs = [r for r in referrals if r["referrer_id"] == user_id]
    
    return {
        "ok": True,
        "user_id": user_id,
        "total_referrals": len(user_refs),
        "pending": len([r for r in user_refs if r["status"] == "pending"]),
        "completed": len([r for r in user_refs if r["status"] == "completed"]),
        "referrals": user_refs
    }

def update_onboarding_status(user_id: str, step: str, completed: bool = True):
    """Update user onboarding progress"""
    ensure_files()
    
    onboarding = json.loads(ONBOARDING_FILE.read_text())
    
    if user_id not in onboarding:
        onboarding[user_id] = {
            "started_at": datetime.utcnow().isoformat(),
            "steps": {}
        }
    
    onboarding[user_id]["steps"][step] = {
        "completed": completed,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    ONBOARDING_FILE.write_text(json.dumps(onboarding, indent=2))
    return {"ok": True, "user_id": user_id, "step": step}

def get_onboarding_status(user_id: str):
    """Get user onboarding progress"""
    ensure_files()
    
    onboarding = json.loads(ONBOARDING_FILE.read_text())
    user_data = onboarding.get(user_id, {
        "started_at": None,
        "steps": {}
    })
    
    expected_steps = ["welcome", "api_key", "first_job", "payment_setup", "dashboard_tour"]
    completed_steps = [s for s, d in user_data.get("steps", {}).items() if d.get("completed")]
    
    return {
        "ok": True,
        "user_id": user_id,
        "started_at": user_data.get("started_at"),
        "progress_pct": int((len(completed_steps) / len(expected_steps)) * 100) if expected_steps else 0,
        "completed_steps": completed_steps,
        "total_steps": len(expected_steps),
        "next_step": next((s for s in expected_steps if s not in completed_steps), None)
    }
