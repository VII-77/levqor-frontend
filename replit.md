# EchoPilot AI Automation Bot

## Overview
EchoPilot is a 100-phase enterprise-ready AI automation platform designed to process tasks from Notion databases using AI (OpenAI via Replit AI Integrations). It features a 60-second polling cycle, autonomous scheduling, dynamic quality assurance (80% QA threshold), and comprehensive job performance tracking (costs, QA scores, token usage, latency).

The platform includes core infrastructure for finance, forecasting, a marketplace API, localization, and legal compliance. Advanced operations cover payments, SLO tracking, incident paging, cost guardrails, and autoscaling. The enterprise suite adds RBAC, JWT authentication, disaster recovery, multi-tenancy, security scanning, compliance automation, predictive maintenance, continuous learning, and automated enterprise validation. It is deployed on a Replit Reserved VM and is production-ready with automated validation and reporting.

## User Preferences
- Communication style: Simple, everyday language
- Development environment: Replit Android app on Galaxy Fold 6 (mobile device)
- Interface: Mobile-optimized instructions preferred

## System Architecture

### Core Architecture
EchoPilot employs a polling-based, event-driven system with Git integration, polling Notion every 60 seconds. All operations are traceable via Git commit hashes, and execution is prevented with a dirty working tree unless explicitly allowed. It leverages Replit Workflows for scheduling and Replit Connectors for OAuth-based integrations.

### SLO Configuration (Production-Ready)
All SLO thresholds are configurable via environment variables:
- **Availability:** `SLO_AVAILABILITY_PCT` (default: 99.9%)
- **P95 Latency:** `SLO_P95_TARGET_MS` (default: 800ms)
- **P99 Latency:** `SLO_P99_TARGET_MS` (default: 1200ms)
- **Webhook Success:** `SLO_WEBHOOK_SUCCESS_PCT` (default: 99%)
- **Error Budget Burn:** `SLO_ERROR_BUDGET_PCT` (default: 2% per day)

See `docs/SLOS.md` for complete documentation.

### Application Structure and Key Features
**Core Automation:**
- **Task Processing:** Manages task execution, dynamic QA, metrics, and alerts.
- **Notion Integration:** Interacts with 13 Notion databases for task queues, logging, and metrics.
- **AI Integration:** Uses OpenAI models (GPT-4o for processing, GPT-4o-mini for QA) with detailed cost/token tracking.
- **Quality Assurance:** Dynamic, multi-criteria QA (Clarity, Accuracy, Completeness, Professional tone) with an 80% pass threshold.

**Enterprise Features:**
- **Finance System:** Tracks revenue, costs, P&L, margins, valuation, and integrates with Stripe.
- **Forecast Engine:** Provides 30-day load and revenue predictions using ML.
- **Marketplace API:** Supports partner integration with API keys, quotas, and job submission/retrieval.
- **Localization:** Multi-language (EN/ES/UR) and multi-currency (USD/EUR/GBP/INR/PKR) support with regional compliance.
- **Legal Compliance:** Includes ToS, Privacy Policy, Cookie Policy, and Accessibility Statement (GDPR/CCPA compliant).
- **Database Infrastructure:** Automated setup of 8 enterprise-specific databases.

**Platform Capabilities:**
- **Authentication:** Handles Notion, Google Drive, and Gmail via Replit Connectors OAuth with dynamic token refresh.
- **Alerting System:** Webhook, email, and Telegram notifications for failures.
- **Monitoring & Diagnostics:** Auto-Operator for self-healing, hourly heartbeats, synthetic tests, daily supervisor reports, and real-time alerts.
- **Metrics Aggregation:** Cross-database metrics system with daily System Pulse reports.
- **Edge Routing:** Railway fallback for specific endpoints (`/supervisor`, `/forecast`, `/metrics`, `/pulse`).
- **Resilience & Auto-Recovery:** Mechanisms for Stripe payment reconciliation, job retry, and media file validation.

**Visual Workflow Builder (Phases 51-55 - 100% Complete):**
- Provides a no-code drag-and-drop interface for creating automation workflows with live execution.
- Supports 6 node types (Trigger, AI Task, Condition, Action, Notification, Delay) and 5 pre-built templates.
- Includes dynamic configuration panels, real-time auto-save, and mobile optimization (Galaxy Fold 6).
- **Live Execution:** Run workflows directly from the builder with real-time visual feedback and execution logs.
- **Debug Mode:** Test workflows with simulated data before running with actual AI/Notion integration.
- Integrates with existing Notion databases, AI models (GPT-4o/mini), and notification systems (Email, Telegram).
- **2,850+ lines of code across 7 files** - Fully production-ready visual automation platform.

**Boss Mode UI v2.0:**
- A comprehensive UI/UX overhaul with a mobile-first dashboard, design system, and improved performance.
- Features enterprise security (rate limiting, CSRF, audit logs), a payments center, status and observability tools (SLOs), and a command palette.
- Includes AI quality systems, growth loops, internationalization, and extensive documentation.

**Enterprise Finale Features (Phases 81-100):**
- **Access & Security:** RBAC, JWT/OAuth, Disaster Recovery, Security Scanning, Privacy & Consent Management.
- **AI & Data:** AI Model Router, FinOps Reports, Data Warehouse Sync, Analytics Hub, Anomaly Detection, Training Audit, Continuous Learning Engine.
- **Operations:** Predictive Maintenance, Compliance Suite 2.0, Governance AI Advisor, Multi-Tenant Core, Tenant Billing, Adaptive Optimizer, Self-Heal v2, Enterprise Validator, Final Enterprise Report.

### Data Flow Architecture
The system utilizes a 13-database structure within Notion: 5 core databases (Automation Queue, Automation Log, EchoPilot Job Log, Notion Client, Notion Status) and 8 enterprise databases (Finance, Governance, Ops Monitor, Forecast, Region Compliance, Partners, Referrals, Growth Metrics). Automated schema enforcement ensures data integrity.

## External Dependencies

### Third-Party APIs
-   **Notion API**: Data storage, task queue, and audit trail via `notion-client` (OAuth2 via Replit Connectors).
-   **OpenAI API**: AI task processing and QA (GPT-4o, GPT-4o-mini) via `openai` SDK (Replit AI Integrations).
-   **Google Drive API**: File handling via `googleapiclient` (OAuth2 via Replit Connectors).
-   **Gmail API**: Automated reports and alerts via `googleapiclient` (Replit Gmail Connector).
-   **Telegram Bot API**: Instant notifications and commands.
-   **Stripe API**: Payment reconciliation and client billing.

### Python Dependencies
-   `notion-client`
-   `openai`
-   `google-api-python-client`, `google-auth`
-   `requests`
-   `schedule`
-   `python-dotenv`
-   `ReportLab` (for PDF generation)