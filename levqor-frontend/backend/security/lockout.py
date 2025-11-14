# SECURITY NOTE: Account lockout and IP-based abuse detection
# Tracks failed login attempts and implements temporary lockouts

from collections import defaultdict
from time import time
from typing import Dict, Tuple
import threading

# Thread-safe storage for failed attempts
_lock = threading.Lock()
_failed_attempts: Dict[str, list] = defaultdict(list)
_lockouts: Dict[str, float] = {}

# Configuration
MAX_ATTEMPTS = 5  # Failed attempts before lockout
LOCKOUT_WINDOW = 10 * 60  # 10 minutes to accumulate failures
LOCKOUT_DURATION = 15 * 60  # 15 minute lockout


def record_failed_attempt(identifier: str) -> None:
    """
    Record a failed authentication attempt for an email or IP.
    
    Args:
        identifier: Email address or IP address
    """
    now = time()
    
    with _lock:
        # Clean old attempts
        _failed_attempts[identifier] = [
            t for t in _failed_attempts[identifier]
            if now - t < LOCKOUT_WINDOW
        ]
        
        # Add new attempt
        _failed_attempts[identifier].append(now)


def record_successful_login(identifier: str) -> None:
    """
    Clear failed attempts on successful login.
    
    Args:
        identifier: Email address or IP address
    """
    with _lock:
        if identifier in _failed_attempts:
            del _failed_attempts[identifier]
        if identifier in _lockouts:
            del _lockouts[identifier]


def is_locked_out(identifier: str) -> Tuple[bool, int]:
    """
    Check if an identifier is currently locked out.
    
    Args:
        identifier: Email address or IP address
    
    Returns:
        Tuple of (is_locked, seconds_remaining)
    """
    now = time()
    
    with _lock:
        # Check existing lockout
        if identifier in _lockouts:
            lockout_until = _lockouts[identifier]
            if now < lockout_until:
                return (True, int(lockout_until - now))
            else:
                # Lockout expired
                del _lockouts[identifier]
                del _failed_attempts[identifier]
                return (False, 0)
        
        # Check if should be locked out
        attempts = _failed_attempts.get(identifier, [])
        recent_attempts = [t for t in attempts if now - t < LOCKOUT_WINDOW]
        
        if len(recent_attempts) >= MAX_ATTEMPTS:
            # Trigger lockout
            _lockouts[identifier] = now + LOCKOUT_DURATION
            return (True, LOCKOUT_DURATION)
        
        return (False, 0)


def get_attempt_count(identifier: str) -> int:
    """Get current failed attempt count for an identifier."""
    now = time()
    with _lock:
        attempts = _failed_attempts.get(identifier, [])
        recent = [t for t in attempts if now - t < LOCKOUT_WINDOW]
        return len(recent)


def clear_lockout(identifier: str) -> None:
    """Manually clear lockout (admin action)."""
    with _lock:
        if identifier in _lockouts:
            del _lockouts[identifier]
        if identifier in _failed_attempts:
            del _failed_attempts[identifier]
