#!/usr/bin/env python3
"""
Phase 53: Observability Snapshot
Creates real-time metrics JSON for dashboard
"""
import os
import sys
import json
import time
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def create_snapshot():
    """Create observability snapshot with system metrics"""
    try:
        import psutil
        
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Process metrics
        try:
            process = psutil.Process()
            process_mem = process.memory_info().rss / 1024 / 1024  # MB
        except:
            process_mem = 0
        
        # Check API health
        api_healthy = True
        api_latency = 0
        try:
            import requests
            start = time.time()
            r = requests.get('http://localhost:5000/', timeout=5)
            api_latency = time.time() - start
            api_healthy = r.status_code == 200
        except:
            api_healthy = False
            api_latency = 999
        
        # Read latest governance data
        governance_status = "unknown"
        try:
            with open('logs/governance_report.json', 'r') as f:
                gov = json.load(f)
                governance_status = gov.get('status', 'unknown')
        except:
            pass
        
        # Read ops sentinel data
        ops_warnings = []
        try:
            with open('logs/ops_sentinel.ndjson', 'r') as f:
                lines = f.readlines()
                if lines:
                    last = json.loads(lines[-1])
                    ops_warnings = last.get('warnings', [])
        except:
            pass
        
        snapshot = {
            "ts": time.time(),
            "ts_iso": datetime.utcnow().isoformat() + "Z",
            "system": {
                "cpu_percent": cpu_percent,
                "mem_percent": mem.percent,
                "mem_available_gb": mem.available / 1024 / 1024 / 1024,
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / 1024 / 1024 / 1024
            },
            "process": {
                "memory_mb": process_mem
            },
            "api": {
                "healthy": api_healthy,
                "latency_sec": api_latency
            },
            "health": {
                "governance_status": governance_status,
                "ops_warnings": ops_warnings,
                "overall": "healthy" if api_healthy and not ops_warnings else "degraded"
            }
        }
        
        # Save snapshot
        os.makedirs('logs', exist_ok=True)
        with open('logs/observability.json', 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        # Also append to NDJSON log
        with open('logs/observability.ndjson', 'a') as f:
            f.write(json.dumps(snapshot) + '\n')
        
        return {"ok": True, "snapshot": snapshot}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = create_snapshot()
    print(json.dumps(result, indent=2))
