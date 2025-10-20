# EchoPilot Platform Runbook

## Quick Reference

**Dashboard:** https://echopilotai.replit.app/dashboard  
**Status:** Production-ready, autonomous operation  
**Version:** Enterprise Expansion (Phases 33-40 complete)

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Environment Variables](#environment-variables)
3. [API Endpoints](#api-endpoints)
4. [Scheduler Tasks](#scheduler-tasks)
5. [Troubleshooting](#troubleshooting)
6. [Security](#security)

---

## System Overview

EchoPilot is an enterprise-ready AI automation platform with:
- Autonomous task processing (60-second polling)
- Real payment processing (Stripe)
- Compliance & audit tools (GDPR, SOC-lite)
- Adaptive AI pricing
- Referral & growth engine
- Multi-region data sync
- AI-powered operational intelligence

**Architecture:** Flask (Gunicorn) + Notion + OpenAI + Stripe  
**Deployment:** Replit Reserved VM  
**Monitoring:** Auto-healing, predictive alerts, health probes

---

## Environment Variables

### Core (Required)
- `DASHBOARD_KEY` - Dashboard authentication key
- `AI_INTEGRATIONS_OPENAI_API_KEY` - OpenAI API key
- `AI_INTEGRATIONS_OPENAI_BASE_URL` - Custom OpenAI base URL
- `AUTOMATION_QUEUE_DB_ID` - Notion queue database ID
- `AUTOMATION_LOG_DB_ID` - Notion log database ID
- `JOB_LOG_DB_ID` - Notion job log database ID

### Payments (Phase 33)
- `STRIPE_MODE` - "test" or "live" (default: test)
- `STRIPE_SECRET_KEY` - Stripe test mode secret key
- `STRIPE_SECRET_LIVE` - Stripe live mode secret key (optional)
- `STRIPE_WEBHOOK_SECRET` - Stripe webhook signing secret

### Pricing & Operations
- `DEFAULT_RATE_USD_PER_MIN` - Base pricing rate (default: 5.0)
- `SESSION_SECRET` - HMAC signing secret for URLs

### Multi-Region (Phase 39)
- `RAILWAY_FALLBACK_PATH` - Optional replica sync destination

### Scheduler
- `SCHED_BRIEF_UTC` - CEO brief time (default: 08:00)
- `SCHED_REPORT_UTC` - Daily report time (default: 09:00)
- `SCHED_SELFHEAL_EVERY_HOURS` - Self-heal interval (default: 6)

---

## API Endpoints

### Phase 33: Payments
- **POST /api/payments/create-invoice**
  - Body: `{"amount": float, "email": string}`
  - Auth: X-Dash-Key required
  - Returns: Stripe checkout URL
  - Test: `curl -H "X-Dash-Key:$KEY" -d '{"amount":5.0}' /api/payments/create-invoice`

### Phase 34: Customer Experience
- **GET /api/customer/signed-url/<client_id>**
  - Auth: X-Dash-Key required
  - Returns: Signed download URL (24h expiry)
  
- **POST /api/customer/unsubscribe**
  - Body: `{"email": string}`
  - Returns: Success confirmation

### Phase 35: Compliance
- **GET /api/compliance/export-data**
  - Auth: X-Dash-Key required
  - Returns: GDPR export manifest with SHA256 hashes

### Phase 36: Pricing AI
- **POST /api/pricing/optimize**
  - Auth: X-Dash-Key required
  - Returns: Pricing recommendation based on QA scores & margins

### Phase 37: Growth
- **POST /api/growth/referral/new**
  - Auth: X-Dash-Key required
  - Returns: New referral code (EP-XXXXXX) with share URL

### Phase 38: Audit
- **GET /api/audit/report**
  - Auth: X-Dash-Key required
  - Returns: SOC-lite audit report with hash chain

### Phase 39: Multi-Region
- **POST /api/regions/sync**
  - Auth: X-Dash-Key required
  - Returns: Replica sync status (files copied)

### Phase 40: AI Ops
- **POST /api/brain/decide**
  - Auth: X-Dash-Key required
  - Returns: AI-generated operational recommendations (GPT-4o-mini)

### Legacy Endpoints
- **GET /api/system-health** - 5-point health check
- **POST /api/self-heal** - Retry failed jobs
- **POST /api/exec/brief** - Generate CEO brief
- **GET /api/finance-metrics** - Revenue & cost metrics
- **GET /api/live-ops** - CPU/Memory/Disk + rate limiting stats

---

## Scheduler Tasks

Automated tasks run via `scripts/exec_scheduler.py`:

| Task | Schedule | Endpoint/Script |
|------|----------|----------------|
| Heartbeat | Every 60 seconds | Internal tick |
| Health Probe | Daily 07:55 UTC | /api/system-health |
| CEO Brief | Daily 08:00 UTC | /api/exec/brief |
| Daily Report | Daily 09:00 UTC | /api/finance-metrics + /api/metrics-summary |
| Self-Heal | Every 6 hours | /api/self-heal |
| Predictive Alerts | Every hour | scripts/predictive_alerts.py |
| **Pricing AI** | **Daily 03:00 UTC** | **/api/pricing/optimize** |
| **Weekly Audit** | **Monday 00:30 UTC** | **/api/audit/report** |
| **Replica Sync** | **Every 2 hours** | **/api/regions/sync** |
| **AI Ops Brain** | **Every 12 hours** | **/api/brain/decide** |

**Control:**
- View status: Dashboard → "Automations Scheduler"
- Manual start: Dashboard → "▶️ Start Scheduler"
- Manual stop: Dashboard → "⏹️ Stop Scheduler"

---

## Troubleshooting

### Payments (Phase 33)

**Issue:** Invoice creation fails  
**Fix:**
1. Verify `STRIPE_SECRET_KEY` is set
2. Check Stripe mode: `echo $STRIPE_MODE` (should be "test")
3. Test with minimum amount: `{"amount": 0.50}`
4. View logs: `grep stripe logs/stripe_webhook.log`

**Issue:** Negative amounts not rejected  
**Fix:** Ensure `scripts/stripe_live_guard.py` has ValueError check in `safe_price()`

### Customer Experience (Phase 34)

**Issue:** Signed URLs fail verification  
**Fix:**
1. Check `SESSION_SECRET` is consistent
2. Verify URL not expired (24h limit)
3. Test: `curl /api/customer/signed-url/test_123 -H "X-Dash-Key:$KEY"`

**Issue:** Unsubscribe not logging  
**Fix:** Check `logs/unsubscribes.log` permissions (should be writable)

### Compliance (Phase 35)

**Issue:** Export fails  
**Fix:**
1. Verify `backups/` directory exists
2. Check logs exist: `ls logs/*.log`
3. Manual run: `python3 scripts/data_export.py`

### Pricing AI (Phase 36)

**Issue:** No pricing recommendations  
**Fix:**
1. Ensure job logs exist (requires historical data)
2. Check `DEFAULT_RATE_USD_PER_MIN` is set
3. Manual test: `python3 scripts/pricing_ai.py`

### Referral Engine (Phase 37)

**Issue:** Invalid code format  
**Fix:** Codes must match `EP-[A-F0-9]{6}` pattern (check UUID generation)

### Audit Pack (Phase 38)

**Issue:** Hash chain fails  
**Fix:**
1. Verify `backups/audit/` directory exists
2. Check log file permissions
3. Manual run: `python3 scripts/audit_pack.py`

### Multi-Region Sync (Phase 39)

**Issue:** Replica sync fails  
**Fix:**
1. Check destination path: `echo $RAILWAY_FALLBACK_PATH` (default: backups/replica)
2. Verify write permissions
3. Manual sync: `python3 scripts/replica_sync.py`

### AI Ops Brain (Phase 40)

**Issue:** No recommendations generated  
**Fix:**
1. Verify `AI_INTEGRATIONS_OPENAI_API_KEY` is set
2. Check operational summaries exist: `ls logs/*COMPLETE*.txt`
3. Test API: `curl -X POST /api/brain/decide -H "X-Dash-Key:$KEY"`

---

## Security

### Authentication
- All admin endpoints require `X-Dash-Key` header
- Public endpoints: `/api/customer/unsubscribe` only
- CSRF protection on POST requests

### Secrets Management
- Never log `DASHBOARD_KEY`, `STRIPE_SECRET_KEY`, or `SESSION_SECRET`
- Rotate `SESSION_SECRET` every 90 days for signed URLs
- Use separate Stripe keys for test/live modes

### Compliance
- GDPR: Use `/api/compliance/export-data` for data subject requests
- Audit trail: Weekly automated reports to `backups/audit/`
- Unsubscribe: Logged to `logs/unsubscribes.log`

### Rate Limiting
- IP-based: 3 strikes in 5 minutes = 10-minute ban
- Check bans: `python3 scripts/rate_guard.py stats`
- Clear specific IP: `python3 scripts/rate_guard.py clear <ip>`

---

## Maintenance

### Daily
- Review dashboard health indicators
- Check scheduler status (should be running)
- Monitor cost metrics (target: <$1/day)

### Weekly
- Review AI Ops Brain recommendations (`logs/ops_brain_*.json`)
- Validate audit reports (`backups/audit/`)
- Check replica sync status

### Monthly
- Review pricing AI suggestions
- Analyze referral code usage (`logs/referrals.log`)
- Update `RUNBOOK.md` with new learnings

---

## Support

**Logs Location:** `logs/`  
**Backups Location:** `backups/`  
**Scripts Location:** `scripts/`  
**Dashboard:** https://echopilotai.replit.app/dashboard

**Common Log Files:**
- `logs/scheduler.log` - Automated task execution
- `logs/health_probe.log` - System health checks
- `logs/sys_probe.log` - CPU/Memory/Disk metrics
- `logs/stripe_webhook.log` - Payment webhooks
- `logs/ops_brain_*.json` - AI recommendations

