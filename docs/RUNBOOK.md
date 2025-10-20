# EchoPilot Operations Runbook

## Overview

This runbook provides step-by-step procedures for common operational tasks, troubleshooting, and incident response.

## Table of Contents

1. [System Health Checks](#system-health-checks)
2. [Common Operations](#common-operations)
3. [Troubleshooting](#troubleshooting)
4. [Incident Response](#incident-response)
5. [Maintenance Procedures](#maintenance-procedures)

---

## System Health Checks

### Daily Health Check (5 minutes)

```bash
# 1. Check workflows are running
curl https://echopilotai.replit.app/api/status/summary

# 2. Review audit logs for anomalies
tail -100 logs/ndjson/audit.ndjson | grep '"ok":false'

# 3. Check error budget
curl https://echopilotai.replit.app/api/slo/status

# 4. Verify scheduler is active
curl https://echopilotai.replit.app/api/scheduler/status
```

**Expected Results:**
- Status summary shows "healthy"
- No repeated auth failures in audit logs
- Error budget >20%
- Scheduler shows "running"

### Weekly Health Check (15 minutes)

```bash
# 1. Review payment reconciliation
curl -H "X-Dash-Key: YOUR_KEY" \
  https://echopilotai.replit.app/api/payments/reconcile

# 2. Check disk usage
df -h

# 3. Review top errors
grep "error" logs/ndjson/audit.ndjson | tail -50

# 4. Verify backups
ls -lh backups/disaster_recovery/ | tail -10
```

---

## Common Operations

### Restart Scheduler

```bash
# Via Replit Workflows
# 1. Go to Replit UI
# 2. Stop "Scheduler" workflow
# 3. Start "Scheduler" workflow

# Verify it restarted
curl https://echopilotai.replit.app/api/scheduler/status
```

### Create Manual Backup

```bash
# Run backup script
python3 scripts/disaster_recovery.py

# Verify backup created
ls -lh backups/disaster_recovery/ | tail -1
```

### Rotate Dashboard Key

```bash
# 1. Generate new key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# 2. Update DASHBOARD_KEY secret in Replit
# 3. Update ROLES_JSON if using RBAC

# 4. Test new key
curl -H "X-Dash-Key: NEW_KEY" \
  https://echopilotai.replit.app/api/supervisor-status
```

### Clear Rate Limits

Rate limits clear automatically after window expires (60 seconds default).

For manual clear (requires code restart):
```bash
# Restart "EchoPilot Bot" workflow in Replit UI
```

### Process Stuck Job

```bash
# 1. Identify stuck job
curl -H "X-Dash-Key: YOUR_KEY" \
  https://echopilotai.replit.app/api/jobs/stuck

# 2. View job details
curl https://echopilotai.replit.app/api/job/{job_id}

# 3. Retry job
curl -X POST -H "X-Dash-Key: YOUR_KEY" \
  https://echopilotai.replit.app/api/job/{job_id}/retry
```

---

## Troubleshooting

### Dashboard Not Loading

**Symptoms:** Blank page, 404, or connection timeout

**Diagnosis:**
```bash
# Check if server is running
curl https://echopilotai.replit.app/api/status/summary

# Check workflow status
# Go to Replit UI → Workflows
```

**Resolution:**
1. Restart "EchoPilot Bot" workflow
2. Check for errors in workflow logs
3. Verify `ALLOW_DIRTY=true` if code is uncommitted
4. Try legacy dashboard: `/dashboard/v1`

### API Returns 429 (Rate Limited)

**Symptoms:** `{"ok": false, "error": "Rate limit exceeded"}`

**Diagnosis:**
```bash
# Check rate limit violations
grep "rate_limit_exceeded" logs/ndjson/audit.ndjson | tail -20
```

**Resolution:**
1. Wait 60 seconds for window to reset
2. Check for misconfigured automation
3. Verify no abuse from IP address

### Scheduler Not Running

**Symptoms:** No new job executions, stale metrics

**Diagnosis:**
```bash
# Check scheduler status
tail -50 logs/scheduler.log

# Check for errors
grep "ERROR" logs/scheduler.log
```

**Resolution:**
1. Restart "Scheduler" workflow
2. Check for blocking errors in logs
3. Verify Notion API credentials valid
4. Check `AUTOMATION_QUEUE_DB_ID` is set

### Stripe Webhook Failures

**Symptoms:** Missing payment confirmations, webhook errors

**Diagnosis:**
```bash
# Check webhook log
tail -50 logs/stripe_webhooks.log

# Check recent failures
grep "failed" logs/stripe_webhooks.log | tail -10
```

**Resolution:**
1. Verify `STRIPE_WEBHOOK_SECRET` is correct
2. Check Stripe dashboard for webhook delivery attempts
3. Ensure endpoint is publicly accessible
4. Review signature validation code

### High Latency (>500ms responses)

**Symptoms:** Slow dashboard, timeouts

**Diagnosis:**
```bash
# Check recent slow requests
grep "Slow request" logs/app.log | tail -20

# Check system load
top -n 1
```

**Resolution:**
1. Check if scheduler is overwhelming resources
2. Review database query performance
3. Clear LRU caches if stale
4. Consider scaling to larger VM

---

## Incident Response

### Severity Levels

- **P0 (Critical):** Complete system outage, payment failures, data loss
- **P1 (High):** Partial outage, degraded performance affecting users
- **P2 (Medium):** Minor functionality broken, workaround available
- **P3 (Low):** Cosmetic issues, documentation errors

### P0 Incident Response

1. **Acknowledge (< 5 minutes)**
   ```bash
   # Check system status
   curl https://echopilotai.replit.app/api/status/summary
   
   # Check all workflows running
   # Replit UI → Workflows
   ```

2. **Diagnose (< 15 minutes)**
   ```bash
   # Check recent errors
   tail -200 logs/ndjson/audit.ndjson
   
   # Check workflow logs
   # Replit UI → Workflows → View Logs
   
   # Check database connectivity
   psql $DATABASE_URL -c "SELECT 1"
   ```

3. **Mitigate (< 30 minutes)**
   - Restart affected workflows
   - Failover to legacy UI if new UI broken
   - Disable problematic feature flags
   - Scale resources if capacity issue

4. **Resolve**
   - Deploy fix
   - Verify resolution
   - Monitor for 30 minutes

5. **Postmortem (within 48 hours)**
   - Document timeline
   - Root cause analysis
   - Identify preventive measures
   - Update runbook

### Communication Templates

**Incident Detected:**
```
🚨 INCIDENT: {Brief description}
Severity: P{0-3}
Impact: {What's affected}
Status: Investigating
ETA: {Estimate or "Unknown"}
```

**Incident Resolved:**
```
✅ RESOLVED: {Brief description}
Root Cause: {Summary}
Resolution: {What was done}
Prevention: {Future steps}
Duration: {Time to resolution}
```

---

## Maintenance Procedures

### Planned Maintenance

1. **Schedule during low-traffic period** (typically 2-6 AM UTC)

2. **Pre-maintenance checklist:**
   ```bash
   # Create backup
   python3 scripts/disaster_recovery.py
   
   # Verify backup
   ls -lh backups/disaster_recovery/ | tail -1
   
   # Document current state
   curl https://echopilotai.replit.app/api/status/summary > pre_maint.json
   ```

3. **Perform maintenance**
   - Apply updates
   - Test functionality
   - Monitor for errors

4. **Post-maintenance verification:**
   ```bash
   # Health check
   curl https://echopilotai.replit.app/api/status/summary
   
   # Compare with pre-maintenance
   diff pre_maint.json <(curl https://echopilotai.replit.app/api/status/summary)
   
   # Monitor for 30 minutes
   tail -f logs/ndjson/audit.ndjson
   ```

### Database Maintenance

```bash
# Check database size
psql $DATABASE_URL -c "\
  SELECT pg_size_pretty(pg_database_size(current_database()))"

# Vacuum (reclaim space)
psql $DATABASE_URL -c "VACUUM ANALYZE"

# Check slow queries (if enabled)
psql $DATABASE_URL -c "\
  SELECT query, calls, total_time, mean_time \
  FROM pg_stat_statements \
  ORDER BY total_time DESC \
  LIMIT 10"
```

### Log Rotation

Logs auto-rotate when they exceed size limits. Manual rotation:

```bash
# Archive old logs
mkdir -p logs/archive/$(date +%Y%m%d)
mv logs/ndjson/*.ndjson logs/archive/$(date +%Y%m%d)/

# Restart workflows to create fresh logs
# Replit UI → Workflows → Restart
```

---

## Monitoring & Alerts

### Key Metrics to Monitor

1. **Uptime:** Target 99.9% (43 minutes downtime/month max)
2. **Latency:** P95 < 400ms
3. **Error Rate:** < 1% of requests
4. **Webhook Success:** > 99%
5. **Scheduler Tick:** Every 60 seconds

### Alert Thresholds

- **Critical:** Error budget < 10%, uptime < 99%
- **Warning:** Error budget < 25%, latency P95 > 500ms
- **Info:** New deployment, feature flag change

---

## Emergency Contacts

- **System Admin:** Check dashboard audit logs
- **Stripe Issues:** Stripe dashboard → Support
- **Notion API:** Notion help center
- **Replit Issues:** Replit support

---

**Last Updated:** October 20, 2025 (Boss Mode UI v2)  
**Version:** 2.0
