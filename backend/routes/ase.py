"""
ASE (Automated Sales Engine) Routes
Lead magnet, sales page, lead scoring
"""

from flask import Blueprint, request, jsonify
from backend.models.sales_models import Lead, LeadActivity
from backend.utils.email_helper import send_email
from app import db
import logging
from datetime import datetime

ase_bp = Blueprint("ase", __name__)
logger = logging.getLogger(__name__)


@ase_bp.route("/api/lead-magnet", methods=["POST"])
def lead_magnet():
    """
    Lead magnet form submission
    
    Body:
        name, email, business_type, problem, phone (optional)
    """
    try:
        data = request.json or {}
        
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        business_type = data.get("business_type", "").strip()
        problem = data.get("problem", "").strip()
        phone = data.get("phone", "").strip()
        
        if not name or not email:
            return jsonify({"ok": False, "error": "Name and email required"}), 400
        
        existing = Lead.query.filter_by(email=email).first()
        if existing:
            existing.tags = "LM-OPTIN" if "LM-OPTIN" not in existing.tags else existing.tags
            existing.updated_at = datetime.utcnow()
            existing.last_contact = datetime.utcnow()
            db.session.commit()
            lead = existing
        else:
            lead = Lead(
                name=name,
                email=email,
                phone=phone,
                business_type=business_type,
                problem=problem,
                tags="LM-OPTIN"
            )
            db.session.add(lead)
            db.session.commit()
        
        score = calculate_lead_score(lead)
        lead.score = score
        db.session.commit()
        
        activity = LeadActivity(
            lead_id=lead.id,
            activity_type="LEAD_MAGNET_OPTIN",
            description=f"Downloaded lead magnet. Score: {score}"
        )
        db.session.add(activity)
        db.session.commit()
        
        send_email('lead_magnet_welcome', email, {'name': name})
        
        logger.info(f"Lead magnet optin: {email} (score: {score})")
        
        return jsonify({
            "ok": True,
            "message": "Thanks! Check your email for the guide."
        }), 200
        
    except Exception as e:
        logger.error(f"Lead magnet error: {e}")
        return jsonify({"ok": False, "error": "Failed to submit"}), 500


def calculate_lead_score(lead):
    """
    Calculate lead score (0-100)
    
    Rules:
    - Provided phone: +20
    - DFY interest keyword: +30
    - Business type (Agency/E-comm): +25
    - Completed form fully: +10
    """
    score = 0
    
    if lead.phone:
        score += 20
    
    if lead.problem:
        problem_lower = lead.problem.lower()
        dfy_keywords = ['automate', 'build', 'setup', 'done for', 'dfy', 'integration']
        if any(kw in problem_lower for kw in dfy_keywords):
            score += 30
    
    if lead.business_type:
        business_lower = lead.business_type.lower()
        if 'agency' in business_lower or 'ecommerce' in business_lower or 'e-commerce' in business_lower:
            score += 25
    
    if lead.name and lead.email and lead.business_type and lead.problem:
        score += 10
    
    return min(score, 100)


@ase_bp.route("/api/leads/<int:lead_id>/score", methods=["GET"])
def get_lead_score(lead_id):
    """Get lead score"""
    lead = Lead.query.get(lead_id)
    if not lead:
        return jsonify({"ok": False, "error": "Lead not found"}), 404
    
    return jsonify({
        "ok": True,
        "lead_id": lead.id,
        "email": lead.email,
        "score": lead.score
    }), 200
