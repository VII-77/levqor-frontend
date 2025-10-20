#!/usr/bin/env python3
"""
Customer Experience - Phase 34
Signed URLs, email verification, unsubscribe management
"""
import os
import json
import hashlib
import time
from datetime import datetime, timedelta

def signed_url(client_id, expiry_hours=24):
    """Generate signed download URL with expiry"""
    secret = os.getenv("SESSION_SECRET", "demo_secret")
    expiry = int(time.time()) + (expiry_hours * 3600)
    
    # Create signature: SHA256(client_id + expiry + secret)
    payload = f"{client_id}:{expiry}:{secret}"
    signature = hashlib.sha256(payload.encode()).hexdigest()[:16]
    
    base_url = "https://echopilotai.replit.app"
    return f"{base_url}/api/public/download/{client_id}?sig={signature}&exp={expiry}"

def verify_signature(client_id, signature, expiry):
    """Verify signed URL is valid and not expired"""
    secret = os.getenv("SESSION_SECRET", "demo_secret")
    
    # Check expiry
    if int(time.time()) > int(expiry):
        return False, "Link expired"
    
    # Verify signature
    payload = f"{client_id}:{expiry}:{secret}"
    expected_sig = hashlib.sha256(payload.encode()).hexdigest()[:16]
    
    if signature != expected_sig:
        return False, "Invalid signature"
    
    return True, "Valid"

def verify_email(email):
    """Basic email validation"""
    if not email or "@" not in email or "." not in email:
        return False
    
    # Split and check parts
    parts = email.split("@")
    if len(parts) != 2:
        return False
    
    local, domain = parts
    if not local or not domain:
        return False
    
    if "." not in domain:
        return False
    
    return True

def unsubscribe(email):
    """Unsubscribe email from notifications"""
    if not verify_email(email):
        return {"ok": False, "message": "Invalid email address"}
    
    # Log to unsubscribe file
    os.makedirs("logs", exist_ok=True)
    with open("logs/unsubscribes.log", "a") as f:
        entry = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "email": email,
            "action": "unsubscribe"
        }
        f.write(json.dumps(entry) + "\n")
    
    return {"ok": True, "message": f"{email} unsubscribed successfully"}

def is_unsubscribed(email):
    """Check if email has unsubscribed"""
    if not os.path.exists("logs/unsubscribes.log"):
        return False
    
    with open("logs/unsubscribes.log", "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("email") == email:
                    return True
            except:
                continue
    
    return False

if __name__ == "__main__":
    # Test customer experience features
    client_id = f"demo_{int(time.time())}"
    url = signed_url(client_id)
    email_valid = verify_email("demo@echopilot.ai")
    
    result = {
        "signed_url": url,
        "email_validation": {
            "demo@echopilot.ai": email_valid,
            "invalid": verify_email("invalid")
        },
        "client_id": client_id
    }
    
    print(json.dumps(result, indent=2))
