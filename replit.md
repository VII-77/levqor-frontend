# Levqor Backend

## Overview
Levqor is a Flask-based job orchestration backend API designed for AI automation. It offers robust validation, cost management, job intake, status tracking, and health monitoring. The platform aims to be a scalable solution for automated workflows, featuring a Next.js frontend and an autonomous self-optimization layer with AI-powered monitoring, anomaly detection, predictive analytics, and auto-scaling. Its business vision includes providing a comprehensive solution for automated sales engines, client delivery, and revenue generation, with a focus on compliance and security.

## User Preferences
None documented yet.

## System Architecture

### UI/UX Decisions
The frontend utilizes Next.js 14 and TypeScript, providing an authentication flow via magic links (Resend) and a protected dashboard. Public pages are dedicated to legal documentation and FAQs.

### Technical Implementations
- **Backend Core**: Flask application for API endpoints, job management, and health monitoring, deployed with Gunicorn.
- **Frontend Core**: Next.js 14 application using `src/app/` and NextAuth v4 for authentication.
- **Job Management**: In-memory storage with future plans for PostgreSQL or Redis.
- **User Management**: Idempotent email-based user management with SQLite for local development and PostgreSQL for production.
- **Error Monitoring System (v8.0)**: Custom in-house error tracking solution replacing Sentry. Features include backend error logging API (`/api/errors/log`, `/api/errors/recent`), frontend error reporting client (`errorClient.ts`), owner dashboard (`/owner/errors`), EchoPilot scheduler integration for critical error Telegram alerts (every 10 min) and daily email summaries (9 AM UTC). Supports severity levels (info, warning, error, critical) with full stack trace capture.
- **Security & Compliance**:
    - **Security Hardening**: Enhanced rate limiting, account lockout system, structured security logging (PII hashing), protected path throttling, frontend API guards, API key authentication with zero-downtime rotation, comprehensive security headers (HSTS, CSP, CORS, etc.), JSON schema validation, and centralized error handling.
    - **GDPR/PECR Compliance Systems**: Cookie consent banner, TOS acceptance tracking (versioned, re-acceptance workflow, email notifications), marketing consent system with double opt-in and granular preference center, high-risk data prohibition system (keyword detection, severity levels), DSAR export system (email-based ZIP attachments), GDPR Right to Object/Opt-out system, payment dunning system (Stripe integration), data retention & deletion system, status page & SLA credits, dispute resolution & emergency contacts. Includes a compliance analytics dashboard.
    - **Compliance Documentation**: Internal compliance pack, ROPA, DPIA, and LIA documents.
- **Health & Monitoring**: Dedicated health endpoints, Sentry integration, and automated HTML email reports.
- **Public Content**: Static files for legal, FAQs, security, and OpenAPI documentation.
- **Database**: PostgreSQL (Neon) for production, SQLite for local development.
- **Referral Tracking**: Database and API for tracking referrals.
- **Analytics Dashboard**: Admin endpoint for user metrics and referral sources.
- **Intelligence Layer (v7.0)**: Features include Anomaly AI, Adaptive Pricing, Profitability Ledger, Smart Alert Router, DB-backed Feature Flags, Stabilize Mode, Auto-Tuning Engine, Growth Intelligence, Behavioral Cohort Retention, Dynamic Discount System, Profit-Driven Autoscale, and Weekly Governance Reporter.
- **Automated Jobs**: Extensive use of APScheduler for various tasks including health monitoring, cost collection, and intelligence layer operations.
- **Expansion Packs**: Integrity + Finalizer Pack, Developer Portal, Data Insights + Reports, Partner API + Registry, Marketplace + Stripe Connect, and Governance & Auditing.
- **Revenue Engine**: Implemented a comprehensive revenue engine including enhanced website features (landing page, pricing, DFY sales, trust pages), automated sales engines (lead magnet, scoring, DFY upsells, client delivery), and advanced revenue generation strategies (traffic engine, conversion engine, retention & expansion, scale engine).

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
- **APScheduler**: Job scheduling.