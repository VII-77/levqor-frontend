#!/usr/bin/env python3
"""
Phase 47: Autonomous Finance Reconciler
Matches Stripe payments with Notion job entries
"""
import os
import sys
import json
from datetime import datetime, timedelta

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def reconcile_payments():
    """Match Stripe payments with Notion jobs"""
    try:
        from bot.notion_api import NotionClientWrapper
        from bot import config
        import stripe
        
        # Get Stripe key
        mode = os.getenv('STRIPE_MODE', 'test')
        if mode == 'live':
            stripe.api_key = os.getenv('STRIPE_SECRET_LIVE', '')
        else:
            stripe.api_key = os.getenv('STRIPE_SECRET_KEY', '')
        
        # Get payments from last 24 hours
        yesterday = int((datetime.utcnow() - timedelta(days=1)).timestamp())
        payments = stripe.PaymentIntent.list(
            created={"gte": yesterday},
            limit=100
        )
        
        succeeded = [p for p in payments.data if p.status == 'succeeded']
        
        # Get Notion jobs
        notion = NotionClientWrapper()
        
        if not config.JOB_LOG_DB_ID:
            return {"ok": False, "error": "JOB_LOG_DB_ID not configured"}
        
        # Query jobs with payment status
        results = notion.notion.databases.query(
            database_id=config.JOB_LOG_DB_ID,
            filter={
                "property": "Payment Status",
                "select": {"is_not_empty": True}
            }
        )
        
        notion_jobs = results.get('results', [])
        
        # Simple matching by count
        matched = min(len(succeeded), len(notion_jobs))
        unmatched_stripe = len(succeeded) - matched
        unmatched_notion = len(notion_jobs) - matched
        
        report = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "event": "finance_reconciliation",
            "stripe_payments": len(succeeded),
            "notion_jobs": len(notion_jobs),
            "matched": matched,
            "unmatched_stripe": unmatched_stripe,
            "unmatched_notion": unmatched_notion,
            "mode": mode
        }
        
        # Save report
        os.makedirs('logs', exist_ok=True)
        with open('logs/finance_reconcile.ndjson', 'a') as f:
            f.write(json.dumps(report) + '\n')
        
        return {
            "ok": True,
            "matched": matched,
            "unmatched": unmatched_stripe + unmatched_notion,
            "total_stripe": len(succeeded),
            "total_notion": len(notion_jobs)
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = reconcile_payments()
    print(json.dumps(result, indent=2))
