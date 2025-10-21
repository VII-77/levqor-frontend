# Disaster Recovery Restore Procedure

## Overview
This document provides step-by-step instructions for restoring EchoPilot from a DR backup in the event of a catastrophic failure.

**Last Updated:** October 21, 2025  
**Backup Location:** `backups/dr/`  
**Automated Backups:** Daily at 02:30 UTC via scheduler

---

## Pre-Restore Checklist

### 1. Verify Backup Availability
```bash
# List all available backups
ls -lh backups/dr/

# Find latest backup
ls -t backups/dr/dr_backup_*.tar.gz | head -1

# Verify backup integrity
python3 scripts/verify_dr_backup.py
```

### 2. Document Current State
```bash
# Before starting, document the current (failed) state
date > restore_$(date +%Y%m%d_%H%M%S).log
curl http://localhost:5000/api/system-health >> restore_*.log 2>&1 || echo "Service down"
ps aux | grep -E "python|gunicorn" >> restore_*.log
ls -la logs/ >> restore_*.log
```

### 3. Assess Failure Scope
Determine what failed:
- **Complete system failure:** Full restore required
- **Data corruption:** Selective restore of affected directories
- **Configuration issue:** Restore configs/ only
- **Log loss:** Restore logs/ only

---

## Full System Restore

### Step 1: Stop All Services
```bash
# Stop running workflows
pkill -f gunicorn
pkill -f "python3 -u scripts/exec_scheduler.py"

# Verify processes stopped
ps aux | grep -E "python|gunicorn"
```

### Step 2: Backup Current (Failed) State
```bash
# Create safety backup of current state
mkdir -p backups/pre_restore/
tar -czf backups/pre_restore/failed_state_$(date +%Y%m%d_%H%M%S).tar.gz \
  logs/ data/ configs/ 2>/dev/null || true

# Verify backup created
ls -lh backups/pre_restore/
```

### Step 3: Select Restore Point
```bash
# List backups with timestamps
ls -lht backups/dr/

# Choose backup to restore (replace YYYYMMDD_HHMMSS with actual timestamp)
RESTORE_BACKUP="backups/dr/dr_backup_YYYYMMDD_HHMMSS.tar.gz"

# Verify backup integrity before restoring
tar -tzf $RESTORE_BACKUP | head -20
python3 scripts/verify_dr_backup.py
```

### Step 4: Restore Data
```bash
# Remove corrupted data (CAUTION: This is destructive)
rm -rf logs/ data/ configs/

# Extract backup
tar -xzf $RESTORE_BACKUP

# Verify extraction
ls -la logs/ data/ configs/
```

### Step 5: Verify Configuration
```bash
# Check critical files restored
test -f logs/scheduler.log && echo "✅ Scheduler log restored"
test -f logs/slo_report.json && echo "✅ SLO report restored"
test -d configs/ && echo "✅ Configs directory restored"
test -d data/ && echo "✅ Data directory restored"

# Check environment secrets still available
env | grep -E "TELEGRAM_BOT_TOKEN|NOTION|STRIPE" | wc -l
# Should show > 0 (secrets are in Replit environment, not in backup)
```

### Step 6: Restart Services
```bash
# Restart via Replit workflows
# Method 1: Use Replit UI to restart workflows
# Method 2: Restart programmatically (if available)

# For manual restart:
gunicorn -w 1 -k gthread -t 120 --bind 0.0.0.0:5000 run:app &
python3 -u scripts/exec_scheduler.py &

# Verify services started
ps aux | grep -E "gunicorn|scheduler"
```

### Step 7: Verify System Health
```bash
# Wait 30 seconds for initialization
sleep 30

# Check system health
curl -s http://localhost:5000/api/system-health | jq .

# Check enterprise validation
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  http://localhost:5000/api/validate/enterprise | jq '.validation.status'

# Check SLO status
python3 scripts/slo_guard.py | jq '.overall_status'

# Check scheduler
tail -20 logs/scheduler.log
```

### Step 8: Validate Data Integrity
```bash
# Check recent logs
tail -20 logs/production_alerts.ndjson
tail -20 logs/http_traces.ndjson

# Verify no corruption
find logs/ -name "*.ndjson" -exec sh -c 'echo "Checking {}"; cat {} | jq . > /dev/null 2>&1 && echo "✅ Valid JSON" || echo "❌ Invalid JSON"' \;

# Check file counts match backup
tar -tzf $RESTORE_BACKUP | wc -l
find logs/ data/ configs/ -type f | wc -l
# Counts should be similar (may differ slightly due to new logs)
```

---

## Selective Restore (Partial Recovery)

### Restore Only Logs
```bash
# Extract logs only
tar -xzf $RESTORE_BACKUP logs/

# Verify
ls -la logs/
tail -20 logs/scheduler.log
```

### Restore Only Configs
```bash
# Extract configs only
tar -xzf $RESTORE_BACKUP configs/

# Verify
ls -la configs/
```

### Restore Only Data
```bash
# Extract data only
tar -xzf $RESTORE_BACKUP data/

# Verify
ls -la data/
```

---

## Post-Restore Validation

### 1. Functional Tests
```bash
# Test API endpoints
curl -s http://localhost:5000/health

# Test authenticated endpoint
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  http://localhost:5000/api/system-health | jq .

# Test automation queue
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  http://localhost:5000/api/queue | jq .
```

### 2. Integration Tests
```bash
# Test Notion connectivity
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  http://localhost:5000/api/notion/status | jq .

# Test AI integration
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  http://localhost:5000/api/ai/status | jq .
```

### 3. Monitor for Issues
```bash
# Watch logs for errors (run in separate terminal)
tail -f logs/scheduler.log | grep -i error

# Watch production alerts
tail -f logs/production_alerts.ndjson | jq .
```

---

## Rollback (If Restore Fails)

### If Restore Made Things Worse
```bash
# Restore the failed state backup
tar -xzf backups/pre_restore/failed_state_*.tar.gz

# Restart services
# Use Replit UI to restart workflows
```

### Contact Support
If restore fails or system is unstable:
1. Document the issue: `logs/restore_issues.txt`
2. Preserve both backups (DR and pre-restore)
3. Review `logs/scheduler.log` for errors
4. Check Replit deployment logs

---

## Preventive Measures

### Regular Backup Verification
```bash
# Run weekly (automated in scheduler at 02:30 UTC):
python3 scripts/verify_dr_backup.py

# Alert if verification fails
```

### Backup Retention Policy
- **Keep:** Last 7 daily backups
- **Keep:** Last 4 weekly backups (Sunday)
- **Keep:** Last 3 monthly backups (1st of month)
- **Purge:** Backups older than 90 days

### Disaster Scenarios

| Scenario | Restore Type | RTO | RPO |
|----------|--------------|-----|-----|
| Complete VM failure | Full restore | 15 min | Last backup (max 24h) |
| Log corruption | Logs only | 5 min | Last backup |
| Config error | Configs only | 2 min | Last backup |
| Data loss | Data only | 10 min | Last backup |

**RTO:** Recovery Time Objective (time to restore)  
**RPO:** Recovery Point Objective (acceptable data loss)

---

## Quick Reference Commands

```bash
# Create backup
python3 scripts/dr_backups.py

# Verify backup
python3 scripts/verify_dr_backup.py

# List backups
ls -lht backups/dr/

# View backup contents
tar -tzf backups/dr/dr_backup_*.tar.gz | head

# Full restore
tar -xzf backups/dr/dr_backup_YYYYMMDD_HHMMSS.tar.gz

# Verify system health
curl -s http://localhost:5000/api/system-health | jq .
```

---

**Remember:** Always verify backup integrity BEFORE attempting a restore!
