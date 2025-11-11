# Levqor Backend

## Overview
Levqor is a Flask-based job orchestration backend API designed for AI automation. It features robust validation, cost guardrails, job intake, status tracking, and comprehensive health monitoring. The project aims to provide a reliable and scalable solution for managing automated workflows, incorporating a full-stack approach with a Next.js frontend for user interaction.

## User Preferences
None documented yet.

## System Architecture

### UI/UX Decisions
The frontend is built with Next.js 14 and TypeScript, focusing on a clear authentication flow using Resend for magic link authentication. It includes a protected dashboard for authenticated users. Public pages serve legal documentation and FAQs.

### Technical Implementations
- **Backend Core**: Flask application managing API endpoints, job intake, status tracking, and health monitoring. It uses Gunicorn for production deployment, supporting 2 workers and 4 threads.
- **Frontend Core**: Next.js 14 application with `src/app/` for App Router pages, `src/auth.ts` for NextAuth v5 configuration, and `src/middleware.ts` for route protection.
- **Job Management**: In-memory storage for jobs, with planned migration to PostgreSQL or Redis.
- **User Management**: Idempotent email-based user upsert, lookup, get, and patch functionalities. Uses an SQLite database for local development and PostgreSQL for production.
- **Security**:
    - API key authentication (`X-Api-Key` header) for all POST/PATCH routes with support for zero-downtime key rotation.
    - Rate limiting (20 requests/minute per IP, 200 requests/minute global).
    - Comprehensive security headers: HSTS, CSP, COOP, COEP.
    - Request size limits (512KB max body, 200KB max payload).
    - JSON schema validation with `FormatChecker` for all API requests, including field length constraints and URL validation.
    - Structured logging with IP and User-Agent tracking.
- **Health & Monitoring**:
    - `/health`, `/public/metrics`, `/ops/uptime`, `/ops/queue_health`, `/billing/health` endpoints for system status.
    - Sentry integration for telemetry and error tracking.
- **Public Content**: Static files for legal documents (`privacy.html`, `terms.html`, `cookies.html`), FAQ (`index.html`), security information (`security.txt`), and API documentation (`openapi.json`).
- **Database**: PostgreSQL (Neon) for production, SQLite for local development with WAL mode. Email indexing and PRAGMA optimizations are applied.
- **Referral Tracking**: `referrals` database table, `POST /api/v1/referrals/track` endpoint, and integration into sign-in flow to capture referral parameters.
- **Analytics Dashboard**: `GET /admin/analytics` endpoint and React component for displaying user metrics and top referral sources.
- **Ops Summary Automation**: `scripts/ops_summary.py` for automated HTML email reports via Resend, covering system health, user metrics, and referral data.
- **Phase 6.4 Intelligence & Revenue Loop** (Nov 2025):
    - Anomaly AI: Statistical latency detection using Z-score + IQR methods
    - Adaptive Pricing: Usage-aware pricing model with load factors and performance bonuses
    - Profitability Ledger: Revenue/costs/payouts tracking via `/api/admin/ledger`
    - Smart Alert Router: Multi-channel notifications (Slack, Telegram, Email)
    - Feature Flags: DB-backed flags with admin UI at `/admin/flags`
    - Stabilize Mode: One-click automation freeze for emergencies
- **Phase 6.5 Intelligence Feedback & Growth Loop** (Nov 2025):
    - Auto-Tuning Engine: SLO/p95 target optimization at `/ops/auto_tune`
    - Growth Intelligence: Funnel analytics and ROI tracking by source
    - Behavioral Cohort Retention: DAU/WAU/MAU tracking by referral source
    - Dynamic Discount System: Usage-aware discount code generation
    - Profit-Driven Autoscale: Prevents scale-up when margin < 10%
    - Weekly Governance Reporter: Automated HTML email summaries
    - APScheduler: 11 automated jobs (retention, SLO, ops, cost, KV sync, growth, governance, health, cost collector, Sentry, pulse)
- **After-Launch Automation** (Nov 11, 2025):
    - Health Monitor: 6-hour endpoint checks for levqor.ai and api.levqor.ai/health
    - Cost Collector: Daily Stripe revenue and spend tracking
    - Sentry Test: Weekly error tracking health verification
    - Weekly Pulse: Friday summary of uptime, revenue, users, and churn
    - All automation integrated into APScheduler (scripts/automation/*.py)
- **Expansion: Integrity + Finalizer Pack** (Nov 11, 2025):
    - E2E integrity testing system with 10 comprehensive checks
    - Finalizer validation with 12 deployment readiness checks
    - PDF evidence report generation via reportlab
    - Stripe product configured (One-time: $49, Monthly: $19)
    - Complete CLI runner and documentation
    - Revenue-ready sellable feature for enterprise customers
    - Notion auto-logging for every integrity run with pass/fail status
- **Notion Integration** (Nov 11, 2025):
    - Helper module for Notion API integration
    - Automation scripts updated to log to Notion databases
    - System Health Log, Cost Dashboard, and Pulse tracking
    - Test script for verifying Notion connectivity
- **Expansion Monitoring Infrastructure** (Nov 11, 2025):
    - Enhanced weekly_pulse.py with 4 expansion metrics: integrity runs, template sales, API revenue, white-label inquiries
    - Extended cost_collector.py with Stripe fees, addon revenue, and net margin calculation
    - Integrity Pack auto-logs results to NOTION_INTEGRITY_DB_ID with pass/fail status
    - Created expansion_verifier.py for nightly health checks (Notion, Stripe, cost thresholds)
    - Created generate_expansion_monitor.py for weekly auto-generated EXPANSION-MONITOR.md reports
    - APScheduler expanded to 13 jobs: added expansion_verifier (nightly 2 AM UTC) and expansion_monitor (Friday 3 PM London)
    - Comprehensive tracking for all 4 expansion products: Integrity Pack, Template Library, API Tier, White-Label Edition
- **Developer Portal - Phase 1 Expansion** (Nov 11, 2025):
    - Complete B2D (Business-to-Developer) platform unlocking ecosystem growth
    - Database: `developer_keys` and `api_usage_log` tables for key management and analytics
    - Backend API: `/api/developer/keys` (POST/GET/DELETE), `/api/developer/usage` for quota tracking
    - Sandbox API: Mock endpoints at `/api/sandbox/*` (jobs, metrics, users) for safe testing
    - Billing: `/api/billing/checkout` for Stripe checkout session creation
    - Rate Limiting: Automatic quota enforcement per tier with 429 responses when exceeded
    - Three Tiers:
        - Sandbox: 1,000 calls/month - Free
        - Pro: 10,000 calls/month - $19/month (STRIPE_PRICE_DEV_PRO)
        - Enterprise: Unlimited - $199/month (STRIPE_PRICE_DEV_ENTERPRISE)
    - Frontend: `/developer` landing with upgrade flow, `/developer/keys` management UI, `/developer/docs` interactive documentation
    - OpenAPI Spec: Complete API documentation at `/public/openapi.json`
    - Notion Integration: API key creation/revocation auto-logged to NOTION_API_KEYS_DB_ID
    - Security: JWT-based authentication for key management, x-api-key header for sandbox API calls
    - Revenue Target: $35k ARR from developer tiers (100 sandbox → 50 Pro → 5 Enterprise by Month 3)
- **Data Insights + Reports - Phase 2 Expansion** (Nov 11, 2025):
    - Thought-leadership data product with anonymized platform insights
    - Modules: `modules/data_insights/` (aggregator, report_builder, uploader)
    - Backend API: `/api/insights/preview` (GET aggregated KPIs), `/api/insights/report` (POST generate PDF)
    - Data Sources: API usage, integrity runs, revenue, uptime from existing telemetry
    - PDF Reports: Generated via reportlab with quarterly metrics summary
    - Google Drive: Auto-upload with shareable public links (requires DRIVE_SERVICE_ACCOUNT_JSON)
    - Frontend: `/insights/data` page with metric cards and report generation UI
    - Automation: `scripts/automation/insights_quarterly.py` for scheduled report generation
    - Metrics Tracked: Revenue, MRR, API calls, uptime, integrity runs, net margin
    - Privacy: All data anonymized and aggregated, no PII included

### Feature Specifications
- **Job Orchestration**: Intake, status tracking, and simulated completion for development.
- **User Authentication**: NextAuth v5 with Resend magic link authentication for the frontend.
- **API Security**: Robust API key system, rate limiting, and extensive input validation.
- **Operational Visibility**: Multiple health and monitoring endpoints, Sentry integration, and automated operational summaries.
- **Scalability**: Designed for production with Gunicorn, Autoscale deployment, and planned database/queue enhancements.

## External Dependencies
- **Flask**: Web framework for the backend API.
- **Gunicorn**: WSGI HTTP Server for production deployment of Flask.
- **jsonschema**: For JSON schema validation of API requests.
- **requests**: For making HTTP requests within the backend.
- **Next.js**: Frontend framework.
- **TypeScript**: Programming language for the frontend.
- **NextAuth v5**: Authentication library for Next.js.
- **Resend**: Email API for magic link authentication and operational summaries.
- **PostgreSQL (Neon)**: Production database.
- **SQLite**: Local development database.
- **Sentry**: Error tracking and performance monitoring.
- **Stripe**: Payment processing integration (health endpoint exists, full integration planned).
- **reportlab**: PDF generation library for Integrity Pack evidence reports.
- **Notion**: Workspace integration for logging automation results and metrics.