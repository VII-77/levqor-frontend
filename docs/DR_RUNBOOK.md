# EchoPilot Disaster Recovery Runbook
**Phase 109: Edge Failover & Emergency Response**

## Overview
This runbook provides step-by-step procedures for handling EchoPilot production incidents, failovers, and disaster recovery scenarios.

---

## 🚨 Incident Response Levels

### Level 1: Degraded Performance
**Symptoms:** Slow responses, elevated latency (>1200ms P99)  
**Impact:** Users experience delays but system remains functional  
**Response Time:** 30 minutes

**Actions:**
1. Check `/health` endpoint for dependency status
2. Review `logs/slo_guard.ndjson` for error budget burn
3. Check SLO dashboard for latency trends
4. Scale up resources if needed (increase workers)
5. Monitor for 15 minutes for recovery

### Level 2: Partial Outage
**Symptoms:** Some features down, 5xx errors, database connection failures  
**Impact:** Core functionality impaired, some users affected  
**Response Time:** 15 minutes

**Actions:**
1. Check `/health` endpoint - review `dependencies` section
2. Verify database connectivity: `psql $DATABASE_URL`
3. Check Notion API status: `curl -I https://api.notion.com`
4. Review `logs/anomaly_guard.ndjson` for anomalies
5. Restart affected services if needed
6. Communicate status to users

### Level 3: Total Outage
**Symptoms:** App unreachable, all health checks failing  
**Impact:** All users affected, complete service disruption  
**Response Time:** IMMEDIATE

**Actions:**
1. Activate **Edge Failover** (see below)
2. Page on-call engineer
3. Notify stakeholders
4. Begin root cause analysis
5. Prepare incident report

---

## 🔄 Edge Failover Procedure

### Automatic Failover
**Trigger:** 3 consecutive health check failures (15-minute window)  
**Monitoring:** `scripts/edge_failover.py` runs every 5 minutes

**Automatic Actions:**
1. Monitor detects 3 failures: `/health` returns 500 or timeout
2. Telegram alert sent to ops team
3. Logs written to `logs/edge_failover.ndjson`
4. State saved to `logs/edge_failover_state.json`

**Verify Failover Status:**
```bash
# Check failover state
cat logs/edge_failover_state.json

# Check recent failover logs
tail -n 50 logs/edge_failover.ndjson
```

### Manual Failover
**Use When:** Planned maintenance, anticipated issues, or automatic failover needs override

**Steps:**
1. **Verify Railway fallback is healthy:**
   ```bash
   curl -i $RAILWAY_FALLBACK_URL/health
   ```

2. **Update environment variable:**
   ```bash
   # In Replit Secrets
   FAILOVER_MODE=true
   ```

3. **Restart workflows:**
   ```bash
   # Workflows will auto-restart on env change
   # Verify restart in Replit UI
   ```

4. **Verify failover:**
   ```bash
   curl -i echopilotai.replit.app/health
   # Should route to Railway fallback
   ```

5. **Monitor logs:**
   ```bash
   tail -f logs/edge_failover.ndjson
   ```

### Failback Procedure
**When to Failback:** Primary health restored for 30+ minutes

**Steps:**
1. **Verify primary health:**
   ```bash
   curl -i https://echopilotai.replit.app/health
   # Check dependencies all show "ok"
   ```

2. **Reset failover state:**
   ```bash
   # Update edge_failover_state.json
   echo '{"consecutive_failures": 0, "failover_active": false}' > logs/edge_failover_state.json
   ```

3. **Remove failover mode:**
   ```bash
   # In Replit Secrets
   # Delete FAILOVER_MODE variable
   ```

4. **Monitor for 1 hour:**
   ```bash
   watch -n 60 'curl -s https://echopilotai.replit.app/health | jq'
   ```

5. **Confirm normal operation:**
   - Check `/health` dependencies
   - Review SLO metrics
   - Verify no errors in logs

---

## 💾 Data Recovery

### Database Backup Restoration
**Location:** `logs/dr_backups/` (created daily at 02:30 UTC)

**Steps:**
1. **List available backups:**
   ```bash
   ls -lh logs/dr_backups/
   ```

2. **Identify backup to restore:**
   ```bash
   # Example: dr_backup_20251021_0230.sql
   BACKUP_FILE=logs/dr_backups/dr_backup_YYYYMMDD_HHMM.sql
   ```

3. **Restore database:**
   ```bash
   psql $DATABASE_URL < $BACKUP_FILE
   ```

4. **Verify restoration:**
   ```bash
   psql $DATABASE_URL -c "SELECT COUNT(*) FROM wh_job_log;"
   ```

### Notion Data Recovery
**Backup:** All Notion databases synced to Postgres warehouse nightly

**Steps:**
1. **Query warehouse for lost data:**
   ```bash
   psql $DATABASE_URL -c "SELECT * FROM wh_clients WHERE client_id = 'LOST_ID';"
   ```

2. **Export specific table:**
   ```bash
   psql $DATABASE_URL -c "\copy wh_automation_log TO 'backup.csv' CSV HEADER"
   ```

3. **Restore to Notion (if needed):**
   - Use Notion API to recreate records
   - See `scripts/warehouse_sync.py` for schema mapping

---

## 🔍 Diagnostic Commands

### Quick Health Check
```bash
# Overall health
curl -s https://echopilotai.replit.app/health | jq

# Strict SLO health
curl -s https://echopilotai.replit.app/healthz/strict | jq

# Supervisor status
curl -s "https://echopilotai.replit.app/supervisor?token=$HEALTH_TOKEN" | jq
```

### Check Dependencies
```bash
# Database
psql $DATABASE_URL -c "SELECT 1;"

# Notion API
curl -I -H "Authorization: Bearer $NOTION_TOKEN" https://api.notion.com/v1/databases/test

# OpenAI API
curl -I -H "Authorization: Bearer $AI_INTEGRATIONS_OPENAI_API_KEY" https://api.openai.com/v1/models
```

### Review Recent Logs
```bash
# Health checks
tail -n 100 logs/health.ndjson | jq

# SLO violations
tail -n 50 logs/slo_guard.ndjson | jq

# Anomaly detection
tail -n 50 logs/anomaly_guard.ndjson | jq

# Edge failover
tail -n 50 logs/edge_failover.ndjson | jq

# Scheduler status
tail -n 50 logs/scheduler.log | jq
```

### Check Workflow Status
```bash
# Check if workflows are running
ps aux | grep -E "(gunicorn|exec_scheduler|anomaly_guard)"

# Check scheduler heartbeat
tail -f logs/scheduler.log
```

---

## 📞 Escalation Contacts

### Level 1 (Degraded Performance)
- **First Responder:** On-call engineer
- **Communication:** Slack #ops-alerts
- **SLA:** 30 minutes

### Level 2 (Partial Outage)
- **Escalate To:** Engineering lead
- **Communication:** Slack #incidents + Telegram
- **SLA:** 15 minutes

### Level 3 (Total Outage)
- **Escalate To:** CTO + Engineering lead
- **Communication:** All channels + Phone
- **SLA:** IMMEDIATE

### Telegram Alerts
All critical alerts sent to: `$TELEGRAM_CHAT_ID`

---

## 🧪 Testing Procedures

### Test Failover (Monthly)
**Schedule:** First Monday of each month at 02:00 UTC

**Steps:**
1. **Notify team:** Post in #ops 24 hours advance
2. **Verify Railway fallback:** `curl $RAILWAY_FALLBACK_URL/health`
3. **Trigger test failover:** Set `FAILOVER_MODE=test`
4. **Monitor for 30 minutes:** Check logs and alerts
5. **Perform failback:** Reset failover state
6. **Document results:** Update runbook if needed

### DR Drill (Quarterly)
**Schedule:** Quarterly, aligned with Sunday at 01:00 UTC

**Automated via:** `scripts/dr_drill.py` (runs weekly, full drill quarterly)

**Manual Steps:**
1. **Backup verification:** Restore backup to test database
2. **Failover test:** Execute manual failover procedure
3. **Communication test:** Send test alerts to all channels
4. **Timing:** Document actual vs. target response times
5. **Lessons learned:** Update runbook with findings

---

## 📊 Post-Incident Review

### Within 24 Hours
1. **Timeline:** Document incident timeline with timestamps
2. **Root Cause:** Identify what went wrong and why
3. **Impact:** Calculate affected users, downtime duration
4. **Response:** Evaluate how well procedures worked

### Within 1 Week
1. **Report:** Complete incident report with findings
2. **Action Items:** List concrete improvements needed
3. **Runbook Updates:** Update this document with learnings
4. **Team Review:** Present findings to engineering team

---

## 🔐 Emergency Access

### Database Access
```bash
# Read-only access
psql $DATABASE_URL -c "SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY;"

# Emergency admin access (use caution)
psql $DATABASE_URL
```

### Secrets Rotation (if compromised)
```bash
# Run emergency rotation
python3 scripts/rotate_secrets.py --emergency

# Verify new secrets deployed
curl -s https://echopilotai.replit.app/health | jq '.dependencies'
```

---

## 📝 Checklist Templates

### Incident Response Checklist
- [ ] Incident detected and logged
- [ ] Severity level determined
- [ ] Appropriate team members notified
- [ ] Mitigation actions initiated
- [ ] Users informed of status
- [ ] Root cause identified
- [ ] Permanent fix implemented
- [ ] Incident report completed
- [ ] Runbook updated

### Failover Checklist
- [ ] Primary health check failed 3+ times
- [ ] Fallback health verified
- [ ] Telegram alert sent
- [ ] Failover state logged
- [ ] Team notified
- [ ] User communication sent
- [ ] Monitoring active
- [ ] Failback planned
- [ ] Post-mortem scheduled

---

## 🚀 Recovery Success Criteria

### Service Restored
- [ ] `/health` returns 200 for 30+ minutes
- [ ] All dependencies show "ok" status
- [ ] SLO error budget burn < 2%/day
- [ ] No 5xx errors in past 15 minutes
- [ ] Latency P99 < 1200ms

### Data Integrity
- [ ] Database queries returning expected results
- [ ] Notion sync completing successfully
- [ ] Warehouse ETL running without errors
- [ ] No data loss detected

### Monitoring
- [ ] All workflows running
- [ ] Logs flowing normally
- [ ] Alerts functioning
- [ ] Metrics collecting

---

**Last Updated:** 2025-10-21  
**Version:** 1.0.0  
**Owner:** EchoPilot Operations Team  
**Review Cycle:** Quarterly
