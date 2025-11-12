# Levqor After-Launch Automation

**Status:** ✅ **ACTIVE**  
**Date Activated:** November 11, 2025  
**Scheduler:** APScheduler (11 jobs running)

---

## 📋 Overview

Levqor's post-launch automation system provides continuous health monitoring, cost tracking, error detection, and weekly reporting through scheduled jobs integrated into the backend APScheduler.

---

## 🤖 Automation Jobs

### 1. Health & Uptime Monitoring
- **Script:** `scripts/automation/health_monitor.py`
- **Schedule:** Every 6 hours
- **Function:** Pings critical endpoints and logs status
- **Endpoints Monitored:**
  - `https://levqor.ai` (Frontend)
  - `https://api.levqor.ai/health` (Backend Health)
  - `https://api.levqor.ai/public/metrics` (Public Metrics)
- **Alerts:** Logs unhealthy endpoints to console
- **Future:** Will push alerts to Notion "System Health Log" database

**Test:**
```bash
python3 scripts/automation/health_monitor.py
```

### 2. Cost Dashboard Sync
- **Script:** `scripts/automation/cost_collector.py`
- **Schedule:** Daily at 1:00 AM UTC
- **Function:** Collects spend and revenue data
- **Data Sources:**
  - Replit API (usage/AI spend) - TODO: implement API
  - Stripe API (revenue, failed payments) - ✅ Active
  - Vercel API (build minutes, bandwidth) - TODO: implement API
- **Alerts:** Triggers warning if Replit spend > $10
- **Future:** Push to Notion "Cost Dashboard" database

**Test:**
```bash
python3 scripts/automation/cost_collector.py
```

### 3. Sentry Error Tracking
- **Script:** `scripts/automation/sentry_test.py`
- **Schedule:** Weekly on Sunday at 10:00 AM UTC
- **Function:** Verifies Sentry integration health
- **Status:** ⚠️ Requires valid SENTRY_DSN configuration
- **Setup:** Add valid Sentry DSN to environment secrets

**Test:**
```bash
python3 scripts/automation/sentry_test.py
```

**To Enable Sentry:**
1. Create project at https://sentry.io
2. Copy DSN (format: `https://xxx@xxx.ingest.sentry.io/xxx`)
3. Update SENTRY_DSN secret in Replit environment
4. Re-run test to verify

### 4. Weekly Pulse Summary
- **Script:** `scripts/automation/weekly_pulse.py`
- **Schedule:** Every Friday at 2:00 PM London time
- **Function:** Generates weekly performance summary
- **Metrics Collected:**
  - 7-day uptime percentage
  - Total spend (Replit + Vercel)
  - Revenue (Stripe)
  - New sign-ups
  - Churn count
  - Active users
- **Outputs:** Console summary (future: Notion + Email)

**Test:**
```bash
python3 scripts/automation/weekly_pulse.py
```

---

## 🔧 Scheduler Configuration

All automation jobs are managed by APScheduler in `monitors/scheduler.py`:

| Job ID | Name | Schedule | Script |
|--------|------|----------|--------|
| `health_monitor` | Health & uptime monitor | Every 6h | `health_monitor.py` |
| `cost_collector` | Daily cost dashboard | Daily 1:00 AM UTC | `cost_collector.py` |
| `sentry_test` | Weekly Sentry health check | Sun 10:00 AM UTC | `sentry_test.py` |
| `weekly_pulse` | Weekly pulse summary | Fri 2:00 PM London | `weekly_pulse.py` |

**Previous Jobs** (already configured):
- `retention_aggregation` - Daily retention metrics (12:05 AM UTC)
- `slo_watchdog` - SLO monitoring (every 5 min)
- `daily_ops_summary` - Daily ops email (9:00 AM London)
- `cost_prediction` - Weekly cost forecast (Mon 2:10 AM UTC)
- `kv_costs` - Hourly KV cost sync
- `growth_retention` - Daily growth by source (12:10 AM UTC)
- `governance_report` - Weekly governance email (Sun 9:00 AM London)

**Total:** 11 automated jobs

---

## 📊 Current Test Results

### ✅ Health Monitor
```
✅ Frontend OK (837ms)
✅ Backend Health OK (152ms)
✅ Public Metrics OK (134ms)
✅ All 3 endpoints healthy
```

### ✅ Cost Collector
```
📊 Cost Dashboard Summary:
  Replit: $0.00
  Stripe Revenue: $0.00
  Stripe Failed: 0
  Vercel Build Min: 0
```

### ⚠️ Sentry Test
```
❌ SENTRY_DSN not configured or invalid
ℹ️  Set a valid Sentry DSN in Secrets (should start with https://)
```

### ✅ Weekly Pulse
```
📊 LEVQOR WEEKLY PULSE
🟢 UPTIME: 99.99%
💰 NET: $0.00
👥 USERS: 0 active
```

---

## 🔮 Future Enhancements

### Notion Integration
- **Status:** Notion connector already added
- **TODO:** Create databases and configure automation scripts
  - "System Health Log" database for health alerts
  - "Cost Dashboard" database for spend tracking
  - "Pulse" database for weekly summaries

### Email Notifications
- **Current:** Resend API already configured (ops_summary.py)
- **TODO:** Integrate Resend into cost alerts and pulse summaries
- **Alternative:** Gmail API for team notifications

### Advanced Alerting
- **Multi-channel:** Slack, Telegram, Email
- **Smart routing:** Different channels for different alert types
- **Escalation:** Critical alerts get immediate notification

### API Integration
- **Replit API:** Pull compute and AI spend data
- **Vercel API:** Track build minutes and bandwidth usage
- **GitHub API:** Monitor deployment frequency

---

## 🚀 How to Restart Automation

Automation runs automatically in the background. To restart:

```bash
# Restart the backend workflow (restarts scheduler)
# Via Replit: Stop/Start workflow button
# Or programmatically: restart_workflow("levqor-backend")
```

---

## 📝 Manual Testing

Test all automation scripts:

```bash
# Run all tests
python3 scripts/automation/health_monitor.py
python3 scripts/automation/cost_collector.py
python3 scripts/automation/sentry_test.py
python3 scripts/automation/weekly_pulse.py
```

---

## ⚡ Quick Status Check

```bash
# Check scheduler logs
tail -f /tmp/logs/levqor-backend_*.log | grep -i "scheduler\|health\|cost\|sentry\|pulse"
```

---

**Last Updated:** November 11, 2025  
**Maintained By:** Levqor DevOps Automation
