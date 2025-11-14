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
    - API key authentication with zero-downtime rotation.
    - Rate limiting and comprehensive security headers.
    - JSON schema validation.
    - Structured logging.
    - **GDPR/PECR Compliance Systems**:
        - Cookie consent banner with granular controls.
        - TOS acceptance enforcement with database tracking.
        - Marketing consent system with double opt-in verification.
        - High-risk data prohibition system blocking medical/legal/financial workflows via keyword detection.
        - **DSAR (Data Subject Access Request) Export System v2.0**: Email-based data exports sent as ZIP attachments (max 5MB) with no download links or tokens. Includes rate limiting (1 request per 24h), in-memory ZIP generation, and comprehensive audit logging. Frontend at `/data-requests`.
        - Payment Dunning System (Stripe integration) for managing failed payments with scheduled email notifications and account suspension logic.
        - Data Retention & Deletion System with configurable retention policies and automated cleanup, including a user-initiated "Delete My Data" feature.
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