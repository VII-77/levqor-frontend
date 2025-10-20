# ⚡ PHASES 76-80 QUICK START GUIDE

## 🚀 What's New?

Phases 76-80 add **enterprise reliability and scaling**:

1. **SLO Budget** (Phase 76) - Error budget tracking with deploy gates
2. **Incident Pager** (Phase 77) - Telegram/Email critical alerts
3. **Customer Portal** (Phase 78) - Signed receipt download links
4. **Cost Guardrails** (Phase 79) - AI spend caps and throttling
5. **Autoscale Workers** (Phase 80) - Predictive worker scaling

---

## 🎯 API Endpoints (10 NEW)

All require `X-Dash-Key` authentication (except signed portal downloads).

### SLO Budget (Phase 76)
```bash
# Get SLO status
curl -H "X-Dash-Key: YOUR_KEY" \
     https://echopilotai.replit.app/api/slo/budget

# Reset baseline
curl -X POST -H "X-Dash-Key: YOUR_KEY" \
     https://echopilotai.replit.app/api/slo/rebaseline
```

### Incident Pager (Phase 77)
```bash
# Raise incident
curl -X POST \
     -H "X-Dash-Key: YOUR_KEY" \
     -H "Content-Type: application/json" \
     -d '{"severity":"CRITICAL","msg":"SLO burn","source":"test"}' \
     https://echopilotai.replit.app/api/incidents/raise

# Get 24h summary
curl -X POST -H "X-Dash-Key: YOUR_KEY" \
     https://echopilotai.replit.app/api/incidents/summary
```

### Customer Portal (Phase 78)
```bash
# Get receipts
curl -H "X-Dash-Key: YOUR_KEY" \
     "https://echopilotai.replit.app/api/portal/receipts?email=customer@example.com"
```

### Cost Guardrails (Phase 79)
```bash
# Get cost status
curl -H "X-Dash-Key: YOUR_KEY" \
     https://echopilotai.replit.app/api/costs/status

# Set cost cap
curl -X POST \
     -H "X-Dash-Key: YOUR_KEY" \
     -H "Content-Type: application/json" \
     -d '{"scope":"daily","usd_cap":30.0}' \
     https://echopilotai.replit.app/api/costs/set-cap
```

### Autoscale Workers (Phase 80)
```bash
# Get scale status
curl -H "X-Dash-Key: YOUR_KEY" \
     https://echopilotai.replit.app/api/scale/status

# Apply scaling (dry-run)
curl -X POST \
     -H "X-Dash-Key: YOUR_KEY" \
     -H "Content-Type: application/json" \
     -d '{"dry_run":true}' \
     https://echopilotai.replit.app/api/scale/apply
```

---

## 🔧 Manual Script Testing

```bash
# Phase 76: SLO budget
python3 scripts/slo_budget.py

# Phase 77: Incident pager
python3 scripts/incident_pager.py

# Phase 78: Customer portal
python3 scripts/customer_portal.py

# Phase 79: Cost guardrails
python3 scripts/cost_guardrails.py

# Phase 80: Autoscale workers
python3 scripts/autoscale_workers.py
```

---

## 📊 View Reports & Logs

```bash
# SLO budget
cat logs/slo_budget.json
tail -20 logs/slo_budget.ndjson

# Incidents
cat logs/incident_summary.json
tail -20 logs/incidents.ndjson

# Portal access audit
tail -20 logs/portal_access.ndjson

# Cost tracking
cat logs/costs.json
tail -20 logs/costs.ndjson

# Autoscale decisions
cat logs/autoscale.json
tail -20 logs/autoscale.ndjson

# Deploy gate check
[ -f logs/deploy_gate.flag ] && cat logs/deploy_gate.flag || echo "No deploy gate active"
```

---

## 🖥️ UI Components

### SLO Budget Card
- **Location:** `static/templates/slo_budget_card.html`
- **Features:** Real-time SLO status, burn rate, baseline reset
- **Style:** Emerald gradient with red/yellow/green indicators
- **Color Coding:**
  - 🟢 Green: OK (< 100% burn rate)
  - 🟡 Yellow: WATCH/WARNING (100-200% burn rate)
  - 🔴 Red: CRITICAL (> 200% burn rate, deploy gate active)

### Customer Portal Card
- **Location:** `static/templates/customer_portal_card.html`
- **Features:** Email lookup, receipt links, test incident button
- **Style:** Blue gradient with input field
- **Functions:** `lookupReceipts()`, `raiseTestIncident()`

### Cost & Scale Card
- **Location:** `static/templates/cost_scale_card.html`
- **Features:** Cost status, autoscale status
- **Style:** Purple gradient with dual buttons
- **Functions:** `loadCostStatus()`, `loadScaleStatus()`

---

## ⏱️ Scheduler Tasks

New autonomous tasks added:

- **SLO Budget** - Every 15 minutes (error budget tracking)
- **Incident Pager** - Every 5 minutes (critical alerts)
- **Cost Guardrails** - Every hour (spend monitoring)
- **Autoscale Workers** - Every 10 minutes (predictive scaling)

Total: **31 autonomous tasks** now running!

---

## 📈 Key Features

### SLO Budget (Phase 76)
- **Metrics:** P95, P99 latency percentiles
- **Window:** 30-day rolling average
- **Burn Alerts:** OK, WATCH, WARNING, CRITICAL
- **Deploy Gate:** Auto-activates at >200% burn rate

### Incident Pager (Phase 77)
- **Channels:** Telegram + Email (optional)
- **Deduplication:** 1-hour fingerprint window
- **Retry:** Exponential backoff (5 attempts)
- **Severity Routing:** CRITICAL → immediate page

### Customer Portal (Phase 78)
- **Security:** HMAC-SHA256 signed tokens
- **Expiration:** 24 hours (configurable)
- **Audit:** IP + email + resource logging
- **Validation:** Tamper-proof token verification

### Cost Guardrails (Phase 79)
- **Caps:** Global daily + model-specific
- **Thresholds:** 90% warn, 100% throttle
- **Action:** Auto-incident on breach
- **Enforcement:** Admin endpoints always allowed

### Autoscale Workers (Phase 80)
- **Triggers:** P95 latency + arrival rate
- **Constraints:** Min/max workers, cooldown
- **Safety:** Deploy gate integration, dry-run mode
- **Logic:** Predictive 30-minute forecast

---

## 🔒 Configuration

### Environment Variables

**SLO Budget:**
```bash
SLO_LAT_P95_MS=800
SLO_LAT_P99_MS=1200
SLO_ERR_BUDGET_DAILY_PCT=1.0
SLO_WINDOW_DAYS=30
```

**Incident Pager:**
```bash
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=alerts@example.com
SMTP_PASS=your_password
```

**Customer Portal:**
```bash
PORTAL_SIGNING_SECRET=your_secret
PORTAL_LINK_TTL_HRS=24
```

**Cost Guardrails:**
```bash
COST_CAP_DAILY_USD=25.0
MODEL_CAPS_JSON='{"gpt-4o":15,"gpt-4o-mini":10}'
```

**Autoscale Workers:**
```bash
SCALE_MIN=1
SCALE_MAX=6
SCALE_COOLDOWN_MIN=10
SCALE_DRY_RUN=true
```

---

## 📈 Current Stats

- **API Endpoints:** 67 total (+10 new)
- **Autonomous Tasks:** 31 total (+4 new)
- **Python Scripts:** 61+ (+5 new)
- **UI Templates:** 6 (+3 new)
- **Lines of Code:** ~19,500 (+500)

---

## 🚨 Rollback Procedure

If issues occur:

```bash
# 1. Disable new tasks in scheduler
# Comment out Phase 76-80 tasks in scripts/exec_scheduler.py

# 2. Neutralize guardrails
export COST_CAP_DAILY_USD=9999
export SCALE_DRY_RUN=true

# 3. Remove deploy gate
rm -f logs/deploy_gate.flag

# 4. Restart scheduler
# Use Replit UI to restart "Scheduler" workflow
```

---

## 🔗 Full Documentation

- **Detailed Guide:** `PHASES_76_80_SUMMARY.md`
- **Phases 71-75:** `PHASES_71_75_SUMMARY.md`
- **Main Project Docs:** `replit.md`

---

**🎉 Phases 76-80 operational with enterprise reliability and scaling!**
