"""
GDPR Opt-out Enforcement Helper Functions
Provides centralized enforcement checks for all opt-out scopes.
"""

import sqlite3
import os
import logging

log = logging.getLogger("levqor.gdpr")

DB_PATH = os.environ.get("SQLITE_PATH", os.path.join(os.getcwd(), "levqor.db"))


def check_opt_out(user_id, scope):
    """
    Check if user has opted out of a specific scope.
    
    Args:
        user_id: User ID to check
        scope: One of 'marketing', 'profiling', 'automation', 'analytics', or 'all'
    
    Returns:
        Boolean: True if opted out, False otherwise
    """
    if not user_id:
        return False
    
    try:
        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()
        
        # Check both the specific scope and the "all" flag
        col_name = f'gdpr_opt_out_{scope}'
        cursor.execute(f"""
            SELECT {col_name}, gdpr_opt_out_all
            FROM users WHERE id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        db.close()
        
        if not row:
            return False
        
        # User opted out if either the specific scope or "all" is True
        return bool(row[0]) or bool(row[1])
    
    except Exception as e:
        log.error(f"Error checking GDPR opt-out for user {user_id}, scope {scope}: {e}")
        # Fail safe: don't allow activity if we can't check
        return True


def get_user_opt_outs(user_id):
    """
    Get all opt-out flags for a user.
    
    Returns:
        Dict with marketing, profiling, automation, analytics, all keys
        Returns None if user not found
    """
    if not user_id:
        return None
    
    try:
        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()
        
        cursor.execute("""
            SELECT gdpr_opt_out_marketing, gdpr_opt_out_profiling,
                   gdpr_opt_out_automation, gdpr_opt_out_analytics,
                   gdpr_opt_out_all
            FROM users WHERE id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        db.close()
        
        if not row:
            return None
        
        return {
            'marketing': bool(row[0]),
            'profiling': bool(row[1]),
            'automation': bool(row[2]),
            'analytics': bool(row[3]),
            'all': bool(row[4])
        }
    
    except Exception as e:
        log.error(f"Error getting GDPR opt-outs for user {user_id}: {e}")
        return None


def should_send_marketing_email(user_id):
    """
    Check if marketing emails can be sent to this user.
    Returns False if user has opted out of marketing.
    """
    return not check_opt_out(user_id, 'marketing')


def should_run_automation(user_id):
    """
    Check if automated workflows can be run for this user.
    Returns False if user has opted out of automation.
    """
    return not check_opt_out(user_id, 'automation')


def should_apply_profiling(user_id):
    """
    Check if profiling/AI suggestions can be applied for this user.
    Returns False if user has opted out of profiling.
    """
    return not check_opt_out(user_id, 'profiling')


def should_track_analytics(user_id):
    """
    Check if analytics can be tracked for this user.
    Returns False if user has opted out of analytics.
    """
    return not check_opt_out(user_id, 'analytics')
