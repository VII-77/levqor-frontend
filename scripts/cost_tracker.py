#!/usr/bin/env python3
"""
Phase 64: Cost Tracker
Infrastructure cost estimation (compute + storage)
"""
import os
import sys
import json
import glob
import time
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Pricing estimates (USD)
PRICES = {
    "storage_per_gb_month": 0.023,  # AWS S3 standard pricing
    "cpu_per_hour": 0.05,            # Reserved VM estimate
    "bandwidth_per_gb": 0.09         # Bandwidth out
}

def calculate_storage_size():
    """Calculate total log/backup storage size"""
    total_bytes = 0
    
    # Scan logs directory
    for pattern in ['logs/**/*', 'backups/**/*']:
        for filepath in glob.glob(pattern, recursive=True):
            if os.path.isfile(filepath):
                try:
                    total_bytes += os.path.getsize(filepath)
                except:
                    continue
    
    return total_bytes

def estimate_compute_hours():
    """Estimate compute hours from scheduler activity"""
    try:
        # Count scheduler ticks as proxy for activity
        tick_count = 0
        if os.path.exists('logs/scheduler.log'):
            with open('logs/scheduler.log', 'r') as f:
                for line in f:
                    if 'tick' in line:
                        tick_count += 1
        
        # Rough estimate: 60 ticks/hour, 0.1 CPU utilization
        hours = (tick_count / 60) * 0.1 if tick_count > 0 else 24 * 0.1  # Default 10% of 24h
        return hours
    except:
        return 2.4  # Default 10% of 24h

def generate_cost_report():
    """Generate infrastructure cost report"""
    try:
        # Calculate storage
        bytes_total = calculate_storage_size()
        gb = bytes_total / (1024 ** 3)  # Convert to GB
        
        # Estimate compute
        cpu_hours = estimate_compute_hours()
        
        # Calculate costs
        storage_cost = gb * PRICES['storage_per_gb_month']
        compute_cost = cpu_hours * PRICES['cpu_per_hour']
        total_cost = storage_cost + compute_cost
        
        # Build report
        report = {
            "ts": time.time(),
            "ts_iso": datetime.utcnow().isoformat() + "Z",
            "storage": {
                "bytes": bytes_total,
                "gb": round(gb, 4),
                "monthly_usd": round(storage_cost, 4)
            },
            "compute": {
                "estimated_hours": round(cpu_hours, 3),
                "monthly_usd": round(compute_cost, 3)
            },
            "total_monthly_usd": round(total_cost, 4),
            "pricing": PRICES
        }
        
        # Save report
        os.makedirs('logs', exist_ok=True)
        with open('logs/cost_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Also append to NDJSON
        with open('logs/cost_report.ndjson', 'a') as f:
            f.write(json.dumps({
                "ts": report['ts_iso'],
                "storage_gb": report['storage']['gb'],
                "total_usd": report['total_monthly_usd']
            }) + '\n')
        
        return {"ok": True, **report}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = generate_cost_report()
    print(json.dumps(result, indent=2))
