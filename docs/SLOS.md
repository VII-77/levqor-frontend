# Service Level Objectives (SLOs) - Phase 51

## Overview

EchoPilot maintains production-grade SLOs to ensure reliable, performant service delivery. This document defines our SLO targets, measurement methodology, and remediation procedures.

**Last Updated:** October 20, 2025  
**Phase:** 51 - Observability & SLOs

---

## SLO Targets

### 1. API Availability: 99.9%
**Definition:** Percentage of HTTP requests that return status < 500  
**Error Budget:** 0.1% (43.2 minutes of downtime per month)  
**Measurement Period:** Rolling 30 days

### 2. P95 Latency: < 400ms
**Definition:** 95th percentile of HTTP request duration  
**Measurement Period:** Rolling 30 days  
**Sample:** All HTTP requests logged to `logs/http_traces.ndjson`

### 3. Webhook Success: 99%
**Definition:** Percentage of Stripe webhooks that succeed  
**Error Budget:** 1% allowed failures  
**Measurement Period:** Rolling 30 days

---

## Measurement Methodology

### Data Sources
1. **HTTP Traces:** `logs/http_traces.ndjson`  
   - Records every HTTP request with timing and status
   - Format: `{"ts", "route", "method", "status", "duration_ms", "path"}`

2. **Webhook Logs:** `logs/stripe_webhooks.ndjson`  
   - Records all Stripe webhook deliveries
   - Format: `{"ts", "event_type", "event_id", "ok", "status"}`

3. **SLO Reports:** `logs/slo_report.json`  
   - Generated every 15 minutes by `slo_guard.py`
   - Contains current SLO status and error budgets

### Calculation Details

**Availability:**
```
availability_pct = (successful_requests / total_requests) * 100
where: successful = status < 500
```

**P95 Latency:**
```
p95_latency = percentile(all_durations, 95)
```

**Webhook Success:**
```
webhook_success_pct = (successful_webhooks / total_webhooks) * 100
where: successful = ok == true OR status == 200
```

**Error Budget:**
```
allowed_failure_pct = 100 - target_pct
actual_failure_pct = 100 - actual_pct
consumed_pct = (actual_failure_pct / allowed_failure_pct) * 100
remaining_pct = 100 - consumed_pct
burn_rate_pct_per_day = consumed_pct / window_days
```

---

## Error Budget Management

### Burn Rate Thresholds
- **OK:** <2% budget burn per day
- **WARNING:** 2-5% budget burn per day
- **CRITICAL:** >5% budget burn per day OR budget exhausted

### Alert Conditions
SLO Guard writes to `logs/production_alerts.ndjson` when:
1. Any SLO is breached (actual < target)
2. Error budget burn rate > 2% per day
3. Error budget consumed > 50%

**Alert Format:**
```json
{
  "ts": "2025-10-20T12:00:00Z",
  "event": "slo_alert",
  "severity": "CRITICAL",
  "breaches": ["availability", "p95_latency"],
  "availability_error_budget": {
    "remaining_pct": 25.5,
    "consumed_pct": 74.5,
    "burn_rate_pct_per_day": 2.48,
    "status": "CRITICAL"
  }
}
```

---

## Monitoring & Dashboards

### Real-Time Monitoring
**Prometheus Metrics:** `GET /metrics` (no auth required)
- `app_uptime_seconds`
- `http_requests_total{route,status}`
- `http_request_duration_ms_bucket{le}`
- `scheduler_tick_total`
- `stripe_webhook_fail_total`
- `payments_error_rate`
- `cpu_percent`, `mem_percent`, `disk_percent`

### API Endpoints
**SLO Report:** `GET /api/observability/slo` (requires `X-Dash-Key`)
- Current SLO status
- Error budgets
- Breach information

**Latency Metrics:** `GET /api/observability/latency` (requires `X-Dash-Key`)
- P50/P95/P99 latency (24h)
- Last 60 request durations (for sparkline)

### Scheduled Checks
- **SLO Guard:** Runs every 15 minutes via scheduler
- **Production Alerts:** Runs every 5 minutes via scheduler

---

## Remediation Procedures

### SLO Breach Response

#### 1. Availability Breach (< 99.9%)
**Immediate Actions:**
1. Check recent incidents: `curl /api/incidents/summary`
2. Review error logs: `grep -i error logs/*.ndjson | tail -50`
3. Check system health: `curl /api/system-health`
4. Review production alerts: `tail -20 logs/production_alerts.ndjson`

**Root Cause Analysis:**
- Identify which routes are failing: check `http_traces.ndjson` for 5xx status
- Check infrastructure: CPU, memory, disk usage in `/metrics`
- Review recent deployments or config changes

**Mitigation:**
- Roll back problematic deployments
- Scale resources if needed
- Implement circuit breakers for failing dependencies
- Enable auto-retry for transient failures

#### 2. P95 Latency Breach (> 400ms)
**Immediate Actions:**
1. Identify slow endpoints: `curl /api/observability/latency`
2. Check database performance: review query logs
3. Review autoscaling status: `curl /api/scale/status`

**Root Cause Analysis:**
- Profile slow endpoints with tracing data
- Check for N+1 queries or missing indexes
- Review external API dependencies
- Analyze traffic patterns

**Mitigation:**
- Add caching for heavy endpoints
- Optimize database queries
- Scale workers: `curl -X POST /api/scale/adjust`
- Implement request queueing

#### 3. Webhook Success Breach (< 99%)
**Immediate Actions:**
1. Check webhook logs: `tail -50 logs/stripe_webhooks.ndjson`
2. Review Stripe dashboard for webhook failures
3. Check network connectivity

**Root Cause Analysis:**
- Verify webhook endpoint availability
- Check signature verification logic
- Review Stripe webhook retry settings

**Mitigation:**
- Fix webhook handler bugs
- Increase timeout settings
- Enable Stripe webhook retry
- Implement async processing

---

## Error Budget Policy

### When Error Budget is Healthy (>50% remaining)
- **Development:** Normal velocity
- **Deployments:** Standard approval process
- **Changes:** Low-risk changes allowed

### When Error Budget is Low (20-50% remaining)
- **Development:** Focus on reliability over features
- **Deployments:** Increased scrutiny, require lead approval
- **Changes:** Only critical bug fixes

### When Error Budget is Exhausted (<20% remaining)
- **Development:** Full freeze on new features
- **Deployments:** Emergency fixes only
- **Changes:** Require VP approval
- **Action:** Dedicate team to reliability improvements

---

## Commands Reference

### Check SLO Status
```bash
# Run SLO guard manually
python3 scripts/slo_guard.py | jq .

# Get SLO report via API
curl -H "X-Dash-Key: $DASHBOARD_KEY" \
  http://localhost:5000/api/observability/slo | jq .

# Get latency metrics
curl -H "X-Dash-Key: $DASHBOARD_KEY" \
  http://localhost:5000/api/observability/latency | jq .
```

### View Metrics
```bash
# Prometheus metrics
curl http://localhost:5000/metrics

# Production alerts
tail -20 logs/production_alerts.ndjson | jq .

# HTTP traces
tail -50 logs/http_traces.ndjson | jq .
```

### Investigate Issues
```bash
# Recent errors
grep '"status":5' logs/http_traces.ndjson | tail -20 | jq .

# Slow requests (>1000ms)
jq 'select(.duration_ms > 1000)' logs/http_traces.ndjson | tail -20

# Webhook failures
grep '"ok":false' logs/stripe_webhooks.ndjson | tail -20 | jq .
```

---

## References

- **Implementation:** `scripts/slo_guard.py`
- **Metrics:** `GET /metrics` endpoint in `run.py`
- **Tracing:** HTTP middleware in `run.py`
- **Scheduler:** `scripts/exec_scheduler.py` (15-min interval)
- **Production Alerts:** `scripts/production_alerts.py`

---

**Note:** SLOs are measured over rolling 30-day windows. Short-term dips may not immediately breach SLOs, but sustained degradation will. Monitor error budget burn rate to catch issues early.
