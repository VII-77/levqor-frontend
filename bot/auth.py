"""
JWT Authentication System for EchoPilot Customer Portal
Handles token generation, verification, and customer session management
"""

import os
import jwt
import json
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from typing import Dict, Optional, Tuple

# Environment Configuration
AUTH_JWT_SECRET = os.getenv("AUTH_JWT_SECRET", os.urandom(32).hex())
AUTH_JWT_EXP_HRS = int(os.getenv("AUTH_JWT_EXP_HRS", "24"))
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@echopilotai.replit.app")
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "support@echopilotai.replit.app")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "https://echopilotai.replit.app")

# Rate limiting store (in-memory, upgrade to Redis for production)
_rate_limit_store = {}


def log_auth_event(event: str, **kwargs):
    """Log authentication events to NDJSON"""
    log_entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "event": event,
        **kwargs
    }
    # Redact sensitive data
    if "password" in log_entry:
        del log_entry["password"]
    if "token" in log_entry:
        log_entry["token"] = "***REDACTED***"
    
    os.makedirs("logs", exist_ok=True)
    with open("logs/auth.ndjson", "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def generate_jwt(email: str, customer_id: Optional[str] = None) -> str:
    """
    Generate a JWT token for authenticated customer
    
    Args:
        email: Customer email address
        customer_id: Optional Stripe customer ID
        
    Returns:
        JWT token string
    """
    payload = {
        "email": email,
        "customer_id": customer_id,
        "exp": datetime.utcnow() + timedelta(hours=AUTH_JWT_EXP_HRS),
        "iat": datetime.utcnow()
    }
    
    token = jwt.encode(payload, AUTH_JWT_SECRET, algorithm="HS256")
    
    log_auth_event("jwt_generated", email=email, exp_hrs=AUTH_JWT_EXP_HRS)
    
    return token


def verify_jwt(token: str) -> Tuple[bool, Optional[Dict]]:
    """
    Verify JWT token and return payload
    
    Args:
        token: JWT token string
        
    Returns:
        (is_valid, payload_dict or None)
    """
    try:
        payload = jwt.decode(token, AUTH_JWT_SECRET, algorithms=["HS256"])
        return True, payload
    except jwt.ExpiredSignatureError:
        log_auth_event("jwt_expired")
        return False, None
    except jwt.InvalidTokenError as e:
        log_auth_event("jwt_invalid", error=str(e))
        return False, None


def require_jwt(f):
    """
    Decorator to require valid JWT for customer routes
    Usage:
        @app.route("/api/me")
        @require_jwt
        def get_profile(current_user):
            return jsonify(current_user)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        
        if not auth_header.startswith("Bearer "):
            log_auth_event("auth_missing", path=request.path, ip=request.remote_addr)
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.replace("Bearer ", "")
        is_valid, payload = verify_jwt(token)
        
        if not is_valid:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Pass current_user data to the route
        return f(current_user=payload, *args, **kwargs)
    
    return decorated_function


def check_rate_limit(identifier: str, limit: int = 5, window: int = 60) -> bool:
    """
    Simple in-memory rate limiting
    
    Args:
        identifier: IP address or user key
        limit: Max requests allowed
        window: Time window in seconds
        
    Returns:
        True if request allowed, False if rate limited
    """
    now = datetime.utcnow()
    
    if identifier not in _rate_limit_store:
        _rate_limit_store[identifier] = []
    
    # Clean old entries
    _rate_limit_store[identifier] = [
        ts for ts in _rate_limit_store[identifier]
        if (now - ts).seconds < window
    ]
    
    # Check limit
    if len(_rate_limit_store[identifier]) >= limit:
        log_auth_event("rate_limited", identifier=identifier, limit=limit)
        return False
    
    # Add current request
    _rate_limit_store[identifier].append(now)
    return True


def rate_limit(limit: int = 5, window: int = 60):
    """
    Decorator for rate limiting endpoints
    Usage:
        @app.route("/api/auth/login", methods=["POST"])
        @rate_limit(limit=5, window=60)
        def login():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            identifier = request.remote_addr or "unknown"
            
            if not check_rate_limit(identifier, limit, window):
                return jsonify({
                    "error": "Rate limit exceeded",
                    "retry_after": window
                }), 429
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def send_magic_link(email: str) -> bool:
    """
    Send magic link email (stub for Phase 103)
    In production, integrate with Gmail API
    
    Args:
        email: Customer email address
        
    Returns:
        True if email queued successfully
    """
    magic_token = generate_jwt(email)
    magic_url = f"{PUBLIC_BASE_URL}/auth/verify?token={magic_token}"
    
    # Stub: Log to emails.ndjson instead of sending
    os.makedirs("logs", exist_ok=True)
    email_log = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "to": email,
        "from": EMAIL_FROM,
        "subject": "EchoPilot Login Link",
        "magic_url": magic_url
    }
    
    with open("logs/emails.ndjson", "a") as f:
        f.write(json.dumps(email_log) + "\n")
    
    log_auth_event("magic_link_sent", email=email)
    
    return True


def get_customer_by_email(email: str) -> Optional[Dict]:
    """
    Lookup customer by email from Notion Client database
    
    Args:
        email: Customer email address
        
    Returns:
        Customer dict with stripe_customer_id or None
    """
    try:
        from bot import notion_api
        
        # Query Notion Client database
        client_db_id = os.getenv("NOTION_CLIENT_DB_ID")
        if not client_db_id:
            return None
        
        response = notion_api.notion.databases.query(
            database_id=client_db_id,
            filter={
                "property": "Email",
                "email": {
                    "equals": email
                }
            }
        )
        
        if response.get("results"):
            client = response["results"][0]
            return {
                "email": email,
                "customer_id": client["properties"].get("Stripe ID", {}).get("rich_text", [{}])[0].get("plain_text", ""),
                "name": client["properties"].get("Name", {}).get("title", [{}])[0].get("plain_text", "")
            }
        
        return None
        
    except Exception as e:
        log_auth_event("customer_lookup_error", email=email, error=str(e))
        return None
