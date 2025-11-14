"""
High-Risk Data Firewall
GDPR/ICO compliance for automated decision-making prevention
Blocks workflows containing medical, legal, or financial content
"""

import logging
from typing import Dict, List, Tuple

log = logging.getLogger("levqor")

# Blocked terms for high-risk categories
BLOCKED_TERMS = [
    # Medical
    "medical", "diagnosis", "diagnose", "treatment", "symptom", "symptoms",
    "prescription", "medication", "disease", "illness", "health condition",
    "patient", "doctor", "physician", "therapy", "medical advice",
    "clinical", "healthcare", "medical record", "medical data",
    
    # Legal
    "legal advice", "lawsuit", "litigation", "attorney", "lawyer",
    "contract drafting", "legal document", "legal opinion", "legal case",
    "court", "judicial", "legal representation", "legal consultation",
    "terms and conditions drafting", "legal rights", "sue", "suing",
    
    # Financial
    "tax advice", "financial advice", "investment advice", "trading signals",
    "credit score", "credit rating", "loan approval", "lending decision",
    "investment recommendation", "stock picks", "portfolio management",
    "financial planning advice", "tax return preparation", "tax filing",
    "credit decision", "underwriting", "financial assessment"
]


def contains_high_risk_content(text: str) -> Tuple[bool, List[str]]:
    """
    Check if text contains high-risk medical, legal, or financial terms
    
    Returns:
        (is_blocked, matched_terms)
    """
    if not text:
        return False, []
    
    text_lower = text.lower()
    matched = []
    
    for term in BLOCKED_TERMS:
        if term in text_lower:
            matched.append(term)
    
    return len(matched) > 0, matched


def validate_workflow_content(data: Dict) -> Tuple[bool, str, List[str]]:
    """
    Validate workflow data for high-risk content
    
    Returns:
        (is_valid, error_message, blocked_terms)
    """
    # Check all text fields
    fields_to_check = []
    
    # Common workflow fields
    if "workflow" in data:
        fields_to_check.append(data["workflow"])
    if "description" in data:
        fields_to_check.append(data["description"])
    if "name" in data:
        fields_to_check.append(data["name"])
    if "title" in data:
        fields_to_check.append(data["title"])
    if "steps" in data:
        fields_to_check.append(str(data["steps"]))
    if "config" in data:
        fields_to_check.append(str(data["config"]))
    if "prompt" in data:
        fields_to_check.append(data["prompt"])
    if "task_description" in data:
        fields_to_check.append(data["task_description"])
    if "payload" in data:
        fields_to_check.append(str(data["payload"]))
    
    # Check all fields
    all_blocked_terms = []
    for field_value in fields_to_check:
        is_blocked, terms = contains_high_risk_content(str(field_value))
        if is_blocked:
            all_blocked_terms.extend(terms)
    
    if all_blocked_terms:
        # Remove duplicates
        all_blocked_terms = list(set(all_blocked_terms))
        
        error_msg = (
            "This workflow cannot be created because it contains restricted "
            "medical, legal, or financial content. Levqor does not automate "
            "workflows involving regulated decisions."
        )
        
        return False, error_msg, all_blocked_terms
    
    return True, "", []


def log_high_risk_block(db_connection, user_id: str, blocked_terms: List[str], 
                        payload_snippet: str, ip_address: str = ""):
    """
    Log a blocked high-risk workflow attempt
    
    Args:
        db_connection: SQLite database connection
        user_id: User ID who attempted the workflow
        blocked_terms: List of matched blocked terms
        payload_snippet: Sanitized snippet (max 200 chars)
        ip_address: IP address of requester
    """
    from time import time
    from uuid import uuid4
    import json
    
    try:
        # Sanitize snippet - max 200 chars, remove sensitive data
        snippet = payload_snippet[:200] if payload_snippet else ""
        
        cursor = db_connection.cursor()
        cursor.execute("""
            INSERT INTO risk_blocks 
            (id, user_id, blocked_terms, payload_snippet, ip_address, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            str(uuid4()),
            user_id,
            json.dumps(blocked_terms),
            snippet,
            ip_address,
            time()
        ))
        
        db_connection.commit()
        
        log.warning(
            f"[RISK_BLOCK] User {user_id} blocked - terms: {', '.join(blocked_terms[:3])}"
        )
        
    except Exception as e:
        log.error(f"Failed to log risk block: {e}")


def check_user_block_rate(db_connection, user_id: str, hours: int = 24) -> int:
    """
    Check how many times a user has been blocked in the last N hours
    
    Args:
        db_connection: SQLite database connection
        user_id: User ID to check
        hours: Time window in hours
        
    Returns:
        Number of blocks in time window
    """
    from time import time
    
    try:
        cursor = db_connection.cursor()
        cutoff = time() - (hours * 60 * 60)
        
        cursor.execute("""
            SELECT COUNT(*) FROM risk_blocks 
            WHERE user_id = ? AND created_at > ?
        """, (user_id, cutoff))
        
        result = cursor.fetchone()
        return result[0] if result else 0
        
    except Exception as e:
        log.error(f"Failed to check block rate: {e}")
        return 0
