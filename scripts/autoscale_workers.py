#!/usr/bin/env python3
"""
Phase 80: Autoscale Workers
Predictive worker scaling based on queue depth and latency
"""
import os
import sys
import json
import time
from datetime import datetime, timedelta

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configuration
SCALE_MIN = int(os.getenv('SCALE_MIN', '1'))
SCALE_MAX = int(os.getenv('SCALE_MAX', '6'))
SCALE_COOLDOWN_MIN = int(os.getenv('SCALE_COOLDOWN_MIN', '10'))
SCALE_DRY_RUN = os.getenv('SCALE_DRY_RUN', 'true').lower() == 'true'

def compute_autoscale():
    """Compute desired worker count based on metrics"""
    try:
        # Check deploy gate
        deploy_gate_active = os.path.exists('logs/deploy_gate.flag')
        
        # Read metrics
        queue_depth = 0
        p95_latency = 0
        arrival_rate = 0
        
        # Mock queue depth - in production, read from actual queue
        if os.path.exists('logs/ops_sentinel.ndjson'):
            cutoff_time = time.time() - 1800  # Last 30 minutes
            latencies = []
            
            with open('logs/ops_sentinel.ndjson', 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        ts = data.get('ts', 0)
                        
                        if ts > cutoff_time:
                            lat = data.get('lat_ms', 0)
                            if lat > 0:
                                latencies.append(lat)
                    except:
                        continue
            
            if latencies:
                sorted_lats = sorted(latencies)
                p95_idx = int(0.95 * len(sorted_lats))
                p95_latency = sorted_lats[p95_idx] if p95_idx < len(sorted_lats) else sorted_lats[-1]
                arrival_rate = len(latencies) / 30  # Requests per minute
        
        # Simple scaling logic
        current_workers = 1  # Mock - in production, read actual worker count
        desired_workers = current_workers
        reason = "stable"
        
        # Scale up if high latency or queue backlog
        if p95_latency > 1000:
            desired_workers = min(SCALE_MAX, current_workers + 1)
            reason = "high_latency"
        elif arrival_rate > 10:
            desired_workers = min(SCALE_MAX, current_workers + 1)
            reason = "high_arrival_rate"
        
        # Scale down if low utilization
        elif p95_latency < 300 and arrival_rate < 2:
            desired_workers = max(SCALE_MIN, current_workers - 1)
            reason = "low_utilization"
        
        # Check cooldown
        last_scale_time = 0
        if os.path.exists('logs/autoscale.json'):
            try:
                with open('logs/autoscale.json', 'r') as f:
                    last = json.load(f)
                    last_ts = last.get('ts', '')
                    last_scale_time = datetime.fromisoformat(last_ts.replace('Z', '+00:00')).timestamp()
            except:
                pass
        
        cooldown_remaining = max(0, (SCALE_COOLDOWN_MIN * 60) - (time.time() - last_scale_time))
        in_cooldown = cooldown_remaining > 0
        
        # Don't scale up if deploy gate is active
        if deploy_gate_active and desired_workers > current_workers:
            desired_workers = current_workers
            reason = "deploy_gate_active"
        
        # Don't scale if in cooldown
        if in_cooldown and desired_workers != current_workers:
            desired_workers = current_workers
            reason = "in_cooldown"
        
        result = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "current_workers": current_workers,
            "desired_workers": desired_workers,
            "reason": reason,
            "dry_run": SCALE_DRY_RUN,
            "metrics": {
                "queue_depth": queue_depth,
                "p95_latency_ms": round(p95_latency, 2),
                "arrival_rate_per_min": round(arrival_rate, 2)
            },
            "constraints": {
                "min": SCALE_MIN,
                "max": SCALE_MAX,
                "cooldown_min": SCALE_COOLDOWN_MIN,
                "cooldown_remaining_sec": round(cooldown_remaining, 0),
                "deploy_gate_active": deploy_gate_active
            }
        }
        
        # Save status
        os.makedirs('logs', exist_ok=True)
        with open('logs/autoscale.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        # Log scaling decision
        with open('logs/autoscale.ndjson', 'a') as f:
            f.write(json.dumps({
                "event": "scale_decision",
                "ts": result['ts'],
                "current": current_workers,
                "desired": desired_workers,
                "reason": reason,
                "dry_run": SCALE_DRY_RUN
            }) + '\n')
        
        return {"ok": True, "data": result}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = compute_autoscale()
    print(json.dumps(result, indent=2))
