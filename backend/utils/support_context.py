"""
Support Context Builder
Gathers user context for private support conversations
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def get_user_context(email):
    """
    Build user context for support AI
    
    Args:
        email: User email address
    
    Returns:
        dict: User context with orders, tickets, account info
    """
    try:
        from app import db
        from backend.models.sales_models import DFYOrder
        
        context = {
            "email": email,
            "orders": [],
            "tickets": [],
            "account_age_days": 0,
            "last_activity": None
        }
        
        # Get DFY orders
        orders = DFYOrder.query.filter_by(customer_email=email).all()
        
        for order in orders:
            context["orders"].append({
                "id": order.id,
                "tier": order.tier,
                "status": order.status,
                "created_at": order.created_at.isoformat() if order.created_at else None,
                "updated_at": order.updated_at.isoformat() if order.updated_at else None,
                "deadline": order.deadline.isoformat() if order.deadline else None,
                "revisions_left": order.revisions_left,
                "files_url": order.files_url
            })
        
        # Calculate account age
        if orders:
            oldest_order = min(orders, key=lambda o: o.created_at)
            account_age = datetime.utcnow() - oldest_order.created_at
            context["account_age_days"] = account_age.days
            context["last_activity"] = orders[-1].updated_at.isoformat()
        
        # Get support tickets (if ticket model exists)
        try:
            tickets = _get_tickets_for_email(email)
            context["tickets"] = tickets
        except Exception:
            # Tickets table might not exist yet
            pass
        
        logger.info(f"support_context.built email={email} orders={len(context['orders'])}")
        return context
        
    except Exception as e:
        logger.error(f"support_context.error email={email} error={str(e)}", exc_info=True)
        return {
            "email": email,
            "orders": [],
            "tickets": [],
            "error": "Unable to load full context"
        }


def _get_tickets_for_email(email):
    """Load support tickets for email (helper function)"""
    import json
    import os
    
    tickets_file = 'data/support_tickets.json'
    
    if not os.path.exists(tickets_file):
        return []
    
    try:
        with open(tickets_file, 'r') as f:
            all_tickets = json.load(f)
        
        user_tickets = [
            t for t in all_tickets 
            if t.get('email') == email
        ]
        
        # Return last 5 tickets with basic info
        return [
            {
                "id": t.get("id"),
                "message": t.get("message", "")[:100],
                "status": t.get("status", "unknown"),
                "created_at": t.get("created_at")
            }
            for t in user_tickets[-5:]
        ]
        
    except Exception as e:
        logger.warning(f"support_context.tickets_error error={str(e)}")
        return []
