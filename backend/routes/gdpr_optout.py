"""
GDPR Right to Object / Opt-out API Endpoints
Allows users to object to marketing, profiling, automation, and analytics.
"""

from flask import Blueprint, request, jsonify
from time import time
from uuid import uuid4
import sqlite3
import os
from datetime import datetime, timezone

gdpr_optout_bp = Blueprint('gdpr_optout', __name__, url_prefix='/api/gdpr')

DB_PATH = os.environ.get("SQLITE_PATH", os.path.join(os.getcwd(), "levqor.db"))

def get_current_user():
    """Get current user from request context"""
    # This should integrate with existing auth system
    # For now, using JWT token from Authorization header
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header[7:]  # Remove 'Bearer ' prefix
    
    # TODO: Verify JWT token and extract user_id
    # For now, returning None to indicate unauthenticated
    # This will be integrated with existing NextAuth system
    
    # Placeholder: extract user_id from token
    # In production, this should verify JWT signature
    try:
        import jwt
        JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret-change-in-prod")
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload.get('user_id')
    except:
        return None


@gdpr_optout_bp.route('/opt-out', methods=['GET'])
def get_opt_out_status():
    """GET /api/gdpr/opt-out - Get current opt-out status"""
    user_id = get_current_user()
    
    if not user_id:
        return jsonify({"error": "unauthorized"}), 401
    
    try:
        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()
        
        cursor.execute("""
            SELECT gdpr_opt_out_marketing, gdpr_opt_out_profiling,
                   gdpr_opt_out_automation, gdpr_opt_out_analytics,
                   gdpr_opt_out_all, gdpr_opt_out_at
            FROM users WHERE id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        db.close()
        
        if not row:
            return jsonify({"error": "user_not_found"}), 404
        
        return jsonify({
            "ok": True,
            "marketing": bool(row[0]),
            "profiling": bool(row[1]),
            "automation": bool(row[2]),
            "analytics": bool(row[3]),
            "all": bool(row[4]),
            "timestamp": row[5]
        })
    
    except Exception as e:
        return jsonify({"error": "internal_error", "details": str(e)}), 500


@gdpr_optout_bp.route('/opt-out', methods=['POST'])
def set_opt_out():
    """POST /api/gdpr/opt-out - Set opt-out preferences"""
    user_id = get_current_user()
    
    if not user_id:
        return jsonify({"error": "unauthorized"}), 401
    
    data = request.get_json()
    if not data or 'scope' not in data:
        return jsonify({"error": "bad_request", "message": "scope required"}), 400
    
    scope = data['scope']
    valid_scopes = ['marketing', 'profiling', 'automation', 'analytics', 'all']
    
    if scope not in valid_scopes:
        return jsonify({
            "error": "bad_request",
            "message": f"scope must be one of: {', '.join(valid_scopes)}"
        }), 400
    
    try:
        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()
        now = time()
        
        # Get current user data
        cursor.execute("""
            SELECT gdpr_opt_out_marketing, gdpr_opt_out_profiling,
                   gdpr_opt_out_automation, gdpr_opt_out_analytics,
                   gdpr_opt_out_all, gdpr_opt_out_at
            FROM users WHERE id = ?
        """, (user_id,))
        
        current = cursor.fetchone()
        if not current:
            db.close()
            return jsonify({"error": "user_not_found"}), 404
        
        # Determine what to update
        updates = {}
        applied = []
        
        if scope == 'all':
            updates = {
                'gdpr_opt_out_marketing': 1,
                'gdpr_opt_out_profiling': 1,
                'gdpr_opt_out_automation': 1,
                'gdpr_opt_out_analytics': 1,
                'gdpr_opt_out_all': 1
            }
            applied = ['marketing', 'profiling', 'automation', 'analytics']
        else:
            # Set individual scope
            col_name = f'gdpr_opt_out_{scope}'
            updates[col_name] = 1
            applied = [scope]
            
            # Check if all individual scopes are now True
            cursor.execute("""
                SELECT gdpr_opt_out_marketing, gdpr_opt_out_profiling,
                       gdpr_opt_out_automation, gdpr_opt_out_analytics
                FROM users WHERE id = ?
            """, (user_id,))
            flags = cursor.fetchone()
            
            # Create a new tuple with the updated value
            flag_list = list(flags)
            scope_index = ['marketing', 'profiling', 'automation', 'analytics'].index(scope)
            flag_list[scope_index] = 1
            
            if all(flag_list):
                updates['gdpr_opt_out_all'] = 1
        
        # Set timestamp if not already set
        if not current[5]:  # gdpr_opt_out_at
            updates['gdpr_opt_out_at'] = now
        
        # Build UPDATE query
        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [user_id]
        
        cursor.execute(f"""
            UPDATE users SET {set_clause} WHERE id = ?
        """, values)
        
        # Log the objection
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_agent = request.headers.get('User-Agent', '')
        
        cursor.execute("""
            INSERT INTO gdpr_objection_log (id, user_id, scope, ip_address, user_agent, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(uuid4()), user_id, scope, ip_address, user_agent, now))
        
        db.commit()
        
        # Get final state
        cursor.execute("""
            SELECT gdpr_opt_out_all, gdpr_opt_out_at
            FROM users WHERE id = ?
        """, (user_id,))
        
        final_state = cursor.fetchone()
        db.close()
        
        return jsonify({
            "ok": True,
            "applied": applied,
            "opt_out_all": bool(final_state[0]),
            "effective_at": datetime.fromtimestamp(final_state[1], tz=timezone.utc).isoformat() if final_state[1] else None
        })
    
    except Exception as e:
        return jsonify({"error": "internal_error", "details": str(e)}), 500
