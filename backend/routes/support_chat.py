"""
Support Chat API Routes
Public and private support endpoints
"""

from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger(__name__)

support_chat_bp = Blueprint("support_chat", __name__)


@support_chat_bp.route('/public', methods=['POST'])
def public_support():
    """
    Public support endpoint for website visitors
    
    POST /api/support/public
    Body: {
        "message": "What does Levqor do?",
        "conversationId": "optional-id"
    }
    
    Returns: {
        "reply": "...",
        "escalationSuggested": false,
        "conversationId": "..."
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Missing 'message' field"
            }), 400
        
        message = data.get('message', '').strip()
        conversation_id = data.get('conversationId')
        
        if not message:
            return jsonify({
                "error": "Message cannot be empty"
            }), 400
        
        # Call public AI
        from backend.services.support_ai import run_public_chat
        
        result = run_public_chat(message, conversation_id)
        
        logger.info(f"support_chat.public message_len={len(message)}")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"support_chat.public_error error={str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "reply": "Sorry, I'm having trouble right now. Please email support@levqor.ai",
            "escalationSuggested": True
        }), 500


@support_chat_bp.route('/private', methods=['POST'])
def private_support():
    """
    Private support endpoint for logged-in users
    
    POST /api/support/private
    Body: {
        "message": "What's the status of my order?",
        "email": "user@example.com",  // Required for now (TODO: use auth session)
        "conversationId": "optional-id"
    }
    
    Returns: {
        "reply": "...",
        "escalationSuggested": false,
        "conversationId": "...",
        "ticketId": "abc123"  // If escalated
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Missing 'message' field"
            }), 400
        
        message = data.get('message', '').strip()
        email = data.get('email', '').strip()
        conversation_id = data.get('conversationId')
        
        if not message:
            return jsonify({
                "error": "Message cannot be empty"
            }), 400
        
        # TODO: Get email from auth session instead of request body
        if not email:
            return jsonify({
                "error": "Missing 'email' field (auth not wired yet)"
            }), 400
        
        # Build user context
        from backend.utils.support_context import get_user_context
        user_context = get_user_context(email)
        
        # Call private AI
        from backend.services.support_ai import run_private_chat
        result = run_private_chat(user_context, message, conversation_id)
        
        logger.info(f"support_chat.private email={email} message_len={len(message)}")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"support_chat.private_error error={str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "reply": "Sorry, I'm having trouble accessing your account. Please email support@levqor.ai",
            "escalationSuggested": True
        }), 500


@support_chat_bp.route('/escalate', methods=['POST'])
def escalate_ticket():
    """
    Create support ticket and escalate to admin
    
    POST /api/support/escalate
    Body: {
        "email": "user@example.com",
        "message": "I need human help",
        "context": { ... }  // Optional
    }
    
    Returns: {
        "status": "ok",
        "ticketId": "abc123"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'message' not in data:
            return jsonify({
                "error": "Missing 'email' or 'message' field"
            }), 400
        
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        context = data.get('context', {})
        
        if not email or not message:
            return jsonify({
                "error": "Email and message cannot be empty"
            }), 400
        
        # Create ticket
        from backend.services.support_tickets import create_ticket
        ticket = create_ticket(email, message, context)
        
        if not ticket:
            return jsonify({
                "error": "Failed to create ticket"
            }), 500
        
        ticket_id = ticket.get('id')
        
        # Send Telegram notification
        from backend.utils.telegram_helper import send_telegram_notification
        
        telegram_message = f"""
🎫 <b>NEW SUPPORT TICKET</b>

Ticket ID: #{ticket_id}
From: {email}

Message:
{message[:200]}

<a href="https://api.levqor.ai/api/support/tickets">View all tickets</a>
        """.strip()
        
        send_telegram_notification(telegram_message)
        
        # Optional: Send WhatsApp (NO-OP if not configured)
        from backend.utils.whatsapp_helper import notify_new_ticket
        notify_new_ticket(email, message)
        
        logger.info(f"support_chat.escalated ticket_id={ticket_id} email={email}")
        
        return jsonify({
            "status": "ok",
            "ticketId": ticket_id,
            "message": "Support ticket created. Our team will respond within 24 hours."
        }), 200
        
    except Exception as e:
        logger.error(f"support_chat.escalate_error error={str(e)}", exc_info=True)
        return jsonify({
            "error": "Failed to create ticket"
        }), 500


@support_chat_bp.route('/tickets', methods=['GET'])
def list_tickets():
    """
    List support tickets (admin endpoint)
    
    GET /api/support/tickets?limit=50&status=open
    
    Headers: X-Internal-Secret (for now, basic protection)
    
    Returns: {
        "tickets": [...],
        "stats": {...}
    }
    """
    try:
        # Basic internal auth (reuse pattern from daily_tasks)
        import os
        internal_secret = request.headers.get('X-Internal-Secret')
        expected_secret = os.environ.get('INTERNAL_API_SECRET', 'levqor-internal-2025')
        
        if internal_secret != expected_secret:
            logger.warning("support_chat.tickets_unauthorized")
            return jsonify({
                "error": "Unauthorized"
            }), 401
        
        limit = int(request.args.get('limit', 50))
        status = request.args.get('status')  # 'open', 'closed', or None
        
        from backend.services.support_tickets import list_tickets, get_ticket_stats
        
        tickets = list_tickets(limit=limit, status=status)
        stats = get_ticket_stats()
        
        logger.info(f"support_chat.tickets_listed count={len(tickets)}")
        
        return jsonify({
            "tickets": tickets,
            "stats": stats,
            "count": len(tickets)
        }), 200
        
    except Exception as e:
        logger.error(f"support_chat.tickets_error error={str(e)}", exc_info=True)
        return jsonify({
            "error": "Failed to list tickets"
        }), 500


@support_chat_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    import os
    
    status = {
        "status": "ok",
        "openai_configured": bool(os.environ.get('OPENAI_API_KEY')),
        "telegram_configured": bool(os.environ.get('TELEGRAM_BOT_TOKEN')),
        "whatsapp_configured": bool(os.environ.get('WHATSAPP_API_URL'))
    }
    
    return jsonify(status), 200
