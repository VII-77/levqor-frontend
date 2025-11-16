"""
Error Logging API
Endpoint for logging errors from frontend and backend
"""

from flask import Blueprint, request, jsonify
from app import db
from backend.models.error_event import ErrorEvent
import logging
import os

log = logging.getLogger("levqor")

error_logging_bp = Blueprint('error_logging', __name__, url_prefix='/api/errors')


@error_logging_bp.route('/log', methods=['POST'])
def log_error():
    """
    Log an error event to the database
    
    Accepts JSON with:
    - source (string): "backend" or "frontend"
    - service (string): service name (e.g. "support_ai", "webhook_checkout")
    - path_or_screen (string, optional): request path or screen name
    - user_email (string, optional): user email if available
    - severity (string, optional): "info", "warning", "error", "critical" (default: "error")
    - message (string): error message
    - stack (string, optional): stack trace (will be truncated if very long)
    """
    try:
        data = request.get_json() or {}
        
        # Extract and validate fields
        source = data.get('source', 'backend')
        service = data.get('service', 'unknown')
        severity = data.get('severity', 'error')
        message = data.get('message', '')
        
        if not message:
            return jsonify({'ok': False, 'error': 'message is required'}), 400
        
        # Truncate stack trace if very long (keep last 5000 chars for most recent trace)
        stack = data.get('stack')
        if stack and len(stack) > 5000:
            stack = '...(truncated)\n' + stack[-5000:]
        
        # Create error event
        error_event = ErrorEvent(
            source=source,
            service=service,
            path_or_screen=data.get('path_or_screen'),
            user_email=data.get('user_email'),
            severity=severity,
            message=message[:2000],  # Truncate message to 2000 chars
            stack=stack
        )
        
        db.session.add(error_event)
        db.session.commit()
        
        log.info(f"Error logged: {severity} from {source}/{service}: {message[:100]}")
        
        return jsonify({'ok': True}), 200
        
    except Exception as e:
        log.exception("Failed to log error event")
        db.session.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 500


@error_logging_bp.route('/recent', methods=['GET'])
def get_recent_errors():
    """
    Get recent error events (owner/admin only)
    
    Query params:
    - limit (int, default 50): number of errors to return
    - severity (string, optional): filter by severity
    - source (string, optional): filter by source
    - service (string, optional): filter by service
    """
    try:
        # Verify internal secret for owner/admin access
        internal_secret = request.headers.get('X-Internal-Secret')
        expected_secret = os.environ.get('INTERNAL_SECRET')
        
        if not internal_secret or not expected_secret or internal_secret != expected_secret:
            return jsonify({'error': 'Unauthorized'}), 401
        
        limit = min(int(request.args.get('limit', 50)), 500)  # Max 500
        
        # Build query
        query = ErrorEvent.query
        
        if request.args.get('severity'):
            query = query.filter_by(severity=request.args.get('severity'))
        
        if request.args.get('source'):
            query = query.filter_by(source=request.args.get('source'))
        
        if request.args.get('service'):
            query = query.filter_by(service=request.args.get('service'))
        
        # Order by most recent first
        errors = query.order_by(ErrorEvent.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'ok': True,
            'errors': [err.to_dict() for err in errors],
            'count': len(errors)
        }), 200
        
    except Exception as e:
        log.exception("Failed to retrieve recent errors")
        return jsonify({'ok': False, 'error': str(e)}), 500
