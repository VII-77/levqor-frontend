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
        - High-risk data prohibition system blocking medical/legal/financial workflows.
        - **DSAR (Data Subject Access Request) Export System**:
            - Email-only delivery with OTP+token dual security (32-byte tokens, 6-digit OTP).
            - SQLite backend with dsar_requests, dsar_exports, dsar_audit_log tables.
            - Automatic data collection from users, referrals, API keys, partnerships, marketplace orders.
            - ZIP export with metadata.json, data.json, README.txt.
            - 24-hour download link expiry, 15-minute OTP expiry, one-time use security.
            - Full audit trail for compliance (request, generation, email, download events).
            - Rate limiting: One request per 24 hours per user.
            - PBKDF2-HMAC-SHA256 OTP hashing with 100k iterations.
            - Frontend pages: /privacy-tools (request UI), /data-export/download (OTP verification).
            - Backend endpoints: POST /api/data-export/request, POST /api/data-export/download.
            - Resend email integration with HTML/text templates.
            - Exports stored in ./exports/ directory (gitignored).
        - **Marketing Consent System (PECR/GDPR Double Opt-In)**:
            - user_marketing_consent table tracking all consent records with status, scope, source.
            - Three consent statuses: pending_double_opt_in, granted, revoked.
            - Double opt-in flow: POST /api/marketing/consent/start → email → GET /api/marketing/consent/confirm.
            - One-click unsubscribe: GET /api/marketing/unsubscribe?token=XYZ.
            - Frontend pages: /marketing/confirmed, /marketing/unsubscribed.
            - Email footer requirements documented in EMAIL_FOOTER_REQUIREMENTS.md.
            - System rule: Marketing emails ONLY to status="granted", transactional emails allowed without consent.
        - **High-Risk Data Firewall (GDPR/ICO Compliance)**:
            - Automatic blocking of medical, legal, and financial workflows at API level.
            - Keyword detection for prohibited content in all workflow fields.
            - risk_blocks audit table logging all blocked attempts with terms, IP, timestamp.
            - Instant rejection with clear error messages.
            - Frontend disclosure page at /risk-disclosure explaining policy.
            - Required for GDPR automated decision-making compliance and liability protection.
        - **Payment Dunning System (Stripe Integration)**:
            - billing_dunning_state table tracking payment failures with user_id, stripe_customer_id, subscription_id, status, next_action_at.
            - billing_events table logging all Stripe webhook events (invoice.payment_failed, invoice.paid) with audit trail.
            - Dunning states: none → day1_notice → day7_notice → day14_final → suspended.
            - Automated email notifications: Day 1 (service active), Day 7 (warning), Day 14 (final notice), Suspension.
            - Next.js webhook handler at /api/stripe/webhook forwarding to backend /api/internal/billing endpoints.
            - Account suspension enforcement: is_account_suspended() blocks POST /api/v1/intake when status="suspended".
            - Frontend billing banner (BillingWarningBanner) displays status-based warnings with Update Billing CTA.
            - GET /api/billing/status endpoint for frontend status checks (polls every 5 minutes).
            - APScheduler job every 6 hours processing dunning states and sending emails.
            - Automatic reset to status="none" when invoice.paid event received.
            - Email templates in billing/dunning_emails.py with Resend integration.
            - /billing page documents dunning timeline and policy for customer transparency.
        - **Data Retention & Deletion System (GDPR Compliance)**:
            - Centralized retention policy in retention/config.py with granular retention periods per table.
            - Automated cleanup engine (retention/cleanup.py) runs daily at 3:00 AM UTC via APScheduler.
            - Retention periods: API logs (90 days), status snapshots (30 days), DSAR exports (30 days), referrals (2 years), billing (7 years).
            - POST /api/privacy/delete-my-data endpoint for user-initiated data deletion (GDPR Article 17).
            - Deletes: workflows, logs, API keys, referrals, DSAR exports, anonymizes user account.
            - Preserves: billing_events, billing_dunning_state, Stripe records (7-year legal requirement).
            - Frontend "Delete My Data (GDPR)" button in /privacy-tools with confirmation modal.
            - Audit logging for all deletions via dsar_audit_log table.
            - Updated /privacy and /data-requests pages documenting retention policy and deletion process.
            - Physical DSAR export file cleanup integrated into daily retention job.
        - **Compliance Documentation (Internal)**:
            - ROPA (Record of Processing Activities) in docs/compliance/ropa.md documenting all data processing activities, legal basis, retention, subprocessors, and security measures.
            - DPIA (Data Protection Impact Assessment) in docs/compliance/dpia-levqor-automation.md assessing risks of AI automation and profiling with mitigation strategies.
            - LIA (Legitimate Interest Assessment) in docs/compliance/lia-marketing-and-analytics.md documenting legitimate interest processing for analytics and security.
            - All docs reviewed annually or upon major feature changes.
        - **Legal Page Updates**:
            - /privacy page includes comprehensive Marketing Communications section (7A) explaining double opt-in, consent logging, and withdrawal process.
            - /terms page includes High-Risk Data Prohibition section (7A) with clear policy and liability disclaimers.
            - /acceptable-use page enhanced with prohibited high-risk data section and system-level enforcement disclosure.
            - /risk-disclosure page already includes comprehensive high-risk data policy with enforcement details.
        - **Marketing Consent Frontend**:
            - /settings/marketing page for user preference management with unsubscribe functionality.
            - /unsubscribe page for one-click unsubscribe from email links (with email parameter).
            - /marketing/confirmed and /marketing/unsubscribed confirmation pages.
            - All pages follow PECR/GDPR double opt-in requirements.
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
- **Automated Jobs**: Extensive use of APScheduler for tasks like health monitoring, cost collection, Sentry testing, weekly pulse reports, insights generation, partner audits, intelligence layer operations, status snapshots (every 5 min), and daily retention cleanup (3am UTC).
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
    - High-risk data prohibition system with keyword scanning and automatic rejection.
    - **DSAR system for GDPR Article 15 compliance** with automated data export, secure delivery, and comprehensive audit logging.
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