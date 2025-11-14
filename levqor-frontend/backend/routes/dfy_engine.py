"""
DFY Engine Routes
DFY orders, revisions, delivery
"""

from flask import Blueprint, request, jsonify, send_file
from backend.models.sales_models import DFYOrder, DFYActivity, UpsellLog
from backend.utils.email_helper import send_email
from backend.utils.storage_helper import save_file, list_files
from app import db
import logging
from datetime import datetime, timedelta
import os

dfy_engine_bp = Blueprint("dfy_engine", __name__)
logger = logging.getLogger(__name__)


@dfy_engine_bp.route("/api/dfy/orders", methods=["GET"])
def get_orders():
    """Get DFY orders for logged-in user"""
    customer_email = request.args.get("email")
    
    if not customer_email:
        return jsonify({"ok": False, "error": "Email required"}), 400
    
    orders = DFYOrder.query.filter_by(customer_email=customer_email).all()
    
    return jsonify({
        "ok": True,
        "orders": [{
            "id": o.id,
            "tier": o.tier,
            "status": o.status,
            "deadline": o.deadline.isoformat() if o.deadline else None,
            "revisions_left": o.revisions_left,
            "files_url": o.files_url,
            "final_package_url": o.final_package_url,
            "created_at": o.created_at.isoformat()
        } for o in orders]
    }), 200


@dfy_engine_bp.route("/api/dfy/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """Get specific DFY order"""
    order = DFYOrder.query.get(order_id)
    
    if not order:
        return jsonify({"ok": False, "error": "Order not found"}), 404
    
    files = list_files(order_id)
    
    return jsonify({
        "ok": True,
        "order": {
            "id": order.id,
            "tier": order.tier,
            "status": order.status,
            "deadline": order.deadline.isoformat() if order.deadline else None,
            "revisions_left": order.revisions_left,
            "files": files,
            "final_package_url": order.final_package_url,
            "created_at": order.created_at.isoformat()
        }
    }), 200


@dfy_engine_bp.route("/api/dfy/revision", methods=["POST"])
def request_revision():
    """
    Request revision for DFY order
    
    Body:
        order_id, description
    """
    try:
        data = request.json or {}
        
        order_id = data.get("order_id")
        description = data.get("description", "").strip()
        
        if not order_id:
            return jsonify({"ok": False, "error": "Order ID required"}), 400
        
        order = DFYOrder.query.get(order_id)
        
        if not order:
            return jsonify({"ok": False, "error": "Order not found"}), 404
        
        if order.revisions_left <= 0:
            return jsonify({"ok": False, "error": "No revisions remaining"}), 400
        
        order.revisions_left -= 1
        order.status = "REVISION"
        order.updated_at = datetime.utcnow()
        db.session.commit()
        
        activity = DFYActivity(
            order_id=order.id,
            activity_type="REVISION_REQUESTED",
            description=description
        )
        db.session.add(activity)
        db.session.commit()
        
        logger.info(f"Revision requested for order {order_id}. Revisions left: {order.revisions_left}")
        
        return jsonify({
            "ok": True,
            "message": "Revision requested",
            "revisions_left": order.revisions_left
        }), 200
        
    except Exception as e:
        logger.error(f"Revision request error: {e}")
        return jsonify({"ok": False, "error": "Failed to request revision"}), 500


@dfy_engine_bp.route("/api/dfy/upload", methods=["POST"])
def upload_file():
    """
    Upload file for DFY order (internal use)
    
    Body:
        order_id, filename, file_data (base64)
    """
    try:
        data = request.json or {}
        
        order_id = data.get("order_id")
        filename = data.get("filename")
        file_data_b64 = data.get("file_data")
        
        if not all([order_id, filename, file_data_b64]):
            return jsonify({"ok": False, "error": "Missing fields"}), 400
        
        order = DFYOrder.query.get(order_id)
        
        if not order:
            return jsonify({"ok": False, "error": "Order not found"}), 404
        
        import base64
        file_data = base64.b64decode(file_data_b64)
        
        file_url = save_file(order_id, file_data, filename)
        
        order.files_url = file_url
        order.updated_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"File uploaded for order {order_id}: {filename}")
        
        return jsonify({
            "ok": True,
            "file_url": file_url
        }), 200
        
    except Exception as e:
        logger.error(f"File upload error: {e}")
        return jsonify({"ok": False, "error": "Upload failed"}), 500


@dfy_engine_bp.route("/api/dfy/complete", methods=["POST"])
def complete_order():
    """
    Mark DFY order as complete
    
    Body:
        order_id, checklist (dict with tested, error_free, naming, docs)
    """
    try:
        data = request.json or {}
        
        order_id = data.get("order_id")
        checklist = data.get("checklist", {})
        
        if not order_id:
            return jsonify({"ok": False, "error": "Order ID required"}), 400
        
        order = DFYOrder.query.get(order_id)
        
        if not order:
            return jsonify({"ok": False, "error": "Order not found"}), 404
        
        required_checks = ['tested', 'error_free', 'naming', 'docs']
        if not all(checklist.get(k) for k in required_checks):
            return jsonify({"ok": False, "error": "QA checklist incomplete"}), 400
        
        order.status = "COMPLETE"
        order.checklist_status = "PASS"
        order.updated_at = datetime.utcnow()
        
        package_url = f"/storage/dfy/{order_id}/final-package.zip"
        order.final_package_url = package_url
        
        db.session.commit()
        
        tier_support_days = {
            'starter': 7,
            'professional': 30,
            'enterprise': 30
        }
        support_days = tier_support_days.get(order.tier.lower(), 7)
        
        send_email('dfy_delivery', order.customer_email, {
            'name': order.customer_id,
            'package_url': package_url,
            'support_days': support_days
        })
        
        activity = DFYActivity(
            order_id=order.id,
            activity_type="ORDER_COMPLETED",
            description="Order marked complete, delivery email sent"
        )
        db.session.add(activity)
        db.session.commit()
        
        logger.info(f"Order {order_id} marked complete")
        
        return jsonify({
            "ok": True,
            "message": "Order completed",
            "package_url": package_url
        }), 200
        
    except Exception as e:
        logger.error(f"Complete order error: {e}")
        return jsonify({"ok": False, "error": "Failed to complete order"}), 500
