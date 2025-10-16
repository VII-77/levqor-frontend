import os
from bot.constants import POLL_INTERVAL_SECONDS, DEFAULT_QA_TARGET

# OpenAI Configuration (via Replit AI Integrations)
OPENAI_API_KEY = os.getenv('AI_INTEGRATIONS_OPENAI_API_KEY')
OPENAI_BASE_URL = os.getenv('AI_INTEGRATIONS_OPENAI_BASE_URL')

# Notion Database IDs
AUTOMATION_QUEUE_DB_ID = os.getenv('AUTOMATION_QUEUE_DB_ID')
AUTOMATION_LOG_DB_ID = os.getenv('AUTOMATION_LOG_DB_ID')
JOB_LOG_DB_ID = os.getenv('JOB_LOG_DB_ID')

# Replit Connectors Configuration
REPLIT_CONNECTORS_HOSTNAME = os.getenv('REPLIT_CONNECTORS_HOSTNAME', 'connectors-svc.util.repl.co')

# Authentication Tokens (REPL or DEPL mode)
REPL_IDENTITY = os.getenv('REPL_IDENTITY')
WEB_REPL_RENEWAL = os.getenv('WEB_REPL_RENEWAL')

# Application Configuration
POLL_INTERVAL = POLL_INTERVAL_SECONDS
QA_TARGET_SCORE = DEFAULT_QA_TARGET

# Git Version Control
ALLOW_DIRTY = os.getenv('ALLOW_DIRTY', 'false').lower() == 'true'

# Alerting Configuration
ALERT_WEBHOOK_URL = os.getenv('ALERT_WEBHOOK_URL')
ALERT_CONSECUTIVE_THRESHOLD = 3  # Trigger alert after 3 consecutive failures
ALERT_DEDUP_WINDOW_HOURS = 1     # De-duplicate alerts within 1 hour

# Session Secret
SESSION_SECRET = os.getenv('SESSION_SECRET', 'default-dev-secret-change-in-production')

# Demo Mode Detection
DEMO_MODE = (
    'demo' in (AUTOMATION_QUEUE_DB_ID or '').lower() or 
    'demo' in (AUTOMATION_LOG_DB_ID or '').lower() or 
    'demo' in (JOB_LOG_DB_ID or '').lower() or
    not AUTOMATION_QUEUE_DB_ID or
    not AUTOMATION_LOG_DB_ID or
    not JOB_LOG_DB_ID
)

def validate_config():
    """Validate required configuration and provide helpful error messages"""
    missing = []
    
    if not OPENAI_API_KEY:
        missing.append("AI_INTEGRATIONS_OPENAI_API_KEY (OpenAI API key)")
    
    if not OPENAI_BASE_URL:
        missing.append("AI_INTEGRATIONS_OPENAI_BASE_URL (OpenAI base URL)")
    
    if not AUTOMATION_QUEUE_DB_ID:
        missing.append("AUTOMATION_QUEUE_DB_ID (Notion queue database)")
    
    if not AUTOMATION_LOG_DB_ID:
        missing.append("AUTOMATION_LOG_DB_ID (Notion log database)")
    
    if not JOB_LOG_DB_ID:
        missing.append("JOB_LOG_DB_ID (Notion job log database)")
    
    if missing:
        error_msg = "Missing required environment variables:\n" + "\n".join(f"  - {m}" for m in missing)
        error_msg += "\n\nPlease configure these in Replit Secrets."
        raise ValueError(error_msg)
    
    return True
