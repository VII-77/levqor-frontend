#!/usr/bin/env python3
"""
Phase 76: SLO Budget Tracking
Compute P95/P99 latency, error rates, and track error budget burn
"""
import os
import sys
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configuration from environment
SLO_LAT_P95_MS = int(os.getenv('SLO_LAT_P95_MS', '800'))
SLO_LAT_P99_MS = int(os.getenv('SLO_LAT_P99_MS', '1200'))
SLO_ERR_BUDGET_DAILY_PCT = float(os.getenv('SLO_ERR_BUDGET_DAILY_PCT', '1.0'))
SLO_WINDOW_DAYS = int(os.getenv('SLO_WINDOW_DAYS', '30'))

def compute_slo_budget():
    """Compute SLO metrics and error budget burn"""
    try:
        latencies = []
        errors = 0
        total_requests = 0
        cutoff_time = time.time() - (SLO_WINDOW_DAYS * 86400)
        
        # Read metrics from job logs
        metrics_file = 'logs/ops_sentinel.ndjson'
        if os.path.exists(metrics_file):
            with open(metrics_file, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        ts = data.get('ts', 0)
                        
                        if ts > cutoff_time:
                            lat = data.get('lat_ms', 0)
                            if lat > 0:
                                latencies.append(lat)
                                total_requests += 1
                                
                                # Count as error if above SLO
                                if lat > SLO_LAT_P95_MS:
                                    errors += 1
                    except:
                        continue
        
        # Calculate percentiles
        if latencies:
            sorted_lats = sorted(latencies)
            p95_idx = int(0.95 * len(sorted_lats))
            p99_idx = int(0.99 * len(sorted_lats))
            
            p95_ms = sorted_lats[p95_idx] if p95_idx < len(sorted_lats) else sorted_lats[-1]
            p99_ms = sorted_lats[p99_idx] if p99_idx < len(sorted_lats) else sorted_lats[-1]
        else:
            p95_ms = 0
            p99_ms = 0
        
        # Calculate error rate
        error_rate = (errors / total_requests * 100) if total_requests > 0 else 0
        
        # Calculate error budget burn
        daily_budget = SLO_ERR_BUDGET_DAILY_PCT
        actual_error_pct = error_rate
        burn_rate = (actual_error_pct / daily_budget * 100) if daily_budget > 0 else 0
        remaining_budget_pct = max(0, 100 - burn_rate)
        
        # Determine burn alert level
        if burn_rate >= 200:  # 2x daily budget
            burn_alert = "CRITICAL"
        elif burn_rate >= 150:  # 1.5x daily budget
            burn_alert = "WARNING"
        elif burn_rate >= 100:  # At budget
            burn_alert = "WATCH"
        else:
            burn_alert = "OK"
        
        result = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "period_days": SLO_WINDOW_DAYS,
            "p95_ms": round(p95_ms, 2),
            "p99_ms": round(p99_ms, 2),
            "error_rate": round(error_rate, 2),
            "total_requests": total_requests,
            "errors": errors,
            "remaining_budget_pct": round(remaining_budget_pct, 2),
            "burn_rate_pct": round(burn_rate, 2),
            "burn_alert": burn_alert,
            "slo_targets": {
                "p95_ms": SLO_LAT_P95_MS,
                "p99_ms": SLO_LAT_P99_MS,
                "daily_error_budget_pct": SLO_ERR_BUDGET_DAILY_PCT
            }
        }
        
        # Save to files
        os.makedirs('logs', exist_ok=True)
        
        # Latest status
        with open('logs/slo_budget.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        # Append to NDJSON log
        with open('logs/slo_budget.ndjson', 'a') as f:
            f.write(json.dumps({
                "event": "slo_tick",
                "ts": result['ts'],
                "p95": p95_ms,
                "p99": p99_ms,
                "err_rate": error_rate,
                "burn": burn_rate,
                "alert": burn_alert
            }) + '\n')
        
        # Deploy gate: if burn is critical for sustained period
        if burn_alert == "CRITICAL":
            gate_file = Path('logs/deploy_gate.flag')
            gate_data = {
                "ts": result['ts'],
                "reason": f"SLO error budget burn at {burn_rate:.1f}% (>200% of daily budget)",
                "burn_rate_pct": burn_rate,
                "error_rate": error_rate
            }
            gate_file.write_text(json.dumps(gate_data, indent=2))
        
        return {"ok": True, "data": result}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = compute_slo_budget()
    print(json.dumps(result, indent=2))
