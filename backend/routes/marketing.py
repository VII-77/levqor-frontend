"""
Marketing consent management with double opt-in
"""

from flask import Blueprint, request, jsonify, redirect
from time import time
import logging
import secrets
import os

log = logging.getLogger("levqor.marketing")

marketing_bp = Blueprint('marketing', __name__, url_prefix='/api/marketing')


def get_db():
    """Import get_db from run.py at runtime to avoid circular imports"""
    from run import get_db as _get_db
    return _get_db()


def send_double_optin_email(email, token):
    """
    Send double opt-in confirmation email.
    Uses existing email infrastructure.
    """
    from billing.dunning_emails import send_billing_email
    
    base_url = os.environ.get("NEXTAUTH_URL", "https://levqor.ai")
    confirm_url = f"{base_url}/api/marketing/confirm?token={token}"
    
    subject = "Confirm your Levqor newsletter subscription"
    
    body = f"""Hi there,

You (or someone using your email address) signed up for the Levqor newsletter.

To complete your subscription and start receiving product updates, automation tips, and exclusive offers, please click the link below:

{confirm_url}

This link will expire in 7 days.

If you did not sign up for our newsletter, you can safely ignore this email.

Best regards,
The Levqor Team

---
This is a confirmation email for newsletter subscription at levqor.ai
"""
    
    # This is transactional (confirming their subscription request)
    send_billing_email(email, subject, body, is_transactional=True)


@marketing_bp.route('/subscribe', methods=['POST'])
def subscribe():
    """
    Initiate marketing consent (double opt-in step 1).
    
    Expected JSON body:
    {
        "email": "user@example.com"
    }
    
    Returns:
        200: {"ok": true, "message": "Check your email to confirm"}
        400: {"ok": false, "error": "..."}
    """
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({"ok": False, "error": "Email required"}), 400
        
        # Validate email format (basic)
        if '@' not in email or '.' not in email:
            return jsonify({"ok": False, "error": "Invalid email format"}), 400
        
        # Generate secure token
        token = secrets.token_urlsafe(32)
        
        db = get_db()
        
        # Check if user exists
        cursor = db.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            # Update existing user
            db.execute("""
                UPDATE users
                SET marketing_consent = 0,
                    marketing_consent_at = ?,
                    marketing_double_opt_in = 0,
                    marketing_double_opt_in_token = ?,
                    updated_at = ?
                WHERE email = ?
            """, (time(), token, time(), email))
        else:
            # Create new user record
            db.execute("""
                INSERT INTO users (
                    id, email, marketing_consent, marketing_consent_at,
                    marketing_double_opt_in, marketing_double_opt_in_token,
                    created_at, updated_at
                )
                VALUES (?, ?, 0, ?, 0, ?, ?, ?)
            """, (
                f"user_{int(time()*1000000)}", email, time(), 
                token, time(), time()
            ))
        
        db.commit()
        
        # Send confirmation email
        try:
            send_double_optin_email(email, token)
            log.info(f"Double opt-in email sent: email={email}")
        except Exception as e:
            log.error(f"Failed to send confirmation email: {e}", exc_info=True)
            # Don't fail the request - token is saved, they can retry
        
        return jsonify({
            "ok": True,
            "message": "Please check your email to confirm your subscription"
        }), 200
        
    except Exception as e:
        log.error(f"Marketing subscription error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


@marketing_bp.route('/confirm', methods=['GET'])
def confirm():
    """
    Confirm marketing consent (double opt-in step 2).
    
    Query params:
        token: Confirmation token from email
    
    Returns:
        Redirect to /marketing/confirmed page
    """
    try:
        token = request.args.get('token', '').strip()
        
        if not token:
            log.warning("Confirmation attempted without token")
            return redirect('/marketing/confirmed?error=invalid_token')
        
        db = get_db()
        
        # Find user by token
        cursor = db.execute("""
            SELECT email, marketing_consent_at
            FROM users
            WHERE marketing_double_opt_in_token = ?
        """, (token,))
        
        row = cursor.fetchone()
        
        if not row:
            log.warning(f"Invalid or expired token: {token[:10]}...")
            return redirect('/marketing/confirmed?error=invalid_token')
        
        email, consent_at = row
        
        # Check if token is still valid (7 days)
        if time() - consent_at > 7 * 24 * 60 * 60:
            log.warning(f"Expired token for email: {email}")
            return redirect('/marketing/confirmed?error=expired_token')
        
        # Activate subscription
        db.execute("""
            UPDATE users
            SET marketing_consent = 1,
                marketing_double_opt_in = 1,
                marketing_double_opt_in_at = ?,
                marketing_double_opt_in_token = NULL,
                updated_at = ?
            WHERE email = ?
        """, (time(), time(), email))
        
        db.commit()
        
        log.info(f"Marketing consent confirmed: email={email}")
        
        return redirect('/marketing/confirmed?success=true')
        
    except Exception as e:
        log.error(f"Confirmation error: {e}", exc_info=True)
        return redirect('/marketing/confirmed?error=server_error')


@marketing_bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """
    Unsubscribe from marketing emails.
    
    Expected JSON body:
    {
        "email": "user@example.com"
    }
    
    Returns:
        200: {"ok": true, "message": "..."}
        400: {"ok": false, "error": "..."}
    """
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({"ok": False, "error": "Email required"}), 400
        
        db = get_db()
        
        # Update consent status
        db.execute("""
            UPDATE users
            SET marketing_consent = 0,
                marketing_double_opt_in = 0,
                updated_at = ?
            WHERE email = ?
        """, (time(), email))
        
        if db.total_changes == 0:
            # Email not found - still return success (idempotent)
            log.info(f"Unsubscribe attempted for non-existent email: {email}")
            return jsonify({
                "ok": True,
                "message": "If this email was subscribed, it has been removed"
            }), 200
        
        db.commit()
        
        log.info(f"Marketing unsubscribe: email={email}")
        
        return jsonify({
            "ok": True,
            "message": "You have been unsubscribed from marketing emails"
        }), 200
        
    except Exception as e:
        log.error(f"Unsubscribe error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


@marketing_bp.route('/status', methods=['POST'])
def status():
    """
    Check marketing consent status.
    
    Expected JSON body:
    {
        "email": "user@example.com"
    }
    
    Returns:
        200: {"ok": true, "subscribed": true/false, "confirmed": true/false}
    """
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({"ok": False, "error": "Email required"}), 400
        
        db = get_db()
        cursor = db.execute("""
            SELECT marketing_consent, marketing_double_opt_in, 
                   marketing_double_opt_in_at
            FROM users
            WHERE email = ?
        """, (email,))
        
        row = cursor.fetchone()
        
        if not row:
            return jsonify({
                "ok": True,
                "subscribed": False,
                "confirmed": False
            }), 200
        
        consent, double_optin, confirmed_at = row
        
        return jsonify({
            "ok": True,
            "subscribed": bool(consent),
            "confirmed": bool(double_optin),
            "confirmed_at": confirmed_at
        }), 200
        
    except Exception as e:
        log.error(f"Status check error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500
