"""
Enhanced High-Risk Firewall with Severity Levels
Improvements:
- Severity levels (critical, high, medium, low)
- User warnings before blocking
- Contextual feedback
- Appeal process
"""

import logging
from typing import Dict, List, Tuple
from enum import Enum

log = logging.getLogger("levqor")


class RiskSeverity(Enum):
    CRITICAL = "critical"  # Block immediately, no warnings
    HIGH = "high"          # Block with explanation
    MEDIUM = "medium"      # Warn but allow
    LOW = "low"            # Log only


# Risk patterns with severity levels
RISK_PATTERNS = {
    # CRITICAL - Medical/Healthcare
    "medical_diagnosis": {
        "terms": ["diagnosis", "diagnose disease", "medical diagnosis", "diagnostic test result"],
        "severity": RiskSeverity.CRITICAL,
        "category": "medical",
        "message": "Levqor cannot automate medical diagnoses. This violates medical device regulations."
    },
    "prescription_management": {
        "terms": ["prescribe medication", "prescription refill", "drug dosage"],
        "severity": RiskSeverity.CRITICAL,
        "category": "medical",
        "message": "Automated prescription management requires medical licensure."
    },
    
    # CRITICAL - Legal
    "legal_representation": {
        "terms": ["legal representation", "represent in court", "file lawsuit"],
        "severity": RiskSeverity.CRITICAL,
        "category": "legal",
        "message": "Legal representation requires a licensed attorney."
    },
    
    # CRITICAL - Financial
    "investment_advice": {
        "terms": ["investment recommendation", "stock picks", "trading signals", "buy stock"],
        "severity": RiskSeverity.CRITICAL,
        "category": "financial",
        "message": "Investment advice requires proper licensing (FCA/SEC)."
    },
    
    # HIGH - Medical/Healthcare
    "medical_general": {
        "terms": ["medical advice", "treatment plan", "symptom analysis"],
        "severity": RiskSeverity.HIGH,
        "category": "medical",
        "message": "Medical advice should only come from qualified healthcare professionals."
    },
    
    # HIGH - Legal
    "legal_advice": {
        "terms": ["legal advice", "legal opinion", "contract drafting"],
        "severity": RiskSeverity.HIGH,
        "category": "legal",
        "message": "Legal advice requires qualified legal counsel."
    },
    
    # MEDIUM - Financial
    "financial_guidance": {
        "terms": ["tax planning", "financial planning", "retirement planning"],
        "severity": RiskSeverity.MEDIUM,
        "category": "financial",
        "message": "Financial planning may require professional certification. Proceed with caution."
    },
    
    # LOW - General awareness
    "health_wellness": {
        "terms": ["health tips", "wellness advice", "fitness recommendations"],
        "severity": RiskSeverity.LOW,
        "category": "wellness",
        "message": "General wellness content detected. Ensure no medical claims are made."
    }
}


def check_risk_level(text: str) -> Tuple[RiskSeverity, str, List[str], str]:
    """
    Check risk level of text content.
    
    Returns:
        (severity, category, matched_patterns, message)
    """
    if not text:
        return RiskSeverity.LOW, "", [], ""
    
    text_lower = text.lower()
    highest_severity = RiskSeverity.LOW
    matched_patterns = []
    category = ""
    message = ""
    
    for pattern_name, pattern_data in RISK_PATTERNS.items():
        for term in pattern_data["terms"]:
            if term in text_lower:
                severity = pattern_data["severity"]
                
                # Track highest severity found
                if severity.value in ["critical", "high"]:
                    if highest_severity == RiskSeverity.LOW or \
                       (severity == RiskSeverity.CRITICAL and highest_severity != RiskSeverity.CRITICAL):
                        highest_severity = severity
                        category = pattern_data["category"]
                        message = pattern_data["message"]
                
                matched_patterns.append(pattern_name)
                break
    
    return highest_severity, category, list(set(matched_patterns)), message


def should_block(severity: RiskSeverity) -> bool:
    """Determine if content should be blocked based on severity"""
    return severity in [RiskSeverity.CRITICAL, RiskSeverity.HIGH]


def format_user_warning(severity: RiskSeverity, category: str, message: str) -> Dict:
    """Format a user-friendly warning message"""
    if severity == RiskSeverity.CRITICAL:
        return {
            "blocked": True,
            "severity": "critical",
            "title": f"Prohibited Content: {category.title()}",
            "message": message,
            "can_proceed": False,
            "learn_more_url": "/risk-disclosure"
        }
    elif severity == RiskSeverity.HIGH:
        return {
            "blocked": True,
            "severity": "high",
            "title": f"High-Risk Content: {category.title()}",
            "message": message,
            "can_proceed": False,
            "learn_more_url": "/risk-disclosure"
        }
    elif severity == RiskSeverity.MEDIUM:
        return {
            "blocked": False,
            "severity": "medium",
            "title": "Proceed with Caution",
            "message": message,
            "can_proceed": True,
            "disclaimer_required": True
        }
    else:  # LOW
        return {
            "blocked": False,
            "severity": "low",
            "message": message,
            "can_proceed": True
        }
