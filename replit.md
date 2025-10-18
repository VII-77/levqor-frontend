# EchoPilot AI Automation Bot

## Overview

EchoPilot is an intelligent automation bot designed to process tasks from Notion databases using AI (OpenAI via Replit AI Integrations). It operates on a 60-second polling cycle, automatically processing triggered tasks, evaluating quality with dynamic per-task-type thresholds, and tracking comprehensive job performance metrics including costs, QA scores, token usage, and latency. The system features a live diagnostics system with hourly heartbeats and synthetic tests for 24/7 monitoring. The project's ambition is to provide a robust, self-managing, and scalable automation solution that can also be monetized into a client service platform.

## User Preferences

- **Communication style:** Simple, everyday language
- **Development environment:** Replit Android app on Galaxy Fold 6 (mobile device)
- **Interface:** Mobile-optimized instructions preferred

## System Architecture

### Core Architecture

EchoPilot employs a polling-based event-driven system with robust Git integration, polling Notion every 60 seconds. All operations are tagged with the Git commit hash for traceability, and the system prevents execution with a dirty working tree unless explicitly allowed.

### Application Structure and Key Features

The application is built with a modular component design focusing on:
-   **Task Processing:** Orchestrates task execution, dynamic QA, metrics collection, and alerting.
-   **Notion Integration:** Manages interactions with Notion databases for task queues, logging, and performance metrics.
-   **AI Integration:** Utilizes OpenAI models (GPT-4o for core processing, GPT-4o-mini for QA scoring) with detailed token usage and cost tracking.
-   **Quality Assurance:** Dynamic QA scoring system with multi-criteria evaluation (Clarity, Accuracy, Completeness, Professional tone) and a fixed 80% pass threshold.
-   **Authentication:** Handles authentication via Replit Connectors OAuth Flow for Notion, Google Drive, and Gmail with dynamic token refresh.
-   **Alerting System:** Comprehensive alerting policy with webhook, email, and Telegram notifications for failures, including de-duplication.
-   **Monitoring & Diagnostics:** Includes an Auto-Operator for self-healing, hourly heartbeats, synthetic tests, daily supervisor reports, and real-time failure alerts via email and Telegram.
-   **Client Management (Optional):** Automated revenue calculation, PDF invoice generation and delivery, and client tracking via Notion.
-   **Compliance & Maintenance:** Features for Data Subject Requests (DSR), refund processing, p95 latency tracking, and automated configuration backups.
-   **Resilience & Auto-Recovery:** Mechanisms for Stripe payment reconciliation (missed webhooks), automatic retry of failed jobs, and media file validation (size/duration limits).

### Data Flow Architecture

The system uses a three-database structure within Notion:
1.  **Automation Queue Database:** Input for tasks.
2.  **Automation Log Database:** Audit trail of bot operations.
3.  **EchoPilot Job Log Database:** Stores performance metrics and job details.

Automated schema enforcement validates and auto-repairs Notion database properties.

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

**Required Environment Variables**:
-   `AI_INTEGRATIONS_OPENAI_API_KEY`
-   `AI_INTEGRATIONS_OPENAI_BASE_URL`
-   `REPLIT_CONNECTORS_HOSTNAME`
-   `REPL_IDENTITY` or `WEB_REPL_RENEWAL`
-   `AUTOMATION_QUEUE_DB_ID`
-   `AUTOMATION_LOG_DB_ID`
-   `JOB_LOG_DB_ID`