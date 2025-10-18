import os
import requests
import stripe

STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY", "").strip()
STRIPE_ACCOUNT = os.getenv("STRIPE_ACCOUNT_ID", "")
NOTION_KEY = os.getenv("NOTION_API_KEY", "")
JOB_DB = os.getenv("JOB_LOG_DB_ID", "")

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}


def _notion_query(filter_json):
    """Query Notion database with filter"""
    url = f"https://api.notion.com/v1/databases/{JOB_DB}/query"
    r = requests.post(url, headers=HEADERS, json=filter_json, timeout=30)
    r.raise_for_status()
    return r.json()


def _notion_set_paid(page_id):
    """Mark a job as paid in Notion"""
    try:
        requests.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers=HEADERS,
            json={"properties": {"Payment Status": {"select": {"name": "Paid"}}}},
            timeout=20
        )
        print(f"[StripePoller] Marked {page_id} as Paid")
        return True
    except Exception as e:
        print(f"[StripePoller] Error marking paid: {e}")
        return False


def poll_and_fix(limit_minutes=10080):
    """
    Scan Unpaid jobs with Stripe payment links.
    If Stripe shows completed payment, update to Paid.
    
    Args:
        limit_minutes: How far back to scan (default: 1 week = 10080 min)
    
    Returns:
        int: Number of jobs fixed
    """
    if not STRIPE_KEY:
        print("[StripePoller] No STRIPE_SECRET_KEY configured")
        return 0
    
    if not JOB_DB:
        print("[StripePoller] No JOB_LOG_DB_ID configured")
        return 0
    
    try:
        stripe.api_key = STRIPE_KEY
        
        # Find Unpaid jobs from the last week
        query = {
            "filter": {
                "and": [
                    {"property": "Payment Status", "select": {"equals": "Unpaid"}},
                    {"timestamp": "last_edited_time", "last_edited_time": {"past_week": {}}}
                ]
            },
            "page_size": 50
        }
        
        pages = _notion_query(query).get("results", [])
        
        if not pages:
            print("[StripePoller] No unpaid jobs found")
            return 0
        
        print(f"[StripePoller] Scanning {len(pages)} unpaid jobs...")
        
        # Fetch recent Stripe events
        events = stripe.Event.list(limit=100)
        
        fixed = 0
        for pg in pages:
            page_id = pg["id"]
            props = pg["properties"]
            
            # Get payment link
            link_prop = props.get("Payment Link", {})
            link = link_prop.get("url", "") if link_prop else ""
            
            # Get job name/ID
            title_prop = props.get("Job Name", {}).get("title", [])
            job_name = title_prop[0].get("plain_text", "") if title_prop else ""
            
            if "stripe" not in link.lower():
                continue
            
            # Check if this job was paid according to Stripe events
            for ev in events.auto_paging_iter():
                event_type = ev.get("type", "")
                obj = ev.get("data", {}).get("object", {})
                
                # Get metadata
                metadata = obj.get("metadata", {}) if isinstance(obj, dict) else {}
                job_id = metadata.get("job_id", "")
                
                # Match by job_id in metadata or job name
                if job_id and (job_id in job_name or job_id == page_id):
                    if event_type in ("checkout.session.completed", "payment_intent.succeeded"):
                        _notion_set_paid(page_id)
                        fixed += 1
                        break
        
        if fixed > 0:
            print(f"[StripePoller] ✅ Fixed {fixed} missed payment(s)")
        else:
            print("[StripePoller] No missed payments found")
        
        return fixed
        
    except Exception as e:
        print(f"[StripePoller] Error: {e}")
        return 0
