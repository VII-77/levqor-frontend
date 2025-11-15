"""
Daily Email Tasks
Scheduled endpoint for sending reminder and upsell emails
"""

from flask import Blueprint, request, jsonify
import logging
from datetime import datetime, timedelta

log = logging.getLogger("levqor.daily_tasks")

daily_tasks_bp = Blueprint('daily_tasks', __name__, url_prefix='/internal')


def verify_internal_secret(request):
    """Verify internal API secret"""
    import os
    expected_secret = os.environ.get('INTERNAL_API_SECRET', 'dev_secret')
    provided_secret = request.headers.get('X-Internal-Secret', '')
    return provided_secret == expected_secret


@daily_tasks_bp.route('/daily-email-tasks', methods=['POST'])
def run_daily_email_tasks():
    """
    Run daily email automation tasks
    
    Sends:
    - Intake reminders (48h after order, if not submitted)
    - Upsell emails (7d after delivery)
    
    Protected endpoint - requires internal secret
    
    Returns:
        200: {"ok": true, "reminders_sent": N, "upsells_sent": M}
        401: {"ok": false, "error": "unauthorized"}
    """
    if not verify_internal_secret(request):
        return jsonify({"ok": False, "error": "unauthorized"}), 401
    
    try:
        from app import db
        from backend.models.sales_models import DFYOrder
        from backend.services.onboarding_automation import (
            send_intake_reminder_email,
            send_upsell_email
        )
        
        reminders_sent = 0
        upsells_sent = 0
        
        # Find orders needing intake reminders (48+ hours old, status still NEW)
        cutoff_time = datetime.utcnow() - timedelta(hours=48)
        orders_needing_reminder = DFYOrder.query.filter(
            DFYOrder.status == 'NEW',
            DFYOrder.created_at < cutoff_time
        ).all()
        
        for order in orders_needing_reminder:
            try:
                if send_intake_reminder_email(order):
                    reminders_sent += 1
                    log.info(f"daily_tasks.reminder_sent order_id={order.id}")
            except Exception as e:
                log.error(f"daily_tasks.reminder_failed order_id={order.id} error={str(e)}")
        
        # Find orders needing upsells (7+ days after delivery, status DONE)
        upsell_cutoff = datetime.utcnow() - timedelta(days=7)
        orders_needing_upsell = DFYOrder.query.filter(
            DFYOrder.status == 'DONE',
            DFYOrder.updated_at < upsell_cutoff
        ).all()
        
        # Check if upsell already sent (using UpsellLog)
        from backend.models.sales_models import UpsellLog
        
        for order in orders_needing_upsell:
            # Skip if already sent
            existing_upsell = UpsellLog.query.filter_by(
                order_id=order.id,
                email_type='7_day_upsell'
            ).first()
            
            if existing_upsell:
                continue
            
            try:
                if send_upsell_email(order):
                    # Log that we sent it
                    upsell_log = UpsellLog(
                        order_id=order.id,
                        email_type='7_day_upsell',
                        status='SENT'
                    )
                    db.session.add(upsell_log)
                    db.session.commit()
                    
                    upsells_sent += 1
                    log.info(f"daily_tasks.upsell_sent order_id={order.id}")
            except Exception as e:
                log.error(f"daily_tasks.upsell_failed order_id={order.id} error={str(e)}")
        
        log.info(
            f"daily_tasks.complete "
            f"reminders={reminders_sent} upsells={upsells_sent}"
        )
        
        return jsonify({
            "ok": True,
            "reminders_sent": reminders_sent,
            "upsells_sent": upsells_sent
        }), 200
        
    except Exception as e:
        log.error(f"daily_tasks.error error={str(e)}", exc_info=True)
        return jsonify({"ok": False, "error": "Internal server error"}), 500


@daily_tasks_bp.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "ok": True,
        "service": "daily_email_tasks"
    }), 200
