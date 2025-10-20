# EchoPilot Production Runbook

**Last Updated:** October 20, 2025  
**Platform:** Replit Reserved VM  
**Environment:** Production

---

## Quick Start

### System Health Check
```bash
# Overall health
curl -H "X-Dash-Key: $DASHBOARD_KEY" \
  http://localhost:5000/api/system-health | jq .

# SLO status
curl -H "X-Dash-Key: $DASHBOARD_KEY" \
  http://localhost:5000/api/observability/slo | jq .

# Enterprise validation
curl -H "X-Dash-Key: $DASHBOARD_KEY" \
  http://localhost:5000/api/validate/enterprise | jq .
```

### Monitoring Dashboards
- **Enterprise Report:** https://echopilotai.replit.app/api/reports/enterprise/html
- **Validation:** https://echopilotai.replit.app/api/validation/html  
- **Prometheus Metrics:** https://echopilotai.replit.app/metrics

---

## Observability (Phase 51)

### Metrics & Tracing
**HTTP Tracing:** All requests logged to `logs/http_traces.ndjson`  
**Prometheus Metrics:** Available at `GET /metrics` (no auth)  
**SLO Monitoring:** Every 15 minutes via `slo_guard.py`

### SLO Targets
- **API Availability:** 99.9%
- **P95 Latency:** < 400ms
- **Webhook Success:** 99%

See `docs/SLOS.md` for complete SLO documentation.

### Key Commands
```bash
# View Prometheus metrics
curl http://localhost:5000/metrics

# Get SLO report
curl -H "X-Dash-Key: $DASHBOARD_KEY" \
  http://localhost:5000/api/observability/slo | jq .

# Get latency metrics (p50/p95/p99 24h)
curl -H "X-Dash-Key: $DASHBOARD_KEY" \
  http://localhost:5000/api/observability/latency | jq .

# Manual SLO check
python3 scripts/slo_guard.py | jq .
```

---

## Production Alerts

**Frequency:** Every 5 minutes  
**Script:** `scripts/production_alerts.py`  
**Logs:** `logs/production_alerts.ndjson`

**Monitors:**
- Webhook failures (>3 in 5min = CRITICAL)
- Payment error rate (>5% in 1h = CRITICAL)
- Revenue dip (>30% DoD = WARNING)
- SLO breaches and error budget burn

```bash
# Run alerts manually
python3 scripts/production_alerts.py | jq .

# View recent alerts
tail -20 logs/production_alerts.ndjson | jq .
```

---

## Incident Response

### 1. High Error Rate
```bash
# Check recent errors
grep '"status":5' logs/http_traces.ndjson | tail -30 | jq .

# Check system resources
curl http://localhost:5000/metrics | grep -E "(cpu|mem|disk)_percent"

# Review incidents
curl -H "X-Dash-Key: $DASHBOARD_KEY" \
  http://localhost:5000/api/incidents/summary | jq .
```

### 2. High Latency
```bash
# Get latency breakdown
curl -H "X-Dash-Key: $DASHBOARD_KEY" \
  http://localhost:5000/api/observability/latency | jq .

# Find slow requests
jq 'select(.duration_ms > 1000)' logs/http_traces.ndjson | tail -20

# Check autoscale status
curl -H "X-Dash-Key: $DASHBOARD_KEY" \
  http://localhost:5000/api/scale/status | jq .
```

### 3. Payment Issues
```bash
# Recent payment events
curl -H "X-Dash-Key: $DASHBOARD_KEY" \
  "http://localhost:5000/api/payments/events?limit=20" | jq .

# Webhook failures
grep '"ok":false' logs/stripe_webhooks.ndjson | tail -20 | jq .

# Cost status
curl -H "X-Dash-Key: $DASHBOARD_KEY" \
  http://localhost:5000/api/costs/status | jq .
```

---

## Maintenance

### Workflows
```bash
# Check scheduler
tail -f logs/scheduler.log | grep -E "(alerts_run_slo|production_alerts)"

# Restart workflows (if needed)
# Use Replit UI to restart "EchoPilot Bot" and "Scheduler"
```

### Logs
```bash
# HTTP traces
tail -f logs/http_traces.ndjson | jq .

# Production alerts
tail -f logs/production_alerts.ndjson | jq .

# SLO reports
cat logs/slo_report.json | jq .

# Scheduler
tail -f logs/scheduler.log
```

---

## Emergency Procedures

### SLO Breach
1. Check error budget status
2. Review recent changes/deployments
3. See `docs/SLOS.md` for detailed remediation

### System Overload
1. Check CPU/memory/disk in `/metrics`
2. Scale workers if needed
3. Enable cost guardrails if spending spike

### Data Loss
1. Check latest DR backup: `ls -lh backups/dr/`
2. Contact support for restore assistance
3. Review backup logs

---

## Regular Operations

### Daily Checks
- Review enterprise report (auto-generated)
- Check SLO status
- Review production alerts log

### Weekly Checks
- Review error budget consumption
- Check DR backup success
- Review cost trends

### Monthly Checks
- Full SLO review
- Error budget policy adjustments
- Capacity planning

---

## References

- **SLO Documentation:** `docs/SLOS.md`
- **Post-Launch Checklist:** `POST_LAUNCH_CHECKLIST.md`
- **Production Ops:** `PRODUCTION_OPS_DEPLOYED.md`
- **Phase 81-100 Summary:** `PHASES_81_100_SUMMARY.md`
