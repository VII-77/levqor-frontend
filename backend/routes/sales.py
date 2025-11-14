"""
Sales & Lead Management Routes
Handles lead capture and DFY kickoff forms
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import logging

sales_bp = Blueprint("sales", __name__)
logger = logging.getLogger(__name__)

# Email configuration
SALES_EMAIL = os.getenv("SALES_EMAIL", "sales@levqor.ai")
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "support@levqor.ai")


@sales_bp.route("/api/sales/lead", methods=["POST"])
def capture_lead():
    """
    Capture lead from contact/demo request forms
    
    Expected body:
    {
        "name": str,
        "email": str,
        "company": str (optional),
        "message": str (optional),
        "source": str (e.g., "landing_page", "pricing_page")
    }
    """
    try:
        data = request.json or {}
        
        # Validate required fields
        if not data.get("name") or not data.get("email"):
            return jsonify({"ok": False, "error": "Name and email are required"}), 400
        
        # Extract data
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        company = data.get("company", "").strip()
        message = data.get("message", "").strip()
        source = data.get("source", "unknown").strip()
        
        # Email validation (basic)
        if "@" not in email or "." not in email:
            return jsonify({"ok": False, "error": "Invalid email address"}), 400
        
        # Log the lead
        logger.info(f"New lead captured: {name} ({email}) from {source}")
        
        # TODO: Store in database (future enhancement)
        # For now, send notification email
        
        # Send notification to sales team
        try:
            send_lead_notification(name, email, company, message, source)
        except Exception as email_error:
            logger.error(f"Failed to send lead notification: {email_error}")
            # Continue anyway - we logged the lead
        
        return jsonify({
            "ok": True,
            "message": "Thank you! We'll be in touch within 24 hours."
        }), 200
        
    except Exception as e:
        logger.error(f"Lead capture error: {e}")
        return jsonify({"ok": False, "error": "Failed to submit. Please try again."}), 500


@sales_bp.route("/api/sales/dfy-kickoff", methods=["POST"])
def dfy_kickoff():
    """
    DFY Kickoff form submission
    
    Expected body:
    {
        "name": str,
        "email": str,
        "plan": str (e.g., "starter", "professional", "enterprise"),
        "workflow_description": str,
        "tools": str (comma-separated list),
        "preferred_date": str (optional),
        "additional_notes": str (optional)
    }
    """
    try:
        data = request.json or {}
        
        # Validate required fields
        required = ["name", "email", "plan", "workflow_description", "tools"]
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({"ok": False, "error": f"Missing fields: {', '.join(missing)}"}), 400
        
        # Extract data
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        plan = data.get("plan", "").strip()
        workflow_desc = data.get("workflow_description", "").strip()
        tools = data.get("tools", "").strip()
        preferred_date = data.get("preferred_date", "").strip()
        additional_notes = data.get("additional_notes", "").strip()
        
        # Email validation
        if "@" not in email or "." not in email:
            return jsonify({"ok": False, "error": "Invalid email address"}), 400
        
        # Log the kickoff
        logger.info(f"DFY kickoff submitted: {name} ({email}) - {plan} plan")
        
        # TODO: Store in database (future enhancement)
        
        # Send notification to delivery team
        try:
            send_dfy_kickoff_notification(
                name, email, plan, workflow_desc, tools, preferred_date, additional_notes
            )
        except Exception as email_error:
            logger.error(f"Failed to send DFY kickoff notification: {email_error}")
        
        return jsonify({
            "ok": True,
            "message": "Kickoff received! We'll schedule your call within 24 hours."
        }), 200
        
    except Exception as e:
        logger.error(f"DFY kickoff error: {e}")
        return jsonify({"ok": False, "error": "Failed to submit. Please try again."}), 500


def send_lead_notification(name, email, company, message, source):
    """
    Send email notification to sales team about new lead
    
    For now, just log. In production, integrate with Resend/SMTP.
    """
    email_subject = f"🔥 New Lead from {source}: {name}"
    email_body = f"""
New lead captured at {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}

Name: {name}
Email: {email}
Company: {company or "Not provided"}
Source: {source}

Message:
{message or "No message provided"}

---
Reply directly to {email} to follow up.
"""
    
    # Log the email (replace with actual email sending in production)
    logger.info(f"[EMAIL] To: {SALES_EMAIL}")
    logger.info(f"[EMAIL] Subject: {email_subject}")
    logger.info(f"[EMAIL] Body:\n{email_body}")
    
    # TODO: Integrate with Resend or existing email infrastructure
    # from backend.services.gdpr_emails import send_email
    # send_email(SALES_EMAIL, email_subject, email_body)


def send_dfy_kickoff_notification(name, email, plan, workflow_desc, tools, preferred_date, notes):
    """
    Send email notification to delivery team about DFY kickoff
    """
    email_subject = f"🚀 DFY Kickoff: {name} ({plan.capitalize()} Plan)"
    email_body = f"""
New DFY kickoff submitted at {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}

CLIENT DETAILS:
---------------
Name: {name}
Email: {email}
Plan: {plan.upper()}

WORKFLOW REQUIREMENTS:
----------------------
Description:
{workflow_desc}

Tools to integrate:
{tools}

Preferred kickoff date: {preferred_date or "ASAP"}

Additional notes:
{notes or "None"}

---
NEXT STEPS:
1. Reply to {email} within 24h to schedule kickoff call
2. Confirm scope and timeline
3. Begin build after kickoff call
4. Target delivery: 48h-7 days depending on plan

---
Auto-generated by Levqor Sales System
"""
    
    # Log the email (replace with actual email sending in production)
    logger.info(f"[EMAIL] To: {SUPPORT_EMAIL}")
    logger.info(f"[EMAIL] Subject: {email_subject}")
    logger.info(f"[EMAIL] Body:\n{email_body}")
    
    # TODO: Integrate with Resend or existing email infrastructure
