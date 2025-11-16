"""
Support AI Engine
OpenAI-powered support chatbot with public and private modes
"""

import os
import logging
import json
from backend.utils.error_logger import log_exception

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Check if OpenAI is available (using new client API v1.x)
OPENAI_AVAILABLE = False
openai_client = None

try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    OPENAI_AVAILABLE = bool(OPENAI_API_KEY)
    logger.info("support_ai.openai_initialized using client v1.x API")
except ImportError:
    logger.warning("support_ai.openai_not_installed")


def run_public_chat(message, conversation_id=None):
    """
    Run public support chat (website visitors)
    Uses only FAQ/public knowledge base
    
    Args:
        message: User message
        conversation_id: Optional conversation ID for context
    
    Returns:
        dict: {
            "reply": str,
            "escalationSuggested": bool,
            "conversationId": str
        }
    """
    if not OPENAI_AVAILABLE:
        return {
            "reply": "I'm currently unavailable. Please email support@levqor.ai for assistance.",
            "escalationSuggested": True,
            "conversationId": conversation_id or "n/a"
        }
    
    try:
        from backend.services.support_faq_loader import get_public_faq_summary
        
        faq_content = get_public_faq_summary()
        
        system_prompt = f"""You are Levqor's public support assistant. 

Help website visitors with basic questions using ONLY the FAQ/knowledge base below. 

Be concise (max 3 sentences), friendly, and helpful. If you cannot answer from the FAQ, suggest they contact support@levqor.ai or create a support ticket.

If the user seems frustrated, angry, or explicitly asks for human help, set escalationSuggested to true.

Knowledge Base:
{faq_content}

Response format: JSON with keys "reply" (string) and "escalationSuggested" (boolean)"""

        if not openai_client:
            raise Exception("OpenAI client not available")
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Cost-efficient model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        reply_text = response.choices[0].message.content.strip()
        
        # Try to parse JSON response
        try:
            result = json.loads(reply_text)
            reply = result.get("reply", reply_text)
            escalation = result.get("escalationSuggested", False)
        except:
            # If not JSON, treat as plain text
            reply = reply_text
            escalation = _detect_escalation_keywords(message)
        
        logger.info(f"support_ai.public_chat conversation_id={conversation_id}")
        
        return {
            "reply": reply,
            "escalationSuggested": escalation,
            "conversationId": conversation_id or "public-" + os.urandom(4).hex()
        }
        
    except Exception as e:
        logger.error(f"support_ai.public_error error={str(e)}", exc_info=True)
        log_exception(
            source="backend",
            service="support_ai_public",
            exc=e,
            severity="error",
            path_or_screen="/api/support/public"
        )
        return {
            "reply": "I'm having trouble right now. Please email support@levqor.ai",
            "escalationSuggested": True,
            "conversationId": conversation_id or "error"
        }


def run_private_chat(user_context, message, conversation_id=None):
    """
    Run private support chat (logged-in users)
    Uses full knowledge base + user account context
    
    Args:
        user_context: Dict with user's orders, tickets, account info
        message: User message
        conversation_id: Optional conversation ID
    
    Returns:
        dict: {
            "reply": str,
            "escalationSuggested": bool,
            "conversationId": str,
            "ticketId": str (if escalated)
        }
    """
    if not OPENAI_AVAILABLE:
        return {
            "reply": "Support AI is currently unavailable. Please email support@levqor.ai",
            "escalationSuggested": True,
            "conversationId": conversation_id or "n/a"
        }
    
    try:
        from backend.services.support_faq_loader import load_support_corpus
        
        corpus = load_support_corpus()
        
        system_prompt = f"""You are Levqor's private support assistant for logged-in customers.

You have access to the user's account context below. Use it to answer questions about their orders, status, delivery, etc.

Be helpful, concise (max 4 sentences), and specific to their situation. If you cannot resolve the issue, set escalationSuggested to true.

User Context:
{json.dumps(user_context, indent=2)}

Knowledge Base:
FAQ: {corpus.get('faq', 'N/A')[:500]}
Pricing: {corpus.get('pricing', 'N/A')[:500]}
Policies: {corpus.get('policies', 'N/A')[:500]}

Response format: JSON with keys "reply" (string) and "escalationSuggested" (boolean)"""

        if not openai_client:
            raise Exception("OpenAI client not available")
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        reply_text = response.choices[0].message.content.strip()
        
        # Try to parse JSON response
        try:
            result = json.loads(reply_text)
            reply = result.get("reply", reply_text)
            escalation = result.get("escalationSuggested", False)
        except:
            reply = reply_text
            escalation = _detect_escalation_keywords(message)
        
        email = user_context.get("email", "unknown")
        logger.info(f"support_ai.private_chat email={email} conversation_id={conversation_id}")
        
        result = {
            "reply": reply,
            "escalationSuggested": escalation,
            "conversationId": conversation_id or "private-" + os.urandom(4).hex()
        }
        
        # Auto-create ticket if escalation suggested
        if escalation:
            from backend.services.support_tickets import create_ticket
            
            ticket = create_ticket(
                email=email,
                message=message,
                context={"ai_suggested_escalation": True}
            )
            
            if ticket:
                result["ticketId"] = ticket.get("id")
        
        return result
        
    except Exception as e:
        logger.error(f"support_ai.private_error error={str(e)}", exc_info=True)
        log_exception(
            source="backend",
            service="support_ai_private",
            exc=e,
            severity="error",
            user_email=user_context.get("email") if user_context else None,
            path_or_screen="/api/support/private"
        )
        return {
            "reply": "I'm having trouble accessing your account info. Please email support@levqor.ai",
            "escalationSuggested": True,
            "conversationId": conversation_id or "error"
        }


def _detect_escalation_keywords(message):
    """Detect if message suggests need for human escalation"""
    message_lower = message.lower()
    
    escalation_keywords = [
        "speak to human",
        "talk to person",
        "real person",
        "escalate",
        "manager",
        "urgent",
        "emergency",
        "not working",
        "broken",
        "angry",
        "disappointed",
        "refund now",
        "cancel immediately"
    ]
    
    return any(keyword in message_lower for keyword in escalation_keywords)
