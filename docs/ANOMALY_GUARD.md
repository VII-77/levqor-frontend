# EchoPilot Phase 102 – Autonomous Maintenance & Anomaly Detection

## Purpose
Adds a 5-minute anomaly scan that:
- Monitors health endpoint latency + resource usage
- Calculates rolling mean/stdev to find outliers
- Auto-runs `self_heal.py` if latency > 3σ or CPU/MEM > 90%
- Logs to `logs/anomaly_guard.ndjson`

## Expected Behaviour

| Metric | Threshold | Action |
|---------|------------|--------|
| Health status != Healthy | immediate | self_heal |
| Latency > 3σ | anomaly | self_heal |
| CPU > 90% | resource | self_heal |
| MEM > 90% | resource | self_heal |
| Disk > 90% | warning | alert |

All results are appended to NDJSON logs for later analysis.

## How It Works

### Detection Logic
1. **Health Check**: Calls `/health` endpoint and measures latency
2. **Resource Check**: Uses psutil to measure CPU, memory, and disk usage
3. **Anomaly Score**: Calculates z-score using rolling 50-sample mean/stdev
4. **Auto-Heal Trigger**: Triggers `scripts/self_heal.py` if any threshold is breached

### Scheduling
- Runs every **5 minutes** via `exec_scheduler.py`
- Configured in Phase 102 section of the scheduler
- Non-blocking execution with 60-second timeout

### Logging Format
All events are logged to `logs/anomaly_guard.ndjson` in NDJSON format:

```json
{
  "ts": "2025-10-21T08:35:00.123456Z",
  "lat": {
    "latency_ms": 45.2,
    "ok": true
  },
  "res": {
    "cpu": 42.3,
    "mem": 31.5,
    "disk": 64.8
  },
  "score": 0.5,
  "mean": 43.1,
  "stdev": 3.8
}
```

When anomalies are detected, an additional alert entry is logged:

```json
{
  "event": "anomaly_trigger",
  "ts": "2025-10-21T08:40:00.123456Z",
  "reasons": ["latency_anomaly_3sigma (score=3.45)", "cpu_critical (92.1%)"],
  "latency": 150.5,
  "score": 3.45,
  "cpu": 92.1,
  "mem": 45.2,
  "disk": 68.3
}
```

## Benefits

### Self-Healing
Automatic restart if Notion/API stalls or becomes unresponsive.

### Early Warning
Detects latency spikes before complete failure occurs.

### Zero-Touch Ops
Runs every 5 minutes with no manual check-ins required.

## Expected Outcomes
- **Uptime**: Maintains 99.99% availability
- **Latency**: Stabilizes response times
- **Forensics**: Provides detailed logs for anomaly analysis

## Impact if Skipped
Minor failures can linger undetected leading to:
- Dashboard freeze
- Delayed job synchronization
- Cascading service degradation

## Monitoring

### View Recent Activity
```bash
tail -20 logs/anomaly_guard.ndjson
```

### Check Latest Status
```bash
python3 scripts/anomaly_guard.py
```

### Analyze Anomaly Patterns
```bash
grep anomaly_trigger logs/anomaly_guard.ndjson | jq .
```

## Configuration

The anomaly guard uses the following thresholds (hardcoded):
- **Latency Anomaly**: > 3 standard deviations from rolling mean
- **CPU Critical**: > 90%
- **Memory Critical**: > 90%
- **Disk Warning**: > 90%
- **Health Check**: Must return status "Healthy"

## Integration

The anomaly guard integrates with:
- **Self-Heal Script**: `scripts/self_heal.py` for automatic recovery
- **Scheduler**: Runs every 5 minutes via `exec_scheduler.py`
- **Metrics Collection**: Uses historical data for anomaly detection
- **Logging System**: NDJSON format for easy parsing and analysis

## Troubleshooting

### Anomaly Guard Not Running
1. Check scheduler logs: `tail logs/scheduler.log`
2. Verify script exists: `ls -la scripts/anomaly_guard.py`
3. Test manually: `python3 scripts/anomaly_guard.py`

### False Positives
If the anomaly guard triggers too frequently:
1. Review recent logs: `tail -50 logs/anomaly_guard.ndjson`
2. Check if latency baseline has changed
3. Adjust thresholds if system behavior has legitimately changed

### Self-Heal Not Triggering
1. Verify self_heal.py exists: `ls -la scripts/self_heal.py`
2. Check for errors in anomaly_guard logs
3. Test self-heal manually: `python3 scripts/self_heal.py`
