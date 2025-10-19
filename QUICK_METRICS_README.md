# EchoPilot Quick Metrics & System Pulse

## Overview

Cross-database metrics aggregation and daily System Pulse reporting for EchoPilot AI automation platform.

**Features:**
- 📊 Real-time metrics from 7 Notion databases
- 🎯 Daily automated System Pulse at 06:30 UTC
- 💰 Revenue and ROI tracking
- ⚡ Uptime monitoring from health logs
- 📝 Governance ledger integration

---

## API Endpoints

### GET `/metrics`

Returns aggregated metrics from all databases.

**Request:**
```bash
curl -fsS "https://echopilotai.replit.app/metrics"
```

**Response:**
```json
{
  "jobs_7d": 42,
  "avg_qa_7d": 87.3,
  "revenue_7d": 1250.50,
  "roi_30d": 234.5,
  "uptime_pct": 99.8
}
```

**Metrics Explained:**
- `jobs_7d` - Total jobs processed in last 7 days (from Job Log)
- `avg_qa_7d` - Average QA score (%) over last 7 days
- `revenue_7d` - Total paid revenue ($) in last 7 days (from Finance DB)
- `roi_30d` - Average ROI (%) over last 30 days (from Cost Dashboard)
- `uptime_pct` - System uptime percentage over last 7 days

---

### POST `/pulse?token=<token>`

Creates a System Pulse entry in Governance Ledger.

**Request:**
```bash
curl -X POST "https://echopilotai.replit.app/pulse?token=$HEALTH_TOKEN"
```

**Response:**
```json
{
  "ok": true,
  "id": "2916155c-cf54-8196-...",
  "metrics": {
    "jobs_7d": 42,
    "avg_qa_7d": 87.3,
    "revenue_7d": 1250.50,
    "roi_30d": 234.5,
    "uptime_pct": 99.8
  }
}
```

**Authentication:**
- Requires `HEALTH_TOKEN` as query parameter
- Returns 401 Unauthorized if token is missing or invalid

---

## Daily Automation

### System Pulse Schedule

**Time:** 06:30 UTC Daily  
**Action:** Automatically triggers `/pulse` endpoint  
**Location:** Writes to Notion Governance Ledger  
**Idempotency:** Runs once per day (tracked via `tmp/last_pulse_utc.txt`)

**Entry Format:**
```
Title: System Pulse 2025-10-19
Notes: Jobs 42 | QA 87.3% | Rev $1250.50 | ROI 234.5% | Uptime 99.8%
Severity: Info
Source: Ops Monitor
```

---

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `HEALTH_TOKEN` | Authentication token for pulse endpoint | `abc123...` |
| `JOB_LOG_DB_ID` | Notion Job Log database ID | `a1b2c3d4...` |

### Optional (for enhanced metrics)

| Variable | Description |
|----------|-------------|
| `NOTION_GOVERNANCE_DB_ID` | Governance Ledger database for pulse entries |
| `NOTION_FINANCE_DB_ID` | Finance database for revenue tracking |
| `NOTION_COST_DASHBOARD_DB_ID` | Cost Dashboard for ROI metrics |

**Note:** Missing optional databases will return 0 for those metrics (graceful degradation).

---

## Health Logging

### Location
`logs/health.ndjson` - NDJSON format (one JSON object per line)

### Format
```json
{"timestamp": "2025-10-19T12:34:56Z", "status": "ok"}
{"timestamp": "2025-10-19T12:35:56Z", "status": "ok"}
```

### Retention
- Keeps last 7 days only
- Automatically cleaned on each write
- Used to calculate `uptime_pct` metric

---

## Data Sources

### Metrics Aggregation Map

| Metric | Source Database | Property | Time Range |
|--------|----------------|----------|------------|
| `jobs_7d` | Job Log | Count rows | Last 7 days |
| `avg_qa_7d` | Job Log | QA Score (number) | Last 7 days |
| `revenue_7d` | Finance | Amount (where Paid=true) | Last 7 days |
| `roi_30d` | Cost Dashboard | ROI (number) | Last 30 days |
| `uptime_pct` | Health Logs | Status="ok" vs total | Last 7 days |

---

## Usage Examples

### Check Current Metrics
```bash
curl -fsS "https://echopilotai.replit.app/metrics" | python3 -m json.tool
```

### Manually Trigger Pulse
```bash
curl -X POST -fsS \
  "https://echopilotai.replit.app/pulse?token=$HEALTH_TOKEN" \
  | python3 -m json.tool
```

### View Health Logs
```bash
cat logs/health.ndjson | tail -20
```

### Check Last Pulse Time
```bash
cat tmp/last_pulse_utc.txt
# Output: 2025-10-19
```

---

## Testing

### Smoke Tests

**Test 1: Metrics Endpoint**
```bash
curl -fsS "$BASE_URL/metrics" | python3 -m json.tool
# Expected: JSON with 5 keys (jobs_7d, avg_qa_7d, revenue_7d, roi_30d, uptime_pct)
```

**Test 2: Pulse Endpoint**
```bash
curl -X POST -fsS "$BASE_URL/pulse?token=$HEALTH_TOKEN" | python3 -m json.tool
# Expected: {"ok": true, "id": "...", "metrics": {...}}
```

**Test 3: Auth Check**
```bash
curl -X POST -fsS "$BASE_URL/pulse?token=wrong"
# Expected: 401 Unauthorized
```

---

## Troubleshooting

### Missing Metrics

**Problem:** Some metrics return 0  
**Cause:** Optional database not configured  
**Solution:** Add database ID to environment variables

### Pulse Not Creating Entries

**Problem:** `/pulse` returns ok but no Notion entry  
**Cause:** `NOTION_GOVERNANCE_DB_ID` not configured  
**Solution:** Add Governance DB ID to secrets

### Health Logs Not Recording

**Problem:** `uptime_pct` always 100%  
**Cause:** Health logs file missing or empty  
**Solution:** Health logging starts automatically on first `/health` request

---

## Architecture

```
┌─────────────────┐
│  Flask App      │
│  (run.py)       │
└────────┬────────┘
         │
         ├─► GET /metrics ─────► bot/metrics.py:get_metrics()
         │                        │
         │                        ├─► Query Job Log DB
         │                        ├─► Query Finance DB
         │                        ├─► Query Cost Dashboard DB
         │                        └─► Read logs/health.ndjson
         │
         └─► POST /pulse ────────► bot/metrics.py:write_pulse()
                                   │
                                   └─► Create Governance Ledger entry
                                   
┌─────────────────┐
│  Scheduler      │
│  (main.py)      │
└────────┬────────┘
         │
         └─► 06:30 UTC ─────────► bot/pulse_scheduler.py
                                   │
                                   ├─► Check tmp/last_pulse_utc.txt
                                   ├─► POST /pulse (internal)
                                   └─► Mark complete
```

---

## File Structure

```
bot/
  ├── metrics.py              # Core metrics aggregation logic
  ├── pulse_scheduler.py      # Daily pulse scheduler (06:30 UTC)
  └── main.py                 # Bot with integrated pulse scheduler

run.py                        # Flask app with /metrics and /pulse routes

logs/
  └── health.ndjson          # Health check history (7 days)

tmp/
  └── last_pulse_utc.txt     # Last pulse execution date (idempotency)

QUICK_METRICS_README.md      # This file
```

---

## Integration with Existing System

**Zero downtime:** All existing bot functionality remains unchanged  
**Graceful degradation:** Missing databases return 0 instead of errors  
**Idempotent:** Daily pulse runs exactly once per day  
**Lightweight:** Minimal performance impact (runs once daily + on-demand)

---

## READY

✅ Endpoints: `/metrics` and `/pulse`  
✅ Daily automation: 06:30 UTC System Pulse  
✅ Health logging: Automatic tracking  
✅ Graceful fallbacks: Works with partial database configuration

**Test Now:**
```bash
BASE_URL="https://echopilotai.replit.app"
curl -fsS "$BASE_URL/metrics" | python3 -m json.tool
curl -X POST -fsS "$BASE_URL/pulse?token=$HEALTH_TOKEN" | python3 -m json.tool
```
