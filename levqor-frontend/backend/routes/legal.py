"""
Legal consent tracking (TOS acceptance)
"""

from flask import Blueprint, request, jsonify
from time import time
import logging

log = logging.getLogger("levqor.legal")

legal_bp = Blueprint('legal', __name__, url_prefix='/api/legal')


def get_db():
    """Import get_db from run.py at runtime to avoid circular imports"""
    from run import get_db as _get_db
    return _get_db()


@legal_bp.route('/accept-terms', methods=['POST'])
def accept_terms():
    """
    Log ToS acceptance.
    
    Expected JSON body:
    {
        "email": "user@example.com",
        "tos_version": "2025-Genesis-v1",
        "privacy_version": "2025-Genesis-v1" (optional)
    }
    
    Returns:
        200: {"ok": true}
        400: {"ok": false, "error": "..."}
    """
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        tos_version = data.get('tos_version', '2025-Genesis-v1')
        
        if not email:
            log.warning("TOS acceptance attempted without email")
            return jsonify({"ok": False, "error": "Email required"}), 400
        
        # Get IP address (handle proxies)
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ',' in ip_address:
            ip_address = ip_address.split(',')[0].strip()
        
        db = get_db()
        
        # Update or insert user TOS acceptance
        db.execute("""
            UPDATE users 
            SET terms_accepted_at = ?,
                terms_version = ?,
                terms_accepted_ip = ?,
                updated_at = ?
            WHERE email = ?
        """, (time(), tos_version, ip_address, time(), email))
        
        if db.total_changes == 0:
            # User doesn't exist yet, create minimal record
            db.execute("""
                INSERT INTO users (
                    id, email, terms_accepted_at, terms_version, 
                    terms_accepted_ip, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                f"user_{int(time()*1000000)}", email, time(), 
                tos_version, ip_address, time(), time()
            ))
        
        db.commit()
        
        log.info(f"TOS accepted: email={email}, version={tos_version}, ip={ip_address}")
        
        return jsonify({"ok": True}), 200
        
    except Exception as e:
        log.error(f"TOS acceptance error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


@legal_bp.route('/check-acceptance', methods=['POST'])
def check_acceptance():
    """
    Check if user has accepted current ToS version.
    
    Expected JSON body:
    {
        "email": "user@example.com",
        "tos_version": "2025-Genesis-v1" (optional, defaults to current)
    }
    
    Returns:
        200: {"ok": true, "accepted": true/false, "version": "...", "accepted_at": timestamp}
    """
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        required_version = data.get('tos_version', '2025-Genesis-v1')
        
        if not email:
            return jsonify({"ok": False, "error": "Email required"}), 400
        
        db = get_db()
        cursor = db.execute("""
            SELECT terms_accepted_at, terms_version, terms_accepted_ip
            FROM users
            WHERE email = ?
        """, (email,))
        
        row = cursor.fetchone()
        
        if not row or not row[0]:
            # No acceptance record
            return jsonify({
                "ok": True,
                "accepted": False,
                "version": None,
                "accepted_at": None
            }), 200
        
        accepted_at, version, ip = row
        version_match = (version == required_version)
        
        return jsonify({
            "ok": True,
            "accepted": version_match,
            "version": version,
            "accepted_at": accepted_at,
            "ip": ip
        }), 200
        
    except Exception as e:
        log.error(f"TOS check error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500
