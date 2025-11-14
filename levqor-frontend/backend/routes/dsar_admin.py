from flask import Blueprint, jsonify
from app import db
from backend.models.dsar_request import DSARRequest

dsar_admin_bp = Blueprint("dsar_admin", __name__, url_prefix="/api/admin/dsar")

@dsar_admin_bp.route("/list", methods=["GET"])
def list_dsar_requests():
    """
    ADMIN USE ONLY.
    Lists all DSAR requests with full metadata.
    No authentication added yet — will be added in a later step.
    """
    items = (
        DSARRequest.query
        .order_by(DSARRequest.requested_at.desc())
        .all()
    )

    return jsonify({
        "ok": True,
        "count": len(items),
        "requests": [
            {
                "gdpr_reference_id": x.gdpr_reference_id,
                "email": x.email,
                "user_id": x.user_id,
                "status": x.status,
                "requested_at": x.requested_at.isoformat() if x.requested_at else None,
                "completed_at": x.completed_at.isoformat() if x.completed_at else None,
                "export_bytes_size": x.export_bytes_size,
                "last_error": x.last_error,
                "request_ip": x.request_ip,
            }
            for x in items
        ]
    }), 200
