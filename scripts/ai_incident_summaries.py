#!/usr/bin/env python3
"""
Phase 75: AI Incident Summaries
Intelligent 24-hour incident aggregation and analysis
"""
import os
import sys
import json
import glob
import time
from datetime import datetime, timedelta

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def analyze_incidents():
    """Analyze last 24h of incidents and generate intelligent summary"""
    try:
        cutoff_time = time.time() - (24 * 3600)  # 24 hours ago
        events = []
        error_types = {}
        
        # Scan all NDJSON log files for events
        log_files = glob.glob('logs/*.ndjson')
        
        for log_file in log_files:
            try:
                with open(log_file, 'r') as f:
                    for line in f:
                        try:
                            event = json.loads(line)
                            
                            # Extract timestamp (various formats)
                            ts = event.get('ts') or event.get('time') or event.get('timestamp')
                            
                            # Convert ISO string to unix timestamp if needed
                            if isinstance(ts, str):
                                try:
                                    dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                                    ts = dt.timestamp()
                                except:
                                    continue
                            
                            # Only include recent events
                            if isinstance(ts, (int, float)) and ts > cutoff_time:
                                events.append(event)
                                
                                # Track error types
                                if 'error' in event:
                                    error_type = event.get('event', 'unknown')
                                    error_types[error_type] = error_types.get(error_type, 0) + 1
                        
                        except json.JSONDecodeError:
                            continue
            
            except Exception:
                continue
        
        # Calculate severity
        event_count = len(events)
        if event_count > 100:
            severity = "high"
        elif event_count > 20:
            severity = "medium"
        else:
            severity = "low"
        
        # Generate intelligent recommendations
        recommendations = []
        
        # Check for specific patterns
        if error_types:
            top_errors = sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:3]
            for error, count in top_errors:
                recommendations.append(f"Investigate {error}: {count} occurrences")
        
        # Load predictive scaling data for CPU/RAM recommendations
        if os.path.exists('logs/predictive_scaling.json'):
            try:
                with open('logs/predictive_scaling.json', 'r') as f:
                    scaling = json.load(f)
                    if scaling.get('cpu', {}).get('p95', 0) > 80:
                        recommendations.append("Scale workers - CPU P95 exceeds threshold")
                    if scaling.get('ram', {}).get('p95', 0) > 85:
                        recommendations.append("Upgrade instance - RAM P95 exceeds threshold")
            except:
                pass
        
        # Check SLO status
        if os.path.exists('logs/slo_status.json'):
            try:
                with open('logs/slo_status.json', 'r') as f:
                    slo = json.load(f)
                    if slo.get('breach'):
                        recommendations.append("SLO breach detected - Review latency and success rates")
            except:
                pass
        
        # Default recommendations if none found
        if not recommendations:
            recommendations = [
                "System operating normally - no critical issues",
                "Continue monitoring P95 latency and success rates",
                "Review backup integrity on schedule"
            ]
        
        # Build summary
        summary = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "period_hours": 24,
            "events_analyzed": event_count,
            "severity": severity,
            "top_errors": dict(sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:5]),
            "recommendations": recommendations
        }
        
        # Save summary
        os.makedirs('logs', exist_ok=True)
        with open('logs/incident_summaries.ndjson', 'a') as f:
            f.write(json.dumps(summary) + '\n')
        
        # Also save latest summary
        with open('logs/incident_summaries.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        return {"ok": True, "summary": summary}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = analyze_incidents()
    print(json.dumps(result, indent=2))
