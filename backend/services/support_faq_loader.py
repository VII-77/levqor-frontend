"""
Support FAQ/Knowledge Base Loader
Loads markdown files for AI context
"""

import os
import logging

logger = logging.getLogger(__name__)

KB_DIR = "knowledge-base"


def load_support_corpus():
    """
    Load knowledge base content from markdown files
    
    Returns:
        dict: Dictionary with 'faq', 'pricing', 'policies' keys
    """
    corpus = {
        "faq": "",
        "pricing": "",
        "policies": ""
    }
    
    files = {
        "faq": "faq.md",
        "pricing": "pricing.md",
        "policies": "policies.md"
    }
    
    for key, filename in files.items():
        filepath = os.path.join(KB_DIR, filename)
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    corpus[key] = content
                    logger.info(f"support_faq.loaded file={filename} size={len(content)}")
            except Exception as e:
                logger.error(f"support_faq.error file={filename} error={str(e)}")
                corpus[key] = f"Error loading {filename}"
        else:
            logger.warning(f"support_faq.missing file={filename}")
            corpus[key] = _get_fallback_content(key)
    
    return corpus


def _get_fallback_content(key):
    """Generate basic fallback content if files don't exist"""
    
    if key == "faq":
        return """
# Levqor FAQ

Levqor is an AI automation platform for small businesses. We offer Done-For-You automation builds (£99-£599 one-time) and subscription plans (£29-£299/month).

For support: support@levqor.ai
For sales: sales@levqor.ai
        """.strip()
    
    elif key == "pricing":
        return """
# Levqor Pricing

**DFY Services:**
- Starter: £99 (1 workflow)
- Professional: £249 (3 workflows)
- Enterprise: £599 (7 workflows)

**Subscriptions:**
- Growth: £29/month
- Business: £99/month
- Enterprise: £299/month

14-day money-back guarantee on all services.
        """.strip()
    
    elif key == "policies":
        return """
# Levqor Policies

**Data Protection:** GDPR/PECR compliant. Privacy policy at www.levqor.ai/privacy

**Refunds:** 14-day money-back guarantee. Contact support@levqor.ai

**High-Risk Data:** We prohibit medical, legal, financial, and safety-critical data for compliance.

**Support:** Email support@levqor.ai or visit www.levqor.ai/emergency for urgent issues.
        """.strip()
    
    return "No content available"


def get_public_faq_summary():
    """
    Get condensed FAQ for public support (website visitors)
    
    Returns:
        str: Shortened FAQ content
    """
    corpus = load_support_corpus()
    faq_full = corpus.get("faq", "")
    
    # Extract first 1000 chars as summary
    if len(faq_full) > 1000:
        return faq_full[:1000] + "\n\n[For more details, visit www.levqor.ai or contact support@levqor.ai]"
    
    return faq_full
