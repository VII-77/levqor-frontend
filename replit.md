# Levqor Backend

## Overview
Levqor is a Flask-based job orchestration backend API designed for AI automation. It offers robust validation, cost guardrails, job intake, status tracking, and comprehensive health monitoring. The project aims to provide a reliable and scalable solution for managing automated workflows, incorporating a full-stack approach with a Next.js frontend. The platform includes an autonomous self-optimization layer with AI-powered monitoring, anomaly detection, predictive analytics, and auto-scaling capabilities.

## User Preferences
None documented yet.

## System Architecture

### UI/UX Decisions
The frontend is built with Next.js 14 and TypeScript, featuring a clear authentication flow using Resend for magic links and a protected dashboard for authenticated users. Public pages provide legal documentation and FAQs.

### Technical Implementations
- **Backend Core**: Flask application managing API endpoints, job intake, status tracking, and health monitoring, deployed with Gunicorn.
- **Frontend Core**: Next.js 14 application utilizing `src/app/` for App Router pages and NextAuth v4 for authentication.
- **Job Management**: In-memory storage for jobs, with future plans for PostgreSQL or Redis integration.
- **User Management**: Idempotent email-based user management with an SQLite database for local development and PostgreSQL for production.
- **Security & Compliance**:
    - API key authentication with zero-downtime rotation.
    - Rate limiting (20 requests/minute per IP, 200 requests/minute global).
    - Comprehensive security headers (HSTS, CSP, COOP, COEP).
    - Request size limits (512KB max body, 200KB max payload).
    - JSON schema validation with `FormatChecker`.
    - Structured logging with IP and User-Agent tracking.
    - **GDPR/PECR Compliance Systems**:
        - Cookie consent banner with granular controls (necessary, functional, analytics, marketing).
        - TOS acceptance enforcement with database tracking (version, timestamp, IP).
        - Middleware protection requiring TOS acceptance for all protected routes.
        - Marketing consent system with double opt-in verification.
        - User data schema includes terms_accepted_at, terms_version, terms_accepted_ip, marketing_consent, marketing_double_opt_in, marketing_double_opt_in_token.
- **Health & Monitoring**:
    - Dedicated endpoints for system status (`/health`, `/public/metrics`, etc.).
    - Sentry integration for telemetry and error tracking.
    - Automated HTML email reports via Resend (`scripts/ops_summary.py`).
- **Public Content**: Static files for legal documents, FAQs, security information, and OpenAPI documentation.
- **Database**: PostgreSQL (Neon) for production, SQLite for local development with WAL mode.
- **Referral Tracking**: Database table and API endpoint to track referrals.
- **Analytics Dashboard**: Admin endpoint and React component for user metrics and referral sources.
- **Intelligence Layer (v7.0)**:
    - Anomaly AI for statistical latency detection.
    - Adaptive Pricing based on usage and performance.
    - Profitability Ledger for tracking revenue, costs, and payouts.
    - Smart Alert Router for multi-channel notifications.
    - DB-backed Feature Flags with an admin UI.
    - Stabilize Mode for emergency automation freezes.
    - Auto-Tuning Engine for SLO/p95 target optimization.
    - Growth Intelligence for funnel analytics and ROI tracking.
    - Behavioral Cohort Retention tracking.
    - Dynamic Discount System.
    - Profit-Driven Autoscale.
    - Weekly Governance Reporter.
- **Automated Jobs**: Extensive use of APScheduler for tasks like health monitoring, cost collection, Sentry testing, weekly pulse reports, insights generation, partner audits, and intelligence layer operations.
- **Expansion Packs**:
    - **Integrity + Finalizer Pack**: End-to-end integrity testing, deployment readiness checks, PDF evidence reports, and Stripe product integration.
    - **Developer Portal**: B2D platform with API key management, sandbox API, billing tiers, and API documentation.
    - **Data Insights + Reports**: Anonymized platform insights, PDF report generation, and Google Drive integration.
    - **Partner API + Registry**: Third-party developer ecosystem with registration, webhooks, HMAC authentication, and Notion integration.
    - **Marketplace + Stripe Connect**: Partner-built modules marketplace with automated revenue sharing and Stripe Connect for payouts.
    - **Governance & Auditing**: Security and compliance framework for the partner ecosystem, including policy engine, audit system, and review cycles.
- **Notion Integration**: Extensive integration for logging automation results, system health, costs, pulse, API keys, partner registrations, marketplace listings, and sales.

### Feature Specifications
- **Job Orchestration**: Intake, status tracking, and simulated completion.
- **User Authentication**: NextAuth v4 with Resend magic link.
- **API Security**: API key system, rate limiting, and input validation.
- **Operational Visibility**: Health endpoints, Sentry, and automated summaries.
- **Scalability**: Designed for production with Gunicorn and Autoscale, with planned database/queue enhancements.
- **Legal Compliance**:
    - Cookie consent system (PECR/GDPR compliant) with localStorage persistence.
    - TOS acceptance system with interstitial page, database tracking, and middleware enforcement.
    - Marketing consent system with double opt-in confirmation via email.
    - Unsubscribe mechanism with audit trail logging.
    - Protected routes: /workflow, /dashboard, /account, /settings, /developer, /api/workflows.

## External Dependencies
- **Flask**: Web framework.
- **Gunicorn**: WSGI HTTP Server.
- **jsonschema**: JSON schema validation.
- **requests**: HTTP requests.
- **Next.js**: Frontend framework.
- **TypeScript**: Frontend language.
- **NextAuth v4**: Authentication library.
- **Resend**: Email API.
- **PostgreSQL (Neon)**: Production database.
- **SQLite**: Local development database.
- **Sentry**: Error tracking and monitoring.
- **Stripe**: Payment processing.
- **reportlab**: PDF generation.
- **Notion**: Workspace integration.
- **APScheduler**: Job scheduling.