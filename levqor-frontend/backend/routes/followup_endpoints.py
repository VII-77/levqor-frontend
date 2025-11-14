"""
Followup and Upsell Support Endpoints
Used by automation scripts
"""

from flask import Blueprint, jsonify, request
from backend.models.sales_models import Lead, LeadActivity, DFYOrder, UpsellLog
from backend.utils.email_helper import send_email
from app import db
from datetime import datetime, timedelta
import logging

followup_bp = Blueprint("followup", __name__)
logger = logging.getLogger(__name__)


@followup_bp.route("/api/leads/followup-needed", methods=["GET"])
def get_leads_needing_followup():
    """Get leads that need followup emails"""
    cutoff = datetime.utcnow() - timedelta(hours=24)
    
    leads = Lead.query.filter(
        Lead.tags.contains("LM-OPTIN"),
        Lead.last_contact < cutoff
    ).all()
    
    return jsonify({
        "ok": True,
        "leads": [{
            "id": l.id,
            "email": l.email,
            "name": l.name,
            "last_contact": l.last_contact.isoformat(),
            "sent_email_1": check_sent(l.id, "followup_value"),
            "sent_email_2": check_sent(l.id, "followup_case_study"),
            "sent_email_3": check_sent(l.id, "followup_soft_pitch")
        } for l in leads]
    }), 200


@followup_bp.route("/api/leads/<int:lead_id>/send-followup", methods=["POST"])
def send_followup(lead_id):
    """Send followup email to lead"""
    try:
        data = request.json or {}
        email_type = data.get("email_type")
        
        if not email_type:
            return jsonify({"ok": False, "error": "email_type required"}), 400
        
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({"ok": False, "error": "Lead not found"}), 404
        
        send_email(email_type, lead.email, {'name': lead.name})
        
        activity = LeadActivity(
            lead_id=lead.id,
            activity_type="EMAIL_SENT",
            description=f"Sent {email_type}"
        )
        db.session.add(activity)
        
        lead.last_contact = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Followup email sent: {email_type} to {lead.email}")
        
        return jsonify({"ok": True}), 200
        
    except Exception as e:
        logger.error(f"Send followup error: {e}")
        return jsonify({"ok": False, "error": "Failed to send"}), 500


@followup_bp.route("/api/dfy/upsell-needed", methods=["GET"])
def get_orders_needing_upsell():
    """Get DFY orders that need upsell emails"""
    orders = DFYOrder.query.filter_by(tier="starter").all()
    
    return jsonify({
        "ok": True,
        "orders": [{
            "id": o.id,
            "customer_email": o.customer_email,
            "tier": o.tier,
            "created_at": o.created_at.isoformat(),
            "sent_welcome": check_upsell_sent(o.id, "dfy_welcome"),
            "sent_upsell_2": check_upsell_sent(o.id, "dfy_upsell_12h"),
            "sent_upsell_3": check_upsell_sent(o.id, "dfy_upsell_36h")
        } for o in orders]
    }), 200


@followup_bp.route("/api/dfy/<int:order_id>/send-upsell", methods=["POST"])
def send_upsell(order_id):
    """Send upsell email for DFY order"""
    try:
        data = request.json or {}
        email_type = data.get("email_type")
        
        if not email_type:
            return jsonify({"ok": False, "error": "email_type required"}), 400
        
        order = DFYOrder.query.get(order_id)
        
        if not order:
            return jsonify({"ok": False, "error": "Order not found"}), 404
        
        send_email(email_type, order.customer_email, {
            'name': order.customer_id,
            'tier': order.tier
        })
        
        upsell_log = UpsellLog(
            order_id=order.id,
            email_type=email_type
        )
        db.session.add(upsell_log)
        db.session.commit()
        
        logger.info(f"Upsell email sent: {email_type} for order {order_id}")
        
        return jsonify({"ok": True}), 200
        
    except Exception as e:
        logger.error(f"Send upsell error: {e}")
        return jsonify({"ok": False, "error": "Failed to send"}), 500


def check_sent(lead_id, email_type):
    """Check if email type was sent to lead"""
    activity = LeadActivity.query.filter_by(
        lead_id=lead_id,
        activity_type="EMAIL_SENT"
    ).filter(
        LeadActivity.description.contains(email_type)
    ).first()
    
    return activity is not None


def check_upsell_sent(order_id, email_type):
    """Check if upsell email was sent"""
    log = UpsellLog.query.filter_by(
        order_id=order_id,
        email_type=email_type
    ).first()
    
    return log is not None
