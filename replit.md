# Levqor Backend

## Overview
Levqor is a Flask-based job orchestration backend API for AI automation. It provides robust validation, cost management, job intake, status tracking, and health monitoring. The platform aims to be a scalable solution for automated workflows, featuring a Next.js frontend and an autonomous self-optimization layer with AI-powered monitoring, anomaly detection, predictive analytics, and auto-scaling.

## User Preferences
None documented yet.

## System Architecture

### UI/UX Decisions
The frontend uses Next.js 14 and TypeScript, offering an authentication flow with magic links via Resend and a protected dashboard. Public pages are dedicated to legal documentation and FAQs.

### Technical Implementations
- **Backend Core**: Flask application for API endpoints, job management, and health monitoring, deployed with Gunicorn.
- **Frontend Core**: Next.js 14 application using `src/app/` and NextAuth v4 for authentication.
- **Job Management**: Currently uses in-memory storage, with future plans for PostgreSQL or Redis.
- **User Management**: Idempotent email-based user management with SQLite for local development and PostgreSQL for production.
- **Security & Compliance**:
    - **Security Hardening (Complete)**:
        - Enhanced rate limiting with security event logging (20 req/min per IP burst, 200 req/min global, 60 req/min for protected paths).
        - Account lockout system (5 failed attempts = 15 minute lockout, 10 minute accumulation window).
        - Structured security logging with PII hashing (SHA256) for audit trail.
        - Protected path throttling for billing, admin, legal, marketing endpoints.
        - Frontend API guards with checkout rate limiting (3 attempts/min).
        - Authentication requirement for sensitive operations.
    - API key authentication with zero-downtime rotation.
    - Comprehensive security headers (HSTS, CSP, CORS, COOP, COEP, X-Frame-Options).
    - JSON schema validation.
    - Centralized error handling with correlation IDs.
    - **GDPR/PECR Compliance Systems** (10/10 Complete):
        - **Cookie Consent Banner**: Granular controls for analytics, marketing, and functional cookies with localStorage persistence.
        - **TOS Acceptance Tracking Backend**: API endpoints (POST `/api/legal/accept-terms`, POST `/api/legal/check-acceptance`) with versioned TOS tracking, IP logging, and timestamp recording. Database schema in `users` table tracks `terms_accepted_at`, `terms_version`, and `terms_accepted_ip`. Integrated with signin flow via `/api/consent/accept`.
        - **Marketing Consent System with Double Opt-In**: Full backend implementation (POST `/api/marketing/subscribe`, GET `/api/marketing/confirm`, POST `/api/marketing/unsubscribe`, POST `/api/marketing/status`) with secure token generation, 7-day token expiration, email confirmation flow, and idempotent operations. Frontend pages at `/marketing/subscribe` and `/marketing/confirmed`. Email sent via existing billing infrastructure.
        - **High-Risk Data Prohibition System**: Keyword detection blocking medical/legal/financial workflows with frontend disclaimers at `/high-risk-data` and `/risk-disclosure`.
        - **DSAR (Data Subject Access Request) Export System v2.0**: Email-based data exports sent as ZIP attachments (max 5MB) with no download links or tokens. Includes rate limiting (1 request per 24h), in-memory ZIP generation, comprehensive audit logging, and 30-day automated cleanup. Backend routes at `backend/routes/dsar.py` (5,851 lines). Frontend at `/data-requests`.
        - **GDPR Right to Object / Opt-out System**: Full end-to-end implementation (868 lines) allowing users to object to marketing, profiling, automation, and analytics processing. Includes API endpoints (GET/POST `/api/gdpr/opt-out`), enforcement helpers, audit logging, confirmation emails, and frontend UI at `/privacy-tools/opt-out`. Opt-out preferences enforced across email, automation, profiling, and analytics, included in DSAR exports.
        - **Payment Dunning System**: Stripe integration for managing failed payments with scheduled email notifications, account suspension logic, and APScheduler job "Billing dunning processor". Email enforcement distinguishes transactional vs. marketing.
        - **Data Retention & Deletion System**: Configurable retention policies with automated cleanup via APScheduler job "Daily retention cleanup". Includes user-initiated "Delete My Data" feature.
        - **Status Page & SLA Credits**: Public pages at `/status` (operational indicators, incident history) and `/sla-credits` (request form with validation).
        - **Dispute Resolution & Emergency Contacts**: Public pages at `/disputes` (4-step resolution process) and `/emergency-contacts` (SEV1 procedures).
    - **Compliance Documentation**: Internal compliance pack, ROPA, DPIA, and LIA documents.
    - **Legal Page Updates**: Comprehensive sections on marketing communications, high-risk data prohibition, and acceptable use.
    - **Marketing Consent Frontend**: Pages for user preference management and one-click unsubscribe.
- **Health & Monitoring**: Dedicated health endpoints, Sentry integration, and automated HTML email reports.
- **Public Content**: Static files for legal, FAQs, security, and OpenAPI documentation.
- **Database**: PostgreSQL (Neon) for production, SQLite for local development.
- **Referral Tracking**: Database and API for tracking referrals.
- **Analytics Dashboard**: Admin endpoint for user metrics and referral sources.
- **Intelligence Layer (v7.0)**: Features include Anomaly AI, Adaptive Pricing, Profitability Ledger, Smart Alert Router, DB-backed Feature Flags, Stabilize Mode, Auto-Tuning Engine, Growth Intelligence, Behavioral Cohort Retention, Dynamic Discount System, Profit-Driven Autoscale, and Weekly Governance Reporter.
- **Automated Jobs**: Extensive use of APScheduler for various tasks including health monitoring, cost collection, and intelligence layer operations.
- **Expansion Packs**: Integrity + Finalizer Pack, Developer Portal, Data Insights + Reports, Partner API + Registry, Marketplace + Stripe Connect, and Governance & Auditing.

### Feature Specifications
- **Job Orchestration**: Intake, status tracking, and simulated completion.
- **User Authentication**: NextAuth v4 with Resend magic link.
- **API Security**: API key system, rate limiting, and input validation.
- **Operational Visibility**: Health endpoints, Sentry, and automated summaries.
- **Scalability**: Designed for production with Gunicorn and Autoscale.
- **Legal Compliance**: Cookie consent, TOS acceptance, marketing consent, high-risk data prohibition, DSAR system, and unsubscribe mechanisms.

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