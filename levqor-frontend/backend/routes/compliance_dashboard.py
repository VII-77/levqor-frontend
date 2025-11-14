"""
Compliance Analytics & Audit Dashboard
Comprehensive compliance monitoring and reporting
"""

from flask import Blueprint, request, jsonify
from time import time
import logging

log = logging.getLogger("levqor.compliance")

compliance_dashboard_bp = Blueprint('compliance_dashboard', __name__, url_prefix='/api/compliance')


def get_db():
    from run import get_db as _get_db
    return _get_db()


@compliance_dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """
    Get comprehensive compliance dashboard (admin only).
    
    Query params:
        admin_token: Admin authorization token
    
    Returns:
        200: {
            "ok": true,
            "tos_compliance": {...},
            "marketing_compliance": {...},
            "gdpr_compliance": {...},
            "high_risk_blocks": {...},
            "data_retention": {...}
        }
    """
    try:
        import os
        admin_token = request.args.get('admin_token')
        
        if admin_token != os.environ.get("ADMIN_TOKEN"):
            return jsonify({"ok": False, "error": "Unauthorized"}), 403
        
        db = get_db()
        
        # TOS Compliance
        cursor = db.execute("SELECT COUNT(*) FROM users WHERE terms_accepted_at IS NOT NULL")
        tos_accepted = cursor.fetchone()[0]
        cursor = db.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        # Marketing Compliance
        cursor = db.execute("SELECT COUNT(*) FROM users WHERE marketing_double_opt_in = 1")
        marketing_consented = cursor.fetchone()[0]
        
        # GDPR Opt-outs
        cursor = db.execute("SELECT COUNT(*) FROM users WHERE gdpr_opt_out_all = 1")
        gdpr_opted_out = cursor.fetchone()[0]
        
        # High-Risk Blocks (last 30 days)
        cursor = db.execute("""
            SELECT COUNT(*) FROM risk_blocks 
            WHERE created_at > ?
        """, (time() - 30*24*60*60,))
        recent_blocks = cursor.fetchone()[0]
        
        # DSAR Requests
        cursor = db.execute("SELECT COUNT(*) FROM dsar_requests WHERE status = 'pending'")
        pending_dsar = cursor.fetchone()[0]
        
        return jsonify({
            "ok": True,
            "generated_at": time(),
            "tos_compliance": {
                "total_users": total_users,
                "accepted": tos_accepted,
                "acceptance_rate": round(tos_accepted / total_users, 3) if total_users > 0 else 0
            },
            "marketing_compliance": {
                "total_consented": marketing_consented,
                "consent_rate": round(marketing_consented / total_users, 3) if total_users > 0 else 0
            },
            "gdpr_compliance": {
                "total_opted_out": gdpr_opted_out,
                "opt_out_rate": round(gdpr_opted_out / total_users, 3) if total_users > 0 else 0,
                "pending_dsar_requests": pending_dsar
            },
            "high_risk_blocks": {
                "last_30_days": recent_blocks
            },
            "data_retention": {
                "status": "automated",
                "next_cleanup": "Daily at 03:00 UTC"
            }
        }), 200
        
    except Exception as e:
        log.error(f"Compliance dashboard error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


@compliance_dashboard_bp.route('/audit-trail', methods=['GET'])
def get_audit_trail():
    """
    Get compliance audit trail (admin only).
    
    Query params:
        admin_token: Admin token
        limit: Number of events (default 100, max 1000)
        event_type: Filter by type (optional)
    
    Returns:
        200: {"ok": true, "events": [...]}
    """
    try:
        import os
        admin_token = request.args.get('admin_token')
        
        if admin_token != os.environ.get("ADMIN_TOKEN"):
            return jsonify({"ok": False, "error": "Unauthorized"}), 403
        
        limit = min(int(request.args.get('limit', 100)), 1000)
        event_type = request.args.get('event_type')
        
        # Read security logs from file
        import os.path
        import json
        
        events = []
        log_file = os.path.join("logs", "audit.log")
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                for line in f.readlines()[-limit:]:
                    try:
                        event = json.loads(line.strip())
                        if not event_type or event.get('event') == event_type:
                            events.append(event)
                    except:
                        continue
        
        return jsonify({
            "ok": True,
            "events": events[-limit:],
            "count": len(events)
        }), 200
        
    except Exception as e:
        log.error(f"Audit trail error: {e}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500
