# SECURITY NOTE: Centralized security event logging for audit trail and anomaly detection
# Logs security events (auth failures, rate limits, lockouts) without exposing PII

import logging
import json
import hashlib
from time import time
from typing import Optional, Dict, Any

log = logging.getLogger("levqor.security")


def hash_identifier(value: str) -> str:
    """
    Hash sensitive identifiers (email, IP) for logging without exposing PII.
    Returns first 8 chars of SHA256 hash.
    """
    if not value or value == "unknown":
        return "unknown"
    return hashlib.sha256(value.encode()).hexdigest()[:8]


def log_security_event(
    event_type: str,
    *,
    user_id: Optional[str] = None,
    email: Optional[str] = None,
    ip: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    severity: str = "info"
) -> None:
    """
    Log a security event with consistent format.
    
    Args:
        event_type: Type of event (rate_limit, auth_failed, account_locked, etc.)
        user_id: User ID (if available)
        email: User email (will be hashed for privacy)
        ip: IP address (will be hashed for privacy)
        details: Additional context (no secrets!)
        severity: Log level (info, warning, error)
    
    Output format: Compact JSON for easy parsing
    """
    event = {
        "event": event_type,
        "ts": int(time()),
        "severity": severity
    }
    
    if user_id:
        event["user_id"] = user_id
    
    if email:
        event["email_hash"] = hash_identifier(email)
    
    if ip:
        event["ip_hash"] = hash_identifier(ip)
    
    if details:
        event["details"] = details
    
    msg = json.dumps(event, separators=(',', ':'))
    
    if severity == "error":
        log.error(f"[SECURITY] {msg}")
    elif severity == "warning":
        log.warning(f"[SECURITY] {msg}")
    else:
        log.info(f"[SECURITY] {msg}")
