# EchoPilot AI Automation Bot

## Overview

EchoPilot is a comprehensive **enterprise-ready AI automation platform** designed to process tasks from Notion databases using AI (OpenAI via Replit AI Integrations). It operates on a 60-second polling cycle with **autonomous scheduling via Replit Workflows**, automatically processing triggered tasks, evaluating quality with an 80% QA threshold, and tracking comprehensive job performance metrics including costs, QA scores, token usage, and latency. 

The platform now includes **enterprise features**: finance & revenue tracking, 30-day forecasting, partner marketplace API, multi-language/multi-currency localization, legal compliance documentation (GDPR/CCPA), and advanced monitoring with self-healing capabilities. The system is deployed on Replit Reserved VM at **https://echopilotai.replit.app** and is ready for production use pending legal document review.

**Current Status (Oct 2025):** 90% enterprise-ready, 100% core features operational, ~16,500 lines of production code, 27 API endpoints, 13 autonomous scheduled tasks.

## User Preferences

- **Communication style:** Simple, everyday language
- **Development environment:** Replit Android app on Galaxy Fold 6 (mobile device)
- **Interface:** Mobile-optimized instructions preferred

## System Architecture

### Core Architecture

EchoPilot employs a polling-based event-driven system with robust Git integration, polling Notion every 60 seconds. All operations are tagged with the Git commit hash for traceability, and the system prevents execution with a dirty working tree unless explicitly allowed.

### Application Structure and Key Features

The application is built with a modular component design focusing on:

**Core Automation:**
-   **Task Processing:** Orchestrates task execution, dynamic QA, metrics collection, and alerting.
-   **Notion Integration:** Manages interactions with 13 Notion databases for task queues, logging, and performance metrics.
-   **AI Integration:** Utilizes OpenAI models (GPT-4o for core processing, GPT-4o-mini for QA scoring) with detailed token usage and cost tracking.
-   **Quality Assurance:** Dynamic QA scoring system with multi-criteria evaluation (Clarity, Accuracy, Completeness, Professional tone) and a fixed 80% pass threshold.

**Enterprise Features (New Oct 2025):**
-   **Finance System:** Revenue tracking, cost analysis, P&L reports, margin calculations, company valuation models (DCF, SaaS multiples), Stripe integration.
-   **Forecast Engine:** 30-day predictions for load and revenue using ML-based moving average + trend analysis, chart exports (JSON/CSV).
-   **Marketplace API:** Partner integration with API keys, quota management, job submission/retrieval endpoints (`/v1/jobs`, `/v1/results`).
-   **Localization:** Multi-language support (EN/ES/UR), multi-currency (USD/EUR/GBP/INR/PKR), regional compliance rules (GDPR/CCPA by country).
-   **Legal Compliance:** Complete Terms of Service, Privacy Policy, Cookie Policy, and Accessibility Statement (GDPR/CCPA compliant, pending legal review).
-   **Database Infrastructure:** 8 new databases designed (Finance, Governance, Ops Monitor, Forecast, Region Compliance, Partners, Referrals, Growth Metrics) with automated setup script.

**Platform Capabilities:**
-   **Authentication:** Handles authentication via Replit Connectors OAuth Flow for Notion, Google Drive, and Gmail with dynamic token refresh.
-   **Alerting System:** Comprehensive alerting policy with webhook, email, and Telegram notifications for failures, including de-duplication.
-   **Monitoring & Diagnostics:** Includes an Auto-Operator for self-healing, hourly heartbeats, synthetic tests, daily supervisor reports, and real-time failure alerts via email and Telegram.
-   **Metrics Aggregation:** Cross-database metrics system with daily System Pulse reports to Governance Ledger, health logging (NDJSON), and uptime tracking.
-   **Edge Routing:** Railway fallback support to work around Replit's GCP Load Balancer proxy limitations for `/supervisor`, `/forecast`, `/metrics`, and `/pulse` endpoints.
-   **Client Management:** Automated revenue calculation, client tracking via Notion, payment processing (Stripe test mode).
-   **Compliance & Maintenance:** Features for Data Subject Requests (DSR), refund processing, p95 latency tracking, and automated configuration backups.
-   **Resilience & Auto-Recovery:** Mechanisms for Stripe payment reconciliation (missed webhooks), automatic retry of failed jobs, and media file validation (size/duration limits).

### Data Flow Architecture

The system uses a **13-database structure** within Notion:

**Core Databases (5 - Active):**
1.  **Automation Queue Database:** Input for tasks.
2.  **Automation Log Database:** Audit trail of bot operations.
3.  **EchoPilot Job Log Database:** Stores performance metrics and job details.
4.  **Notion Client Database:** Client tracking and invoicing.
5.  **Notion Status Database:** System health monitoring.

**Enterprise Databases (8 - Schemas Ready):**
6.  **Finance Database:** Revenue, costs, margins, P&L tracking.
7.  **Governance Database:** Decision log, board approvals, risk register.
8.  **Ops Monitor Database:** System metrics, alerts, auto-fix logs.
9.  **Forecast Database:** 30-day predictions, accuracy tracking.
10. **Region Compliance Database:** Multi-region rules, GDPR/CCPA flags.
11. **Partners Database:** API keys, quotas, revenue share, payouts.
12. **Referrals Database:** Referral codes, credits, revenue tracking.
13. **Growth Metrics Database:** CAC, LTV, conversion rates, ROI.

**Setup:** Automated schema enforcement validates and auto-repairs Notion database properties. Run `python bot/database_setup.py` to create enterprise databases.

## External Dependencies

### Third-Party APIs

-   **Notion API**: Primary data storage, task queue, and audit trail via `notion-client` with OAuth2 through Replit Connectors.
-   **OpenAI API**: AI task processing and QA evaluation (GPT-4o, GPT-4o-mini) via `openai` SDK, custom base URL through Replit AI Integrations.
-   **Google Drive API**: File handling and storage via `googleapiclient` with OAuth2 through Replit Connectors.
-   **Gmail API**: Sending automated reports and alerts via `googleapiclient` with OAuth2 through Replit Gmail Connector.
-   **Telegram Bot API**: Instant notifications and interactive commands via direct HTTP API calls.
-   **Stripe API**: For payment reconciliation and client billing.

### Python Dependencies

-   `notion-client`
-   `openai`
-   `google-api-python-client`, `google-auth`
-   `requests`
-   `schedule`
-   `python-dotenv`
-   `ReportLab` (for PDF generation)

### Configuration Requirements

**Core Environment Variables (Required)**:
-   `AI_INTEGRATIONS_OPENAI_API_KEY`
-   `AI_INTEGRATIONS_OPENAI_BASE_URL`
-   `REPLIT_CONNECTORS_HOSTNAME`
-   `REPL_IDENTITY` or `WEB_REPL_RENEWAL`
-   `AUTOMATION_QUEUE_DB_ID`
-   `AUTOMATION_LOG_DB_ID`
-   `JOB_LOG_DB_ID`

**Enterprise Environment Variables (Optional - for new features)**:
-   `NOTION_FINANCE_DB_ID` - Finance & revenue tracking
-   `NOTION_FORECAST_DB_ID` - 30-day predictions
-   `NOTION_PARTNERS_DB_ID` - Marketplace API
-   `NOTION_REGION_COMPLIANCE_DB_ID` - Localization
-   `NOTION_GOVERNANCE_DB_ID` - Decision log
-   `NOTION_OPS_MONITOR_DB_ID` - System metrics
-   `NOTION_REFERRALS_DB_ID` - Referral tracking
-   `NOTION_GROWTH_METRICS_DB_ID` - CAC/LTV tracking

**Payment & Alerts**:
-   `STRIPE_SECRET_KEY` (currently test mode: sk_test_...)
-   `STRIPE_WEBHOOK_SECRET`
-   `TELEGRAM_BOT_TOKEN`
-   `TELEGRAM_CHAT_ID`

**Railway Fallback (Optional - for external API access)**:
-   `EDGE_ENABLE` - Set to `true` to enable Railway proxy routing
-   `EDGE_BASE_URL` - Your Railway deployment URL (e.g., `https://your-app.railway.app`)

**Setup:** Use `bot/database_setup.py` to auto-generate database IDs and environment variable configs.

## Railway Fallback Feature

EchoPilot supports **dual deployment** to work around Replit's proxy routing issues:

-   **Replit Reserved VM**: Runs all automation, polling, and background tasks (works perfectly)
-   **Railway Deployment** (optional): Provides stable external API access for endpoints blocked by Replit's proxy

**Affected Endpoints** (return 404 on Replit's public URL):
-   `/supervisor` - System supervisor status
-   `/forecast` - 30-day forecasting
-   `/metrics` - Cross-database metrics
-   `/pulse` - System pulse reports

**How it Works**: When `EDGE_ENABLE=true` and `EDGE_BASE_URL` is set, Replit automatically proxies these endpoints to your Railway deployment, providing transparent fallback routing with zero code changes.

**Setup Guide**: See `RAILWAY_FALLBACK_SETUP.md` for detailed instructions.
**Test Script**: Run `bash scripts/test_edge.sh` to verify Railway fallback configuration.
## Autonomous Scheduler (Phases 30-50 - Oct 2025)

**Status:** ✅ FULLY OPERATIONAL using Replit Workflows  
**Total Tasks:** 13 autonomous operations

The scheduler runs as a dedicated Replit Workflow called "Scheduler" alongside the main "EchoPilot Bot" workflow.

### Core Features (Phases 30-40)

- **Heartbeat Ticks:** Every 60 seconds with next run calculations
- **CEO Brief:** Daily at 08:00 UTC (GPT-4o-mini powered executive intelligence)
- **Daily Report:** Daily at 09:00 UTC (finance metrics + metrics summary)
- **Self-Heal:** Every 6 hours (automatic retry of failed jobs)
- **Pricing AI:** Daily at 03:00 UTC (dynamic pricing optimization)
- **Weekly Audit:** Mondays at 00:30 UTC (compliance reports)
- **Replica Sync:** Every 2 hours (multi-region synchronization)
- **AI Ops Brain:** Every 12 hours (autonomous operational decisions)
- **Production Alerts:** Every 5 minutes (critical monitoring)
- **Signal Handling:** Graceful shutdown on SIGTERM/SIGINT
- **Comprehensive Logging:** NDJSON format to `logs/scheduler.log`

### Enterprise Reinforcement (Phases 41-50)

- **Ops Sentinel:** Every 3 minutes (system health watchdog - CPU, RAM, disk, latency)
- **Revenue Intelligence:** Every 30 minutes (AI-powered revenue trend analysis with GPT-4o-mini)
- **Finance Reconciler:** Every 6 hours (Stripe-Notion payment matching)
- **Auto-Governance:** Every hour (KPI monitoring and health aggregation)

### Implementation

Uses Replit's Workflow system (NOT traditional daemonization):

```python
# Workflow configuration
workflows_set_run_config_tool(
    name="Scheduler",
    command="python3 -u scripts/exec_scheduler.py",
    output_type="console"
)
```

**Why Workflows?** Replit's environment does not support traditional daemonization (os.setsid, nohup, etc.). 
Background processes exit immediately. Workflows provide systemd-like process management with automatic 
restart, persistence, and log management.

### How to Control

1. **Replit UI** (Recommended):
   - Find "Scheduler" in Tools panel
   - Click ▶️ to start, ⏹️ to stop

2. **Production Deployment**:
   - Both "EchoPilot Bot" and "Scheduler" workflows deploy automatically
   - Run reliably in production with auto-restart on failure

3. **Manual Triggers** (Dashboard):
   - CEO Brief, Self-Heal, Finance Metrics all work via dashboard buttons

### Files

- `scripts/exec_scheduler.py` - Main scheduler (263 lines, hardened with signal handling)
- `scripts/run_automations.sh` - Helper script for manual control (optional)
- `logs/scheduler.log` - NDJSON event log

**Deprecated:** `scripts/daemonize.py` (replaced by Workflow system)

See `logs/SCHEDULER_PERSISTENCE_SOLVED.md` for detailed investigation and solution.
