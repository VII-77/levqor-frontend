#!/usr/bin/env python3
"""
SLO Guard - Monitor SLOs and error budgets (Phase 51)

SLO Targets (configurable via environment variables):
- API Availability: 99.9% (43.2 min downtime/month) - set SLO_AVAILABILITY_PCT
- P95 Latency: < 800ms - set SLO_P95_TARGET_MS
- P99 Latency: < 1200ms - set SLO_P99_TARGET_MS
- Webhook Success: 99% - set SLO_WEBHOOK_SUCCESS_PCT
"""
import json
import os
from datetime import datetime, timedelta, timezone
from collections import defaultdict

# SLO Targets (configurable via environment variables)
SLO_TARGETS = {
    'availability_pct': float(os.getenv('SLO_AVAILABILITY_PCT', '99.9')),
    'p95_latency_ms': int(os.getenv('SLO_P95_TARGET_MS', '800')),
    'p99_latency_ms': int(os.getenv('SLO_P99_TARGET_MS', '1200')),
    'webhook_success_pct': float(os.getenv('SLO_WEBHOOK_SUCCESS_PCT', '99.0'))
}

# Error budget thresholds
ERROR_BUDGET_BURN_ALERT_PCT_PER_DAY = float(os.getenv('SLO_ERROR_BUDGET_PCT', '2.0'))  # Alert if burning >2% budget per day

NOW = datetime.now(timezone.utc)
WINDOW_DAYS = 30

def read_ndjson_lines(path, max_lines=100000):
    """Read NDJSON file"""
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
            return lines[-max_lines:] if len(lines) > max_lines else lines
    except:
        return []

def parse_timestamp(ts_str):
    """Parse ISO timestamp"""
    try:
        return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
    except:
        return None

def window_filter(lines, days):
    """Filter lines to time window"""
    cutoff = NOW - timedelta(days=days)
    result = []
    for line in lines:
        try:
            obj = json.loads(line)
            ts = parse_timestamp(obj.get('ts', ''))
            if ts and ts >= cutoff:
                result.append(obj)
        except:
            pass
    return result

def compute_availability(traces):
    """Compute API availability from HTTP traces"""
    if not traces:
        return 100.0, 0, 0
    
    total = len(traces)
    errors = sum(1 for t in traces if t.get('status', 200) >= 500)
    success = total - errors
    availability_pct = (success / total * 100) if total > 0 else 100.0
    
    return availability_pct, success, total

def compute_p95_latency(traces):
    """Compute P95 latency from HTTP traces"""
    if not traces:
        return 0.0
    
    durations = sorted([t.get('duration_ms', 0) for t in traces])
    idx = int(len(durations) * 0.95)
    return durations[min(idx, len(durations) - 1)]

def compute_p99_latency(traces):
    """Compute P99 latency from HTTP traces"""
    if not traces:
        return 0.0
    
    durations = sorted([t.get('duration_ms', 0) for t in traces])
    idx = int(len(durations) * 0.99)
    return durations[min(idx, len(durations) - 1)]

def compute_webhook_success(webhooks):
    """Compute webhook success rate"""
    if not webhooks:
        return 100.0, 0, 0
    
    total = len(webhooks)
    success = sum(1 for w in webhooks if w.get('ok', True) or w.get('status') in (200, '200'))
    success_pct = (success / total * 100) if total > 0 else 100.0
    
    return success_pct, success, total

def compute_error_budget(actual_pct, target_pct, window_days):
    """
    Compute error budget remaining and burn rate
    
    Error budget = allowed failure rate over the window
    For 99.9% availability: allowed 0.1% errors = 0.1% of requests can fail
    """
    if actual_pct >= target_pct:
        return {
            'remaining_pct': 100.0,
            'consumed_pct': 0.0,
            'burn_rate_pct_per_day': 0.0,
            'status': 'OK'
        }
    
    allowed_failure_pct = 100.0 - target_pct
    actual_failure_pct = 100.0 - actual_pct
    consumed_pct = (actual_failure_pct / allowed_failure_pct * 100) if allowed_failure_pct > 0 else 0
    remaining_pct = max(0, 100 - consumed_pct)
    burn_rate_pct_per_day = consumed_pct / window_days
    
    if burn_rate_pct_per_day > ERROR_BUDGET_BURN_ALERT_PCT_PER_DAY:
        status = 'CRITICAL'
    elif consumed_pct > 50:
        status = 'WARNING'
    else:
        status = 'OK'
    
    return {
        'remaining_pct': round(remaining_pct, 2),
        'consumed_pct': round(consumed_pct, 2),
        'burn_rate_pct_per_day': round(burn_rate_pct_per_day, 2),
        'status': status
    }

def main():
    # Read traces
    traces = window_filter(read_ndjson_lines('logs/http_traces.ndjson'), WINDOW_DAYS)
    webhooks = window_filter(read_ndjson_lines('logs/stripe_webhooks.ndjson'), WINDOW_DAYS)
    
    # Compute SLOs
    availability_pct, avail_success, avail_total = compute_availability(traces)
    p95_latency_ms = compute_p95_latency(traces)
    p99_latency_ms = compute_p99_latency(traces)
    webhook_success_pct, webhook_success, webhook_total = compute_webhook_success(webhooks)
    
    # Error budgets
    avail_budget = compute_error_budget(availability_pct, SLO_TARGETS['availability_pct'], WINDOW_DAYS)
    webhook_budget = compute_error_budget(webhook_success_pct, SLO_TARGETS['webhook_success_pct'], WINDOW_DAYS)
    
    # Latency status
    p95_status = 'OK' if p95_latency_ms <= SLO_TARGETS['p95_latency_ms'] else 'BREACH'
    p99_status = 'OK' if p99_latency_ms <= SLO_TARGETS['p99_latency_ms'] else 'BREACH'
    
    # Overall SLO status
    breaches = []
    if availability_pct < SLO_TARGETS['availability_pct']:
        breaches.append('availability')
    if p95_latency_ms > SLO_TARGETS['p95_latency_ms']:
        breaches.append('p95_latency')
    if p99_latency_ms > SLO_TARGETS['p99_latency_ms']:
        breaches.append('p99_latency')
    if webhook_success_pct < SLO_TARGETS['webhook_success_pct']:
        breaches.append('webhook_success')
    
    overall_status = 'BREACH' if breaches else 'OK'
    
    # Build report
    report = {
        'ts': NOW.isoformat().replace('+00:00', 'Z'),
        'window_days': WINDOW_DAYS,
        'overall_status': overall_status,
        'breaches': breaches,
        'slos': {
            'availability': {
                'actual_pct': round(availability_pct, 3),
                'target_pct': SLO_TARGETS['availability_pct'],
                'status': 'OK' if availability_pct >= SLO_TARGETS['availability_pct'] else 'BREACH',
                'success_requests': avail_success,
                'total_requests': avail_total,
                'error_budget': avail_budget
            },
            'p95_latency': {
                'actual_ms': round(p95_latency_ms, 2),
                'target_ms': SLO_TARGETS['p95_latency_ms'],
                'status': p95_status,
                'sample_count': len(traces)
            },
            'p99_latency': {
                'actual_ms': round(p99_latency_ms, 2),
                'target_ms': SLO_TARGETS['p99_latency_ms'],
                'status': p99_status,
                'sample_count': len(traces)
            },
            'webhook_success': {
                'actual_pct': round(webhook_success_pct, 3),
                'target_pct': SLO_TARGETS['webhook_success_pct'],
                'status': 'OK' if webhook_success_pct >= SLO_TARGETS['webhook_success_pct'] else 'BREACH',
                'success_webhooks': webhook_success,
                'total_webhooks': webhook_total,
                'error_budget': webhook_budget
            }
        }
    }
    
    # Write report
    os.makedirs('logs', exist_ok=True)
    with open('logs/slo_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Write alert if breach or high burn rate
    if overall_status == 'BREACH' or avail_budget['status'] in ('WARNING', 'CRITICAL') or webhook_budget['status'] in ('WARNING', 'CRITICAL'):
        alert = {
            'ts': NOW.isoformat().replace('+00:00', 'Z'),
            'event': 'slo_alert',
            'severity': 'CRITICAL' if overall_status == 'BREACH' else 'WARNING',
            'breaches': breaches,
            'availability_error_budget': avail_budget,
            'webhook_error_budget': webhook_budget,
            'p95_latency_ms': round(p95_latency_ms, 2),
            'p99_latency_ms': round(p99_latency_ms, 2)
        }
        
        with open('logs/production_alerts.ndjson', 'a') as f:
            f.write(json.dumps(alert) + '\n')
    
    # Print summary
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
