from flask import Blueprint, request, jsonify, send_file
from datetime import datetime, timedelta, timezone
import os
from app import db
from backend.models.dsar_request import DSARRequest
from backend.utils.ids import generate_gdpr_reference
from backend.config import GDPR_DSAR_EXPORT_RETENTION_DAYS

dsar_bp = Blueprint("dsar", __name__, url_prefix="/api/dsar")

def _get_request_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()
    return request.remote_addr or "unknown"

@dsar_bp.route("/request", methods=["POST"])
def create_dsar_request():
    """
    Minimal DSAR request endpoint.

    Accepts:
      - Authenticated user (preferred), OR
      - JSON body with {"email": "..."} as a fallback.

    Creates a DSARRequest row with status='pending' and returns a GDPR reference ID.
    No export is generated here yet – that will be handled later.
    """
    data = request.get_json(silent=True) or {}

    email = data.get("email")
    user_id = None

    try:
        from flask_login import current_user
        if getattr(current_user, "is_authenticated", False):
            user_id = getattr(current_user, "id", None)
            if not email:
                email = getattr(current_user, "email", None)
    except Exception:
        pass

    if not email:
        return jsonify(
            {
                "ok": False,
                "error": "Email is required if you are not signed in.",
            }
        ), 400

    ref_id = generate_gdpr_reference()
    req_ip = _get_request_ip()

    dsar = DSARRequest(
        user_id=user_id,
        email=email,
        status="pending",
        requested_at=datetime.utcnow(),
        request_ip=req_ip,
        gdpr_reference_id=ref_id,
    )
    db.session.add(dsar)
    db.session.commit()

    return jsonify(
        {
            "ok": True,
            "gdpr_reference_id": ref_id,
            "status": "pending",
            "message": "Your data export request has been recorded. We will email you when it is ready.",
        }
    ), 202

@dsar_bp.route("/status/<ref_id>", methods=["GET"])
def get_dsar_status(ref_id: str):
    """
    Simple DSAR status check endpoint.
    Allows user to see if their request is pending/completed/errored.
    """
    dsar = DSARRequest.query.filter_by(gdpr_reference_id=ref_id).first()

    if not dsar:
        return jsonify({"ok": False, "error": "Request not found"}), 404

    return jsonify(
        {
            "ok": True,
            "gdpr_reference_id": dsar.gdpr_reference_id,
            "status": dsar.status,
            "requested_at": dsar.requested_at.isoformat() if dsar.requested_at else None,
            "completed_at": dsar.completed_at.isoformat() if dsar.completed_at else None,
            "export_bytes_size": dsar.export_bytes_size,
            "last_error": dsar.last_error,
        }
    ), 200


@dsar_bp.route("/download/<reference_id>", methods=["GET"])
def download_dsar(reference_id: str):
    """
    Authenticated users can download their completed DSAR ZIP.
    
    Security checks:
    - User must be authenticated (current_user check)
    - DSARRequest must exist
    - Must belong to current user (checked by email)
    - Status must be "completed"
    - Export file must exist on disk
    
    Returns:
    - 200: ZIP file stream
    - 401: Not authenticated
    - 403: Forbidden (not user's request)
    - 404: Request not found
    - 400: Export not ready
    - 500: File missing on disk
    """
    user_email = None
    
    try:
        from flask_login import current_user
        if getattr(current_user, "is_authenticated", False):
            user_email = getattr(current_user, "email", None)
    except Exception:
        pass

    if not user_email:
        return jsonify({
            "ok": False,
            "error": "Authentication required. Please sign in to download your data export."
        }), 401

    req = DSARRequest.query.filter_by(gdpr_reference_id=reference_id).first()
    if not req:
        return jsonify({"ok": False, "error": "DSAR request not found"}), 404

    if req.email != user_email:
        return jsonify({
            "ok": False,
            "error": "Forbidden: This request does not belong to you"
        }), 403

    if req.status != "completed":
        return jsonify({
            "ok": False,
            "error": f"Export not ready. Current status: {req.status}",
            "status": req.status,
            "message": "Your export is still being processed. Please check back later."
        }), 400

    export_root = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "backend", "exports", "dsar"
    )
    
    filename = f"levqor-dsar-{req.gdpr_reference_id}.zip"
    file_path = os.path.join(export_root, filename)

    if not os.path.isfile(file_path):
        retention_days = GDPR_DSAR_EXPORT_RETENTION_DAYS
        cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)

        ts = req.completed_at or req.requested_at
        if ts and ts.replace(tzinfo=timezone.utc) < cutoff:
            return jsonify({
                "ok": False,
                "error": "Export expired",
                "message": f"DSAR exports are automatically deleted after {retention_days} days for security purposes.",
                "retention_days": retention_days,
                "expired_on": (ts + timedelta(days=retention_days)).isoformat()
            }), 410

        return jsonify({
            "ok": False,
            "error": "Export file not found on server. Please contact support.",
            "reference_id": reference_id
        }), 500

    return send_file(
        file_path,
        mimetype="application/zip",
        as_attachment=True,
        download_name=filename
    )
