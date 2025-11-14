"""
DSAR ZIP Export Generator
Produces ZIP files containing all user data in JSON format.
Updates DSARRequest metadata after successful generation.
"""

import io
import json
import os
import zipfile
from datetime import datetime, timezone

from app import db
from backend.models.dsar_request import DSARRequest
from backend.services.dsar_collectors import collect_all_user_data
from run import get_db


EXPORT_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports", "dsar")


def _ensure_export_dir():
    """Create export directory if it doesn't exist"""
    os.makedirs(EXPORT_ROOT, exist_ok=True)


def _safe_iso(dt):
    """Convert datetime to ISO format safely"""
    if not dt:
        return None
    try:
        return dt.astimezone(timezone.utc).isoformat()
    except Exception:
        return dt.isoformat()


def build_dsar_zip_bytes(user_id: str, reference_id: str) -> tuple[bytes, dict]:
    """
    Collects user data via DSAR collectors and builds an in-memory ZIP.
    Returns (zip_bytes, meta_dict).
    Does not touch the database.
    """
    sqlite_conn = get_db()
    collected = collect_all_user_data(user_id, reference_id, sqlite_conn)

    now = datetime.now(timezone.utc)
    timestamp_str = now.strftime("%Y%m%d-%H%M%S")
    root_folder = f"levqor-dsar-{reference_id or user_id}-{timestamp_str}"

    meta = {
        "schema_version": "2025-11-DSAR-01",
        "generated_at": _safe_iso(now),
        "reference_id": reference_id,
        "user_id": user_id,
        "sections": list(collected.keys()),
        "notes": [
            "This export is provided under GDPR / UK GDPR data access rights.",
            "Fields may be redacted or omitted where legally required.",
            "API keys show prefixes only for security.",
        ],
    }

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            f"{root_folder}/meta.json",
            json.dumps(meta, indent=2, ensure_ascii=False),
        )

        zf.writestr(
            f"{root_folder}/account.json",
            json.dumps(collected.get("account"), indent=2, ensure_ascii=False),
        )

        zf.writestr(
            f"{root_folder}/referrals.json",
            json.dumps(collected.get("referrals"), indent=2, ensure_ascii=False),
        )

        zf.writestr(
            f"{root_folder}/developer_keys.json",
            json.dumps(collected.get("developer_keys"), indent=2, ensure_ascii=False),
        )

        zf.writestr(
            f"{root_folder}/api_usage.json",
            json.dumps(collected.get("api_usage"), indent=2, ensure_ascii=False),
        )

        zf.writestr(
            f"{root_folder}/partnerships.json",
            json.dumps(collected.get("partnerships"), indent=2, ensure_ascii=False),
        )

        zf.writestr(
            f"{root_folder}/marketplace_orders.json",
            json.dumps(collected.get("marketplace_orders"), indent=2, ensure_ascii=False),
        )

        zf.writestr(
            f"{root_folder}/marketing_consent.json",
            json.dumps(collected.get("marketing_consent"), indent=2, ensure_ascii=False),
        )

        zf.writestr(
            f"{root_folder}/risk_blocks.json",
            json.dumps(collected.get("risk_blocks"), indent=2, ensure_ascii=False),
        )

        zf.writestr(
            f"{root_folder}/billing_events.json",
            json.dumps(collected.get("billing_events"), indent=2, ensure_ascii=False),
        )

        zf.writestr(
            f"{root_folder}/dsar_request.json",
            json.dumps(collected.get("dsar_request"), indent=2, ensure_ascii=False),
        )

    buf.seek(0)
    data = buf.read()
    size_bytes = len(data)

    meta["zip_bytes"] = size_bytes

    return data, meta


def persist_dsar_export(reference_id: str) -> dict:
    """
    High-level helper used by workers / admin tasks.

    - Looks up DSARRequest by gdpr_reference_id
    - Builds ZIP with all user data
    - Saves file to disk under exports/dsar
    - Updates DSARRequest fields: completed_at, export_bytes_size, last_error
    - Returns dict with status + file_path + meta
    """
    _ensure_export_dir()

    req = DSARRequest.query.filter_by(gdpr_reference_id=reference_id).first()
    if not req:
        return {
            "ok": False,
            "error": f"DSARRequest not found for reference_id={reference_id}",
        }

    if not req.email:
        return {
            "ok": False,
            "error": "DSARRequest has no associated email",
        }
    
    # Look up actual user_id from SQLite users table using email
    sqlite_conn = get_db()
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (req.email,))
    user_row = cursor.fetchone()
    
    if not user_row:
        return {
            "ok": False,
            "error": f"No user found with email {req.email}",
        }
    
    actual_user_id = user_row[0]

    try:
        zip_bytes, meta = build_dsar_zip_bytes(actual_user_id, req.gdpr_reference_id)

        filename = f"levqor-dsar-{req.gdpr_reference_id}.zip"
        file_path = os.path.join(EXPORT_ROOT, filename)

        with open(file_path, "wb") as f:
            f.write(zip_bytes)

        size_bytes = len(zip_bytes)
        now = datetime.now(timezone.utc)

        req.export_bytes_size = size_bytes
        req.completed_at = now
        req.last_error = None
        req.status = "completed"

        db.session.add(req)
        db.session.commit()

        return {
            "ok": True,
            "file_path": file_path,
            "bytes": size_bytes,
            "reference_id": req.gdpr_reference_id,
            "meta": meta,
        }

    except Exception as e:
        req.last_error = str(e)
        req.status = "failed"
        db.session.add(req)
        db.session.commit()

        return {
            "ok": False,
            "error": f"DSAR export failed: {e}",
            "reference_id": reference_id,
        }
