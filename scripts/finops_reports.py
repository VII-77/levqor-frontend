#!/usr/bin/env python3
"""Phase 85: FinOps Reports - Financial Operations Reporting"""
import os, sys, json
from datetime import datetime, timedelta

FINOPS_ALERT_USD = float(os.getenv('FINOPS_ALERT_USD', '50'))

def generate_finops_report():
    """Generate comprehensive FinOps report"""
    try:
        # Aggregate costs from various sources
        total_ai_spend = 0.0
        total_infrastructure = 0.02  # Base Replit cost
        
        # Read cost data
        if os.path.exists('logs/costs.json'):
            with open('logs/costs.json', 'r') as f:
                costs = json.load(f)
                total_ai_spend = costs.get('data', {}).get('total_spent_usd', 0.0)
        
        total_spend = total_ai_spend + total_infrastructure
        utilization = (total_spend / FINOPS_ALERT_USD * 100) if FINOPS_ALERT_USD > 0 else 0
        
        result = {
            "ok": True,
            "ts": datetime.utcnow().isoformat() + "Z",
            "period": "monthly",
            "total_spend_usd": round(total_spend, 2),
            "breakdown": {
                "ai_models": round(total_ai_spend, 2),
                "infrastructure": total_infrastructure,
                "storage": 0.0,
                "bandwidth": 0.0
            },
            "budget_cap_usd": FINOPS_ALERT_USD,
            "utilization_pct": round(utilization, 2),
            "forecast_eom_usd": round(total_spend * 1.1, 2),
            "recommendations": [
                "Switch to gpt-4o-mini for simple tasks" if total_ai_spend > 10 else "AI spend under control",
                "Monitor daily spend trends"
            ]
        }
        
        # Save report
        os.makedirs('logs', exist_ok=True)
        with open('logs/finops_report.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        with open('logs/finops_reports.ndjson', 'a') as f:
            f.write(json.dumps(result) + '\n')
        
        return result
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = generate_finops_report()
    print(json.dumps(result, indent=2))
