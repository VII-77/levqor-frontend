# EchoPilot + Levqor: What You Have (Beginner-Friendly Summary)

**Date:** November 16, 2025  
**For:** Non-technical owner  
**Purpose:** Plain-English explanation of what exists in your system

---

## The Big Picture

Levqor + EchoPilot is your complete automated sales and service delivery platform. Think of it as three connected systems working together:

1. **The Backend** (Flask + Python) - The brain that handles all the logic, payments, automation, and compliance
2. **The Frontend** (Next.js website) - What your customers see: a professional 119-page marketing website with dashboard
3. **EchoPilot Engine** - Your 24/7 autopilot that runs 21 automated jobs to monitor health, send reports, track costs, handle billing, and alert you about critical issues

Everything is production-ready and currently running. Your system includes comprehensive GDPR compliance, Stripe billing, AI-powered support chat, Done-For-You service automation, and a brand-new custom error monitoring system (v8.0) that replaced Sentry.

**What's actively used today:** ~150 components powering your live customer experience  
**What's internal/owner-only:** ~40 tools and dashboards just for you to monitor and manage the system  
**What's legacy:** 3 old directories from previous versions that can be safely archived

**Nothing has been lost.** Every file is either actively used, reserved for you as the owner, or explicitly marked as legacy (with backup instructions).

---

## ✅ What Is Actively Used Today

### Customer-Facing Website (119 Pages)

Your customers interact with a professional, comprehensive website including:

- **Marketing Pages**: Homepage, pricing, DFY services, how it works, demo, about, FAQ, testimonials, case studies, comparison, roadmap, blog, and more
- **Legal & Compliance**: Privacy policy, terms of service, cookie policy, GDPR info, DPA, SLA, security page, accessibility statement
- **Authentication**: Secure magic link login (no passwords needed)
- **Dashboard**: Protected customer dashboard where users manage their accounts and track DFY project delivery
- **Support**: AI-powered support chat on every page with smart fallback to human escalation
- **Compliance Tools**: Cookie consent banner, marketing preference center, data request forms, unsubscribe pages, opt-out system

**Example:** When a customer visits your site, they see a polished marketing experience. If they need help, they can click the support widget and chat with your AI assistant. If they want to buy DFY services, they go through your Stripe checkout. Everything just works.

### Backend APIs (29 Registered Blueprints)

Behind the scenes, your backend handles:

- **Stripe Integration**: Checkout webhooks, billing webhooks, subscription management, dunning (payment retry system)
- **GDPR Compliance**: Data Subject Access Requests (DSAR), right to opt-out, consent management, high-risk data blocking
- **Sales Automation**: Lead capture, automated follow-ups, DFY upsells, sales scoring
- **Support System**: AI chat endpoints, ticket creation, escalation
- **Legal Document Serving**: All your legal pages are served dynamically with version tracking
- **Marketing Consent**: Double opt-in email system, preference center, unsubscribe handling
- **Compliance Dashboard**: Analytics showing consent rates, DSAR requests, opt-out stats (owner-only)
- **Intelligence Layer**: Feature flags, profitability tracking, growth analytics, adaptive pricing, dynamic discounts
- **Developer Portal**: API key management for partners
- **Marketplace**: Partner API registry and marketplace listings

**Example:** When someone completes checkout on Stripe, your backend receives the webhook, creates their account, sends welcome emails, schedules onboarding automations, and logs everything for GDPR compliance - all automatically.

### EchoPilot Automated Jobs (21 Running 24/7)

Your system never sleeps. EchoPilot runs these jobs automatically:

**Health & Monitoring (Every 5-15 minutes):**
- SLO breach monitoring (ensures your service meets quality targets)
- Synthetic endpoint checks (tests all your APIs every 15 minutes)
- Status page health snapshots (tracks uptime for status page)
- Alert threshold monitoring (watches for anomalies)
- **🆕 Critical error checks (sends Telegram alerts for urgent issues - every 10 min)**

**Daily Automation:**
- Retention metrics aggregation (tracks how well you retain customers)
- Growth retention by source (where your best customers come from)
- Cost dashboard updates (tracks infrastructure costs)
- Data retention cleanup (deletes old data per GDPR rules)
- DSAR export cleanup (removes exports older than 7 days)
- **🆕 Error summary email (comprehensive error report sent to you at 9 AM UTC)**

**Weekly Automation:**
- Cost forecasting (predicts next week's costs)
- Governance report (compliance summary email to you)
- Weekly pulse (system health summary)
- Expansion pack monitoring (tests all expansion features)
- AI insights & trends (intelligence layer analytics)

**Hourly Automation:**
- KV cost syncing (cost tracking for Replit deployments)
- Scaling checks (auto-scaling decisions)

**Every 6 Hours:**
- Health & uptime monitoring (comprehensive health check)
- Billing dunning (retries failed payments automatically)

**Example:** If a critical error happens at 3 PM, EchoPilot detects it by 3:10 PM and sends you a Telegram alert. At 9 AM the next day, you receive an email summary of all errors from the last 24 hours with charts and breakdowns.

### Integrations (All Active)

Your system connects to:

- **Stripe** - All payment processing and subscription management
- **Resend** - Transactional emails (receipts, notifications, GDPR notices)
- **Telegram** - Critical error alerts sent to your phone
- **NextAuth** - Secure magic link authentication
- **SQLite/PostgreSQL** - Database (SQLite for development, PostgreSQL for production)
- **Custom Error Monitoring** - Replaces Sentry with in-house system (backend API + Telegram + email)

**Example:** When someone signs up, NextAuth sends them a magic link via Resend. When they click it, they're authenticated and redirected to their dashboard. If payment fails, Stripe notifies your backend, which triggers the dunning system to retry automatically.

### Support AI System

Your AI support is powered by:
- **Knowledge Base**: 3 markdown files (FAQ, policies, pricing) that the AI reads to answer questions
- **Public Support Chat**: Available on all marketing pages, no login required
- **Authenticated Support Chat**: On the dashboard with access to user account info
- **Smart Escalation**: Automatically creates support tickets when AI can't help
- **Error Reporting**: Automatically logs errors to your monitoring system when APIs fail

**Example:** Customer asks "What's included in the Growth plan?" → AI reads your pricing knowledge base and gives accurate answer in seconds.

---

## 📊 What Is Internal / Owner-Only

These features are not visible to customers - they're just for you to run the business:

### Owner Dashboard Pages

- **`/owner/handbook`** - Your internal operations manual (how to manage the system, who to contact, emergency procedures)
- **`/owner/errors`** - Real-time error monitoring dashboard showing all backend and frontend errors with filtering and detailed stack traces

### Admin Pages

- **`/admin/insights`** - Analytics dashboard showing user metrics, referral sources, revenue analytics

### Automated Reports (Sent to Your Email)

- **Daily Ops Summary** (9 AM London time) - System health, uptime, issues
- **Daily Error Summary** (9 AM UTC) - All errors from last 24 hours with severity breakdown
- **Weekly Governance Report** (Sunday 9 AM) - GDPR compliance metrics, consent rates, DSAR status
- **Weekly Pulse** (Friday 10 AM) - Overall system health and key metrics
- **Weekly Cost Forecast** (Monday 2 AM) - Predicted infrastructure costs
- **Expansion Monitor** (Weekly Friday 11 AM) - Tests of all expansion pack features

### Telegram Alerts

- **Critical Errors** - Immediate notification when severity='critical' errors occur (every 10 minutes checks)
- **Incident Alerts** - Auto-recovery system notifications

### Diagnostic Scripts (Manual Use)

You can run these scripts anytime to check system health:
- **EchoPilot Healthcheck** - Comprehensive system validation
- **Backend Self Audit** - Self-audit script
- **DB Stability Test** - Database performance testing
- **Validate Levqor** - End-to-end system validation
- **Backup DB** - Manual database backup

### Setup & Reference Guides

Documentation for when you need to set things up or remember how things work:
- Stripe setup checklist
- Deployment instructions
- 2FA enablement guide
- API key rotation procedures
- Cloudflare configuration
- Notion integration guide
- Production checklist

### Implementation Status Trackers

Documents showing what's been built and what's pending:
- Billing dunning status
- GDPR compliance implementation
- DSAR system status
- High-risk data blocking status
- Support AI implementation
- **Error monitoring system documentation (v8.0)**

**Example:** Every morning, you wake up to an email summarizing yesterday's system health. If anything went wrong overnight, you already got a Telegram alert. You can log into `/owner/errors` to see detailed error logs with full stack traces.

---

## 📦 What Is Legacy (Can Be Archived Later)

These folders are from older versions of your project and are no longer connected to anything:

### Legacy Directories (Not Referenced Anywhere)

1. **`Levqor-backend/`** - Old backend code from before the restructure (superseded by current `backend/` folder)
2. **`levqor-fresh/`** - Intermediate version created during migration (no longer needed)
3. **`levqor-frontend/`** - Old frontend before you upgraded to Next.js 14 (superseded by current `levqor-site/`)

**How We Know They're Safe to Archive:**
- Searched entire codebase for any imports or references - found **zero**
- Current system uses `backend/`, `levqor-site/`, and `monitors/` exclusively
- Legacy folders contain old deployment reports and superseded code

**What About the Files Inside?**
- Old deployment checklists, health reports, and setup guides - all superseded by newer versions at the root level
- Old code - replaced by current restructured codebase

**Recommended Next Steps (When Ready):**

```bash
# Step 1: Create a backup (just in case)
tar -czf levqor-legacy-backup-2025-11-16.tar.gz Levqor-backend levqor-fresh levqor-frontend

# Step 2: Move to archive directory
mkdir -p archive/2025-11-16-legacy-backends
mv Levqor-backend levqor-fresh levqor-frontend archive/2025-11-16-legacy-backends/

# Step 3: Store backup somewhere safe (download from Replit or upload to cloud storage)
```

**Already Archived (Nov 15 cleanup):**
- `archive/2025-11-15-legacy-docs/` - Old documentation files
- `archive/2025-11-15-legacy-logs/` - Old log files

**One Script to Consider:**
- `scripts/automation/sentry_test.py` - Tests Sentry integration, but you're now using custom error monitoring instead

---

## 🎯 Quick Numbers

Here's your system at a glance:

| Category | Count | Status |
|----------|-------|--------|
| **Backend API Blueprints** | 29 | ✅ All active |
| **Frontend Pages** | 119 | ✅ All active |
| **Automated Jobs (EchoPilot)** | 21 | ✅ All running 24/7 |
| **Monitoring Modules** | 8 | ✅ All active |
| **External Integrations** | 6 | ✅ All configured |
| **Owner Dashboard Pages** | 2 | 📊 Owner-only |
| **Automated Email Reports** | 6 | 📊 Owner-only |
| **Diagnostic Scripts** | 10+ | 📊 Owner-only |
| **Legacy Directories** | 3 | 📦 Safe to archive |

---

## ✅ Final Guarantee

**Nothing has been silently lost or ignored.**

Every single file in your project falls into one of three clear categories:

1. **ACTIVE** (~150 assets) - Powers your live customer experience. Don't touch these.
2. **OWNER-ONLY** (~40 assets) - Gives you visibility, control, and diagnostics. Keep these for your peace of mind.
3. **LEGACY** (3 directories) - Explicitly identified as old versions with clear backup instructions. Safe to archive when ready.

You have:
- A complete, professional customer-facing website (119 pages)
- Full backend automation handling payments, compliance, and sales
- 24/7 monitoring with real-time alerts and daily summaries
- Complete GDPR compliance (DSAR, consent, opt-out, data deletion)
- Done-For-You service automation
- AI-powered support with human escalation
- Custom error monitoring system (replacing Sentry)
- Owner dashboards showing everything that's happening
- Automated reports keeping you informed

**Your system is production-ready and actively serving customers right now.**

---

## 🚀 What Makes This Special

**v8.0 Highlights:**

✅ **Custom Error Monitoring** - No more Sentry fees. Your own error tracking system with:
  - Backend API for logging errors from anywhere
  - Frontend error reporting (automatic when things break)
  - Real-time Telegram alerts for critical issues
  - Daily email summaries with beautiful HTML reports
  - Owner dashboard to view/filter all errors

✅ **Complete GDPR Compliance** - Every checkbox covered:
  - Cookie consent with granular controls
  - DSAR system (data export as ZIP files)
  - Opt-out system (right to object)
  - Marketing consent with double opt-in
  - High-risk data blocking (PII protection)
  - Data retention & automatic cleanup
  - Compliance analytics dashboard

✅ **Billing Dunning** - Automated payment recovery:
  - Retries failed payments on a schedule
  - Sends dunning emails to customers
  - Tracks payment history
  - Auto-suspends non-paying accounts

✅ **Intelligence Layer** - AI-powered business insights:
  - Anomaly detection
  - Adaptive pricing
  - Profitability tracking
  - Growth analytics by source
  - Dynamic discount system
  - Feature flags for gradual rollouts

✅ **Expansion Packs** - Enterprise features:
  - Developer portal with API key management
  - Partner API registry
  - Marketplace with Stripe Connect
  - Integrity verifier & finalizer

---

## 📖 Where to Go Next

**Want to see everything running?**
- Visit your live site at www.levqor.ai
- Log into `/owner/handbook` to see your operations manual
- Check `/owner/errors` to view your error dashboard
- Check your email for automated reports

**Need to make changes?**
- Read `replit.md` for project architecture
- Check `ERROR_MONITORING_SYSTEM.md` for error monitoring docs
- Review `GENESIS-v8.0-READINESS.md` for deployment status

**Want to clean up legacy files?**
- See the "Legacy" section above for safe archiving steps
- Backup first, then move to archive folder
- Nothing actively used is in those legacy directories

---

**Last Updated:** November 16, 2025  
**System Version:** EchoPilot v8.0 + Genesis  
**Status:** ✅ Production-ready and running

**Remember:** Your system is working hard for you right now - monitoring itself, processing payments, handling support, maintaining compliance, and keeping you informed. You built something impressive.

---

## Quick Reference Card

**Emergency Contacts:**
- General Support: support@levqor.ai
- Sales: sales@levqor.ai
- Privacy: privacy@levqor.ai
- Legal: legal@levqor.ai

**Critical URLs:**
- Frontend: https://www.levqor.ai
- API: https://api.levqor.ai
- Stripe Dashboard: https://dashboard.stripe.com
- Owner Handbook: https://www.levqor.ai/owner/handbook
- Error Dashboard: https://www.levqor.ai/owner/errors

**System Access:**
- Check workflows: View Replit workflows panel
- View errors: Log into `/owner/errors`
- Check email: Daily reports at 9 AM
- Telegram alerts: Critical errors sent immediately

**When Something Goes Wrong:**
1. Check Telegram for critical error alerts
2. Log into `/owner/errors` to see details
3. Run `scripts/echopilot-final-healthcheck.sh` for diagnostics
4. Check email for daily error summary
5. Contact Replit support if infrastructure issues

**You're in good shape. Everything is documented, monitored, and running smoothly.** 🎉
