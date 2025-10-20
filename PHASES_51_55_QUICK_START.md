# 🚀 PHASES 51-55: QUICK START GUIDE

**Deployment Status:** ✅ COMPLETE & OPERATIONAL  
**Date:** October 20, 2025  

---

## 🎯 WHAT WAS DEPLOYED

### 4 New Production Scripts:
1. **scripts/emailer.py** - SMTP email system (dry-run safe)
2. **scripts/observability_snapshot.py** - Real-time metrics dashboard
3. **scripts/fraud_guard.py** - Fraud detection & velocity limiting
4. **scripts/customer_portal.py** - Signed portal link generation

### 4 New API Endpoints:
1. `POST /api/email/send` - Send SMTP emails
2. `GET /api/observability/snapshot` - Get real-time metrics
3. `POST /api/fraud/check` - Fraud risk evaluation
4. `POST /api/portal/link` - Generate customer portal link

### 1 New Scheduled Task:
1. **Observability Snapshot** - Every hour

---

## 📊 QUICK TESTS

### Test From Command Line:

```bash
# Email system (safe - dry-run if SMTP not configured)
python3 scripts/emailer.py

# Get system metrics snapshot
python3 scripts/observability_snapshot.py

# Test fraud guard rules
python3 scripts/fraud_guard.py

# Generate portal link
python3 scripts/customer_portal.py
```

### Test Via API (requires DASHBOARD_KEY):

```bash
# Get observability snapshot
curl -H "X-Dash-Key: YOUR_KEY" \
     https://echopilotai.replit.app/api/observability/snapshot

# Check fraud risk
curl -H "X-Dash-Key: YOUR_KEY" \
     -H "Content-Type: application/json" \
     -X POST https://echopilotai.replit.app/api/fraud/check \
     -d '{"email":"test@example.com","card_type":"credit","amount":100}'

# Generate portal link
curl -H "X-Dash-Key: YOUR_KEY" \
     -H "Content-Type: application/json" \
     -X POST https://echopilotai.replit.app/api/portal/link \
     -d '{"email":"customer@example.com"}'
```

---

## 📝 MONITORING

### View Real-Time Logs:

```bash
# System observability
tail -f logs/observability.ndjson

# Email activity
tail -f logs/emails.ndjson

# Fraud checks
tail -f logs/fraud_guard.ndjson

# Portal link generation
tail -f logs/portal_links.ndjson
```

### Latest Snapshots:

```bash
# Current observability metrics
cat logs/observability.json

# Production alerts
cat logs/production_alerts.json
```

---

## 🔧 CONFIGURATION

### SMTP Email (Optional):

```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=465
export SMTP_USER=your-email@gmail.com
export SMTP_PASS=your-app-password
export SMTP_FROM=ops@echopilot.ai
```

If not configured, emails will dry-run (safe mode).

### Fraud Guard Rules (Optional):

```bash
export GUARD_BLOCK_PREPAID=0        # 1 to block prepaid cards
export GUARD_MAX_PER_HOUR=5         # Max txns per card/hour
export GUARD_MAX_AMOUNT_DAY=10000   # Max $ per email/day
export GUARD_EMAIL_ALLOW=vip@test.com  # VIP allowlist
```

---

## ✅ VALIDATION

All systems tested and operational:

✅ Email System - Dry-run mode working  
✅ Observability - Real-time metrics collected  
✅ Fraud Guard - All rules validated  
✅ Portal Links - Signed link generation working  

---

## 🔄 SCHEDULER STATUS

Now running **14 autonomous tasks** total.

**New in Phases 51-55:**
- 📊 Observability Snapshot (hourly)

---

## 📖 DOCUMENTATION

- **Full Details:** `PHASES_51_55_SUMMARY.md`
- **System Docs:** `replit.md`
- **Previous Phases:** `PHASES_41_50_SUMMARY.md`

---

**🎉 All systems operational!**
