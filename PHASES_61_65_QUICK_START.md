# ⚡ PHASES 61-65 QUICK START GUIDE

## 🚀 What's New?

Phases 61-65 add **infrastructure management and experimentation** capabilities:

1. **Support Inbox** (Phase 61) - Email monitoring
2. **Feature Flags** (Phase 62) - Dynamic feature toggles
3. **Experiments** (Phase 63) - A/B testing framework
4. **Cost Tracker** (Phase 64) - Infrastructure cost estimation
5. **Incident Autoresponder** (Phase 65) - Automated incident detection

---

## 🎯 API Endpoints (10 NEW)

All require `X-Dash-Key` authentication header.

### Support Inbox (Phase 61)
```bash
# Fetch support digest
curl -X POST \
     -H "X-Dash-Key: YOUR_KEY" \
     https://echopilotai.replit.app/api/support/digest
```

### Feature Flags (Phase 62)
```bash
# Get all flags
curl -H "X-Dash-Key: YOUR_KEY" \
     https://echopilotai.replit.app/api/flags/get

# Set flag
curl -X POST \
     -H "X-Dash-Key: YOUR_KEY" \
     -H "Content-Type: application/json" \
     -d '{"key": "ui.new_dashboard", "value": true}' \
     https://echopilotai.replit.app/api/flags/set
```

### Experiments (Phase 63)
```bash
# Assign user to experiment
curl "https://echopilotai.replit.app/api/exp/assign?user=user123&exp=pricing_v2" \
     -H "X-Dash-Key: YOUR_KEY"

# Log experiment event
curl -X POST \
     -H "X-Dash-Key: YOUR_KEY" \
     -H "Content-Type: application/json" \
     -d '{"event": "conversion", "user": "user123", "exp": "pricing_v2"}' \
     https://echopilotai.replit.app/api/exp/log
```

### Cost Tracker (Phase 64)
```bash
# Get cost report
curl -H "X-Dash-Key: YOUR_KEY" \
     https://echopilotai.replit.app/api/costs/report
```

### Incident Scanner (Phase 65)
```bash
# Scan for incidents
curl -X POST \
     -H "X-Dash-Key: YOUR_KEY" \
     https://echopilotai.replit.app/api/incidents/scan
```

---

## 🔧 Manual Script Testing

```bash
# Phase 61: Support inbox
python3 scripts/support_inbox.py

# Phase 62: Feature flags
python3 scripts/feature_flags.py

# Phase 63: Experiments
python3 scripts/experiments.py

# Phase 64: Cost tracking
python3 scripts/cost_tracker.py

# Phase 65: Incident detection
python3 scripts/incident_autoresponder.py
```

---

## 📊 View Reports

```bash
# Support inbox digest
cat logs/support_digest.json

# Feature flags
cat configs/flags.json

# Experiment assignments
tail logs/experiments.ndjson

# Cost report
cat logs/cost_report.json

# Incidents
tail logs/incidents.ndjson
```

---

## 📝 Configuration Files

**Feature Flags** (`configs/flags.json`):
```json
{
  "payments.live": true,
  "ui.new_dashboard": false,
  "ab.pricing_v2": false,
  "features.churn_ai": true,
  "features.slo_monitoring": true
}
```

**Experiments** (`configs/experiments.json`):
```json
{
  "pricing_v2": {
    "variants": ["A", "B"],
    "salt": "ECHO2025",
    "description": "Test new pricing page design"
  },
  "onboarding_flow": {
    "variants": ["standard", "guided", "quick"],
    "salt": "ONBOARD2025",
    "description": "Test onboarding variations"
  }
}
```

---

## ⏱️ Scheduler Tasks

New autonomous tasks added:

- **Support Inbox** - Every hour
- **Cost Tracker** - Daily at 01:10 UTC
- **Incident Scanner** - Every 5 minutes

Total: **20 autonomous tasks** now running!

---

## 🚨 Dry-Run Modes

**Support Inbox** and **Incident Alerts** work in dry-run mode without credentials:

- Support Inbox generates sample data when IMAP not configured
- Incident Scanner logs incidents but doesn't send alerts without Telegram credentials

This ensures production safety!

---

## 📈 Current Stats

- **API Endpoints:** 47 total (+10 new)
- **Autonomous Tasks:** 20 total (+3 new)
- **Python Scripts:** 49+ (+5 new)
- **Infrastructure Cost:** ~$0.02/month (tracked by Phase 64)

---

## 🔗 Full Documentation

- **Detailed Guide:** `PHASES_61_65_SUMMARY.md`
- **Main Project Docs:** `replit.md`

---

**🎉 Phases 61-65 operational and production-ready!**
