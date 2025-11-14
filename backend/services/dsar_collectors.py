"""
DSAR Data Collectors
Internal server-side functions to gather all user data from the database.
These do not send emails, create zips, or expose data externally.
Pure internal collectors for GDPR compliance.
"""

from app import db
from backend.models.dsar_request import DSARRequest


def collect_user_account(user_id, db_connection):
    """Collect user account data from SQLite"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT id, email, name, locale, currency, created_at, updated_at,
               terms_accepted_at, terms_version, marketing_consent, 
               marketing_consent_at, meta
        FROM users WHERE id = ?
    """, (user_id,))
    
    row = cursor.fetchone()
    if not row:
        return None

    return {
        "user_id": row[0],
        "email": row[1],
        "full_name": row[2],
        "locale": row[3],
        "currency": row[4],
        "created_at": row[5],
        "updated_at": row[6],
        "terms_accepted_at": row[7],
        "terms_version": row[8],
        "marketing_consent": bool(row[9]),
        "marketing_consent_at": row[10],
        "metadata": row[11],
    }


def collect_user_referrals(user_id, db_connection):
    """Collect user referral data"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT id, source, campaign, medium, created_at
        FROM referrals WHERE user_id = ?
    """, (user_id,))
    
    return [
        {
            "referral_id": r[0],
            "source": r[1],
            "campaign": r[2],
            "medium": r[3],
            "created_at": r[4],
        }
        for r in cursor.fetchall()
    ]


def collect_user_developer_keys(user_id, db_connection):
    """Collect user API keys (prefixes only for security)"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT id, key_prefix, created_at, last_used_at, is_active
        FROM developer_keys WHERE user_id = ?
    """, (user_id,))
    
    return [
        {
            "key_id": k[0],
            "key_prefix": k[1],
            "created_at": k[2],
            "last_used_at": k[3],
            "is_active": bool(k[4]),
        }
        for k in cursor.fetchall()
    ]


def collect_user_api_usage(user_id, db_connection):
    """Collect API usage logs"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT created_at, endpoint, status_code
        FROM api_usage_log WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 1000
    """, (user_id,))
    
    return [
        {
            "created_at": u[0],
            "endpoint": u[1],
            "status_code": u[2],
        }
        for u in cursor.fetchall()
    ]


def collect_user_partnerships(user_id, db_connection):
    """Collect partnership data - Note: partners table doesn't have user_id"""
    # Partners table doesn't link to users, so return empty list
    return []


def collect_user_marketplace_orders(user_id, db_connection):
    """Collect marketplace order history"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT id, listing_id, amount_cents, status, created_at, completed_at
        FROM marketplace_orders WHERE user_id = ?
    """, (user_id,))
    
    return [
        {
            "order_id": o[0],
            "listing_id": o[1],
            "amount_cents": o[2],
            "status": o[3],
            "created_at": o[4],
            "completed_at": o[5],
        }
        for o in cursor.fetchall()
    ]


def collect_user_marketing_consent(user_id, db_connection):
    """Collect marketing consent history"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT status, created_at, ip_address, confirmed_at
        FROM user_marketing_consent WHERE user_id = ?
    """, (user_id,))
    
    return [
        {
            "status": m[0],
            "created_at": m[1],
            "ip_address": m[2],
            "confirmed_at": m[3],
        }
        for m in cursor.fetchall()
    ]


def collect_user_risk_blocks(user_id, db_connection):
    """Collect risk blocking history"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT id, blocked_terms, created_at
        FROM risk_blocks WHERE user_id = ?
    """, (user_id,))
    
    return [
        {
            "block_id": r[0],
            "blocked_terms": r[1],
            "created_at": r[2],
        }
        for r in cursor.fetchall()
    ]


def collect_user_billing_events(user_id, db_connection):
    """Collect billing event history"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT id, event_type, created_at, event_payload_snippet
        FROM billing_events WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 500
    """, (user_id,))
    
    return [
        {
            "event_id": b[0],
            "event_type": b[1],
            "created_at": b[2],
            "payload_snippet": b[3],
        }
        for b in cursor.fetchall()
    ]


def collect_dsar_request_metadata(reference_id):
    """Collect DSAR request metadata using PostgreSQL session"""
    from app import db as postgres_db
    
    session = postgres_db.session
    req = session.query(DSARRequest).filter_by(gdpr_reference_id=reference_id).first()
    if not req:
        return None

    return {
        "gdpr_reference_id": req.gdpr_reference_id,
        "email": req.email,
        "status": req.status,
        "requested_at": req.requested_at.isoformat() if req.requested_at else None,
        "completed_at": req.completed_at.isoformat() if req.completed_at else None,
        "export_bytes_size": req.export_bytes_size,
        "last_error": req.last_error,
        "request_ip": req.request_ip,
    }


def collect_all_user_data(user_id, reference_id, db_connection):
    """
    Main collector used by the DSAR export generator.
    Returns a dict containing ALL user-associated data.
    
    Args:
        user_id: User ID to collect data for
        reference_id: GDPR reference ID for the request
        db_connection: SQLite database connection
        
    Returns:
        dict: All user data organized by category
    """
    return {
        "account": collect_user_account(user_id, db_connection),
        "referrals": collect_user_referrals(user_id, db_connection),
        "developer_keys": collect_user_developer_keys(user_id, db_connection),
        "api_usage": collect_user_api_usage(user_id, db_connection),
        "partnerships": collect_user_partnerships(user_id, db_connection),
        "marketplace_orders": collect_user_marketplace_orders(user_id, db_connection),
        "marketing_consent": collect_user_marketing_consent(user_id, db_connection),
        "risk_blocks": collect_user_risk_blocks(user_id, db_connection),
        "billing_events": collect_user_billing_events(user_id, db_connection),
        "dsar_request": collect_dsar_request_metadata(reference_id),
    }
