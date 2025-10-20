"""
Status Summary API for Boss Mode Dashboard
Aggregates: scheduler status, SLO metrics, payments, error budget
"""

import os
import time
from datetime import datetime, timedelta
from pathlib import Path

def get_status_summary():
    """Aggregate system status for dashboard"""
    
    summary = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "overall": "healthy",
        "components": {}
    }
    
    # Scheduler Status
    try:
        from bot.scheduler_status import get_scheduler_info
        scheduler = get_scheduler_info()
        summary["components"]["scheduler"] = {
            "status": "running" if scheduler.get("running") else "stopped",
            "next_jobs": scheduler.get("next_tasks", [])[:5]
        }
    except Exception as e:
        summary["components"]["scheduler"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Stripe Webhooks (last 10)
    try:
        webhook_log = Path("logs/stripe_webhooks.log")
        if webhook_log.exists():
            lines = webhook_log.read_text().strip().split('\n')[-10:]
            summary["components"]["stripe_webhooks"] = {
                "count": len(lines),
                "recent": lines[-3:] if lines else []
            }
        else:
            summary["components"]["stripe_webhooks"] = {
                "count": 0,
                "recent": []
            }
    except:
        summary["components"]["stripe_webhooks"] = {"status": "unknown"}
    
    # SLO Error Budget
    try:
        from bot.slo import calculate_error_budget
        budget = calculate_error_budget()
        summary["components"]["slo"] = {
            "uptime_target": 99.9,
            "current_uptime": budget.get("uptime_pct", 100),
            "error_budget_remaining": budget.get("remaining_pct", 100),
            "status": "ok" if budget.get("remaining_pct", 100) > 20 else "warning"
        }
    except:
        summary["components"]["slo"] = {
            "status": "unknown",
            "uptime_target": 99.9
        }
    
    # Overall status determination
    statuses = [c.get("status", "ok") for c in summary["components"].values()]
    if "error" in statuses:
        summary["overall"] = "degraded"
    elif "warning" in statuses:
        summary["overall"] = "warning"
    else:
        summary["overall"] = "healthy"
    
    return summary
