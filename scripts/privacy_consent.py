#!/usr/bin/env python3
"""Phase 96: Privacy & Consent Management"""
import os, sys, json
from datetime import datetime, timedelta

CONSENT_TTL_DAYS = int(os.getenv('CONSENT_TTL_DAYS', '365'))

def record_consent(user_email, purpose, granted=True):
    """Record user consent"""
    try:
        consents = {}
        if os.path.exists('data/consents.json'):
            with open('data/consents.json', 'r') as f:
                consents = json.load(f)
        
        if user_email not in consents:
            consents[user_email] = []
        
        consents[user_email].append({
            "purpose": purpose,
            "granted": granted,
            "ts": datetime.utcnow().isoformat() + "Z",
            "expires": (datetime.utcnow() + timedelta(days=CONSENT_TTL_DAYS)).isoformat() + "Z"
        })
        
        os.makedirs('data', exist_ok=True)
        with open('data/consents.json', 'w') as f:
            json.dump(consents, f, indent=2)
        
        return {"ok": True, "recorded": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = record_consent("user@example.com", "marketing")
    print(json.dumps(result, indent=2))
