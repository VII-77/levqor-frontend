#!/usr/bin/env python3
"""
Phase 68: SLO Monitor Refinement
Enhanced SLO status tracking with historical logging
"""
import os
import sys
import json
import time
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def monitor_slo():
    """Monitor SLO status and log results"""
    try:
        # Read latest SLO report
        slo_data = {"ok": False, "breach": False}
        if os.path.exists("logs/slo_report.json"):
            try:
                with open("logs/slo_report.json", "r") as f:
                    slo_data = json.load(f)
            except:
                pass
        
        # Determine status
        status = "FAIL" if slo_data.get("breach") else "PASS"
        
        # Build monitoring result
        result = {
            "ts": time.time(),
            "ts_iso": datetime.utcnow().isoformat() + "Z",
            "status": status,
            "breach": slo_data.get("breach", False),
            "p95_ms": slo_data.get("p95_ms", 0),
            "success_rate": slo_data.get("success_rate", 1.0),
            "details": slo_data
        }
        
        # Append to status log
        os.makedirs("logs", exist_ok=True)
        with open("logs/slo_status.ndjson", "a") as f:
            f.write(json.dumps({
                "ts": result["ts_iso"],
                "status": status,
                "breach": result["breach"]
            }) + "\n")
        
        # Also save latest status
        with open("logs/slo_status.json", "w") as f:
            json.dump(result, f, indent=2)
        
        return {"ok": True, **result}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = monitor_slo()
    print(json.dumps(result, indent=2))
