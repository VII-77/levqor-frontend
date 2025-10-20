# EchoPilot Operational Dashboard Guide
## Phase 101: Command & Control Layer

**Version:** 1.0  
**Last Updated:** October 20, 2025  
**Status:** Production Ready

---

## Overview

The **Operational Dashboard** is the command and control layer for EchoPilot's autonomous enterprise systems. It provides real-time monitoring, AI-powered command interpretation, and predictive maintenance capabilities.

**Key Features:**
- Live telemetry aggregation from all autonomous systems
- Governance loop (15-minute SLO compliance checks)
- AI-powered predictive maintenance
- Natural language command console
- Real-time system health visualization
- Automated alerting via Telegram

---

## Architecture

### Components

1. **Telemetry Collector** (`scripts/telemetry_collector.py`)
   - Aggregates metrics from scheduler, finance, SLO, security, system resources
   - Provides unified health status
   - Updates every 10 seconds via `/api/ops/telemetry`

2. **Governance Loop** (`scripts/governance_loop.py`)
   - Runs every 15 minutes
   - Compares SLO targets vs actuals
   - Calculates compliance index (0-100)
   - Triggers Telegram alerts on breach > 10%

3. **Predictive Maintenance** (`scripts/predictive_maintenance.py`)
   - Runs every hour
   - Uses GPT-4o-mini to forecast failures within 24h
   - Creates Notion tickets for high-risk predictions
   - Analyzes CPU, memory, disk, errors, webhooks, payments

4. **AI Command Console** (`scripts/ai_command_console.py`)
   - Interprets natural language admin commands
   - Uses GPT-4o-mini with function calling
   - Logs all actions to `logs/ai_console.ndjson`
   - Supports: status, audit, payments, KPIs, SLO, risk forecasts

---

## API Endpoints

### `/api/ops/telemetry` (GET)
**Authentication:** Requires `X-Dash-Key` header

**Description:** Returns live telemetry snapshot from all systems

**Response:**
```json
{
  "ts": "2025-10-20T18:50:00Z",
  "overall_health": "green|yellow|red",
  "autonomy": "verified|operational|degraded",
  "components": {
    "scheduler": {
      "status": "healthy",
      "pid": 6521,
      "heartbeat_age_seconds": 15.3,
      "last_tick": 150
    },
    "finance": {
      "status": "ok",
      "total_revenue_usd": 1250.00,
      "revenue_24h_usd": 150.00,
      "failed_payments_total": 2
    },
    "slo": {
      "status": "OK",
      "breaches": [],
      "availability_pct": 99.95,
      "p95_latency_ms": 180.5,
      "webhook_success_pct": 99.8,
      "error_budget_remaining_pct": 98.5
    },
    "security": {
      "status": "ok",
      "alerts_1h": 3,
      "critical": 0,
      "warning": 1,
      "info": 2,
      "threshold_status": "OK"
    },
    "system": {
      "cpu_percent": 45.2,
      "memory_percent": 62.1,
      "disk_percent": 68.3,
      "status": "healthy"
    },
    "automation": {
      "total_scripts": 73,
      "scheduled_tasks": 48,
      "status": "ok"
    },
    "governance": {
      "status": "OK",
      "compliance_index": 95,
      "okr_status": {
        "availability": "✅",
        "latency": "✅",
        "webhooks": "✅",
        "payments": "✅"
      },
      "last_check": "2025-10-20T18:45:00Z"
    }
  }
}
```

**Health Status:**
- `green` - All systems operational
- `yellow` - Minor issues detected (SLO degraded, high alerts)
- `red` - Critical issues (scheduler down, SLO breach)

**Usage:**
```bash
curl -H "X-Dash-Key: $DASHBOARD_KEY" \
  https://echopilotai.replit.app/api/ops/telemetry | jq .
```

---

## Scripts

### 1. Telemetry Collector
```bash
# Run manually
python3 scripts/telemetry_collector.py

# Output: JSON snapshot of all components
```

**Collects:**
- Scheduler: PID, heartbeat age, tick count
- Finance: Revenue (total, 24h), failed payments
- SLO: Overall status, breaches, availability, latency, webhooks, error budget
- Security: Alerts count (1h), severity breakdown
- System: CPU, memory, disk usage
- Automation: Script count, scheduled task count
- Governance: Compliance index, OKR status

### 2. Governance Loop
```bash
# Run manually
python3 scripts/governance_loop.py

# Scheduled: Every 15 minutes (automatic)
```

**Functions:**
- Checks SLO compliance (availability, latency, webhooks)
- Checks finance health (payment failure rate)
- Calculates compliance index (0-100 score)
- Determines overall status (OK/WARN/BREACH)
- Sends Telegram alert if breach severity > 10%

**Output:** `logs/governance_loop.ndjson`
```json
{
  "ts": "2025-10-20T18:45:00Z",
  "status": "OK",
  "compliance_index": 95,
  "slo": {
    "status": "OK",
    "breaches": [],
    "breach_severity": 0
  },
  "finance": {
    "status": "OK",
    "failure_rate_pct": 2.5
  },
  "okr_status": {
    "availability": "✅",
    "latency": "✅",
    "webhooks": "✅",
    "payments": "✅"
  }
}
```

**Compliance Index Scoring:**
- Start: 100 points
- -20 per SLO breach
- -10 if breach severity > 10%
- -15 if payment failure rate > 5%
- -5 if > 10 security alerts/hour

### 3. Predictive Maintenance
```bash
# Run manually
python3 scripts/predictive_maintenance.py

# Scheduled: Every hour (automatic)
```

**Functions:**
- Collects 24h historical metrics (CPU, memory, disk, errors)
- Uses GPT-4o-mini to predict failures within 24h
- Assesses risk level (LOW/MEDIUM/HIGH/CRITICAL)
- Creates Notion tickets for HIGH/CRITICAL predictions

**Output:** `logs/predictive_maintenance.ndjson`
```json
{
  "ts": "2025-10-20T19:00:00Z",
  "metrics": {
    "cpu_samples": [45.2],
    "memory_samples": [62.1],
    "disk_samples": [68.3],
    "error_count": 2,
    "webhook_failures": 1,
    "payment_failures": 0
  },
  "prediction": {
    "risk_level": "LOW",
    "predicted_failures": [],
    "recommendations": ["Continue monitoring", "Review disk usage trends"],
    "confidence": 85
  },
  "tickets_created": []
}
```

**Risk Levels:**
- `LOW` - No action needed
- `MEDIUM` - Monitor closely
- `HIGH` - Create ticket, plan preventive action
- `CRITICAL` - Immediate intervention required

### 4. AI Command Console
```bash
# Interactive mode
python3 scripts/ai_command_console.py

# Single command mode
python3 scripts/ai_command_console.py "show system status"
python3 scripts/ai_command_console.py "run audit"
python3 scripts/ai_command_console.py "analyze payments"
```

**Available Commands:**
- `show system status` - Display current health
- `run audit` - Execute final audit script
- `analyze payments` - Show payment metrics
- `summarize kpis` - Display key performance indicators
- `check slo` - Show SLO compliance
- `forecast risk` - Run predictive maintenance
- `view logs [filename]` - Show recent log entries

**How it Works:**
1. User enters natural language command
2. GPT-4o-mini interprets intent and extracts parameters
3. System executes corresponding function
4. Results displayed to user
5. Action logged to `logs/ai_console.ndjson`

**Example Session:**
```
EchoPilot Supervisor AI - Command Console
================================================================================

Command: show system status

🧠 Interpreting command...
   Command: show_system_status
   Action: Display current system health metrics

⚙️  Executing...
✅ Success!
{
  "overall_health": "green",
  "autonomy": "verified",
  "components": { ... }
}

📝 Action logged to logs/ai_console.ndjson
```

---

## Scheduler Integration

Both governance loop and predictive maintenance run automatically via the scheduler:

**In `scripts/exec_scheduler.py`:**
```python
# 47) Governance Loop - Every 15 minutes
if 'governance_loop' not in last_run or \
   (datetime.utcnow() - last_run['governance_loop']).total_seconds() >= (15 * 60):
    run_governance_loop()
    mark_run('governance_loop')

# 48) Predictive Maintenance - Every hour
if is_time_match(datetime.utcnow().hour, 0) and should_run('predictive_maintenance'):
    run_predictive_maintenance()
    mark_run('predictive_maintenance')
```

---

## Monitoring & Alerting

### Telegram Alerts

Governance loop sends Telegram alerts when:
- Breach severity > 10%
- Compliance index < 70
- Critical SLO violation

**Alert Format:**
```
🚨 GOVERNANCE ALERT

Status: BREACH
Compliance Index: 65/100
Breach Severity: 12.5%

Breaches: availability, p95_latency

Immediate review required!
```

**Configuration:**
- `TELEGRAM_BOT_TOKEN` - Bot token
- `TELEGRAM_CHAT_ID` - Chat/channel ID

### Logs

All Phase 101 components write to NDJSON logs:

- `logs/governance_loop.ndjson` - Governance checks
- `logs/predictive_maintenance.ndjson` - Maintenance predictions
- `logs/ai_console.ndjson` - AI command console actions
- `logs/maintenance_tickets.ndjson` - Predictive maintenance tickets

**View Recent Logs:**
```bash
tail -20 logs/governance_loop.ndjson | jq .
tail -20 logs/predictive_maintenance.ndjson | jq .
tail -20 logs/ai_console.ndjson | jq .
```

---

## Dashboard Cards (Conceptual)

The Ops Control Panel would include these 7 cards:

### Card 1: 🧠 System Health
- Heartbeat age (< 60s = green)
- Uptime percentage (> 99% = green)
- Scheduler status
- Resource usage (CPU, memory, disk)

### Card 2: 💰 Finance Live Feed
- Revenue Δ % (24h)
- Failed payments count
- Payment success rate
- Stripe webhook status

### Card 3: 🛡️ Security & Threat AI
- Alerts (< 1/h = green)
- Threat level
- Recent incidents
- Anomaly detection status

### Card 4: 📊 Governance KPIs
- OKR status (4 indicators)
- Compliance index (0-100)
- SLO breaches
- Error budget remaining

### Card 5: 📡 Scheduler & Automation
- 48+ jobs status
- Last run timestamps
- Failed task count
- Next scheduled runs

### Card 6: 🗂 Docs & Reports Viewer
- View `/docs/*.md`
- View `/logs/*.txt`
- Download audit reports
- Export compliance data

### Card 7: 🚨 Intervention Console
- Start/stop tasks
- Restart scheduler
- Run manual checks
- View live logs

---

## Security

### Authentication
- All `/api/ops/*` routes require `X-Dash-Key` header
- AI console logs all actions
- WebSocket channels (future) will use JWT tokens

### Data Protection
- No customer data exposed to AI console
- Logs auto-redacted before model input
- Telegram alerts sanitized

### Audit Trail
- Every AI command logged with timestamp, input, interpretation, execution
- Governance checks logged every 15 minutes
- Predictive maintenance runs logged hourly

---

## Troubleshooting

### Telemetry API Returns Error
**Problem:** `/api/ops/telemetry` returns 500 error

**Solution:**
```bash
# Test telemetry collector directly
python3 scripts/telemetry_collector.py

# Check for errors
# Fix any missing dependencies or file permissions
```

### Governance Loop Not Running
**Problem:** No entries in `logs/governance_loop.ndjson`

**Solution:**
```bash
# Run manually to test
python3 scripts/governance_loop.py

# Check scheduler is running
cat logs/scheduler.pid
ps -p $(cat logs/scheduler.pid)

# Verify scheduler includes governance loop
grep "governance_loop" scripts/exec_scheduler.py
```

### AI Command Console Fails
**Problem:** "OpenAI API key not configured"

**Solution:**
```bash
# Verify API key exists
echo $AI_INTEGRATIONS_OPENAI_API_KEY

# If missing, set it
export AI_INTEGRATIONS_OPENAI_API_KEY=your_key_here

# Test again
python3 scripts/ai_command_console.py "show system status"
```

### Predictive Maintenance Skipped
**Problem:** No predictions generated

**Solution:**
```bash
# Verify OpenAI API key
echo $AI_INTEGRATIONS_OPENAI_API_KEY

# Run manually with debug
python3 scripts/predictive_maintenance.py

# Check logs for errors
tail -20 logs/predictive_maintenance.ndjson | jq .
```

---

## Best Practices

1. **Monitor Compliance Index Daily**
   - Target: ≥ 90
   - Action if < 85: Investigate SLO breaches

2. **Review Predictive Maintenance Weekly**
   - Check for recurring HIGH risk predictions
   - Plan preventive actions for identified risks

3. **Use AI Console for Quick Checks**
   - Faster than manual log viewing
   - Natural language interface
   - All actions logged

4. **Set Up Telegram Alerts**
   - Get notified of critical breaches
   - Faster response time
   - Mobile-friendly

5. **Run Manual Audits Monthly**
   ```bash
   python3 scripts/final_audit.py
   python3 scripts/compliance_export.py
   ```

---

## Future Enhancements

- **Web UI Dashboard:** React-based real-time dashboard
- **WebSocket Live Updates:** Push-based telemetry updates
- **Historical Trends:** Time-series graphs for metrics
- **Anomaly Visualization:** Interactive anomaly detection charts
- **Custom Alerting Rules:** User-defined alert thresholds
- **Multi-User Access:** Role-based access control for dashboard

---

## References

- **Phase 51:** Observability & SLOs (`docs/SLOS.md`)
- **Runbook:** Operational procedures (`RUNBOOK.md`)
- **Final Audit:** System verification (`docs/FINAL_AUDIT_REPORT.md`)
- **Replit.md:** Platform architecture (`replit.md`)

---

**For Support:** Contact Fahad (Boss)  
**Documentation Version:** 1.0  
**Last Updated:** October 20, 2025
