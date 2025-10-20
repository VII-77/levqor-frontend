#!/usr/bin/env python3
"""
Phase 55: Customer Portal
Generates signed links for customer self-service portal
"""
import os
import sys
import json
import hmac
import hashlib
import time
import base64
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

SECRET = (os.getenv('SESSION_SECRET', 'dev-secret-change-me')).encode()

def generate_signature(payload):
    """Generate HMAC signature for payload"""
    sig = hmac.new(SECRET, payload.encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(sig).decode().rstrip('=')

def verify_signature(payload, signature):
    """Verify HMAC signature"""
    expected = generate_signature(payload)
    return hmac.compare_digest(expected, signature)

def create_portal_link(email, expiry_hours=24):
    """
    Create signed portal link for customer
    
    Args:
        email: Customer email
        expiry_hours: Link expiry in hours (default 24)
    
    Returns:
        dict with url and expiration
    """
    try:
        exp = int(time.time()) + (expiry_hours * 3600)
        payload = f"{email}.{exp}"
        token = generate_signature(payload)
        
        url = f"/portal?e={email}&exp={exp}&sig={token}"
        
        # Log link generation
        log_entry = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "event": "portal_link_created",
            "email": email,
            "expires_at": datetime.fromtimestamp(exp).isoformat() + "Z"
        }
        
        os.makedirs('logs', exist_ok=True)
        with open('logs/portal_links.ndjson', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return {
            "ok": True,
            "url": url,
            "full_url": f"https://echopilotai.replit.app{url}",
            "expires_at": datetime.fromtimestamp(exp).isoformat() + "Z"
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def validate_portal_link(email, exp, signature):
    """Validate a portal link"""
    try:
        # Check expiration
        if int(time.time()) > int(exp):
            return {"ok": False, "error": "link_expired"}
        
        # Verify signature
        payload = f"{email}.{exp}"
        if not verify_signature(payload, signature):
            return {"ok": False, "error": "invalid_signature"}
        
        return {
            "ok": True,
            "email": email,
            "valid": True
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    # Test link generation
    result = create_portal_link("customer@example.com")
    print(json.dumps(result, indent=2))
    
    # Test validation
    if result['ok']:
        # Extract params from URL
        import urllib.parse
        parsed = urllib.parse.parse_qs(result['url'].split('?')[1])
        email = parsed['e'][0]
        exp = parsed['exp'][0]
        sig = parsed['sig'][0]
        
        validation = validate_portal_link(email, exp, sig)
        print(json.dumps(validation, indent=2))
