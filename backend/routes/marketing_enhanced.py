"""
Enhanced Marketing Consent with Granular Preferences
Improvements:
- Granular consent categories (product updates, offers, technical, events)
- Preference center API
- Consent analytics
- Unsubscribe confirmation emails
"""

from flask import Blueprint, request, jsonify
from time import time
import logging
import json

log = logging.getLogger("levqor.marketing")

marketing_enhanced_bp = Blueprint('marketing_enhanced', __name__, url_prefix='/api/marketing/v2')


def get_db():
    from run import get_db as _get_db
    return _get_db()


# Marketing Preference Categories
PREFERENCE_CATEGORIES = {
    "product_updates": {
        "name": "Product Updates & News",
        "description": "Major product launches, feature releases, and platform updates",
        "frequency": "Monthly",
        "default": True
    },
    "offers_promotions": {
        "name": "Special Offers & Promotions",
        "description": "Exclusive discounts, early access, and limited-time offers",
        "frequency": "Weekly",
        "default": False
    },
    "technical_updates": {
        "name": "Technical & API Updates",
        "description": "API changes, deprecation notices, and technical documentation",
        "frequency": "As needed",
        "default": True
    },
    "events_webinars": {
        "name": "Events & Webinars",
        "description": "Invitations to webinars, workshops, and community events",
        "frequency": "Monthly",
        "default": False
    },
    "educational_content": {
        "name": "Educational Content",
        "description": "Automation tips, best practices, and use case guides",
        "frequency": "Bi-weekly",
        "default": True
    }
}


@marketing_enhanced_bp.route('/preferences/categories', methods=['GET'])
def get_categories():
    """
    Get available marketing preference categories.
    
    Returns:
        200: {"ok": true, "categories": {...}}
    """
    return jsonify({
        "ok": True,
        "categories": PREFERENCE_CATEGORIES
    }), 200


@marketing_enhanced_bp.route('/preferences/get', methods=['POST'])
def get_preferences():
    """
    Get user's current marketing preferences.
    
    Expected JSON body:
    {
        "email": "user@example.com"
    }
    
    Returns:
        200: {
            "ok": true,
            "preferences": {
                "product_updates": true,
                "offers_promotions": false,
                ...
            },
            "email_verified": true,
            "subscribed_at": timestamp
        }
    """
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({"ok": False, "error": "Email required"}), 400
        
        db = get_db()
        cursor = db.execute("""
            SELECT 
                marketing_double_opt_in,
                marketing_double_opt_in_at,
                meta
            FROM users
            WHERE email = ?
        """, (email,))
        
        row = cursor.fetchone()
        
        if not row:
            # User doesn't exist - return defaults
            return jsonify({
                "ok": True,
                "preferences": {k: v["default"] for k, v in PREFERENCE_CATEGORIES.items()},
                "email_verified": False,
                "subscribed_at": None
            }), 200
        
        is_verified, subscribed_at, meta_json = row
        
        # Parse stored preferences from meta
        try:
            meta = json.loads(meta_json) if meta_json else {}
            stored_prefs = meta.get("marketing_preferences", {})
        except:
            stored_prefs = {}
        
        # Merge with defaults
        preferences = {
            k: stored_prefs.get(k, v["default"])
            for k, v in PREFERENCE_CATEGORIES.items()
        }
        
        return jsonify({
            "ok": True,
            "preferences": preferences,
            "email_verified": bool(is_verified),
            "subscribed_at": subscribed_at
        }), 200
        
    except Exception as e:
        log.error(f"Get preferences error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


@marketing_enhanced_bp.route('/preferences/update', methods=['POST'])
def update_preferences():
    """
    Update user's marketing preferences.
    
    Expected JSON body:
    {
        "email": "user@example.com",
        "preferences": {
            "product_updates": true,
            "offers_promotions": false,
            ...
        }
    }
    
    Returns:
        200: {"ok": true}
    """
    from backend.security import log_security_event
    
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        preferences = data.get('preferences', {})
        
        if not email:
            return jsonify({"ok": False, "error": "Email required"}), 400
        
        # Validate preferences
        for key in preferences.keys():
            if key not in PREFERENCE_CATEGORIES:
                return jsonify({"ok": False, "error": f"Invalid preference: {key}"}), 400
        
        db = get_db()
        
        # Get current meta
        cursor = db.execute("SELECT meta FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        
        if not row:
            return jsonify({"ok": False, "error": "User not found"}), 404
        
        # Update meta with new preferences
        try:
            meta = json.loads(row[0]) if row[0] else {}
        except:
            meta = {}
        
        meta["marketing_preferences"] = preferences
        meta["preferences_updated_at"] = time()
        
        db.execute("""
            UPDATE users
            SET meta = ?,
                updated_at = ?
            WHERE email = ?
        """, (json.dumps(meta), time(), email))
        
        db.commit()
        
        # Log preference change
        log_security_event(
            "marketing_preferences_updated",
            email=email,
            details={"preferences": list(preferences.keys())},
            severity="info"
        )
        
        log.info(f"Marketing preferences updated: {email}")
        
        return jsonify({"ok": True}), 200
        
    except Exception as e:
        log.error(f"Update preferences error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


@marketing_enhanced_bp.route('/preferences/unsubscribe-all', methods=['POST'])
def unsubscribe_all():
    """
    Unsubscribe from all marketing categories (with confirmation email).
    
    Expected JSON body:
    {
        "email": "user@example.com",
        "reason": "too_frequent|not_relevant|never_subscribed|other"
    }
    
    Returns:
        200: {"ok": true}
    """
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        reason = data.get('reason', 'other')
        
        if not email:
            return jsonify({"ok": False, "error": "Email required"}), 400
        
        db = get_db()
        
        # Set all preferences to false
        cursor = db.execute("SELECT meta FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        
        if not row:
            return jsonify({"ok": False, "error": "User not found"}), 404
        
        try:
            meta = json.loads(row[0]) if row[0] else {}
        except:
            meta = {}
        
        # Turn off all categories
        meta["marketing_preferences"] = {k: False for k in PREFERENCE_CATEGORIES.keys()}
        meta["unsubscribe_reason"] = reason
        meta["unsubscribed_at"] = time()
        
        db.execute("""
            UPDATE users
            SET meta = ?,
                marketing_consent = 0,
                marketing_double_opt_in = 0,
                updated_at = ?
            WHERE email = ?
        """, (json.dumps(meta), time(), email))
        
        db.commit()
        
        # Send confirmation email
        send_unsubscribe_confirmation(email, reason)
        
        log.info(f"User unsubscribed from all marketing: {email}, reason={reason}")
        
        return jsonify({"ok": True}), 200
        
    except Exception as e:
        log.error(f"Unsubscribe all error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


def send_unsubscribe_confirmation(email: str, reason: str):
    """Send unsubscribe confirmation email"""
    from billing.dunning_emails import send_billing_email
    import os
    
    base_url = os.environ.get("NEXTAUTH_URL", "https://levqor.ai")
    
    subject = "You've been unsubscribed - Levqor"
    
    body = f"""Hi there,

You've successfully unsubscribed from all Levqor marketing emails.

You will no longer receive:
• Product updates and news
• Special offers and promotions
• Technical updates
• Event invitations
• Educational content

You'll still receive important account and billing notifications.

Changed your mind? You can resubscribe anytime at: {base_url}/settings/marketing

If you didn't request this, please contact support@levqor.ai.

Best regards,
The Levqor Team

---
This is a confirmation email from levqor.ai
"""
    
    send_billing_email(email, subject, body, is_transactional=True)


@marketing_enhanced_bp.route('/analytics/consent-rate', methods=['GET'])
def get_consent_rate():
    """
    Get marketing consent analytics (admin only).
    
    Query params:
        admin_token: Admin authorization token
    
    Returns:
        200: {
            "ok": true,
            "total_users": 1000,
            "consented_users": 450,
            "consent_rate": 0.45,
            "by_category": {...}
        }
    """
    try:
        import os
        admin_token = request.args.get('admin_token')
        
        if admin_token != os.environ.get("ADMIN_TOKEN"):
            return jsonify({"ok": False, "error": "Unauthorized"}), 403
        
        db = get_db()
        
        # Total users
        cursor = db.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        # Consented users (double opt-in)
        cursor = db.execute("SELECT COUNT(*) FROM users WHERE marketing_double_opt_in = 1")
        consented_users = cursor.fetchone()[0]
        
        # Get category breakdown
        cursor = db.execute("SELECT meta FROM users WHERE marketing_double_opt_in = 1")
        rows = cursor.fetchall()
        
        category_counts = {k: 0 for k in PREFERENCE_CATEGORIES.keys()}
        
        for (meta_json,) in rows:
            try:
                meta = json.loads(meta_json) if meta_json else {}
                prefs = meta.get("marketing_preferences", {})
                for cat, enabled in prefs.items():
                    if enabled and cat in category_counts:
                        category_counts[cat] += 1
            except:
                continue
        
        return jsonify({
            "ok": True,
            "total_users": total_users,
            "consented_users": consented_users,
            "consent_rate": round(consented_users / total_users, 3) if total_users > 0 else 0,
            "by_category": {
                k: {
                    "count": category_counts[k],
                    "percentage": round(category_counts[k] / consented_users, 3) if consented_users > 0 else 0
                }
                for k in PREFERENCE_CATEGORIES.keys()
            }
        }), 200
        
    except Exception as e:
        log.error(f"Consent analytics error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500
