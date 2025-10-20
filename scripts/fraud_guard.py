#!/usr/bin/env python3
"""
Phase 54: Fraud/Risk Guard
Simple velocity limits and risk detection
"""
import os
import sys
import json
import time
from datetime import datetime, timedelta

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configuration from environment
BLOCK_PREPAID = os.getenv('GUARD_BLOCK_PREPAID', '0') == '1'
MAX_PER_HOUR = int(os.getenv('GUARD_MAX_PER_HOUR', '5'))
MAX_AMOUNT_PER_DAY = float(os.getenv('GUARD_MAX_AMOUNT_DAY', '10000'))

# Email allowlist
ALLOW_EMAILS = set([
    x.strip().lower() 
    for x in os.getenv('GUARD_EMAIL_ALLOW', '').split(',') 
    if x.strip()
])

def evaluate_payment(email, card_type, amount, recent_count=0, daily_total=0):
    """
    Evaluate payment for fraud risk
    
    Args:
        email: Customer email
        card_type: Card type (credit, debit, prepaid, etc)
        amount: Payment amount
        recent_count: Number of payments from this card in last hour
        daily_total: Total amount from this email today
    
    Returns:
        dict with ok, decision, reason
    """
    email_lower = email.lower()
    
    # Allowlist check
    if email_lower in ALLOW_EMAILS:
        return {
            "ok": True,
            "decision": "allow",
            "reason": "allowlisted"
        }
    
    # Prepaid card block
    if BLOCK_PREPAID and card_type.lower() == 'prepaid':
        return {
            "ok": False,
            "decision": "block",
            "reason": "prepaid_card_blocked"
        }
    
    # Velocity check (payments per hour)
    if recent_count > MAX_PER_HOUR:
        return {
            "ok": False,
            "decision": "block",
            "reason": f"velocity_exceeded_{recent_count}_per_hour"
        }
    
    # Daily amount limit
    if daily_total + amount > MAX_AMOUNT_PER_DAY:
        return {
            "ok": False,
            "decision": "block",
            "reason": f"daily_limit_exceeded_{daily_total + amount:.2f}"
        }
    
    # Suspicious amount patterns
    if amount > 5000:
        return {
            "ok": True,
            "decision": "review",
            "reason": "high_amount_requires_review"
        }
    
    # All checks passed
    return {
        "ok": True,
        "decision": "allow",
        "reason": "all_checks_passed"
    }

def log_fraud_check(email, decision, reason):
    """Log fraud check for audit trail"""
    log_entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "event": "fraud_check",
        "email": email,
        "decision": decision,
        "reason": reason
    }
    
    os.makedirs('logs', exist_ok=True)
    with open('logs/fraud_guard.ndjson', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

if __name__ == "__main__":
    # Test cases
    test_cases = [
        ("test@example.com", "credit", 100, 1, 0),
        ("vip@example.com", "prepaid", 50, 1, 0),
        ("suspicious@test.com", "debit", 100, 10, 0),
        ("normal@test.com", "credit", 6000, 1, 0),
    ]
    
    for email, card_type, amount, count, daily in test_cases:
        result = evaluate_payment(email, card_type, amount, count, daily)
        print(f"{email}: {result['decision']} - {result['reason']}")
