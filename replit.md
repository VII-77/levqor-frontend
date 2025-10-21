# EchoPilot AI Automation Bot

## Overview
EchoPilot is an enterprise-ready AI automation platform that processes tasks from Notion databases using AI (OpenAI via Replit AI Integrations). It features a 60-second polling cycle, autonomous scheduling, dynamic quality assurance, and comprehensive job performance tracking. The platform includes core infrastructure for finance, forecasting, a marketplace API, localization, and legal compliance. Advanced operations cover payments, SLO tracking, incident paging, cost guardrails, autoscaling, RBAC, JWT authentication, disaster recovery, multi-tenancy, security scanning, compliance automation, predictive maintenance, continuous learning, and automated enterprise validation. All 130 phases are operational, including platform extensions like PWA support, an integrations hub, an AI data lake, predictive load balancing, self-healing 2.0, enterprise marketplace, compliance APIs, multi-region edge runtime, a partner portal, and a unified orchestration layer. It is deployed on a Replit Reserved VM and is production-ready.

## User Preferences
- Communication style: Simple, everyday language
- Development environment: Replit Android app on Galaxy Fold 6 (mobile device)
- Interface: Mobile-optimized instructions preferred

## System Architecture

### Core Architecture
EchoPilot uses a polling-based, event-driven system with Git integration, polling Notion every 60 seconds. Operations are traceable via Git commit hashes, and execution is prevented with a dirty working tree unless explicitly allowed. It leverages Replit Workflows for scheduling and Replit Connectors for OAuth-based integrations.

### SLO Configuration
All SLO thresholds are configurable via environment variables for Availability, P95/P99 Latency, Webhook Success, and Error Budget Burn.

### Application Structure and Key Features
**Core Automation:**
- **Task Processing:** Manages task execution, dynamic QA, metrics, and alerts.
- **Notion Integration:** Interacts with 13 Notion databases.
- **AI Integration:** Uses OpenAI models (GPT-4o for processing, GPT-4o-mini for QA) with cost/token tracking.
- **Quality Assurance:** Dynamic, multi-criteria QA with an 80% pass threshold.

**Enterprise Features:**
- **Finance System:** Tracks revenue, costs, P&L, and integrates with Stripe.
- **Forecast Engine:** Provides 30-day load and revenue predictions using ML.
- **Marketplace API:** Supports partner integration with API keys and quotas.
- **Localization:** Multi-language (EN/ES/UR) and multi-currency (USD/EUR/GBP/INR/PKR) support with regional compliance.
- **Legal Compliance:** Includes ToS, Privacy Policy, Cookie Policy, and Accessibility Statement (GDPR/CCPA compliant).
- **Database Infrastructure:** Automated setup of 8 enterprise-specific databases.

**Platform Capabilities:**
- **Authentication:** Handles Notion, Google Drive, and Gmail via Replit Connectors OAuth.
- **Alerting System:** Webhook, email, and Telegram notifications.
- **Monitoring & Diagnostics:** Auto-Operator for self-healing, heartbeats, synthetic tests, and reports.
- **Metrics Aggregation:** Cross-database metrics system with daily reports.
- **Edge Routing:** Railway fallback for specific endpoints.
- **Resilience & Auto-Recovery:** Mechanisms for payment reconciliation, job retry, and media file validation.

**Visual Workflow Builder:** Provides a no-code drag-and-drop interface for creating automation workflows with live execution, debug mode, and mobile optimization.

**Boss Mode UI v2.0:** A mobile-first dashboard with enterprise security, payments center, observability tools, and internationalization.

**Enterprise Finale Features:** Covers RBAC, JWT/OAuth, Disaster Recovery, Security Scanning, Privacy & Consent, AI Model Routing, FinOps Reports, Data Warehouse Sync, Analytics Hub, Anomaly Detection, Continuous Learning, Predictive Maintenance, Compliance Suite, Governance AI Advisor, Multi-Tenant Core, and Adaptive Optimization.

**Autonomous Maintenance:** Real-time anomaly detection, statistical analysis, and auto-heal triggers for system health, pushing uptime to 99.99%.

**Production Extras:** Includes a demo environment, smoke test suite, observability pack (request ID, log tailing, Prometheus metrics), security guardrails (JWT, WAF-style validation, CSP), DX tools (dev checker, unified test runner, pre-commit hooks), UX polish (custom 404, dark theme), and comprehensive documentation.

**Analytics & Operations:** Product analytics (telemetry, usage tracking), operator chat console, auto-scaler (CPU/RAM/queue load predictions), security scanner & SBOM generation, and advanced DR with backup integrity verification.

**Multi-Tenancy & Growth:** Tenantization hardening, FinOps cost & profitability tracking, compliance webhooks & audit API, edge queue for distributed job processing, and a growth & marketing referral system.

**Platform Extensions:** PWA & mobile app support, an integrations hub (9+ connectors), AI data lake & prompt analytics, predictive load & staff hints, self-healing 2.0, enterprise marketplace, external compliance APIs (GDPR, CCPA, SOC2), multi-region edge runtime, partner/affiliate portal, and the EchoPilot OS orchestration layer.

### Data Flow Architecture
The system uses a 13-database structure within Notion: 5 core and 8 enterprise databases. Automated schema enforcement ensures data integrity.

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
-   `ReportLab`