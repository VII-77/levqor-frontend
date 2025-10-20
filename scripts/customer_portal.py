#!/usr/bin/env python3
"""
Phase 78: Customer Portal v1
Generate signed links for receipts, invoices, and downloads
"""
import os
import sys
import json
import time
import hmac
import hashlib
from datetime import datetime, timedelta

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configuration
PORTAL_SIGNING_SECRET = os.getenv('SESSION_SECRET', 'dev-secret-key')
PORTAL_LINK_TTL_HRS = int(os.getenv('PORTAL_LINK_TTL_HRS', '24'))

def generate_signed_token(email, resource_id, expires_at):
    """Generate HMAC-signed token for portal access"""
    message = f"{email}:{resource_id}:{expires_at}"
    signature = hmac.new(
        PORTAL_SIGNING_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"{signature[:32]}"

def verify_signed_token(email, resource_id, expires_at, token):
    """Verify HMAC-signed token"""
    expected = generate_signed_token(email, resource_id, expires_at)
    return hmac.compare_digest(expected, token)

def get_customer_receipts(email):
    """Get receipts/invoices for customer email"""
    try:
        receipts = []
        
        # Mock data - in production, query Notion/Stripe
        # For now, generate sample receipts
        receipts.append({
            "id": "rcpt_001",
            "date": "2025-10-15",
            "amount_usd": 29.99,
            "description": "EchoPilot Pro - Monthly",
            "status": "paid"
        })
        
        # Generate signed download links
        expires_at = int(time.time()) + (PORTAL_LINK_TTL_HRS * 3600)
        
        for receipt in receipts:
            token = generate_signed_token(email, receipt['id'], expires_at)
            receipt['download_url'] = f"/api/portal/download?email={email}&id={receipt['id']}&expires={expires_at}&token={token}"
            receipt['expires_at'] = expires_at
            receipt['expires_iso'] = datetime.fromtimestamp(expires_at).isoformat() + "Z"
        
        # Log access
        os.makedirs('logs', exist_ok=True)
        with open('logs/portal_access.ndjson', 'a') as f:
            f.write(json.dumps({
                "ts": datetime.utcnow().isoformat() + "Z",
                "email": email,
                "resource": "receipts",
                "status": "success",
                "count": len(receipts)
            }) + '\n')
        
        return {
            "ok": True,
            "email": email,
            "receipts": receipts,
            "link_ttl_hours": PORTAL_LINK_TTL_HRS
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def verify_download_token(email, resource_id, expires_at, token, ip=None):
    """Verify download token and log access"""
    try:
        # Check expiration
        if time.time() > expires_at:
            return {"ok": False, "error": "Token expired", "status": 403}
        
        # Verify signature
        if not verify_signed_token(email, resource_id, expires_at, token):
            return {"ok": False, "error": "Invalid token", "status": 403}
        
        # Log access
        os.makedirs('logs', exist_ok=True)
        with open('logs/portal_access.ndjson', 'a') as f:
            f.write(json.dumps({
                "ts": datetime.utcnow().isoformat() + "Z",
                "email": email,
                "resource": resource_id,
                "ip": ip or "unknown",
                "status": "download_success"
            }) + '\n')
        
        return {
            "ok": True,
            "resource_id": resource_id,
            "download_allowed": True
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e), "status": 500}

if __name__ == "__main__":
    # Test mode
    result = get_customer_receipts("test@example.com")
    print(json.dumps(result, indent=2))
