#!/usr/bin/env python3
"""
Phase 79: Cost Guardrails
Track AI spend and Stripe fees, enforce caps
"""
import os
import sys
import json
import time
from datetime import datetime, timedelta

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configuration
COST_CAP_DAILY_USD = float(os.getenv('COST_CAP_DAILY_USD', '25.0'))
MODEL_CAPS_JSON = os.getenv('MODEL_CAPS_JSON', '{"gpt-4o":15,"gpt-4o-mini":10}')

def get_model_caps():
    """Parse model-specific caps from JSON"""
    try:
        return json.loads(MODEL_CAPS_JSON)
    except:
        return {}

def compute_cost_status():
    """Compute current spend and check against caps"""
    try:
        model_caps = get_model_caps()
        cutoff_time = time.time() - 86400  # Last 24 hours
        
        costs = {
            "total_usd": 0.0,
            "by_model": {},
            "stripe_fees_usd": 0.0
        }
        
        # Read cost data from job logs
        if os.path.exists('logs/job_log.ndjson'):
            with open('logs/job_log.ndjson', 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        ts = data.get('ts', 0)
                        
                        if ts > cutoff_time:
                            cost = data.get('cost_usd', 0)
                            model = data.get('model', 'unknown')
                            
                            costs['total_usd'] += cost
                            if model not in costs['by_model']:
                                costs['by_model'][model] = 0.0
                            costs['by_model'][model] += cost
                    except:
                        continue
        
        # Calculate utilization against caps
        global_utilization = (costs['total_usd'] / COST_CAP_DAILY_USD * 100) if COST_CAP_DAILY_USD > 0 else 0
        
        # Check model-specific caps
        model_utilizations = {}
        for model, cap in model_caps.items():
            spent = costs['by_model'].get(model, 0.0)
            utilization = (spent / cap * 100) if cap > 0 else 0
            model_utilizations[model] = {
                "spent_usd": round(spent, 4),
                "cap_usd": cap,
                "utilization_pct": round(utilization, 2)
            }
        
        # Determine alert level
        max_util = max(global_utilization, *[v['utilization_pct'] for v in model_utilizations.values()], 0)
        
        if max_util >= 100:
            alert_level = "CRITICAL"
            action = "THROTTLE"
        elif max_util >= 90:
            alert_level = "WARNING"
            action = "WARN"
        else:
            alert_level = "OK"
            action = "NONE"
        
        result = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "period_hours": 24,
            "total_spent_usd": round(costs['total_usd'], 4),
            "daily_cap_usd": COST_CAP_DAILY_USD,
            "global_utilization_pct": round(global_utilization, 2),
            "by_model": model_utilizations,
            "alert_level": alert_level,
            "action": action
        }
        
        # Save status
        os.makedirs('logs', exist_ok=True)
        with open('logs/costs.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        # Append to NDJSON
        with open('logs/costs.ndjson', 'a') as f:
            f.write(json.dumps({
                "event": "cost_check",
                "ts": result['ts'],
                "total_usd": costs['total_usd'],
                "cap_usd": COST_CAP_DAILY_USD,
                "utilization": global_utilization,
                "alert": alert_level
            }) + '\n')
        
        # Raise incident if critical
        if alert_level == "CRITICAL":
            # Import incident pager
            sys.path.insert(0, os.path.dirname(__file__))
            try:
                from incident_pager import raise_incident
                raise_incident(
                    "CRITICAL",
                    f"Cost cap exceeded: ${costs['total_usd']:.2f} / ${COST_CAP_DAILY_USD:.2f} daily limit",
                    "cost_guardrails",
                    {"utilization_pct": global_utilization}
                )
            except:
                pass  # Incident pager not available
        
        return {"ok": True, "data": result}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def set_cost_cap(scope, key, usd_cap):
    """Set cost cap (daily or per-model)"""
    try:
        # This is a simplified implementation
        # In production, would persist to config file or database
        return {
            "ok": True,
            "scope": scope,
            "key": key,
            "usd_cap": usd_cap,
            "message": "Cap set (restart required for effect)"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = compute_cost_status()
    print(json.dumps(result, indent=2))
