from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from backend.models.dsar_request import DSARRequest
from backend.utils.ids import generate_gdpr_reference

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
