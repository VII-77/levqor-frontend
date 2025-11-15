# ECHOPILOT HEALTH INVENTORY

**Generated:** 2025-11-15 18:35:00 UTC  
**System:** Levqor + EchoPilot Genesis v8.0

## OVERVIEW

EchoPilot is the internal "brain" of Levqor - an automated monitoring, auditing, and governance system that runs alongside the Levqor API backend in the same Replit project (`Levqor-backend`).

---

## EXISTING HEALTH & AUDIT SCRIPTS

### Active Scripts (Currently Relevant)

| Script | Path | Purpose | How to Run | Status |
|--------|------|---------|------------|--------|
| **Backend Self-Audit** | `scripts/backend-self-audit.sh` | Tests backend health, Stripe webhook, runs pytest suite | `./scripts/backend-self-audit.sh` | ✅ ACTIVE |
| **Health Monitor** | `scripts/automation/health_monitor.py` | Monitors API health, generates reports | `python scripts/automation/health_monitor.py` | ✅ ACTIVE |
| **Intelligence Monitor** | `scripts/automation/intelligence_monitor.py` | AI-powered anomaly detection, metrics collection | Called by scheduler | ✅ ACTIVE |
| **Synthetic Checks** | `scripts/monitoring/synthetic_checks.py` | Tests production endpoints (api.levqor.ai) | Called by scheduler | ✅ ACTIVE |
| **Weekly Pulse** | `scripts/automation/weekly_pulse.py` | Weekly governance and metrics summary | `python scripts/automation/weekly_pulse.py` | ✅ ACTIVE |
| **SLO Watchdog** | `monitors/slo_watchdog.py` | Service Level Objective monitoring | Called by scheduler | ✅ ACTIVE |
| **Alerting System** | `scripts/monitoring/alerting.py` | Alert routing and notifications | Imported by other scripts | ✅ ACTIVE |

### Legacy/Archive Scripts (Historical)

| Script | Path | Status | Notes |
|--------|------|--------|-------|
| **Daily Burn-in Check** | `scripts/daily_burnin_check.sh` | 🟠 LEGACY | From Day-2 deployment phase |
| **Ops Summary** | `scripts/ops_summary.py` | 🟠 LEGACY | Replaced by intelligence monitor |
| **Governance Report** | `scripts/governance_report.py` | 🟠 LEGACY | Replaced by weekly pulse |

### Configuration & Setup Scripts

| Script | Purpose | Frequency |
|--------|---------|-----------|
| `scripts/create_stripe_prices.py` | Create Stripe pricing objects | One-time setup |
| `scripts/configure_cloudflare.py` | Configure Cloudflare settings | One-time setup |
| `scripts/setup_stripe_prices.sh` | Batch Stripe setup | One-time setup |
| `scripts/dunning_smoke_test.py` | Test dunning system | Manual testing |

---

## SCHEDULED JOBS (APScheduler)

**Scheduler Location:** `monitors/scheduler.py`

### Active Jobs

| Job Name | Frequency | Function | Purpose |
|----------|-----------|----------|---------|
| **Intelligence monitoring cycle** | Every 15 min | `run_intelligence_monitor()` | Collects metrics, detects anomalies, attempts self-heal |
| **Synthetic endpoint checks** | Every 15 min | `run_synthetic_checks()` | Tests production API endpoints (api.levqor.ai) |
| **SLO monitoring** | Every 5 min | `run_slo_watchdog()` | Checks service level objectives |
| **Status page health check** | Every 5 min | `run_status_health_check()` | Creates status snapshots in DB |
| **Alert threshold checks** | Every 5 min | `run_alert_checks()` | Monitors alert thresholds |
| **Weekly intelligence** | Weekly | `run_weekly_intelligence()` | AI insights and trend analysis |
| **Retention aggregation** | Daily | `run_retention_aggregation()` | Aggregates retention metrics |
| **Billing dunning processor** | Daily | `run_dunning_processor()` | Processes failed payments |
| **Daily retention cleanup** | Daily | `run_retention_cleanup()` | Cleans up old data per retention policies |

### Detected Job Count
**Total Active Jobs:** ~15-20 (based on scheduler.py)

---

## WHAT ECHOPILOT CURRENTLY MONITORS

### ✅ Currently Monitored Automatically

1. **Backend Health**
   - Local health endpoint (localhost:8000/health)
   - Production health endpoint (api.levqor.ai/health)
   - Response times and availability
   - Every 5-15 minutes

2. **Production API Endpoints**
   - `/health`
   - `/api/sandbox/metrics`
   - `/api/insights/preview`
   - `/api/intelligence/status`
   - **Current Status:** All returning 404 (deployment issue detected)

3. **Database Connectivity**
   - SQLite connection test
   - Table existence checks
   - Every 5 minutes via status health check

4. **Anomaly Detection**
   - Backend failure patterns
   - Response time anomalies
   - Error rate spikes
   - Automated alerts via Intelligence Monitor

5. **Service Level Objectives (SLOs)**
   - P99 latency targets
   - Error rate thresholds
   - Availability targets
   - Every 5 minutes

6. **Retention & Cleanup**
   - User data retention policies
   - Automated cleanup of expired data
   - Daily execution

7. **Billing & Payment Dunning**
   - Failed payment detection
   - Automated retry sequences
   - Account suspension logic
   - Daily execution

8. **Weekly Governance**
   - System health trends
   - Metrics aggregation
   - Compliance status

### ❌ NOT Currently Monitored (Gaps)

1. **Stripe API Connectivity**
   - No active Stripe API health check
   - Should verify API key validity

2. **OpenAI API Connectivity**
   - Support AI integration exists but no health check
   - Should verify OPENAI_API_KEY validity

3. **Email Service (Resend) Health**
   - No active email delivery monitoring
   - Should verify Resend API connectivity

4. **Frontend (Vercel) Health**
   - Frontend monitored separately
   - No cross-system health correlation

5. **Cloudflare Routing**
   - No active check that api.levqor.ai → levqor-backend.replit.app routing works
   - Current routing appears broken (404s)

6. **Database Schema Integrity**
   - No automated schema validation
   - No migration status checks

7. **Secret Expiry Monitoring**
   - No checks for expiring API keys
   - No rotation reminders

---

## EXISTING AUDIT REPORTS

| Report File | Purpose | Last Generated |
|-------------|---------|----------------|
| `LEVQOR-PRODUCTION-REALITY-REPORT.md` | Complete production status audit | 2025-11-15 16:40 UTC |
| `NUCLEAR-AUDIT-REPORT.md` | System-wide cleanup audit | Historical |
| `FRONTEND-NUCLEAR-CLEANUP-REPORT.md` | Frontend cleanup report | Historical |
| `integrity_reports/integrity_report_*.json` | Integrity pack evidence | 2024-11-11 |
| `integrity_reports/finalizer_report_*.json` | Finalizer pack evidence | 2024-11-11 |

---

## DIRECTORIES & STRUCTURE

```
Levqor-backend/
├── monitors/              # EchoPilot core modules
│   ├── scheduler.py       # APScheduler job definitions
│   ├── anomaly_ai.py      # AI anomaly detection
│   ├── auto_tune.py       # Auto-tuning engine
│   ├── autoscale.py       # Auto-scaling logic
│   ├── incident_response.py
│   ├── slo_watchdog.py
│   └── alert_router.py
│
├── scripts/
│   ├── automation/        # Automated monitoring scripts
│   │   ├── health_monitor.py
│   │   ├── intelligence_monitor.py
│   │   └── weekly_pulse.py
│   │
│   ├── monitoring/        # Monitoring utilities
│   │   ├── synthetic_checks.py
│   │   ├── alerting.py
│   │   └── notion_go_nogo_dashboard.py
│   │
│   ├── backend-self-audit.sh
│   └── ...
│
├── integrity_reports/     # Historical integrity evidence
├── ops/                   # Operations utilities
└── retention/             # Retention policy configs
```

---

## HEALTH ENDPOINT LOCATIONS

### Backend Routes (run.py)

| Endpoint | Line | Purpose | Local URL | Production URL |
|----------|------|---------|-----------|----------------|
| `/health` | 609 | Main health check | http://localhost:8000/health | https://api.levqor.ai/health |
| `/status` | 612 | System status | http://localhost:8000/status | https://api.levqor.ai/status |
| `/public/metrics` | 616 | Public metrics | http://localhost:8000/public/metrics | https://api.levqor.ai/public/metrics |
| `/ops/health` | TBD | Operations health | TBD | TBD |
| `/billing/health` | TBD | Billing health | TBD | TBD |

**Current Issue:** Production endpoints returning 404 (deployment configuration mismatch)

---

## CRITICAL CONFIGURATION

### Port Configuration Issue Detected

| Environment | Port | Configuration Location |
|-------------|------|------------------------|
| **Local development** | 5000 | run.py line 2957: `app.run(port=5000)` |
| **Workflow (dev)** | 8000 | .replit line 87: `--bind 0.0.0.0:8000` |
| **Deployment (prod)** | 5000 | .replit line 107: `--bind 0.0.0.0:5000` |

**Issue:** Workflow runs on port 8000, but deployment expects port 5000. This is correct for Replit Autoscale deployments.

---

## ECHOPILOT STATUS SUMMARY

### Overall Health: 🟠 PARTIALLY OPERATIONAL

**Working Components:**
- ✅ Scheduler active with 15+ automated jobs
- ✅ Local monitoring (localhost:8000) functional
- ✅ Anomaly detection running every 15 minutes
- ✅ Database health checks active
- ✅ SLO monitoring active
- ✅ Alert system functional

**Broken Components:**
- ❌ Production API monitoring (detecting 404s - correct detection)
- ❌ Production deployment not serving requests
- ❌ Stripe connectivity not actively monitored
- ❌ OpenAI connectivity not actively monitored

**Recommended Next Steps:**
1. Fix backend deployment configuration (Phase 3)
2. Add Stripe API connectivity check to health monitor
3. Add OpenAI API connectivity check to health monitor
4. Verify Cloudflare routing once deployment is fixed
5. Create unified health dashboard

---

## NOTES FOR GENESIS v8.0

- All scheduler jobs are defined and active
- Intelligence monitoring detects production failures correctly
- Self-healing attempts are logged but cannot fix deployment issues
- Historical audit files preserved (do not delete)
- EchoPilot is production-ready but deployment infrastructure is broken

---

**Inventory Complete** - Proceed to Phase 2 for unified health check script.
