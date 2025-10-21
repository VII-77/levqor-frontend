# EchoPilot AI Automation Bot

## Overview
EchoPilot is a 115-phase enterprise-ready AI automation platform designed to process tasks from Notion databases using AI (OpenAI via Replit AI Integrations). It features a 60-second polling cycle, autonomous scheduling, dynamic quality assurance (80% QA threshold), and comprehensive job performance tracking (costs, QA scores, token usage, latency).

The platform includes core infrastructure for finance, forecasting, a marketplace API, localization, and legal compliance. Advanced operations cover payments, SLO tracking, incident paging, cost guardrails, and autoscaling. The enterprise suite adds RBAC, JWT authentication, disaster recovery, multi-tenancy, security scanning, compliance automation, predictive maintenance, continuous learning, and automated enterprise validation.

**New in Phases 111-115**: Product analytics with DAU/WAU/MAU tracking, operator chat console with secure command execution, auto-scaler with load predictions, security scanner with SBOM generation, and advanced DR restore verification.

It is deployed on a Replit Reserved VM and is production-ready with automated validation and reporting.

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

**Autonomous Maintenance (Phase 102):**
- **Anomaly Guard:** Real-time anomaly detection with 5-minute polling cycle monitoring health endpoint latency and system resources.
- **Statistical Analysis:** Calculates rolling mean/stdev using 50-sample window to identify latency outliers (>3σ threshold).
- **Auto-Heal Triggers:** Automatically invokes self-heal script when health check fails, CPU/MEM >90%, or latency anomaly detected.
- **NDJSON Logging:** Comprehensive event logging to `logs/anomaly_guard.ndjson` for forensic analysis and trend detection.
- **Reliability Target:** Pushes system uptime from 99.9% → 99.99% through early warning and zero-touch recovery.

**Production Extras (E1-E7 - 100% Complete):**
- **Extra 1 - Demo Environment:** Idempotent demo data seeder (`scripts/seed_demo.py`) with 5 categories (clients, automations, finance, growth, partners). DEMO_MODE support with read-only protection, demo banner, and write operation blocking.
- **Extra 2 - Smoke Test Suite:** Basic smoke tests (`scripts/smoke.sh`, 19+ tests, ~30s) and advanced smoke tests (`scripts/smoke_advanced.sh`, 14 tests, ~60s) with color-coded output, NDJSON logging, and CI/CD integration. Complete documentation in `docs/SMOKE_TESTS.md`.
- **Extra 3 - Observability Pack:** Request ID middleware with X-Request-ID header propagation. Real-time log tailing API (`GET /api/logs`) with 8 log file support and request ID filtering. Prometheus metrics endpoint (`GET /metrics`) with HTTP requests, latency quantiles, database health, and scheduler metrics.
- **Extra 4 - Security Guardrails:** JWT authentication system (access 15min + refresh 24hr) with token rotation, blacklist-based revocation, and 4 API endpoints (`/api/auth/*`). WAF-style request validation detecting SQL injection, XSS, and path traversal with audit logging. CSP headers and comprehensive security documentation.
- **Extra 5 - DX Tools:** Development environment checker (`scripts/dev_check.py`) validating Python, dependencies, env vars, directories, git, database, port, and disk space. Unified test runner (`scripts/test_all.sh`) orchestrating 8 test suites. Pre-commit hooks (`.pre-commit-config.yaml`) with black, isort, flake8, bandit, shellcheck, and custom validators.
- **Extra 6 - UX Polish:** Custom 404 page with search box, keyword routing, and navigation links. Mobile-responsive dark theme design.
- **Extra 7 - Documentation:** Comprehensive SECURITY.md (400+ lines) covering 7 security features, best practices, vulnerability reporting, compliance standards (OWASP, GDPR, CCPA, SOC 2), and security checklists.

**Phases 111-115 - Analytics & Operations (100% Complete):**
- **Phase 111 - Product Analytics:** DAU/WAU/MAU tracking with client-side telemetry (`static/js/telemetry.js`), event ingestion API (`POST /api/analytics/event`), usage summary API (`GET /api/analytics/usage`), daily rollup job at 03:15 UTC, and comprehensive documentation in `docs/ANALYTICS.md`.
- **Phase 112 - Operator Chat Console:** Secure admin copilot with allow-listed commands (`restart_scheduler`, `run_backup`, `reconcile_payments`, `tail_logs`, etc.), dry-run by default with `confirm=true` execution, full audit trail in `logs/ops_console.ndjson`, and APIs at `POST /api/ops/command` and `GET /api/ops/commands`.
- **Phase 113 - Auto-Scaler:** CPU/RAM/queue load predictions with `scripts/autoscaler.py`, linear regression trend analysis, scaling recommendations (scale_up/scale_down), metrics logging to `logs/autoscaler.ndjson`, and integration with scheduler.
- **Phase 114 - Security Scanner & SBOM:** Automated security scanning with `scripts/security_scanner.py`, pip audit integration, secret scanning with false positive filtering, SBOM generation (65 components), and comprehensive reports in `logs/security_report.json` and `logs/sbom.json`.
- **Phase 115 - Advanced DR:** Backup integrity verification with `scripts/dr_restore_check.py`, dry-run restore testing, tarball validation, metadata verification, and DR reports in `logs/dr_restore_report.json`.

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