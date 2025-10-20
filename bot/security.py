"""
Security utilities for EchoPilot Boss Mode
- Rate limiting
- CSRF protection
- Audit logging
- PII redaction
"""

import time
import hashlib
import secrets
import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from functools import wraps
from flask import request, jsonify

# ===== Rate Limiting =====
class RateLimiter:
    """Simple in-memory rate limiter with exponential backoff"""
    
    def __init__(self):
        self.attempts = defaultdict(list)  # {key: [timestamp, ...]}
        self.lockouts = {}  # {key: unlock_timestamp}
        
    def is_rate_limited(self, key, max_requests=10, window_seconds=60):
        """Check if key is rate limited"""
        now = time.time()
        
        # Check if locked out
        if key in self.lockouts:
            if now < self.lockouts[key]:
                return True, "Rate limit exceeded. Locked out."
            else:
                del self.lockouts[key]
        
        # Clean old attempts
        self.attempts[key] = [t for t in self.attempts[key] if now - t < window_seconds]
        
        # Check rate
        if len(self.attempts[key]) >= max_requests:
            # Apply lockout (exponential backoff)
            lockout_duration = min(300, 60 * (2 ** (len(self.attempts[key]) // max_requests)))
            self.lockouts[key] = now + lockout_duration
            return True, f"Rate limit exceeded. Try again in {lockout_duration}s"
        
        # Record attempt
        self.attempts[key] = [t for t in self.attempts[key] if now - t < window_seconds]
        self.attempts[key].append(now)
        return False, None

rate_limiter = RateLimiter()

def rate_limit(max_requests=10, window=60):
    """Decorator for rate limiting endpoints"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Use IP + User-Agent as key
            key = f"{request.remote_addr}:{request.headers.get('User-Agent', 'unknown')}"
            key_hash = hashlib.sha256(key.encode()).hexdigest()[:16]
            
            limited, message = rate_limiter.is_rate_limited(key_hash, max_requests, window)
            
            if limited:
                audit_log("rate_limit_exceeded", {
                    "ip": request.remote_addr,
                    "endpoint": request.path,
                    "message": message
                })
                return jsonify({"ok": False, "error": message}), 429
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

# ===== CSRF Protection =====
csrf_tokens = {}  # In production, use Redis

def generate_csrf_token(session_id=None):
    """Generate CSRF token"""
    if not session_id:
        session_id = secrets.token_urlsafe(16)
    
    token = secrets.token_urlsafe(32)
    csrf_tokens[session_id] = {
        'token': token,
        'created': time.time()
    }
    
    # Clean old tokens
    now = time.time()
    expired = [k for k, v in csrf_tokens.items() if now - v['created'] > 3600]
    for k in expired:
        del csrf_tokens[k]
    
    return token, session_id

def verify_csrf_token(session_id, token):
    """Verify CSRF token"""
    if session_id not in csrf_tokens:
        return False
    
    stored = csrf_tokens[session_id]
    
    # Check expiry
    if time.time() - stored['created'] > 3600:
        del csrf_tokens[session_id]
        return False
    
    return secrets.compare_digest(stored['token'], token)

def require_csrf(f):
    """Decorator requiring CSRF token for POST/PUT/DELETE"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'DELETE']:
            session_id = request.headers.get('X-Session-ID')
            csrf_token = request.headers.get('X-CSRF-Token')
            
            if not session_id or not csrf_token:
                audit_log("csrf_missing", {"endpoint": request.path})
                return jsonify({"ok": False, "error": "CSRF token required"}), 403
            
            if not verify_csrf_token(session_id, csrf_token):
                audit_log("csrf_invalid", {"endpoint": request.path})
                return jsonify({"ok": False, "error": "Invalid CSRF token"}), 403
        
        return f(*args, **kwargs)
    return wrapped

# ===== Audit Logging =====
AUDIT_LOG_PATH = Path(__file__).parent.parent / "logs" / "ndjson" / "audit.ndjson"

def audit_log(action, details=None, user=None, ok=True, latency_ms=None):
    """Write structured audit log entry"""
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "user": user or "system",
        "ok": ok,
        "ip": getattr(request, 'remote_addr', None) if request else None,
        "endpoint": getattr(request, 'path', None) if request else None,
        "method": getattr(request, 'method', None) if request else None
    }
    
    if details:
        entry["details"] = redact_pii(details)
    
    if latency_ms is not None:
        entry["latency_ms"] = latency_ms
    
    try:
        with open(AUDIT_LOG_PATH, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        print(f"Audit log error: {e}")

# ===== PII Redaction =====
PII_FIELDS = {'email', 'phone', 'ssn', 'credit_card', 'password', 'token', 'secret', 'api_key'}

def redact_pii(data):
    """Redact PII from data structures"""
    if isinstance(data, dict):
        return {
            k: "[REDACTED]" if k.lower() in PII_FIELDS else redact_pii(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [redact_pii(item) for item in data]
    elif isinstance(data, str):
        # Redact email-like patterns
        import re
        data = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', data)
        # Redact credit card-like patterns
        data = re.sub(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '[CARD]', data)
    return data

# ===== Security Headers =====
def get_security_headers():
    """Generate security headers for responses"""
    return {
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:;",
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
    }

def apply_security_headers(response):
    """Apply security headers to Flask response"""
    for header, value in get_security_headers().items():
        response.headers[header] = value
    return response
