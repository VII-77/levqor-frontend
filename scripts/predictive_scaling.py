#!/usr/bin/env python3
"""
Phase 71: Predictive Scaling
Forecasts CPU/RAM/latency trends for proactive scaling
"""
import os
import sys
import json
import statistics as st
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def project_metric(values):
    """Project metric trends and calculate P95"""
    if not values:
        return {"current": 0, "p95": 0, "trend": "unknown", "avg": 0}
    
    # Calculate statistics
    current = values[-1] if values else 0
    avg = st.mean(values) if values else 0
    p95 = sorted(values)[int(0.95 * len(values)) - 1] if len(values) > 1 else current
    
    # Determine trend
    if len(values) > 3:
        recent_avg = st.mean(values[-3:])
        if recent_avg > avg * 1.1:
            trend = "up"
        elif recent_avg < avg * 0.9:
            trend = "down"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"
    
    return {
        "current": round(current, 2),
        "p95": round(p95, 2),
        "avg": round(avg, 2),
        "trend": trend,
        "samples": len(values)
    }

def analyze_scaling_needs():
    """Analyze system metrics and predict scaling needs"""
    try:
        cpu_values = []
        ram_values = []
        latency_values = []
        
        # Read ops sentinel data
        if os.path.exists('logs/ops_sentinel.ndjson'):
            with open('logs/ops_sentinel.ndjson', 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        if 'cpu_pct' in data:
                            cpu_values.append(data['cpu_pct'])
                        if 'ram_pct' in data:
                            ram_values.append(data['ram_pct'])
                        if 'lat_ms' in data:
                            latency_values.append(data['lat_ms'])
                    except:
                        continue
        
        # Project each metric
        cpu_projection = project_metric(cpu_values[-100:])  # Last 100 samples
        ram_projection = project_metric(ram_values[-100:])
        latency_projection = project_metric(latency_values[-100:])
        
        # Determine scaling recommendation
        recommendations = []
        
        if cpu_projection['p95'] > 80:
            recommendations.append("HIGH CPU: Consider adding workers")
        elif cpu_projection['trend'] == 'up' and cpu_projection['p95'] > 60:
            recommendations.append("CPU trending up: Monitor for scaling")
        
        if ram_projection['p95'] > 85:
            recommendations.append("HIGH MEMORY: Consider upgrading instance")
        elif ram_projection['trend'] == 'up' and ram_projection['p95'] > 70:
            recommendations.append("RAM trending up: Monitor for scaling")
        
        if latency_projection['p95'] > 1500:
            recommendations.append("HIGH LATENCY: Investigate bottlenecks")
        elif latency_projection['trend'] == 'up':
            recommendations.append("Latency trending up: Monitor performance")
        
        if not recommendations:
            recommendations.append("System metrics healthy - no action needed")
        
        result = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "cpu": cpu_projection,
            "ram": ram_projection,
            "latency": latency_projection,
            "recommendations": recommendations
        }
        
        # Save prediction
        os.makedirs('logs', exist_ok=True)
        with open('logs/predictive_scaling.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        # Also append to historical log
        with open('logs/predictive_scaling.ndjson', 'a') as f:
            f.write(json.dumps({
                "ts": result['ts'],
                "cpu_p95": cpu_projection['p95'],
                "ram_p95": ram_projection['p95'],
                "lat_p95": latency_projection['p95']
            }) + '\n')
        
        return {"ok": True, "data": result}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = analyze_scaling_needs()
    print(json.dumps(result, indent=2))
