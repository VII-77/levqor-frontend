# EchoPilot AI Automation Bot

## Overview

EchoPilot is an intelligent automation bot designed to process tasks from Notion databases using AI (OpenAI via Replit AI Integrations). It operates on a 60-second polling cycle, automatically processing triggered tasks, evaluating quality with dynamic per-task-type thresholds, and tracking comprehensive job performance metrics including costs, QA scores, token usage, and latency. The system features a live diagnostics system with hourly heartbeats and synthetic tests for 24/7 monitoring.

**Deployment:** Replit Reserved VM (24/7 uptime)  
**Production URL:** https://Echopilotai.replit.app  
**Cost:** $20/month (covered by Replit Core credits)

## User Preferences

- **Communication style:** Simple, everyday language
- **Development environment:** Replit Android app on Galaxy Fold 6 (mobile device)
- **Interface:** Mobile-optimized instructions preferred

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
- `auto_operator.py`: Self-healing monitoring system that checks health every 5 minutes and auto-escalates issues.
- `payments.py`: Stripe and PayPal payment integration for automated billing per job.
- `reconcile_payments.py`: Nightly payment reconciliation system (2:10 UTC daily).
- `client_manager.py`: Client management, revenue tracking, invoice generation, and email delivery system.
- `executive_report.py`: Daily executive PDF reports with 7-day performance summaries and revenue analytics (06:55 UTC daily).

### AI Integration

The bot integrates OpenAI via Replit AI Integrations:
- **GPT-4o**: Used for core task processing, with tracking of tokens_in, tokens_out, cost, and duration.
- **GPT-4o-mini**: Utilized for QA scoring with dynamic thresholds and a temperature of 0.3 for consistent evaluations.
- Token usage is meticulously tracked, and actual costs are computed for every AI operation.

### Quality Assurance System

A dynamic QA scoring system is in place with a fixed 80% pass threshold:
- **Multi-criteria evaluation**: Clarity (30%), Accuracy (30%), Completeness (20%), Professional tone (20%).
- **Fixed threshold**: All tasks use 80% (QC_PASS_THRESHOLD = 80), with option for custom overrides via a "QA Target" field.
- **Status handling**: 
  - QA ≥ 80% → Status "Done" (auto-passed)
  - QA < 80% → Status "Waiting Human" (needs review)
- Jobs are logged with appropriate status for tracking and metrics.

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
- **Auto-Operator (Self-Healing)**: Runs every 5 minutes to check system health, detect issues (stuck jobs, quality drops, integration failures), and auto-escalate via email/Telegram. Posts status to Notion Status Board. Available at `/ops-report` endpoint.
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

## Client Management & Revenue Tracking System

EchoPilot includes an optional client management system that transforms it from an internal automation bot to a monetized client service platform:

### Revenue Calculation
- **Automatic tracking**: Calculates gross revenue (Duration × Client Rate), profit (Revenue - AI Cost), and margin percentage
- **Custom pricing tiers**: Per-client rates stored in Notion Clients database
- **Fallback rates**: Uses `DEFAULT_RATE_USD_PER_MIN` environment variable (default: $5/min) when no client-specific rate is set

### Invoice Generation & Delivery
- **PDF invoices**: Professional invoices generated with ReportLab, including job details, financial summary, and branding
- **Email delivery**: Automated invoice emails sent via Gmail API (OAuth-based, no SMTP credentials needed)
- **Client notifications**: Clients receive invoice PDF attachments automatically after job completion

### Notion Integration
- **Client Database**: Optional "EchoPilot Clients" database tracks client names, emails, rates, and active status
- **Revenue fields in Job Log**: Automatically logs Client Rate USD/min, Gross USD, Profit USD, and Margin % for each job
- **Relation support**: Jobs can be linked to clients via Notion relations for automatic rate lookup

### Configuration
**Optional Environment Variables**:
- `NOTION_CLIENT_DB_ID` (Client database ID for client management)
- `DEFAULT_RATE_USD_PER_MIN` (Default billing rate, default: 5.0)

**Required Notion Fields** (Job Log):
- Client Rate USD/min (Number)
- Gross USD (Number)
- Profit USD (Number)
- Margin % (Number)
- Client (Relation to Clients DB, optional)
- Client Email (Email, optional)

See `CLIENT_SYSTEM_GUIDE.md` for complete setup and usage instructions.

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