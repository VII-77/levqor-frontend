#!/usr/bin/env python3
"""
Phase 59: SLO Guardrails
Monitors service level objectives (latency & success rate)
"""
import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# SLO Thresholds
SLO_P95_MS = int(os.getenv('SLO_P95_MS', '1200'))  # 1.2 seconds
SLO_SUCCESS_RATE = float(os.getenv('SLO_SUCCESS_RATE', '0.98'))  # 98%

def load_ndjson(filepath):
    """Load NDJSON file and return list of records"""
    if not Path(filepath).exists():
        return []
    
    records = []
    with open(filepath, 'r') as f:
        for line in f:
            try:
                records.append(json.loads(line.strip()))
            except:
                continue
    return records

def evaluate_slo():
    """Evaluate SLO compliance"""
    try:
        # Load recent API access logs (last 1000 events)
        events = load_ndjson('logs/api_access.ndjson')[-1000:]
        
        if not events:
            # No data yet, create placeholder
            return {
                "ok": True,
                "p95_ms": 0,
                "success_rate": 1.0,
                "breach": False,
                "message": "No API access data yet"
            }
        
        # Extract latencies and success counts
        latencies = [e.get('lat_ms', 0) for e in events if 'lat_ms' in e]
        successful = sum(1 for e in events if e.get('ok', False))
        total = len(events)
        
        # Calculate P95 latency
        if latencies:
            sorted_latencies = sorted(latencies)
            p95_index = int(0.95 * len(sorted_latencies))
            p95_ms = sorted_latencies[p95_index] if p95_index < len(sorted_latencies) else sorted_latencies[-1]
        else:
            p95_ms = 0
        
        # Calculate success rate
        success_rate = successful / total if total > 0 else 1.0
        
        # Check for SLO breaches
        latency_breach = p95_ms > SLO_P95_MS
        success_breach = success_rate < SLO_SUCCESS_RATE
        breach = latency_breach or success_breach
        
        # Build report
        report = {
            "ts": time.time(),
            "ts_iso": datetime.utcnow().isoformat() + "Z",
            "p95_ms": round(p95_ms, 2),
            "success_rate": round(success_rate, 3),
            "breach": breach,
            "thresholds": {
                "p95_ms": SLO_P95_MS,
                "success_rate": SLO_SUCCESS_RATE
            },
            "breach_details": {
                "latency": latency_breach,
                "success": success_breach
            },
            "sample_size": total
        }
        
        # Save report
        os.makedirs('logs', exist_ok=True)
        with open('logs/slo_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Also append to NDJSON
        with open('logs/slo_report.ndjson', 'a') as f:
            f.write(json.dumps({
                "ts": report['ts_iso'],
                "p95_ms": report['p95_ms'],
                "success_rate": report['success_rate'],
                "breach": breach
            }) + '\n')
        
        # Send alert if breach
        if breach:
            alert_message = f"SLO Breach: "
            if latency_breach:
                alert_message += f"P95 latency {p95_ms:.0f}ms > {SLO_P95_MS}ms. "
            if success_breach:
                alert_message += f"Success rate {success_rate:.1%} < {SLO_SUCCESS_RATE:.1%}."
            
            # Log alert
            with open('logs/slo_alerts.ndjson', 'a') as f:
                f.write(json.dumps({
                    "ts": report['ts_iso'],
                    "message": alert_message
                }) + '\n')
        
        return {"ok": True, **report}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = evaluate_slo()
    print(json.dumps(result, indent=2))
