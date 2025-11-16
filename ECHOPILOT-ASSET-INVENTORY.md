# EchoPilot + Levqor Complete Asset Inventory

**Generated:** November 16, 2025  
**Purpose:** Complete catalog of all code, jobs, pages, integrations, and documentation

---

## 1. Backend Code

### Core Application Files

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| Main Application | Flask App | `run.py` | Core Flask application with 2,980+ lines, registers all blueprints and routes |
| App Entry Point | Gunicorn Entry | `app.py` | Minimal entry point for Gunicorn |
| Backend Config | Configuration | `backend/config.py` | Backend configuration and settings |

### Backend Routes (Blueprints)

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| DSAR Endpoints | Blueprint | `backend/routes/dsar.py` | GDPR Data Subject Access Request handling |
| DSAR Admin | Blueprint | `backend/routes/dsar_admin.py` | Admin endpoints for DSAR management |
| GDPR Opt-Out | Blueprint | `backend/routes/gdpr_optout.py` | Right to object / opt-out system |
| Legal Pages | Blueprint | `backend/routes/legal.py` | Legal document serving |
| Legal Enhanced | Blueprint | `backend/routes/legal_enhanced.py` | Enhanced legal compliance features |
| Marketing Consent | Blueprint | `backend/routes/marketing.py` | Marketing consent management |
| Marketing Enhanced | Blueprint | `backend/routes/marketing_enhanced.py` | Double opt-in, preference center |
| Compliance Dashboard | Blueprint | `backend/routes/compliance_dashboard.py` | Compliance analytics and metrics |
| Billing Webhooks | Blueprint | `backend/routes/billing_webhooks.py` | Stripe billing event handlers |
| Stripe Checkout | Blueprint | `backend/routes/stripe_checkout_webhook.py` | Checkout session webhook handler |
| Daily Tasks | Blueprint | `backend/routes/daily_tasks.py` | Scheduled daily automation tasks |
| Sales Engine | Blueprint | `backend/routes/sales.py` | Lead capture and sales automation |
| ASE (Automated Sales) | Blueprint | `backend/routes/ase.py` | Automated sales engine endpoints |
| DFY Engine | Blueprint | `backend/routes/dfy_engine.py` | Done-For-You service automation |
| Follow-up Endpoints | Blueprint | `backend/routes/followup_endpoints.py` | Email follow-up automation |
| Support Chat | Blueprint | `backend/routes/support_chat.py` | AI support chat API endpoints |
| Stripe Check | Blueprint | `backend/routes/stripe_check.py` | Stripe configuration validation |
| Stripe Webhook Test | Blueprint | `backend/routes/stripe_webhook_test.py` | Webhook testing endpoints |
| Error Logging | Blueprint | `backend/routes/error_logging.py` | Custom error monitoring API (replaces Sentry) |

### Backend Services

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| DSAR Collectors | Service | `backend/services/dsar_collectors.py` | Data collection for DSAR exports |
| DSAR Exporter | Service | `backend/services/dsar_exporter.py` | ZIP export generation |
| GDPR Emails | Service | `backend/services/gdpr_emails.py` | GDPR notification emails |
| GDPR Enforcement | Service | `backend/services/gdpr_enforcement.py` | High-risk data blocking |
| Onboarding Automation | Service | `backend/services/onboarding_automation.py` | Automated onboarding workflows |
| Support AI | Service | `backend/services/support_ai.py` | AI-powered support chat logic |
| Support FAQ Loader | Service | `backend/services/support_faq_loader.py` | FAQ knowledge base loading |
| Support Tickets | Service | `backend/services/support_tickets.py` | Ticket creation and management |

### Backend Models

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| DSAR Request | SQLAlchemy Model | `backend/models/dsar_request.py` | DSAR request tracking |
| Error Event | SQLAlchemy Model | `backend/models/error_event.py` | Error monitoring storage |
| Sales Models | SQLAlchemy Models | `backend/models/sales_models.py` | Lead, DFYOrder, UpsellLog, Activity tracking |

### Backend Utilities

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| Email Helper | Utility | `backend/utils/email_helper.py` | Email sending utilities |
| Error Logger | Utility | `backend/utils/error_logger.py` | Error logging helper functions |
| ID Generator | Utility | `backend/utils/ids.py` | Unique ID generation |
| Resend Sender | Utility | `backend/utils/resend_sender.py` | Resend API integration |
| Storage Helper | Utility | `backend/utils/storage_helper.py` | File storage utilities |
| Support Context | Utility | `backend/utils/support_context.py` | Support chat context management |
| Telegram Helper | Utility | `backend/utils/telegram_helper.py` | Telegram bot notifications |
| WhatsApp Helper | Utility | `backend/utils/whatsapp_helper.py` | WhatsApp integration (placeholder) |

### Backend Security

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| Account Lockout | Security Module | `backend/security/lockout.py` | Brute-force protection |
| Security Logger | Security Module | `backend/security/logger.py` | Structured security event logging |

### Backend Billing

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| Auto Suspend | Billing Service | `backend/billing/auto_suspend.py` | Automated account suspension |
| Billing Config | Configuration | `backend/billing/config.py` | Billing system configuration |
| Dunning System | Billing Service | `backend/billing/dunning.py` | Payment retry and recovery |

### Backend CLI

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| DSAR Commands | Click CLI | `backend/cli/dsar_commands.py` | DSAR management CLI commands |

---

## 2. EchoPilot Engine (Schedulers, Monitors, Health Scripts)

### EchoPilot Core Scheduler

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| Scheduler | APScheduler | `monitors/scheduler.py` | Main scheduler with 21 automated jobs |

### Scheduled Jobs (21 Total)

| Job ID | Frequency | Function | Description |
|--------|-----------|----------|-------------|
| retention_aggregation | Daily 00:05 UTC | `run_retention_aggregation` | Daily retention metrics aggregation |
| slo_watchdog | Every 5 min | `run_slo_watchdog` | SLO breach monitoring |
| daily_ops_summary | Daily 09:00 London | `run_daily_ops_summary` | Daily ops health email |
| cost_prediction | Weekly Mon 02:10 | `run_cost_prediction` | Weekly cost forecasting |
| kv_costs | Hourly | `update_kv_costs` | KV cost tracking sync |
| growth_retention | Daily 00:10 UTC | `run_growth_retention` | Growth retention by source |
| governance_report | Weekly Sun 09:00 | `run_governance_report` | Weekly governance email |
| health_monitor | Every 6 hours | `run_health_monitor` | Health & uptime monitoring |
| cost_collector | Daily 01:00 UTC | `run_cost_collector` | Cost dashboard updates |
| sentry_check | Weekly | `run_sentry_health_check` | Sentry integration health |
| weekly_pulse | Weekly Fri 10:00 | `run_weekly_pulse` | Weekly summary report |
| expansion_verifier | Nightly 02:00 | `run_expansion_verifier` | Expansion pack verification |
| expansion_monitor | Weekly Fri 11:00 | `run_expansion_monitor` | Expansion monitoring report |
| intelligence_monitor | Every 15 min | `run_intelligence_monitor` | Intelligence monitoring cycle |
| weekly_intelligence | Weekly Sun 03:00 | `run_weekly_intelligence` | AI insights & trend analysis |
| billing_dunning | Every 6 hours | `process_billing_dunning` | Billing dunning processor |
| scaling_check | Hourly | `run_scaling_check` | Dynamic scaling check |
| synthetic_checks | Every 15 min | `run_synthetic_checks` | Synthetic endpoint checks |
| status_health_check | Every 5 min | `run_status_health_check` | Status page health snapshots |
| retention_cleanup | Daily 03:00 UTC | `run_retention_cleanup` | Data retention cleanup |
| alert_checks | Every 5 min | `run_alert_checks` | Alert threshold monitoring |
| dsar_cleanup | Daily 03:30 UTC | `run_dsar_cleanup` | DSAR export cleanup (7 day retention) |
| **critical_error_check** | **Every 10 min** | `check_critical_errors` | **Critical error Telegram alerts** |
| **daily_error_summary** | **Daily 09:00 UTC** | `send_daily_error_summary` | **Daily error email summary** |

### EchoPilot Monitors

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| AI Insights | Monitor | `monitors/ai_insights.py` | AI-powered insights generation |
| Alert Router | Monitor | `monitors/alert_router.py` | Smart alert routing logic |
| Anomaly AI | Monitor | `monitors/anomaly_ai.py` | Anomaly detection system |
| Autoscale | Monitor | `monitors/autoscale.py` | Dynamic autoscaling controller |
| Auto Tune | Monitor | `monitors/auto_tune.py` | Auto-tuning engine |
| Incident Response | Monitor | `monitors/incident_response.py` | Automated incident recovery |
| Runbooks | Monitor | `monitors/runbooks.py` | Operational runbooks |
| SLO Watchdog | Monitor | `monitors/slo_watchdog.py` | Service Level Objective monitoring |

---

## 3. Intelligence Layer & Expansion Packs

### Intelligence Layer API Endpoints

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| Feature Flags | Blueprint | `api/admin/flags.py` | DB-backed feature flag system |
| Profitability Ledger | Blueprint | `api/admin/ledger.py` | Profit tracking and analytics |
| Growth Intelligence | Blueprint | `api/admin/growth.py` | Behavioral cohort retention |
| Adaptive Pricing | Blueprint | `api/billing/pricing.py` | Dynamic pricing engine |
| Dynamic Discounts | Blueprint | `api/billing/discounts.py` | Profit-driven discount system |
| Billing Checkout | Blueprint | `api/billing/checkout.py` | Checkout flow management |
| Admin Insights | Blueprint | `api/admin/insights.py` | Admin analytics dashboard |
| Developer Keys | Blueprint | `api/developer/keys.py` | API key management |
| Partner Registry | Blueprint | `modules/partner_api/registry.py` | Partner API integration |
| Marketplace Listings | Blueprint | `modules/marketplace/listings.py` | Marketplace + Stripe Connect |

---

## 4. Frontend (Next.js 14 App Router)

### Total Pages: 119 Routes

### Core Marketing Pages

| Asset | URL | Path | Description |
|-------|-----|------|-------------|
| Homepage | `/` | `levqor-site/src/app/page.tsx` | Main landing page |
| Pricing | `/pricing` | `levqor-site/src/app/pricing/page.tsx` | Pricing tiers and plans |
| DFY Services | `/dfy` | `levqor-site/src/app/dfy/page.tsx` | Done-For-You services |
| DFY Pro | `/dfy-pro` | `levqor-site/src/app/dfy-pro/page.tsx` | Premium DFY tier |
| DFY Upgrade | `/dfy-upgrade` | `levqor-site/src/app/dfy-upgrade/page.tsx` | DFY upgrade flow |
| About | `/about` | `levqor-site/src/app/about/page.tsx` | Company information |
| FAQ | `/faq` | `levqor-site/src/app/faq/page.tsx` | Frequently asked questions |
| Contact | `/contact` | `levqor-site/src/app/contact/page.tsx` | Contact form |
| Support | `/support` | `levqor-site/src/app/support/page.tsx` | Support chat page |
| How It Works | `/how-it-works` | `levqor-site/src/app/how-it-works/page.tsx` | Product explanation |
| Demo | `/demo` | `levqor-site/src/app/demo/page.tsx` | Product demo |
| Tour | `/tour` | `levqor-site/src/app/tour/page.tsx` | Product tour |
| Roadmap | `/roadmap` | `levqor-site/src/app/roadmap/page.tsx` | Product roadmap |
| Changelog | `/changelog` | `levqor-site/src/app/changelog/page.tsx` | Product updates |
| Blog | `/blog` | `levqor-site/src/app/blog/page.tsx` | Blog/content hub |

### Trust & Legal Pages

| Asset | URL | Path | Description |
|-------|-----|------|-------------|
| Privacy Policy | `/privacy` | `levqor-site/src/app/privacy/page.tsx` | Privacy policy |
| Terms of Service | `/terms` | `levqor-site/src/app/terms/page.tsx` | Terms and conditions |
| Security | `/security` | `levqor-site/src/app/security/page.tsx` | Security overview |
| Cookies | `/cookies` | `levqor-site/src/app/cookies/page.tsx` | Cookie policy |
| GDPR | `/gdpr` | `levqor-site/src/app/gdpr/page.tsx` | GDPR compliance info |
| DPA | `/dpa` | `levqor-site/src/app/dpa/page.tsx` | Data Processing Agreement |
| SLA | `/sla` | `levqor-site/src/app/sla/page.tsx` | Service Level Agreement |

### Authentication & Dashboard

| Asset | URL | Path | Description |
|-------|-----|------|-------------|
| Sign In | `/signin` | `levqor-site/src/app/signin/page.tsx` | Magic link auth |
| Sign In Verify | `/signin/verify` | `levqor-site/src/app/signin/verify/page.tsx` | Email verification |
| Dashboard | `/dashboard` | `levqor-site/src/app/dashboard/page.tsx` | User dashboard |
| Dashboard Delivery | `/dashboard/delivery` | `levqor-site/src/app/dashboard/delivery/page.tsx` | DFY delivery tracking |

### Owner-Only Pages

| Asset | URL | Path | Description |
|-------|-----|------|-------------|
| **Owner Handbook** | `/owner/handbook` | `levqor-site/src/app/owner/handbook/page.tsx` | Internal operations manual |
| **Owner Error Dashboard** | `/owner/errors` | `levqor-site/src/app/owner/errors/page.tsx` | Error monitoring dashboard |

### Compliance & GDPR Pages

| Asset | URL | Path | Description |
|-------|-----|------|-------------|
| Cookie Settings | `/cookie-settings` | `levqor-site/src/app/cookie-settings/page.tsx` | Cookie consent management |
| Data Requests | `/data-requests` | `levqor-site/src/app/data-requests/page.tsx` | DSAR request form |
| Data Export Download | `/data-export/download` | `levqor-site/src/app/data-export/download/page.tsx` | DSAR download page |
| Privacy Tools | `/privacy-tools` | `levqor-site/src/app/privacy-tools/page.tsx` | Privacy tools hub |
| Privacy Opt-Out | `/privacy-tools/opt-out` | `levqor-site/src/app/privacy-tools/opt-out/page.tsx` | GDPR opt-out form |
| Email Unsubscribe | `/email-unsubscribe` | `levqor-site/src/app/email-unsubscribe/page.tsx` | Email opt-out |
| Marketing Consent | `/marketing-consent` | `levqor-site/src/app/marketing-consent/page.tsx` | Marketing preferences |
| Marketing Subscribe | `/marketing/subscribe` | `levqor-site/src/app/marketing/subscribe/page.tsx` | Newsletter signup |
| Marketing Confirm | `/marketing/confirm` | `levqor-site/src/app/marketing/confirm/page.tsx` | Double opt-in confirmation |
| Marketing Confirmed | `/marketing/confirmed` | `levqor-site/src/app/marketing/confirmed/page.tsx` | Confirmation success |
| Marketing Unsubscribe | `/marketing/unsubscribe` | `levqor-site/src/app/marketing/unsubscribe/page.tsx` | Marketing opt-out |
| Marketing Unsubscribed | `/marketing/unsubscribed` | `levqor-site/src/app/marketing/unsubscribed/page.tsx` | Unsubscribe confirmation |
| Settings Marketing | `/settings/marketing` | `levqor-site/src/app/settings/marketing/page.tsx` | Marketing settings |
| High Risk Data | `/high-risk-data` | `levqor-site/src/app/high-risk-data/page.tsx` | High-risk data policy |
| My Data | `/my-data` | `levqor-site/src/app/my-data/page.tsx` | Personal data portal |
| Delete Account | `/delete-account` | `levqor-site/src/app/delete-account/page.tsx` | Account deletion |

### Frontend Components

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| Support Chat | Component | `levqor-site/src/components/support/SupportChat.tsx` | AI support chat widget |
| Public Help Widget | Component | `levqor-site/src/components/support/PublicHelpWidget.tsx` | Public support widget |
| Dashboard Support | Component | `levqor-site/src/components/support/DashboardSupportChat.tsx` | Authenticated support chat |
| Cookie Banner | Component | `levqor-site/src/components/cookies/CookieBanner.tsx` | GDPR cookie consent banner |
| Cookie Modal | Component | `levqor-site/src/components/cookies/CookieModal.tsx` | Cookie preferences modal |
| High Risk Warning | Component | `levqor-site/src/components/HighRiskWarning.tsx` | High-risk data warning |
| High Risk Blocked Modal | Component | `levqor-site/src/components/HighRiskBlockedModal.tsx` | High-risk block notification |
| High Risk Warning Modal | Component | `levqor-site/src/components/HighRiskWarningModal.tsx` | High-risk warning modal |
| Pricing Component | Component | `levqor-site/src/components/Pricing.tsx` | Pricing table |
| Hero | Component | `levqor-site/src/components/Hero.tsx` | Homepage hero section |
| Footer | Component | `levqor-site/src/components/Footer.tsx` | Site footer |
| PublicNav | Component | `levqor-site/src/components/PublicNav.tsx` | Navigation bar |
| Testimonials | Component | `levqor-site/src/components/Testimonials.tsx` | Customer testimonials |
| Trust Section | Component | `levqor-site/src/components/TrustSection.tsx` | Trust indicators |

### Frontend Libraries

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| **Error Client** | Library | `levqor-site/src/lib/errorClient.ts` | **Error reporting to backend API** |
| Support Client | Library | `levqor-site/src/lib/supportClient.ts` | Support chat API client |
| Cookies | Library | `levqor-site/src/lib/cookies.ts` | Cookie consent utilities |
| Security | Library | `levqor-site/src/lib/security.ts` | Security helpers |
| High Risk Logger | Library | `levqor-site/src/lib/logHighRiskReject.ts` | High-risk rejection logging |

---

## 5. Integrations

| Integration | Components | Description |
|-------------|-----------|-------------|
| **Stripe** | Webhooks, checkout, dunning, pricing | Payment processing and billing |
| **Resend** | Email API, transactional emails | Email delivery via Resend API |
| **Telegram** | Bot notifications | Critical error alerts and admin notifications |
| **Sentry** | (Deprecated) | Being replaced by custom error monitoring |
| **Custom Error Monitoring** | Error logging API, Telegram alerts, email summaries | In-house error tracking system (v8.0) |
| **NextAuth v4** | Magic link authentication | User authentication via email |
| **SQLite/PostgreSQL** | Database ORM | Data persistence (SQLite dev, PostgreSQL prod) |

---

## 6. Scripts & Utilities

### Automation Scripts

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| Cost Collector | Python | `scripts/automation/cost_collector.py` | Cost tracking automation |
| Expansion Verifier | Python | `scripts/automation/expansion_verifier.py` | Expansion pack testing |
| Expansion Monitor | Python | `scripts/automation/generate_expansion_monitor.py` | Expansion monitoring reports |
| Health Monitor | Python | `scripts/automation/health_monitor.py` | System health monitoring |
| Intelligence Monitor | Python | `scripts/automation/intelligence_monitor.py` | Intelligence layer monitoring |
| Insights Quarterly | Python | `scripts/automation/insights_quarterly.py` | Quarterly insights generation |
| Partner Audit | Python | `scripts/automation/partner_audit.py` | Partner API auditing |
| Sentry Test | Python | `scripts/automation/sentry_test.py` | Sentry integration testing |
| Weekly Pulse | Python | `scripts/automation/weekly_pulse.py` | Weekly summary generation |

### Monitoring Scripts

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| Alerting | Python | `scripts/monitoring/alerting.py` | Alert threshold checks |
| Synthetic Checks | Python | `scripts/monitoring/synthetic_checks.py` | Endpoint health checks |
| Notion Go/NoGo | Python | `scripts/monitoring/notion_go_nogo_dashboard.py` | Notion dashboard integration |

### Operational Scripts

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| Ops Summary | Python | `scripts/ops_summary.py` | Operations summary generation |
| Governance Report | Python | `scripts/governance_report.py` | Governance reporting |
| Cost Predict | Python | `scripts/cost_predict.py` | Cost prediction analytics |
| DB Stability Test | Python | `scripts/db_stability_test.py` | Database stability testing |
| Dunning Smoke Test | Python | `scripts/dunning_smoke_test.py` | Dunning system testing |
| Run Dunning Cycle | Python | `scripts/run_dunning_cycle.py` | Manual dunning execution |
| Validate Levqor | Python | `scripts/validate_levqor.py` | System validation |

### Setup & Configuration Scripts

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| Add Vercel Secrets | Bash | `add_vercel_secrets.sh` | Vercel secret management |
| Backend Self Audit | Bash | `scripts/backend-self-audit.sh` | Backend self-audit |
| Backup DB | Bash | `scripts/backup_db.sh` | Database backup |
| Check Cache | Bash | `scripts/check_cache.sh` | Cache verification |
| Daily Burnin Check | Bash | `scripts/daily_burnin_check.sh` | Daily system health |
| EchoPilot Final Healthcheck | Bash | `scripts/echopilot-final-healthcheck.sh` | Comprehensive health check |
| Setup Stripe Prices | Bash | `scripts/setup_stripe_prices.sh` | Stripe price creation |
| Configure Cloudflare | Python | `scripts/configure_cloudflare.py` | Cloudflare setup automation |
| Create Stripe Prices | Python | `scripts/create_stripe_prices.py` | Stripe product/price creation |
| Create Stripe Pricing v7 | JavaScript | `scripts/create_stripe_pricing_v7.js` | v7 pricing setup |
| Setup Stripe Tiers | JavaScript | `scripts/setup-stripe-tiers.js` | Tier-based pricing |
| Create Enterprise Addons | JavaScript | `scripts/create_enterprise_addons.js` | Enterprise addon creation |
| Create Integrity Pack | Python | `scripts/create_integrity_pack_stripe_product.py` | Integrity pack Stripe product |
| Setup Developer Products | Python | `scripts/setup_developer_stripe_products.py` | Developer tier products |

### Sales & Follow-up Scripts

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| ASE Follow-up | JavaScript | `scripts/ase-followup.mjs` | Automated sales follow-ups |
| DFY Upsells | JavaScript | `scripts/dfy-upsells.mjs` | DFY upsell automation |

### Data & Analytics Scripts

| Asset | Type | Path | Description |
|-------|------|------|-------------|
| Aggregate Retention | Python | `scripts/aggregate_retention.py` | Retention data aggregation |
| Aggregate Growth Retention | Python | `scripts/aggregate_growth_retention.py` | Growth retention by source |
| Audit High Risk Workflows | Python | `scripts/audit_high_risk_workflows.py` | High-risk data auditing |

---

## 7. Knowledge Base & Documentation

### Knowledge Base

| Asset | Path | Description |
|-------|------|-------------|
| FAQ Content | `knowledge-base/faq.md` | Support AI FAQ content |
| Policies Content | `knowledge-base/policies.md` | Policy information for support |
| Pricing Content | `knowledge-base/pricing.md` | Pricing FAQ for support |

### Active Reports

| Asset | Path | Description |
|-------|------|-------------|
| **Error Monitoring System** | `ERROR_MONITORING_SYSTEM.md` | **Custom error tracking documentation (NEW v8.0)** |
| Expansion Monitor | `reports/EXPANSION-MONITOR.md` | Expansion pack monitoring report |
| Backend Automation Report | `BACKEND-AUTOMATION-REPORT.md` | Automation system status |
| Brutal Audit Report | `BRUTAL-AUDIT-REPORT.md` | Comprehensive system audit |
| Cleanup Summary | `CLEANUP-SUMMARY-2025-11-15.md` | Recent cleanup activities |
| EchoPilot Final Health Summary | `ECHOPILOT-FINAL-HEALTH-SUMMARY.md` | EchoPilot health status |
| Genesis v8.0 Readiness | `GENESIS-v8.0-READINESS.md` | v8.0 deployment readiness |
| Production Verification Report | `PRODUCTION-VERIFICATION-REPORT.md` | Production system verification |
| Security Hardening Report | `SECURITY-HARDENING-REPORT.md` | Security implementation status |
| Stripe Webhook Final Report | `STRIPE-WEBHOOK-FINAL-REPORT.md` | Stripe webhook testing results |

### Owner Documentation

| Asset | Path | Description |
|-------|------|-------------|
| replit.md | `replit.md` | Project overview and architecture |
| Start Here | `START_HERE.md` | Quick start guide |
| Production Checklist | `PRODUCTION_CHECKLIST.md` | Pre-launch checklist |
| Ready to Deploy | `READY_TO_DEPLOY.md` | Deployment readiness guide |
| Deployment Instructions | `DEPLOYMENT_INSTRUCTIONS.md` | Deployment guide |
| Backend Deployment Status | `BACKEND-DEPLOYMENT-STATUS.md` | Backend deployment tracking |

### Setup & Configuration Guides

| Asset | Path | Description |
|-------|------|-------------|
| 2FA Enablement Guide | `2FA-ENABLEMENT-GUIDE.md` | Two-factor auth setup |
| Access Review Checklist | `ACCESS-REVIEW-CHECKLIST.md` | Security access review |
| API Key Rotation | `API_KEY_ROTATION.md` | API key rotation procedures |
| Auth Setup Complete | `AUTH_SETUP_COMPLETE.md` | Authentication implementation |
| Automation Setup | `AUTOMATION-SETUP.md` | Automation configuration |
| Backup Restore Procedure | `BACKUP-RESTORE-PROCEDURE.md` | Backup and restore guide |
| Cloudflare Configuration | `CLOUDFLARE-CONFIGURATION.md` | Cloudflare setup |
| Notion Quick Start | `NOTION-QUICK-START.md` | Notion integration guide |
| Stripe Setup Checklist | `STRIPE_SETUP_CHECKLIST.md` | Stripe configuration |

### Implementation Status Documents

| Asset | Path | Description |
|-------|------|-------------|
| Billing Dunning Status | `BILLING_DUNNING_IMPLEMENTATION_STATUS.md` | Dunning system status |
| Compliance Implementation | `COMPLIANCE_IMPLEMENTATION_STATUS.md` | GDPR compliance status |
| DSAR Implementation | `DSAR_IMPLEMENTATION_SUMMARY.md` | DSAR system status |
| High Risk Blocking Status | `HIGH_RISK_BLOCKING_IMPLEMENTATION_STATUS.md` | Data blocking status |
| Support AI Implementation | `SUPPORT-AI-IMPLEMENTATION-SUMMARY.md` | AI support system status |
| Trust UX Implementation | `TRUST_UX_IMPLEMENTATION_STATUS.md` | Trust indicators status |

---

## 8. Legacy Directories & Archives

### Legacy Folders

| Asset | Type | Description |
|-------|------|-------------|
| `Levqor-backend/` | Legacy Directory | Old backend version (pre-restructure) |
| `levqor-fresh/` | Legacy Directory | Intermediate version during migration |
| `levqor-frontend/` | Legacy Directory | Old frontend before Next.js 14 migration |
| `archive/2025-11-15-legacy-docs/` | Archive | Archived documentation from Nov 15 cleanup |
| `archive/2025-11-15-legacy-logs/` | Archive | Archived logs from Nov 15 cleanup |

### Integrity Reports

| Asset | Path | Description |
|-------|------|-------------|
| Integrity Report JSON | `integrity_reports/integrity_report_1762866750.json` | System integrity snapshot |
| Integrity Evidence PDF | `integrity_reports/integrity_evidence_1762866750.pdf` | Evidence documentation |
| Finalizer Report JSON | `integrity_reports/finalizer_report_1762866750.json` | Finalizer pack report |

---

## Summary Statistics

- **Backend Routes**: 19 blueprints + 10 intelligence/expansion blueprints = **29 total blueprints**
- **Scheduled Jobs**: **21 automated jobs** (including 2 new error monitoring jobs)
- **Frontend Pages**: **119 routes** (marketing, legal, compliance, dashboards)
- **Frontend Components**: 25+ reusable components
- **Monitors**: 8 EchoPilot monitoring modules
- **Scripts**: 40+ automation, setup, and monitoring scripts
- **Integrations**: 8 external services (Stripe, Resend, Telegram, NextAuth, etc.)
- **Documentation**: 80+ markdown files (guides, reports, status docs)

---

**Last Updated:** November 16, 2025  
**Version:** EchoPilot v8.0 + Genesis  
**Next Steps:** See `ECHOPILOT-USED-VS-UNUSED.md` for usage classification
