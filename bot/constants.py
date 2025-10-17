"""
Constants and configuration values for EchoPilot
Centralized location for all magic numbers and limits
"""

# Cost calculation rates (OpenAI GPT-4o pricing)
GPT4O_INPUT_TOKEN_COST = 0.00001   # $0.01 per 1K tokens
GPT4O_OUTPUT_TOKEN_COST = 0.00003  # $0.03 per 1K tokens

# Content truncation limits (Notion API limits)
NOTION_RICH_TEXT_LIMIT = 2000
NOTION_NOTES_LIMIT = 2000
JOB_RESULT_PREVIEW_LIMIT = 500
QA_CONTENT_EVALUATION_LIMIT = 1000

# AI Model configuration
MODEL_GPT4O = "gpt-4o"
MODEL_GPT4O_MINI = "gpt-4o-mini"

# Temperature settings
TEMP_PROCESSING = 0.7  # Creative task processing
TEMP_QA_SCORING = 0.3  # Consistent QA evaluation

# Token limits
MAX_TOKENS_PROCESSING = 2000
MAX_TOKENS_QA = 10

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
RETRY_BACKOFF_MULTIPLIER = 2

# API timeout (seconds)
OPENAI_TIMEOUT_SECONDS = 60

# QA Score bounds
QA_SCORE_MIN = 0
QA_SCORE_MAX = 100

# Polling configuration
POLL_INTERVAL_SECONDS = 60
DEFAULT_QA_TARGET = 95

# QA Pass Threshold (auto-pass gate)
QC_PASS_THRESHOLD = 80
