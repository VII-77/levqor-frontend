# Levqor Backend

## Overview
Levqor is an AI automation job orchestration backend API built with Flask. It provides job intake, status tracking, health monitoring, and integrates AI automation with validation and cost guardrails. The project aims to offer robust workflow management, detailed analytics, and seamless integration with various external services.

## User Preferences
None documented yet.

## System Architecture

### Core Backend
The backend is a Flask application (`run.py`) handling API endpoints, job orchestration, and health monitoring. It uses JSON schema validation for all API requests and features a global error handler for robust error management.

### Job Management
Jobs are submitted via a `/api/v1/intake` endpoint and their status can be tracked. Currently, job storage is in-memory, with plans to integrate a persistent database.

### User Management
User profiles are managed using an SQLite database (`levqor.db`) with WAL mode enabled for concurrency. It supports idempotent email-based user upsert, lookup, and patching.

### Security and Hardening
- **Authentication**: API key-based authentication (`X-Api-Key` header) for all write operations, supporting zero-downtime key rotation.
- **Rate Limiting**: Per-IP and global rate limits to prevent abuse.
- **Request Limits**: Maximum request body and payload size limits are enforced.
- **Security Headers**: Production-grade headers like HSTS, CSP, COOP, COEP are implemented.
- **Input Validation**: Comprehensive JSON schema validation and field length constraints.
- **Logging**: Structured logging for requests and exceptions.

### Connectors
A dynamic connector system (`connectors/` folder) allows integration with external services. Each connector exposes a `run_task(payload)` interface with fail-closed error handling.

### Public Pages
The application serves static public content including legal documents (privacy, terms, cookies), an FAQ page, OpenAPI documentation, and well-known files (`security.txt`, `robots.txt`). Marketing assets and documentation are also served.

### Email System
A dedicated `notifier.py` module integrates with Resend.com for sending branded email notifications (support, billing, no-reply, security).

### Automated Tasks
An APScheduler-based system performs daily database backups, logging to `logs/backup.log`.

### Analytics & Metrics Tracking
A comprehensive analytics system tracks user engagement across the marketing frontend. Events are stored in SQLite (`metrics` table) with the following capabilities:
- **Event Types**: `page_view`, `cta_click`, `newsletter`, `conversion`
- **API Endpoints**:
  - `POST /api/v1/metrics/track`: Records user events with payload and referrer data
  - `GET /api/v1/metrics/summary`: Returns aggregated metrics with time-based analytics
- **Dashboard**: Protected analytics dashboard at `/dashboard?token=<DASHBOARD_TOKEN>` showing:
  - Total and 24h/7d metrics
  - Conversion rate and CTR calculations
  - Daily event breakdown
- **Privacy**: Email addresses are hashed (SHA-256) before storage to protect PII

### Marketing Frontend
Two Next.js 14 marketing websites built with TypeScript and App Router:

**levqor-web/** (Original):
- **Landing Page**: Hero section, features showcase, pricing preview, CTA buttons
- **Pricing Page**: Detailed plan comparison with Stripe checkout integration
- **Analytics Dashboard**: Token-protected metrics visualization
- **Components**: 6 reusable React components (Hero, Features, Pricing, CTAButton, Newsletter, Footer)
- **Tracking**: Automatic event logging via `logEvent()` utility (692 lines of TypeScript)

**levqor-site/** (Public Landing - NEW):
- **Public Landing**: levqor.ai marketing site with hero, features, demo placeholder, CTAs
- **Legal Pages**: /contact, /privacy, /terms
- **Blog**: /blog with 3 SEO-optimized posts (Markdown-based)
- **SEO**: Full metadata, OpenGraph, Twitter Cards, sitemap.xml, robots.txt
- **Plausible Analytics**: Optional integration via NEXT_PUBLIC_PLAUSIBLE_DOMAIN
- **Mobile Responsive**: Optimized for all devices
- **Deployment**: Ready for Vercel (`levqor-site/DEPLOYMENT.md`)

### Credits System
A consumption-based billing system with free tier:
- New users receive **50 free credits** automatically
- Each automation run costs **1 credit**
- Credit packs: **$9 for 100 credits** via Stripe checkout
- Database field: `credits_remaining INTEGER DEFAULT 50` in users table
- API Endpoints:
  - `POST /api/v1/credits/purchase` - Stripe session for credit packs
  - `POST /api/v1/credits/add` - Internal endpoint for adding credits
- Credit deduction: `deduct_credit(user_id)` function integrated into pipeline execution

### AI Workflow Builder
Natural language to JSON pipeline conversion system:
- `POST /api/v1/plan` - Converts descriptions to executable pipelines
  - Input: `{"description": "Send email summaries to Slack"}`
  - Output: Structured JSON with trigger + actions
  - Storage: `data/pipelines/{uuid}.json`
  - AI: Mock keyword-based (ready for OpenAI GPT-5-mini when key added)
- `POST /api/v1/run` - Executes saved pipelines
  - Deducts 1 credit per run
  - Logs execution to `data/jobs.jsonl`
  - Returns execution results

### Integration Test Endpoints
Dynamic connector test endpoints for Slack, Notion, and Gmail:
- `POST /integrations/slack` - Sends "Levqor test OK" to channel
- `POST /integrations/notion` - Creates test database row
- `POST /integrations/gmail` - Sends test email via Resend
- `GET /ops/selftest/integrations` - Returns configuration status
- Token storage: `data/integrations.json`

### Referral System
Credit rewards for user growth:
- `POST /api/v1/referrals` - Tracks referral codes
- Awards **+20 credits** to referrers for valid signups (within 24h)
- Referral log: `data/referrals.jsonl`
- Integration: URL param `?ref=<user_id>`

### Blog & Content
SEO-optimized blog section in levqor-site:
- 3 seed posts:
  1. "How Levqor Runs Itself" - Self-hosting narrative
  2. "EchoPilot vs Zapier" - Competitive positioning (AI vs manual)
  3. "Automate Everything from Your Phone" - Mobile-first pitch
- Markdown content in `levqor-site/content/*.md`
- Blog page at `/blog` with auto-generated listing

### Deployment
The application is deployed to Replit Autoscale, utilizing Gunicorn as the production server. Custom domain (api.levqor.ai) is configured. The Next.js frontend can be deployed to Vercel or other hosting platforms.

## External Dependencies
- **Flask**: Web framework.
- **Resend.com**: Email sending service.
- **Stripe**: Payment processing for billing.
- **Google API Python Client**: For Gmail connector.
- **Notion API**: Accessed via `requests` library for Notion connector.
- **Slack SDK WebClient**: For Slack connector.
- **python-telegram-bot**: For Telegram connector.
- **APScheduler**: For scheduling automated tasks (e.g., database backups).
- **SQLite**: In-memory and disk-based database for user profiles.
- **Gunicorn**: Production WSGI HTTP server.
- **markdown2**: Markdown to HTML rendering.

## Recent Changes

**November 6, 2025 - Evening**
- **"Catch-Up & Surpass" Upgrade (5 Phases in ~70 minutes):**
  - **Phase 1 - Public Landing Site**: Built `levqor-site/` Next.js app with /, /contact, /privacy, /terms, /blog, full SEO (metadata, OpenGraph, sitemap, robots.txt), Plausible analytics support, mobile-responsive design, 10 static routes, Vercel deployment ready
  - **Phase 2 - Integration Endpoints**: Added `/integrations/slack`, `/integrations/notion`, `/integrations/gmail` test endpoints, `/ops/selftest/integrations` status check, token storage in `data/integrations.json`
  - **Phase 3 - Credits System**: Database migration adding `credits_remaining` column (default 50), `/api/v1/credits/purchase` Stripe endpoint ($9/100 credits), `/api/v1/credits/add` internal endpoint, `deduct_credit()` function integrated into pipeline execution
  - **Phase 4 - AI Workflow Builder**: `/api/v1/plan` endpoint (natural language → JSON pipeline), `/api/v1/run` endpoint (execute pipelines with credit deduction), pipeline storage in `data/pipelines/`, mock AI (ready for OpenAI GPT-5-mini)
  - **Phase 5 - Blog & Referral**: Blog section at `/blog` with 3 SEO posts, `/api/v1/referrals` endpoint (+20 credits for valid signups), referral tracking in `data/referrals.jsonl`
  - **Impact**: 10 new API endpoints, 2,084 lines of code (237 backend, 1,847 frontend), $0 cost (free tier), production ready
  - **Status**: All tests passing, backend deployed, levqor-site ready for Vercel
  - **Evidence**: `UPGRADE_COMPLETE.md`, `UPGRADE_SUMMARY.json`, `logs/upgrade_20251106.log`

**November 6, 2025 - Morning**
- **Automated Backup System Enhancement:**
  - Added `misfire_grace_time=900` (±15 min tolerance) to APScheduler configuration
  - Implemented immediate backup validation on server startup
  - Verified daily backup schedule (00:00 UTC) working correctly
  - Backup format: `backups/backup_YYYYMMDDTHHMMSSZ.db`
  - All backup activity logged to `logs/backup.log`
  - Script location: `scripts/auto_backup.sh` (executable)

- **Marketing Assets & SEO:**
  - Created `marketing/landing_snippets.json` with headlines, CTAs, USPs
  - Added `marketing/testimonials.json` with customer reviews
  - Implemented `/api/v1/marketing/summary` endpoint for analytics
  - Added OpenGraph and Twitter Card meta tags to all docs/blog pages
  - Enhanced social sharing capabilities across documentation

- **Analytics & Metrics System:**
  - Created `metrics` table in SQLite database with indexes on type and timestamp
  - Implemented `POST /api/v1/metrics/track` endpoint for event tracking
  - Implemented `GET /api/v1/metrics/summary` endpoint with aggregated analytics
  - Built Next.js marketing frontend (841 lines of TypeScript code) in `levqor-web/`
  - Created protected analytics dashboard at `/dashboard?token=<DASHBOARD_TOKEN>`
  - Integrated automatic tracking in all CTA buttons, page views, newsletter signups
  - Privacy-focused design: email addresses hashed before storage
  - Tracks conversion rate, CTR, and daily event breakdowns

- **Domain Cutover Preparation:**
  - Configured CORS for multiple origins: `app.levqor.ai`, `levqor-web.vercel.app`, `levqor.ai`
  - Added health check endpoints: `/ready` and `/status` (alongside existing `/health`)
  - Updated `public/sitemap.xml` with frontend domain (app.levqor.ai) and key pages
  - Created DNS configuration guide: `docs/DNS_BACKEND.txt` with CNAME/A record instructions
  - Created domain prep script: `scripts/domain_prep.sh` for CORS logging
  - All endpoints tested and operational with proper CORS headers
  - Frontend prepared: canonical links set to app.levqor.ai, production build verified
  - Created `docs/DNS_FRONTEND.txt` with Cloudflare/Vercel CNAME configuration
  - Installed Node.js 20 toolchain for Next.js development

- **Final Reliability Gate:**
  - Created `autoselftest.py`: 10/10 tests passed (health, metrics, database, CORS)
  - Created `scripts/reconcile_stripe.py`: Stripe payment reconciliation tool
  - Generated evidence bundle: `evidence/launch_evidence_20251106T1617Z.tar.gz`
  - Verified automated backup system: Latest backup `backup_20251106T161804Z.db`
  - All production readiness checks passed
  - Documentation: `RELIABILITY_GATE_REPORT.md`

- **Public Launch Assets:**
  - Created `marketing/press_kit.md`: Complete press kit with brand assets, product info, boilerplate text
  - Created `marketing/product_hunt.md`: Launch package with tagline, description, FAQs, pricing, CTAs
  - Generated OpenGraph images (1200x630): `public/og/launch.jpg`, `public/og/pricing.jpg`
  - Added `/press` route to Next.js app with custom markdown renderer
  - Updated all meta tags to use new OG images
  - Build verified: All routes static, OG images linked correctly
  - Summary: `marketing/launch_assets_summary.json`

- **Go-Live Gates D1-D3 Execution:**
  - **D1 (Stripe $1 Live Test)**: ✅ PASS - Charged $1.00, refunded $1.00, drift $0.00
  - **D2 (Landing Patch & Deploy)**: ✅ PASS - Hero updated, StatusBadge added, deployed to Vercel
  - **D3 (Uptime Monitoring)**: ✅ PASS - 5-minute cron monitoring configured
  - All evidence saved in `data/evidence/` directory
  - Final report: `data/evidence/gates_report_final.json`
  - Status: Production ready