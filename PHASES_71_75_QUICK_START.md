# ⚡ PHASES 71-75 QUICK START GUIDE

## 🚀 What's New?

Phases 71-75 add **predictive analytics, smart retries, and AI-powered operations**:

1. **Predictive Scaling** (Phase 71) - CPU/RAM/latency forecasting
2. **Smart Retries** (Phase 72) - Exponential backoff with jitter
3. **Email Reports 2.0** (Phase 73) - Enhanced daily HTML reports
4. **Ops Analytics UI** (Phase 74) - Dashboard component
5. **AI Incident Summaries** (Phase 75) - Intelligent 24h analysis

---

## 🎯 API Endpoints (4 NEW)

All require `X-Dash-Key` authentication header.

### Predictive Scaling (Phase 71)
```bash
# Get predictive analytics
curl -H "X-Dash-Key: YOUR_KEY" \
     https://echopilotai.replit.app/api/ops/analytics
```

### Smart Retries (Phase 72)
```bash
# Simulate smart retry
curl -X POST \
     -H "X-Dash-Key: YOUR_KEY" \
     https://echopilotai.replit.app/api/retries/simulate
```

### Email Reports (Phase 73)
```bash
# Generate daily report
curl -X POST \
     -H "X-Dash-Key: YOUR_KEY" \
     https://echopilotai.replit.app/api/reports/email-daily
```

### AI Incident Summaries (Phase 75)
```bash
# Get incident summary
curl -X POST \
     -H "X-Dash-Key: YOUR_KEY" \
     https://echopilotai.replit.app/api/incidents/summarize
```

---

## 🔧 Manual Script Testing

```bash
# Phase 71: Predictive scaling
python3 scripts/predictive_scaling.py

# Phase 72: Smart retries
python3 scripts/smart_retries.py

# Phase 73: Email reports
python3 scripts/email_reports_v2.py

# Phase 75: AI incident summaries
python3 scripts/ai_incident_summaries.py
```

---

## 📊 View Reports & Logs

```bash
# Predictive scaling
cat logs/predictive_scaling.json

# Smart retries
cat logs/smart_retries.json

# Latest HTML report
ls -t reports/*.html | head -1

# Incident summaries
cat logs/incident_summaries.json

# Historical trends
tail -20 logs/predictive_scaling.ndjson
tail -20 logs/incident_summaries.ndjson
```

---

## 🖥️ UI Component

### Ops Analytics Card
- **Location:** `static/templates/ops_analytics.html`
- **Features:** Real-time analytics, incident viewer, retry simulator
- **Style:** Indigo gradient card with interactive buttons
- **Integration:** Include in dashboard pages

---

## ⏱️ Scheduler Tasks

New autonomous tasks added:

- **Predictive Scaling** - Every hour
- **AI Incident Summaries** - Every 30 minutes
- **Smart Retries Test** - Every 6 hours
- **Email Reports** - Daily at 07:45 UTC

Total: **27 autonomous tasks** now running!

---

## 📈 Key Features

### Predictive Scaling
- **Forecasts:** CPU, RAM, latency trends
- **Metrics:** Current, average, P95
- **Trends:** Up, down, stable
- **Recommendations:** Automated scaling suggestions

### Smart Retries
- **Algorithm:** Exponential backoff with jitter
- **Jitter:** 50-100% randomization
- **Max Delay:** 8 seconds (configurable)
- **Logging:** Comprehensive retry tracking

### Email Reports 2.0
- **Format:** Beautiful HTML with gradients
- **Metrics:** SLO, incidents, backups, costs
- **Schedule:** Daily at 07:45 UTC
- **SMTP:** Optional email sending

### AI Incident Summaries
- **Period:** Last 24 hours
- **Analysis:** Error aggregation, severity classification
- **Integration:** Links with predictive scaling
- **Recommendations:** Actionable insights

---

## 🔒 Configuration

### Smart Retries
```bash
export RETRY_TARGET="/api/health"
export RETRY_BASE="0.6"           # Base delay (seconds)
export RETRY_MAX="8"              # Max delay (seconds)
export RETRY_ATTEMPTS="5"         # Max attempts
```

### Email Reports (Optional SMTP)
```bash
export SMTP_USER="noreply@example.com"
export SMTP_PASS="your_password"
```

---

## 📈 Current Stats

- **API Endpoints:** 57 total (+4 new)
- **Autonomous Tasks:** 27 total (+4 new)
- **Python Scripts:** 56+ (+4 new)
- **UI Templates:** 3 (+1 new)
- **Report Types:** HTML email reports

---

## 🔗 Full Documentation

- **Detailed Guide:** `PHASES_71_75_SUMMARY.md`
- **Phases 66-70:** `PHASES_66_70_SUMMARY.md`
- **Main Project Docs:** `replit.md`

---

**🎉 Phases 71-75 operational with predictive analytics and AI-powered operations!**
