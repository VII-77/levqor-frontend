# EchoPilot AI Automation Bot

## Overview

EchoPilot is an intelligent automation bot designed to process tasks from Notion databases using AI (OpenAI via Replit AI Integrations). It operates on a 60-second polling cycle, automatically processing triggered tasks, evaluating quality with dynamic per-task-type thresholds, and tracking comprehensive job performance metrics including costs, QA scores, token usage, and latency. The system features a live diagnostics system with hourly heartbeats and synthetic tests for 24/7 monitoring of its Reserved VM deployment.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Architecture Pattern

EchoPilot employs a polling-based event-driven system with robust Git integration. It polls Notion every 60 seconds, and all operations are tagged with the Git commit hash for traceability. The system ensures code integrity by refusing to run if the working tree is dirty (unless explicitly allowed).

### Application Structure

The application is built with a modular component design:
- `main.py`: Orchestrates the bot, including health checks, Git integration, and alert management.
- `processor.py`: Handles task processing, dynamic QA, metrics collection, and alerting.
- `notion_api.py`: Manages interactions with Notion, including enhanced logging.
- `google_drive_client.py`: Provides Google Drive integration for file handling.
- `gmail_client.py`: Manages Gmail email sending via Replit Gmail Connector (OAuth-based).
- `telegram_bot.py`: Handles Telegram messaging and command polling for instant notifications and remote control.
- `supervisor_report.py`: Generates and sends daily supervisor health reports via email.
- `config.py`: Centralizes application configuration.
- `git_utils.py`: Manages Git commit tracking and dirty tree detection.
- `schema_validator.py`: Automates schema validation and repair for Notion databases.
- `qa_thresholds.py`: Manages dynamic QA thresholds based on task types.
- `alerting.py`: Implements the alerting policy with webhook, email, and Telegram integration.
- `metrics.py`: Collects and rolls up performance metrics.
- `diagnostics.py` and `scheduler_diag.py`: Implement the live diagnostics and monitoring system.

### AI Integration

The bot integrates OpenAI via Replit AI Integrations:
- **GPT-4o**: Used for core task processing, with tracking of tokens_in, tokens_out, cost, and duration.
- **GPT-4o-mini**: Utilized for QA scoring with dynamic thresholds and a temperature of 0.3 for consistent evaluations.
- Token usage is meticulously tracked, and actual costs are computed for every AI operation.

### Quality Assurance System

A dynamic QA scoring system is in place with task-type specific thresholds:
- **Multi-criteria evaluation**: Clarity (30%), Accuracy (30%), Completeness (20%), Professional tone (20%).
- **Per-task-type thresholds**: Customizable (e.g., Research: 95%, Drafting: 90%), with an option for custom overrides via a "QA Target" field.
- Jobs failing to meet the threshold are marked with detailed failure notes.

### Authentication & Token Management

Authentication is handled via Replit Connectors OAuth Flow (Python Implementation), providing dynamic token refresh for Notion and Google Drive, along with automatic renewal upon expiration.

### Version Control Integration

Every job and log entry includes the current Git commit hash for full traceability. A health endpoint provides details including the commit and branch. The system prevents execution with a dirty working tree unless explicitly configured.

### Data Flow Architecture

The system utilizes a three-database structure within Notion:
1.  **Automation Queue Database**: Input for tasks, including Task Name, Description, Trigger, Status, Task Type, and an optional QA Target.
2.  **Automation Log Database**: An audit trail with Task, Status, Message, Details, Timestamp, and Commit.
3.  **EchoPilot Job Log Database**: Stores performance metrics such as Job Name, QA Score, Cost, Status, Notes, Timestamp, Commit, Task Type, Duration, Tokens In, and Tokens Out.

### Schema Enforcement

Automated pre-flight validation is performed on Notion databases, validating properties and types. It can auto-repair missing properties and raises blocking errors with precise diffs if repair is impossible.

### Alerting System

The system includes a comprehensive alerting policy with multiple notification channels:
- **Failure Detection**: Detects consecutive failures (≥3 within 24h) per task type and globally
- **Notification Channels**: 
  - Automation Log entries for audit trail
  - Webhook POST to configurable URL
  - Gmail email alerts via Replit Gmail Connector (OAuth, no SMTP credentials needed)
  - Telegram instant messaging alerts with bot commands
- **De-duplication**: Alerts are de-duplicated with 1-hour cooldown to prevent spam

### Metrics & Error-Budget Dashboard

Weekly metric rollups are computed, tracking total jobs, failures, failure rates, top failure causes, mean QA, p95 latency, and total cost. These reports are stored in the Job Log, facilitating performance analysis and trend tracking.

### Live Diagnostics & Monitoring System

The system includes comprehensive monitoring capabilities:
- **Status Board Diagnostics**: Hourly heartbeats and 6-hour synthetic tests posted to Notion Status Board for 24/7 health monitoring
- **Daily Supervisor Reports**: Automated email reports sent at 06:45 UTC daily containing:
  - System health status (Notion, Google Drive, OpenAI connectivity)
  - Recent QA score averages (last 10 jobs)
  - Git commit tracking
  - Service availability checks
- **Real-time Failure Alerts**: Email and Telegram notifications sent immediately when consecutive failures (≥3) detected, with 1-hour de-duplication
- **Telegram Bot Commands**: Interactive monitoring via Telegram chat:
  - `/status` - Check bot status (polling interval, QA target, commit, branch)
  - `/health` - System health check (services, message, commit)
  - `/report` - Trigger on-demand supervisor report via email
  - `/help` - Show available commands

## External Dependencies

### Third-Party APIs

-   **Notion API**: Primary data storage, task queue, and audit trail, integrated via the official `notion-client` Python SDK with OAuth2 through Replit Connectors.
-   **OpenAI API**: Used for AI task processing and QA evaluation (GPT-4o and GPT-4o-mini), integrated via the official `openai` SDK, with a custom base URL through Replit AI Integrations.
-   **Google Drive API**: For file handling and storage, integrated using the `googleapiclient` library with OAuth2 via Replit Connectors.
-   **Gmail API**: For sending automated supervisor reports and failure alerts, integrated via `googleapiclient` with OAuth2 through Replit Gmail Connector (no SMTP credentials required).
-   **Telegram Bot API**: For instant push notifications and interactive chat commands, integrated via direct HTTP API calls with bot token authentication.

### Python Dependencies

-   `notion-client`: For Notion database interactions.
-   `openai`: For AI model interactions.
-   `google-api-python-client`, `google-auth`: For Google Drive and OAuth2.
-   `requests`: For HTTP client functionalities.
-   `schedule`: For task scheduling.
-   `python-dotenv`: For environment variable management.

### Configuration Requirements

**Required Environment Variables**:
-   `AI_INTEGRATIONS_OPENAI_API_KEY`
-   `AI_INTEGRATIONS_OPENAI_BASE_URL`
-   `REPLIT_CONNECTORS_HOSTNAME`
-   `REPL_IDENTITY` or `WEB_REPL_RENEWAL`
-   `AUTOMATION_QUEUE_DB_ID`
-   `AUTOMATION_LOG_DB_ID`
-   `JOB_LOG_DB_ID`

**Optional Environment Variables**:
-   `ALERT_WEBHOOK_URL` (for webhook-based alerts)
-   `ALERT_TO` (email address for supervisor reports and failure alerts)
-   `TELEGRAM_BOT_TOKEN` (Telegram bot token from @BotFather for instant messaging alerts)
-   `TELEGRAM_CHAT_ID` (Telegram chat ID for receiving messages and commands)
-   `ALLOW_DIRTY` (allow execution with uncommitted Git changes)
-   `NOTION_STATUS_DB_ID` (for live diagnostics posting to Status Board)

**Application Constants**:
-   `POLL_INTERVAL_SECONDS` (60)
-   `QA_TARGET_SCORE` (95, default global threshold)
-   `QA_DEFAULTS` (Per-task-type thresholds)