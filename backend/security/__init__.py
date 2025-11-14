# SECURITY NOTE: Security utilities module initialization
from .logger import log_security_event, hash_identifier
from .lockout import (
    record_failed_attempt,
    record_successful_login,
    is_locked_out,
    get_attempt_count,
    clear_lockout
)

__all__ = [
    'log_security_event',
    'hash_identifier',
    'record_failed_attempt',
    'record_successful_login',
    'is_locked_out',
    'get_attempt_count',
    'clear_lockout'
]
