#!/usr/bin/env python3
"""Phase 93: Anomaly Detection - Statistical Anomaly Detection"""
import os, sys, json, statistics
from datetime import datetime

def detect_anomalies():
    """Detect statistical anomalies in metrics"""
    try:
        anomalies = []
        
        # Check latency anomalies
        if os.path.exists('logs/ops_sentinel.ndjson'):
            latencies = []
            with open('logs/ops_sentinel.ndjson', 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        if 'lat_ms' in data:
                            latencies.append(data['lat_ms'])
                    except:
                        pass
            
            if len(latencies) > 10:
                mean = statistics.mean(latencies)
                stdev = statistics.stdev(latencies)
                
                for lat in latencies[-5:]:
                    if lat > mean + (2 * stdev):
                        anomalies.append({
                            "type": "latency_spike",
                            "value": lat,
                            "threshold": mean + (2 * stdev),
                            "severity": "medium"
                        })
        
        result = {
            "ok": True,
            "ts": datetime.utcnow().isoformat() + "Z",
            "anomalies_detected": len(anomalies),
            "anomalies": anomalies[:10]
        }
        
        os.makedirs('logs', exist_ok=True)
        with open('logs/anomaly_detection.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        return result
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = detect_anomalies()
    print(json.dumps(result, indent=2))
