# EchoPilot AI Automation Bot

## Overview

EchoPilot is an enterprise-ready AI automation platform that processes tasks from Notion databases using AI (OpenAI via Replit AI Integrations). It operates on a 60-second polling cycle with autonomous scheduling via Replit Workflows. The platform includes robust features for task processing, dynamic quality assurance (80% QA threshold), and comprehensive job performance tracking (costs, QA scores, token usage, latency).

Recently, EchoPilot has been enhanced with enterprise functionalities including finance and revenue tracking, 30-day forecasting, a partner marketplace API, multi-language/multi-currency localization, legal compliance documentation (GDPR/CCPA), and advanced monitoring with self-healing capabilities. It is deployed on a Replit Reserved VM at https://echopilotai.replit.app and is production-ready pending legal review.

## User Preferences

- Communication style: Simple, everyday language
- Development environment: Replit Android app on Galaxy Fold 6 (mobile device)
- Interface: Mobile-optimized instructions preferred

## System Architecture

### Core Architecture

EchoPilot uses a polling-based, event-driven system with Git integration, polling Notion every 60 seconds. All operations are tagged with the Git commit hash for traceability, and execution is prevented with a dirty working tree unless explicitly allowed. The system leverages Replit Workflows for autonomous scheduling and Replit Connectors for OAuth-based integrations.

### Application Structure and Key Features

**Core Automation:**
- **Task Processing:** Orchestrates task execution, dynamic QA, metrics collection, and alerting.
- **Notion Integration:** Manages interactions with 13 Notion databases for task queues, logging, and performance metrics.
- **AI Integration:** Utilizes OpenAI models (GPT-4o for processing, GPT-4o-mini for QA) with detailed cost and token usage tracking.
- **Quality Assurance:** Dynamic, multi-criteria QA scoring (Clarity, Accuracy, Completeness, Professional tone) with an 80% pass threshold.

**Enterprise Features:**
- **Finance System:** Revenue tracking, cost analysis, P&L reports, margin calculations, company valuation models, and Stripe integration.
- **Forecast Engine:** 30-day load and revenue predictions using ML-based moving average and trend analysis.
- **Marketplace API:** Partner integration with API keys, quota management, and job submission/retrieval endpoints.
- **Localization:** Multi-language (EN/ES/UR) and multi-currency (USD/EUR/GBP/INR/PKR) support with regional compliance rules.
- **Legal Compliance:** Comprehensive Terms of Service, Privacy Policy, Cookie Policy, and Accessibility Statement (GDPR/CCPA compliant, pending review).
- **Database Infrastructure:** Automated setup of 8 new enterprise-specific databases (Finance, Governance, Ops Monitor, Forecast, Region Compliance, Partners, Referrals, Growth Metrics).

**Platform Capabilities:**
- **Authentication:** Handles Notion, Google Drive, and Gmail authentication via Replit Connectors OAuth Flow with dynamic token refresh.
- **Alerting System:** Webhook, email, and Telegram notifications for failures with de-duplication.
- **Monitoring & Diagnostics:** Auto-Operator for self-healing, hourly heartbeats, synthetic tests, daily supervisor reports, and real-time failure alerts.
- **Metrics Aggregation:** Cross-database metrics system with daily System Pulse reports and health logging.
- **Edge Routing:** Railway fallback support for specific endpoints (`/supervisor`, `/forecast`, `/metrics`, `/pulse`) to bypass Replit's proxy limitations.
- **Resilience & Auto-Recovery:** Mechanisms for Stripe payment reconciliation, automatic retry of failed jobs, and media file validation.

### Data Flow Architecture

The system is built on a 13-database structure within Notion:
- **Core Databases (5):** Automation Queue, Automation Log, EchoPilot Job Log, Notion Client, Notion Status.
- **Enterprise Databases (8):** Finance, Governance, Ops Monitor, Forecast, Region Compliance, Partners, Referrals, Growth Metrics.
Automated schema enforcement ensures database property validity.

## External Dependencies

### Third-Party APIs

-   **Notion API**: Primary data storage, task queue, and audit trail via `notion-client` with OAuth2 through Replit Connectors.
-   **OpenAI API**: AI task processing and QA evaluation (GPT-4o, GPT-4o-mini) via `openai` SDK, custom base URL through Replit AI Integrations.
-   **Google Drive API**: File handling and storage via `googleapiclient` with OAuth2 through Replit Connectors.
-   **Gmail API**: Sending automated reports and alerts via `googleapiclient` with OAuth2 through Replit Gmail Connector.
-   **Telegram Bot API**: Instant notifications and interactive commands.
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
-   `AI_INTEGRATIONS_OPENAI_API_KEY`, `AI_INTEGRATIONS_OPENAI_BASE_URL`
-   `REPLIT_CONNECTORS_HOSTNAME`, `REPL_IDENTITY` or `WEB_REPL_RENEWAL`
-   `AUTOMATION_QUEUE_DB_ID`, `AUTOMATION_LOG_DB_ID`, `JOB_LOG_DB_ID`

**Enterprise Environment Variables (Optional - for new features)**:
-   `NOTION_FINANCE_DB_ID`, `NOTION_FORECAST_DB_ID`, `NOTION_PARTNERS_DB_ID`
-   `NOTION_REGION_COMPLIANCE_DB_ID`, `NOTION_GOVERNANCE_DB_ID`, `NOTION_OPS_MONITOR_DB_ID`
-   `NOTION_REFERRALS_DB_ID`, `NOTION_GROWTH_METRICS_DB_ID`

**Payment & Alerts**:
-   `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
-   `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`

**Railway Fallback (Optional - for external API access)**:
-   `EDGE_ENABLE`, `EDGE_BASE_URL`