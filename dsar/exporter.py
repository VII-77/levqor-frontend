"""
DSAR Data Exporter
Collects all user data from the database and creates a ZIP export
"""
import json
import os
import zipfile
import tempfile
import io
from datetime import datetime
from time import time


def generate_user_export(db_connection, user_id):
    """
    Generate a complete export of all data for a specific user
    
    Returns:
        dict with keys: storage_path, data_categories, metadata
    """
    
    # Collect user data
    cursor = db_connection.cursor()
    
    # 1. User account data
    cursor.execute("""
        SELECT id, email, name, locale, currency, meta, created_at, updated_at,
               terms_accepted_at, terms_version, terms_accepted_ip,
               marketing_consent, marketing_consent_at, marketing_double_opt_in
        FROM users WHERE id = ?
    """, (user_id,))
    user_row = cursor.fetchone()
    
    if not user_row:
        raise ValueError(f"User {user_id} not found")
    
    user_data = {
        "id": user_row[0],
        "email": user_row[1],
        "name": user_row[2],
        "locale": user_row[3],
        "currency": user_row[4],
        "metadata": json.loads(user_row[5]) if user_row[5] else {},
        "created_at": datetime.fromtimestamp(user_row[6]).isoformat() if user_row[6] else None,
        "updated_at": datetime.fromtimestamp(user_row[7]).isoformat() if user_row[7] else None,
        "terms_accepted_at": datetime.fromtimestamp(user_row[8]).isoformat() if user_row[8] else None,
        "terms_version": user_row[9],
        "terms_accepted_ip": user_row[10],
        "marketing_consent": bool(user_row[11]),
        "marketing_consent_at": datetime.fromtimestamp(user_row[12]).isoformat() if user_row[12] else None,
        "marketing_double_opt_in": bool(user_row[13]),
    }
    
    # 2. Referrals (if any)
    cursor.execute("""
        SELECT id, source, campaign, medium, created_at
        FROM referrals WHERE user_id = ?
    """, (user_id,))
    referrals = []
    for row in cursor.fetchall():
        referrals.append({
            "id": row[0],
            "source": row[1],
            "campaign": row[2],
            "medium": row[3],
            "created_at": datetime.fromtimestamp(row[4]).isoformat() if row[4] else None
        })
    
    # 3. Developer API keys (if any)
    cursor.execute("""
        SELECT id, name, prefix, created_at, last_used_at, expires_at, is_active
        FROM developer_keys WHERE user_id = ?
    """, (user_id,))
    api_keys = []
    for row in cursor.fetchall():
        api_keys.append({
            "id": row[0],
            "name": row[1],
            "prefix": row[2],  # Only prefix, never full key
            "created_at": datetime.fromtimestamp(row[3]).isoformat() if row[3] else None,
            "last_used_at": datetime.fromtimestamp(row[4]).isoformat() if row[4] else None,
            "expires_at": datetime.fromtimestamp(row[5]).isoformat() if row[5] else None,
            "is_active": bool(row[6])
        })
    
    # 4. Partner registrations (if any)
    cursor.execute("""
        SELECT id, company_name, contact_email, webhook_url, is_verified, is_active, created_at
        FROM partners WHERE user_id = ?
    """, (user_id,))
    partnerships = []
    for row in cursor.fetchall():
        partnerships.append({
            "id": row[0],
            "company_name": row[1],
            "contact_email": row[2],
            "webhook_url": row[3],
            "is_verified": bool(row[4]),
            "is_active": bool(row[5]),
            "created_at": datetime.fromtimestamp(row[6]).isoformat() if row[6] else None
        })
    
    # 5. Marketplace orders (if any)
    cursor.execute("""
        SELECT id, listing_id, amount_cents, status, created_at, completed_at
        FROM marketplace_orders WHERE user_id = ?
    """, (user_id,))
    orders = []
    for row in cursor.fetchall():
        orders.append({
            "id": row[0],
            "listing_id": row[1],
            "amount_cents": row[2],
            "status": row[3],
            "created_at": datetime.fromtimestamp(row[4]).isoformat() if row[4] else None,
            "completed_at": datetime.fromtimestamp(row[5]).isoformat() if row[5] else None
        })
    
    # Build export structure
    export_data = {
        "metadata": {
            "generated_at": datetime.utcnow().isoformat(),
            "version": "1.0",
            "format": "JSON",
            "user_id": user_id,
            "email": user_data["email"]
        },
        "user_account": user_data,
        "referrals": referrals,
        "developer_api_keys": api_keys,
        "partnerships": partnerships,
        "marketplace_orders": orders,
        "notes": {
            "passwords": "Password hashes are excluded for security",
            "api_keys": "Full API keys are excluded, only prefixes shown",
            "tokens": "Authentication tokens and secrets are excluded",
            "workflows": "Workflow execution data may be added in future exports"
        }
    }
    
    # Determine data categories present
    data_categories = ["user_account"]
    if referrals:
        data_categories.append("referrals")
    if api_keys:
        data_categories.append("api_keys")
    if partnerships:
        data_categories.append("partnerships")
    if orders:
        data_categories.append("marketplace_orders")
    
    # Create ZIP file
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"levqor_export_{user_id}_{timestamp}.zip"
    zip_path = os.path.join("exports", zip_filename)
    
    # Ensure exports directory exists
    os.makedirs("exports", exist_ok=True)
    
    # Write ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add metadata file
        metadata_json = json.dumps(export_data["metadata"], indent=2)
        zf.writestr("metadata.json", metadata_json)
        
        # Add full data file
        data_json = json.dumps(export_data, indent=2, ensure_ascii=False)
        zf.writestr("data.json", data_json)
        
        # Add README
        readme_content = """# Levqor Data Export

This archive contains all your personal data from Levqor.

## Files Included

- `metadata.json` - Export metadata (timestamp, version, user info)
- `data.json` - Complete data export in JSON format
- `README.txt` - This file

## Data Categories

"""
        readme_content += "\n".join(f"- {cat}" for cat in data_categories)
        readme_content += """

## Privacy & Security

For security reasons, this export excludes:
- Password hashes
- Full API keys and authentication tokens
- OAuth secrets and refresh tokens

If you need assistance interpreting this data or have questions about your privacy rights, 
contact: privacy@levqor.ai

## GDPR Rights

Under UK GDPR and EU GDPR, you have the right to:
- Access your personal data (this export)
- Rectify incorrect data
- Erase your data ("right to be forgotten")
- Restrict processing
- Data portability
- Object to processing

To exercise these rights, contact privacy@levqor.ai
"""
        zf.writestr("README.txt", readme_content)
    
    return {
        "storage_path": zip_path,
        "data_categories": json.dumps(data_categories),
        "metadata": export_data["metadata"]
    }


def generate_user_export_bytes(db_connection, user_id):
    """
    Generate export as in-memory bytes for email attachment (no disk storage)
    
    Returns:
        tuple: (zip_bytes, filename, size_bytes, data_categories)
    """
    cursor = db_connection.cursor()
    
    # Get user data first
    cursor.execute("SELECT id, email, name FROM users WHERE id = ?", (user_id,))
    user_row = cursor.fetchone()
    
    if not user_row:
        raise ValueError(f"User {user_id} not found")
    
    user_id_val, email, name = user_row
    
    # Generate timestamp for filename
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    filename = f"levqor-dsar-user-{user_id[:8]}-{timestamp}.zip"
    
    # Collect all user data using existing logic
    cursor.execute("""
        SELECT id, email, name, locale, currency, meta, created_at, updated_at,
               terms_accepted_at, terms_version, terms_accepted_ip,
               marketing_consent, marketing_consent_at, marketing_double_opt_in
        FROM users WHERE id = ?
    """, (user_id,))
    user_row = cursor.fetchone()
    
    export_data = {
        "metadata": {
            "export_version": "2.0",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            "email": email,
            "data_subject_request_type": "access"
        },
        "user": {
            "id": user_row[0],
            "email": user_row[1],
            "name": user_row[2],
            "locale": user_row[3],
            "currency": user_row[4],
            "metadata": json.loads(user_row[5]) if user_row[5] else {},
            "created_at": datetime.fromtimestamp(user_row[6]).isoformat() if user_row[6] else None,
            "updated_at": datetime.fromtimestamp(user_row[7]).isoformat() if user_row[7] else None,
            "terms_accepted_at": datetime.fromtimestamp(user_row[8]).isoformat() if user_row[8] else None,
            "terms_version": user_row[9],
            "marketing_consent": bool(user_row[11]),
            "marketing_consent_at": datetime.fromtimestamp(user_row[12]).isoformat() if user_row[12] else None,
        }
    }
    
    # Add referrals
    cursor.execute("""
        SELECT id, source, campaign, medium, created_at
        FROM referrals WHERE user_id = ?
    """, (user_id,))
    export_data["referrals"] = [
        {
            "id": r[0], "source": r[1], "campaign": r[2], "medium": r[3],
            "created_at": datetime.fromtimestamp(r[4]).isoformat() if r[4] else None
        }
        for r in cursor.fetchall()
    ]
    
    # Add API keys (prefix only, not full keys)
    cursor.execute("""
        SELECT id, name, prefix, created_at, last_used_at, is_active
        FROM developer_keys WHERE user_id = ?
    """, (user_id,))
    export_data["api_keys"] = [
        {
            "id": r[0], "name": r[1], "prefix": r[2],
            "created_at": datetime.fromtimestamp(r[3]).isoformat() if r[3] else None,
            "last_used_at": datetime.fromtimestamp(r[4]).isoformat() if r[4] else None,
            "is_active": bool(r[5])
        }
        for r in cursor.fetchall()
    ]
    
    # Add partners if table exists
    try:
        cursor.execute("""
            SELECT id, company_name, contact_email, is_verified, is_active, created_at
            FROM partners WHERE user_id = ?
        """, (user_id,))
        export_data["partnerships"] = [
            {
                "id": r[0], "company_name": r[1], "contact_email": r[2],
                "is_verified": bool(r[3]), "is_active": bool(r[4]),
                "created_at": datetime.fromtimestamp(r[5]).isoformat() if r[5] else None
            }
            for r in cursor.fetchall()
        ]
    except:
        export_data["partnerships"] = []
    
    # Add audit logs
    try:
        cursor.execute("""
            SELECT action, timestamp, ip_address, details
            FROM dsar_audit_log WHERE user_id = ? ORDER BY timestamp DESC LIMIT 100
        """, (user_id,))
        export_data["audit_logs"] = [
            {
                "action": r[0],
                "timestamp": datetime.fromtimestamp(r[1]).isoformat() if r[1] else None,
                "ip_address": r[2],
                "details": r[3]
            }
            for r in cursor.fetchall()
        ]
    except:
        export_data["audit_logs"] = []
    
    data_categories = ["user_profile", "referrals", "api_keys", "partnerships", "audit_logs"]
    
    # Create ZIP in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add user_data.json
        data_json = json.dumps(export_data, indent=2, ensure_ascii=False)
        zf.writestr("user_data.json", data_json)
        
        # Add README
        readme = f"""# Levqor Data Export (GDPR/UK-GDPR)

Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}
User: {email}

## Files Included

- user_data.json - Complete JSON export of all your data

## Data Categories

{chr(10).join(f"- {cat}" for cat in data_categories)}

## Privacy & Security

For security, this export excludes:
- Password hashes
- Full API keys (only prefixes included)
- OAuth secrets

## Your Rights (UK GDPR / EU GDPR)

You have the right to:
- Access your data (this export)
- Correct inaccurate data
- Request deletion ("right to be forgotten")
- Restrict or object to processing
- Data portability

Contact: privacy@levqor.ai
"""
        zf.writestr("README.txt", readme)
    
    # Get ZIP bytes
    zip_bytes = zip_buffer.getvalue()
    size_bytes = len(zip_bytes)
    
    return (zip_bytes, filename, size_bytes, json.dumps(data_categories))
