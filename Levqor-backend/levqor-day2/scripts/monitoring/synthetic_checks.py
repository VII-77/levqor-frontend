"""
Synthetic Monitoring Checks
Runs health checks against critical endpoints every 15 minutes
"""
import requests
import time
from datetime import datetime
import os
import json

ENDPOINTS_TO_CHECK = [
    "https://api.levqor.ai/api/sandbox/metrics",
    "https://api.levqor.ai/api/insights/preview",
    "https://api.levqor.ai/health",
    "https://api.levqor.ai/api/intelligence/status",
]

def run_synthetic_checks():
    """Run synthetic health checks on all critical endpoints"""
    print(f"\n🔍 Running synthetic checks at {datetime.utcnow().isoformat()}")
    
    results = []
    
    for endpoint in ENDPOINTS_TO_CHECK:
        try:
            start = time.time()
            response = requests.get(endpoint, timeout=10)
            latency = int((time.time() - start) * 1000)
            
            result = {
                "endpoint": endpoint,
                "status_code": response.status_code,
                "latency_ms": latency,
                "success": response.status_code == 200,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            if response.status_code == 200:
                print(f"  ✅ {endpoint} - {latency}ms")
            else:
                print(f"  ❌ {endpoint} - {response.status_code}")
                
            results.append(result)
            
        except Exception as e:
            print(f"  ❌ {endpoint} - ERROR: {str(e)}")
            results.append({
                "endpoint": endpoint,
                "status_code": 0,
                "latency_ms": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
    
    # Calculate summary
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    success_rate = (successful / total * 100) if total > 0 else 0
    
    print(f"\n📊 Synthetic check summary: {successful}/{total} passed ({success_rate:.1f}%)")
    
    # Log to database if available
    try:
        from modules.auto_intel.db_adapter import log_intel_event
        log_intel_event(
            event='synthetic_check',
            value=success_rate,
            mean=100.0  # Target is 100%
        )
    except Exception as e:
        print(f"⚠️ Could not log to database: {e}")
    
    return results

if __name__ == "__main__":
    run_synthetic_checks()
