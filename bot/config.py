import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('AI_INTEGRATIONS_OPENAI_API_KEY')
OPENAI_BASE_URL = os.getenv('AI_INTEGRATIONS_OPENAI_BASE_URL')

REPLIT_CONNECTORS_HOSTNAME = os.getenv('REPLIT_CONNECTORS_HOSTNAME')
REPL_IDENTITY = os.getenv('REPL_IDENTITY')
WEB_REPL_RENEWAL = os.getenv('WEB_REPL_RENEWAL')

POLL_INTERVAL_SECONDS = 60
QA_TARGET_SCORE = 95

AUTOMATION_QUEUE_DB_ID = os.getenv('AUTOMATION_QUEUE_DB_ID', '')
AUTOMATION_LOG_DB_ID = os.getenv('AUTOMATION_LOG_DB_ID', '')
JOB_LOG_DB_ID = os.getenv('JOB_LOG_DB_ID', '')

ALERT_WEBHOOK_URL = os.getenv('ALERT_WEBHOOK_URL', '')
ALLOW_DIRTY = os.getenv('ALLOW_DIRTY', 'false').lower() == 'true'

DEMO_MODE = (
    'demo' in AUTOMATION_QUEUE_DB_ID.lower() or 
    'demo' in AUTOMATION_LOG_DB_ID.lower() or 
    'demo' in JOB_LOG_DB_ID.lower() or
    not AUTOMATION_QUEUE_DB_ID or
    not AUTOMATION_LOG_DB_ID or
    not JOB_LOG_DB_ID
)
