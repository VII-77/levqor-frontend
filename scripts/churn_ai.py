#!/usr/bin/env python3
"""
Phase 58: Churn AI
Risk scoring for customer retention analysis
"""
import os
import sys
import json
import time
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def calculate_churn_risk(customer):
    """
    Calculate churn risk score for a customer
    
    Factors:
    - Days since last job
    - Number of jobs in last 30 days
    - Payment history (90 days)
    - Success rate
    
    Returns risk score 0.0-1.0 (0=low risk, 1=high risk)
    """
    days_since_last = customer.get('days_since_last_job', 30)
    jobs_30d = customer.get('jobs_30d', 0)
    payments_90d = customer.get('payments_90d', 0)
    success_rate = customer.get('success_rate', 1.0)
    
    # Calculate risk components
    recency_risk = min(1.0, days_since_last / 30.0)  # High risk if >30 days inactive
    usage_risk = max(0.0, 1.0 - (jobs_30d / 10.0))   # High risk if <10 jobs/month
    payment_risk = max(0.0, 1.0 - (payments_90d / 3.0))  # High risk if <3 payments in 90d
    quality_risk = 1.0 - success_rate  # High risk if low success rate
    
    # Weighted average
    risk = (
        0.35 * recency_risk +
        0.25 * usage_risk +
        0.25 * payment_risk +
        0.15 * quality_risk
    )
    
    # Determine tier
    if risk < 0.3:
        tier = "LOW"
    elif risk < 0.6:
        tier = "MEDIUM"
    else:
        tier = "HIGH"
    
    return {
        "id": customer['id'],
        "risk_score": round(risk, 3),
        "tier": tier,
        "factors": {
            "recency": round(recency_risk, 2),
            "usage": round(usage_risk, 2),
            "payment": round(payment_risk, 2),
            "quality": round(quality_risk, 2)
        }
    }

def analyze_churn():
    """Analyze churn risk for all customers"""
    try:
        # In production, fetch from Notion client database
        # For now, use sample data
        customers = [
            {
                "id": "C001",
                "name": "Acme Corp",
                "days_since_last_job": 3,
                "jobs_30d": 15,
                "payments_90d": 3,
                "success_rate": 0.95
            },
            {
                "id": "C002",
                "name": "Beta Inc",
                "days_since_last_job": 45,
                "jobs_30d": 0,
                "payments_90d": 0,
                "success_rate": 0.80
            },
            {
                "id": "C003",
                "name": "Gamma LLC",
                "days_since_last_job": 15,
                "jobs_30d": 5,
                "payments_90d": 2,
                "success_rate": 0.92
            }
        ]
        
        # Calculate risk for each customer
        results = [calculate_churn_risk(c) for c in customers]
        
        # Sort by risk score (highest first)
        results.sort(key=lambda x: x['risk_score'], reverse=True)
        
        # Summary
        summary = {
            "total": len(results),
            "high_risk": sum(1 for r in results if r['tier'] == 'HIGH'),
            "medium_risk": sum(1 for r in results if r['tier'] == 'MEDIUM'),
            "low_risk": sum(1 for r in results if r['tier'] == 'LOW'),
            "avg_risk": round(sum(r['risk_score'] for r in results) / len(results), 3) if results else 0
        }
        
        # Save report
        report = {
            "ts": time.time(),
            "ts_iso": datetime.utcnow().isoformat() + "Z",
            "summary": summary,
            "results": results
        }
        
        os.makedirs('logs', exist_ok=True)
        with open('logs/churn_risk.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Also append to NDJSON
        with open('logs/churn_risk.ndjson', 'a') as f:
            f.write(json.dumps({"ts": report['ts_iso'], "summary": summary}) + '\n')
        
        return {"ok": True, "summary": summary, "count": len(results)}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = analyze_churn()
    print(json.dumps(result, indent=2))
