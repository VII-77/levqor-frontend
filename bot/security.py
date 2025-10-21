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

# ===== EXTRA 4: JWT Token Rotation =====
import jwt
import os

JWT_SECRET = os.getenv('SESSION_SECRET', 'default-secret-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_ACCESS_EXPIRY = 900  # 15 minutes
JWT_REFRESH_EXPIRY = 86400  # 24 hours

# NOTE: In-memory blacklist - NOT production-safe for multi-instance deployments
# For production: Use Redis or shared database for token_blacklist
# Example: token_blacklist = RedisSet('jwt_blacklist') 
token_blacklist = set()  # WARNING: Cleared on restart/scale-out

def generate_jwt_pair(user_id, user_data=None):
    """Generate access and refresh token pair"""
    now = time.time()
    
    access_payload = {
        'user_id': user_id,
        'type': 'access',
        'exp': now + JWT_ACCESS_EXPIRY,
        'iat': now,
        'jti': secrets.token_urlsafe(16)
    }
    
    refresh_payload = {
        'user_id': user_id,
        'type': 'refresh',
        'exp': now + JWT_REFRESH_EXPIRY,
        'iat': now,
        'jti': secrets.token_urlsafe(16)
    }
    
    if user_data:
        access_payload['data'] = user_data
    
    access_token = jwt.encode(access_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': JWT_ACCESS_EXPIRY
    }

def verify_jwt(token, token_type='access'):
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Check token type
        if payload.get('type') != token_type:
            return None, "Invalid token type"
        
        # Check blacklist
        if payload.get('jti') in token_blacklist:
            return None, "Token has been revoked"
        
        return payload, None
        
    except jwt.ExpiredSignatureError:
        return None, "Token has expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"

def rotate_jwt(refresh_token):
    """Rotate access token using refresh token and blacklist old refresh token"""
    payload, error = verify_jwt(refresh_token, token_type='refresh')
    
    if error or not payload:
        return None, error or "Invalid token"
    
    # Generate new access token
    user_id = payload.get('user_id')
    user_data = payload.get('data')
    
    if not user_id:
        return None, "Missing user_id in token"
    
    # Blacklist the old refresh token to prevent reuse
    jti = payload.get('jti')
    if jti:
        token_blacklist.add(jti)
        audit_log("jwt_refresh_revoked", {"jti": jti, "user_id": user_id})
    
    return generate_jwt_pair(user_id, user_data), None

def revoke_jwt(token):
    """Add JWT to blacklist"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], options={"verify_exp": False})
        jti = payload.get('jti')
        if jti:
            token_blacklist.add(jti)
            audit_log("jwt_revoked", {"jti": jti})
            return True
    except:
        return False

def require_jwt(f):
    """Decorator requiring valid JWT access token"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            audit_log("jwt_missing", {"endpoint": request.path})
            return jsonify({"ok": False, "error": "JWT token required"}), 401
        
        token = auth_header.split(' ')[1]
        payload, error = verify_jwt(token, token_type='access')
        
        if error or not payload:
            audit_log("jwt_invalid", {"endpoint": request.path, "error": error or "Invalid token"})
            return jsonify({"ok": False, "error": error or "Invalid token"}), 401
        
        # Attach user info to request (dynamic attributes)
        setattr(request, 'jwt_user_id', payload.get('user_id'))
        setattr(request, 'jwt_data', payload.get('data'))
        
        return f(*args, **kwargs)
    return wrapped

# ===== EXTRA 4: WAF-style Request Validation =====
import re
from urllib.parse import unquote

# SQL injection patterns
SQL_PATTERNS = [
    r"(\bUNION\b.*\bSELECT\b)",
    r"(\bSELECT\b.*\bFROM\b)",
    r"(\bINSERT\b.*\bINTO\b)",
    r"(\bDELETE\b.*\bFROM\b)",
    r"(\bDROP\b.*\bTABLE\b)",
    r"(--|\#|\/\*|\*\/)",
    r"(\bOR\b\s+\d+\s*=\s*\d+)",
    r"('\s+OR\s+')",
]

# XSS patterns
XSS_PATTERNS = [
    r"<script[^>]*>.*?</script>",
    r"javascript:",
    r"onerror\s*=",
    r"onload\s*=",
    r"onclick\s*=",
    r"<iframe[^>]*>",
]

# Path traversal patterns
PATH_TRAVERSAL_PATTERNS = [
    r"\.\./",
    r"\.\.\\"
]

def is_malicious_request(data_str):
    """Check if request data contains malicious patterns"""
    data_str = unquote(data_str).lower()
    
    # Check SQL injection
    for pattern in SQL_PATTERNS:
        if re.search(pattern, data_str, re.IGNORECASE):
            return True, "Potential SQL injection detected"
    
    # Check XSS
    for pattern in XSS_PATTERNS:
        if re.search(pattern, data_str, re.IGNORECASE):
            return True, "Potential XSS attack detected"
    
    # Check path traversal
    for pattern in PATH_TRAVERSAL_PATTERNS:
        if re.search(pattern, data_str):
            return True, "Path traversal attempt detected"
    
    return False, None

def validate_request_waf():
    """WAF-style request validation middleware"""
    # Check query parameters
    if request.args:
        query_str = str(request.args.to_dict())
        is_malicious, reason = is_malicious_request(query_str)
        if is_malicious:
            return reason
    
    # Check JSON body
    if request.is_json:
        try:
            body_str = str(request.get_json())
            is_malicious, reason = is_malicious_request(body_str)
            if is_malicious:
                return reason
        except:
            pass
    
    # Check form data
    if request.form:
        form_str = str(request.form.to_dict())
        is_malicious, reason = is_malicious_request(form_str)
        if is_malicious:
            return reason
    
    return None

def waf_protection(f):
    """Decorator for WAF-style protection"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        threat = validate_request_waf()
        
        if threat:
            audit_log("waf_blocked", {
                "endpoint": request.path,
                "threat": threat,
                "ip": request.remote_addr
            }, ok=False)
            return jsonify({
                "ok": False,
                "error": "Request blocked by security policy"
            }), 403
        
        return f(*args, **kwargs)
    return wrapped
