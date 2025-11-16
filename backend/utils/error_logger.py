"""
Error Logging Utility
Helper function to log errors to the database
"""

from app import db
from backend.models.error_event import ErrorEvent
from datetime import datetime
import logging
import traceback

log = logging.getLogger("levqor")


def log_error_event(
    source,
    service,
    message,
    severity="error",
    path_or_screen=None,
    user_email=None,
    stack=None
):
    """
    Log an error event to the database
    
    Args:
        source: "backend" or "frontend"
        service: Service name (e.g. "support_ai", "webhook_checkout")
        message: Error message
        severity: "info", "warning", "error", "critical" (default: "error")
        path_or_screen: Request path or screen name (optional)
        user_email: User email if available (optional)
        stack: Stack trace (optional)
    
    Returns:
        bool: True if logged successfully, False otherwise
    """
    try:
        # Truncate stack trace if very long
        if stack and len(stack) > 5000:
            stack = '...(truncated)\n' + stack[-5000:]
        
        # Create error event
        error_event = ErrorEvent(
            created_at=datetime.utcnow(),
            source=source,
            service=service,
            path_or_screen=path_or_screen,
            user_email=user_email,
            severity=severity,
            message=message[:2000],  # Truncate to 2000 chars
            stack=stack
        )
        
        db.session.add(error_event)
        db.session.commit()
        
        log.debug(f"Error logged: {severity} from {source}/{service}")
        return True
        
    except Exception as e:
        # Don't crash on logging errors
        log.error(f"Failed to log error event: {e}")
        try:
            db.session.rollback()
        except:
            pass
        return False


def log_exception(source, service, exc=None, severity="error", user_email=None, path_or_screen=None):
    """
    Log an exception with automatic stack trace extraction
    
    Args:
        source: "backend" or "frontend"
        service: Service name
        exc: Exception object (if None, uses current exception)
        severity: Severity level
        user_email: User email (optional)
        path_or_screen: Path or screen name (optional)
    """
    try:
        message = str(exc) if exc else "Unknown error"
        stack_trace = traceback.format_exc() if exc or True else None
        
        return log_error_event(
            source=source,
            service=service,
            message=message,
            severity=severity,
            path_or_screen=path_or_screen,
            user_email=user_email,
            stack=stack_trace
        )
    except Exception as e:
        log.error(f"Failed to log exception: {e}")
        return False
