# LEVQOR AUTOMATED TASKS SCHEDULE

**Status**: ✅ ACTIVE  
**Scheduler**: APScheduler (Production-Grade)  
**Timezone**: UTC  

---

## 📅 SCHEDULED TASKS

### Daily Tasks

#### 1. Daily Database Backup
**Schedule**: `00:00 UTC` (Midnight)  
**Script**: Internal backup function  
**Purpose**: Create SQLite database snapshot  
**Log**: Application logs  
**Status**: ✅ Active

#### 2. PostgreSQL Backup (Phase-4)
**Schedule**: `03:00 UTC` (3 AM)  
**Script**: Internal PostgreSQL backup  
**Purpose**: Backup production PostgreSQL database  
**Log**: Application logs  
**Status**: ✅ Active

#### 3. Reset Daily Metrics
**Schedule**: `00:05 UTC` (12:05 AM)  
**Script**: Internal metrics reset  
**Purpose**: Reset daily counters for analytics  
**Log**: Application logs  
**Status**: ✅ Active

#### 4. Daily Cost Report
**Schedule**: `09:00 UTC` (9 AM)  
**Script**: `scripts/daily_cost_report.py`  
**Purpose**: Generate and email daily cost breakdown  
**Output**: Console + email notification  
**Log**: `logs/daily.log`  
**Status**: ✅ Active

#### 5. Spend Guard Check
**Schedule**: `10:00 UTC` (10 AM)  
**Script**: `monitors/spend_guard.py`  
**Purpose**: Check daily spending against $50 limit  
**Output**: Alert if threshold exceeded  
**Log**: `logs/spend_guard.log`  
**Status**: ✅ Active

### Weekly Tasks

#### 6. Weekly Backup with Checksum
**Schedule**: `02:00 UTC on Mondays` (2 AM Monday)  
**Script**: `scripts/backup_cycle.sh`  
**Purpose**: Full backup with SHA-256 verification  
**Features**:
- Database backup
- Checksum generation
- Optional Google Drive upload
- Retention policy (keep last 30)
**Log**: `logs/backup.log`  
**Status**: ✅ Active

---

## 📊 TASK OVERVIEW

```
┌─────────────────────────────────────────────────────────┐
│ TIME (UTC) │ TASK                     │ FREQUENCY      │
├────────────┼──────────────────────────┼────────────────┤
│ 00:00      │ Database Backup          │ Daily          │
│ 00:05      │ Reset Metrics            │ Daily          │
│ 02:00      │ Weekly Backup (Mon)      │ Weekly         │
│ 03:00      │ PostgreSQL Backup        │ Daily          │
│ 09:00      │ Cost Report              │ Daily          │
│ 10:00      │ Spend Guard Check        │ Daily          │
└────────────┴──────────────────────────┴────────────────┘
```

---

## 🔄 SCHEDULER DETAILS

**Implementation**: APScheduler (Python)  
**Execution**: Background daemon process  
**Misfire Grace Time**:
- Daily tasks: 15 minutes
- Spend guard: 10 minutes
- Weekly backup: 30 minutes

**Features**:
- Automatic retry on failure
- Graceful handling of missed runs
- Persistent across application restarts
- Full logging integration

---

## 📝 LOG FILES

All automated tasks write to dedicated log files:

```bash
# Daily cost report output
tail -f logs/daily.log

# Spend guard alerts
tail -f logs/spend_guard.log

# Weekly backup activity
tail -f logs/backup.log

# All scheduler activity (main app log)
tail -f logs/levqor.log
```

---

## ✅ VERIFICATION

**Check scheduler status:**
```bash
# View all registered jobs
curl http://localhost:5000/status
```

**Test individual tasks manually:**
```bash
# Test cost report
python3 scripts/daily_cost_report.py

# Test spend guard
python3 monitors/spend_guard.py

# Test backup cycle
bash scripts/backup_cycle.sh
```

---

## ⚙️ CONFIGURATION

**Modify schedule times** (edit `run.py`):
```python
scheduler.add_job(
    func=run_daily_cost_report,
    trigger=CronTrigger(hour=9, minute=0, timezone='UTC'),
    id='daily_cost_report',
    name='Daily Cost Report (09:00 UTC)',
    replace_existing=True
)
```

**Environment variables:**
- `DAILY_SPEND_LIMIT` - Spend guard threshold (default: $50)
- `GDRIVE_FOLDER_ID` - Enable Google Drive backups
- `TELEGRAM_CHAT_ID` - Enable Telegram alerts

---

## 🚨 ALERTS & NOTIFICATIONS

**Spend Guard Alerts:**
- Triggers when daily spending exceeds limit
- Sends alert via configured channels
- Pauses billing to prevent overages

**Backup Alerts:**
- Success/failure logged to console
- Optional Telegram notifications
- Email alerts for critical failures

**Cost Report:**
- Daily summary email
- Revenue vs. cost breakdown
- Partner commission tracking

---

## 📈 MONITORING

**Health Check:**
All scheduled tasks run automatically. Monitor via:
- Application logs
- `/ops/uptime` endpoint
- Log files in `logs/` directory

**Next Scheduled Runs:**
Check APScheduler logs on application startup to see when each job will next execute.

---

## 🎯 BENEFITS

✅ **Automated Operations** - Zero manual intervention  
✅ **Cost Control** - Daily spend limit protection  
✅ **Data Safety** - Regular backups with verification  
✅ **Financial Transparency** - Daily cost tracking  
✅ **Production Ready** - Battle-tested scheduler  
✅ **Easy Monitoring** - Centralized logging  

---

*Last Updated: 2025-11-07*  
*Scheduler Version: APScheduler 3.x*  
*Platform: Levqor v6.0*
