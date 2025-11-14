"""
Enhanced Legal Consent Tracking with Version Management
Improvements:
- TOS version changelog
- Re-acceptance workflow when TOS updates
- Email notifications for TOS changes
- Structured audit trail
"""

from flask import Blueprint, request, jsonify
from time import time
import logging
import json

log = logging.getLogger("levqor.legal")

legal_enhanced_bp = Blueprint('legal_enhanced', __name__, url_prefix='/api/legal/v2')


def get_db():
    """Import get_db from run.py at runtime to avoid circular imports"""
    from run import get_db as _get_db
    return _get_db()


# TOS Version Changelog
TOS_VERSIONS = {
    "2025-Genesis-v1": {
        "version": "2025-Genesis-v1",
        "effective_date": "2025-11-14",
        "summary": "Initial Terms of Service for Levqor Genesis launch",
        "changes": [
            "Initial terms covering AI automation services",
            "Data processing and GDPR compliance",
            "Payment terms and subscription policies",
            "Acceptable use policies and high-risk restrictions"
        ],
        "requires_reaccept": False,  # First version
    },
    "2025-Genesis-v1.1": {
        "version": "2025-Genesis-v1.1",
        "effective_date": "2025-12-01",
        "summary": "Minor clarifications on data retention",
        "changes": [
            "Clarified data retention periods (Section 4.2)",
            "Added DSAR export timelines (Section 5.1)",
            "Updated contact information"
        ],
        "requires_reaccept": False,  # Minor changes
    },
}

CURRENT_TOS_VERSION = "2025-Genesis-v1"


@legal_enhanced_bp.route('/versions', methods=['GET'])
def get_tos_versions():
    """
    Get all TOS versions with changelog.
    
    Returns:
        200: {"ok": true, "current": "...", "versions": [...]}
    """
    try:
        versions_list = [
            {
                **v,
                "is_current": v["version"] == CURRENT_TOS_VERSION
            }
            for v in TOS_VERSIONS.values()
        ]
        
        # Sort by effective_date descending
        versions_list.sort(key=lambda x: x["effective_date"], reverse=True)
        
        return jsonify({
            "ok": True,
            "current": CURRENT_TOS_VERSION,
            "versions": versions_list
        }), 200
        
    except Exception as e:
        log.error(f"TOS versions error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


@legal_enhanced_bp.route('/check-user-status', methods=['POST'])
def check_user_status():
    """
    Check if user needs to re-accept TOS.
    
    Expected JSON body:
    {
        "email": "user@example.com"
    }
    
    Returns:
        200: {
            "ok": true,
            "needs_acceptance": true/false,
            "current_version": "2025-Genesis-v1",
            "user_version": "...",
            "changelog": [...]
        }
    """
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({"ok": False, "error": "Email required"}), 400
        
        db = get_db()
        cursor = db.execute("""
            SELECT terms_accepted_at, terms_version
            FROM users
            WHERE email = ?
        """, (email,))
        
        row = cursor.fetchone()
        
        # User doesn't exist or hasn't accepted TOS
        if not row or not row[0]:
            return jsonify({
                "ok": True,
                "needs_acceptance": True,
                "current_version": CURRENT_TOS_VERSION,
                "user_version": None,
                "changelog": list(TOS_VERSIONS[CURRENT_TOS_VERSION]["changes"])
            }), 200
        
        user_version = row[1]
        
        # Check if current version requires re-acceptance
        needs_reaccept = (
            user_version != CURRENT_TOS_VERSION and
            TOS_VERSIONS.get(CURRENT_TOS_VERSION, {}).get("requires_reaccept", False)
        )
        
        # Get changelog between versions
        changelog = []
        if user_version != CURRENT_TOS_VERSION:
            current_info = TOS_VERSIONS.get(CURRENT_TOS_VERSION, {})
            changelog = current_info.get("changes", [])
        
        return jsonify({
            "ok": True,
            "needs_acceptance": needs_reaccept,
            "current_version": CURRENT_TOS_VERSION,
            "user_version": user_version,
            "changelog": changelog
        }), 200
        
    except Exception as e:
        log.error(f"TOS status check error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


@legal_enhanced_bp.route('/accept-with-audit', methods=['POST'])
def accept_with_audit():
    """
    Accept TOS with enhanced audit logging.
    
    Expected JSON body:
    {
        "email": "user@example.com",
        "tos_version": "2025-Genesis-v1",
        "user_agent": "...",
        "consent_method": "explicit_click|implied|forced"
    }
    
    Returns:
        200: {"ok": true, "audit_id": "..."}
    """
    from backend.security import log_security_event
    
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        tos_version = data.get('tos_version', CURRENT_TOS_VERSION)
        user_agent = data.get('user_agent', request.headers.get('User-Agent', ''))
        consent_method = data.get('consent_method', 'explicit_click')
        
        if not email:
            return jsonify({"ok": False, "error": "Email required"}), 400
        
        # Validate TOS version exists
        if tos_version not in TOS_VERSIONS:
            return jsonify({"ok": False, "error": "Invalid TOS version"}), 400
        
        # Get IP address
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ',' in ip_address:
            ip_address = ip_address.split(',')[0].strip()
        
        db = get_db()
        
        # Check if user exists
        cursor = db.execute("SELECT id, terms_version FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        
        previous_version = row[1] if row else None
        
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
            # User doesn't exist yet
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
        
        # Enhanced security logging
        log_security_event(
            "tos_accepted",
            email=email,
            ip=ip_address,
            details={
                "tos_version": tos_version,
                "previous_version": previous_version,
                "consent_method": consent_method,
                "user_agent": user_agent[:100]  # Truncate
            },
            severity="info"
        )
        
        log.info(f"TOS accepted: email={email}, version={tos_version}, method={consent_method}")
        
        return jsonify({
            "ok": True,
            "version": tos_version,
            "accepted_at": time()
        }), 200
        
    except Exception as e:
        log.error(f"TOS acceptance error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


@legal_enhanced_bp.route('/notify-tos-update', methods=['POST'])
def notify_tos_update():
    """
    Notify all users about TOS update (admin only).
    
    Expected JSON body:
    {
        "admin_token": "...",
        "new_version": "2025-Genesis-v1.1",
        "requires_reaccept": true/false
    }
    
    Returns:
        200: {"ok": true, "emails_sent": 123}
    """
    try:
        data = request.get_json() or {}
        admin_token = data.get('admin_token')
        new_version = data.get('new_version')
        requires_reaccept = data.get('requires_reaccept', False)
        
        # Verify admin token
        import os
        if admin_token != os.environ.get("ADMIN_TOKEN"):
            return jsonify({"ok": False, "error": "Unauthorized"}), 403
        
        if new_version not in TOS_VERSIONS:
            return jsonify({"ok": False, "error": "Invalid version"}), 400
        
        db = get_db()
        
        # Get all users who need notification
        cursor = db.execute("""
            SELECT email, name
            FROM users
            WHERE terms_version != ? OR terms_version IS NULL
        """, (new_version,))
        
        users = cursor.fetchall()
        emails_sent = 0
        
        for email, name in users:
            try:
                send_tos_update_email(
                    email=email,
                    name=name or "User",
                    new_version=new_version,
                    requires_reaccept=requires_reaccept,
                    changelog=TOS_VERSIONS[new_version]["changes"]
                )
                emails_sent += 1
            except Exception as e:
                log.error(f"Failed to send TOS update email to {email}: {e}")
        
        log.info(f"TOS update notifications sent: {emails_sent} users")
        
        return jsonify({
            "ok": True,
            "emails_sent": emails_sent,
            "total_users": len(users)
        }), 200
        
    except Exception as e:
        log.error(f"TOS notification error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


def send_tos_update_email(email: str, name: str, new_version: str, 
                          requires_reaccept: bool, changelog: list):
    """Send TOS update notification email"""
    from billing.dunning_emails import send_billing_email
    import os
    
    base_url = os.environ.get("NEXTAUTH_URL", "https://levqor.ai")
    
    if requires_reaccept:
        subject = "ACTION REQUIRED: Updated Terms of Service - Levqor"
        action_text = f"You must review and accept the new terms to continue using Levqor. Please visit {base_url}/terms to review and accept."
    else:
        subject = "Updated Terms of Service - Levqor"
        action_text = f"No action is required. The changes will take effect automatically. You can review the updated terms at {base_url}/terms."
    
    changelog_html = "\n".join([f"• {change}" for change in changelog])
    
    body = f"""Hi {name},

We've updated our Terms of Service (Version {new_version}).

What's changed:
{changelog_html}

{action_text}

If you have any questions, please contact support@levqor.ai.

Best regards,
The Levqor Team

---
This is an important service notification from levqor.ai
"""
    
    send_billing_email(email, subject, body, is_transactional=True)
