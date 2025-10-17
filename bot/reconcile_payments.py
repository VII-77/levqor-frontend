import os
import requests
import datetime
import time
import json
from bot.payments import paypal_capture, PAYPAL_ID, PAYPAL_SEC
from bot.notion_api import get_notion_client

HEADERS = {
    "Authorization": f"Bearer {os.getenv('NOTION_TOKEN', '')}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
JOB_LOG_DB_ID = os.getenv("JOB_LOG_DB_ID", "")


def query_unpaid_jobs():
    try:
        client = get_notion_client()
        response = client.databases.query(
            database_id=JOB_LOG_DB_ID,
            filter={
                "property": "Payment Status",
                "select": {"equals": "Unpaid"}
            },
            page_size=100
        )
        return response.get("results", [])
    except Exception as e:
        print(f"[Reconcile] Error querying unpaid jobs: {e}")
        return []


def get_property_value(page, prop_name, prop_type):
    props = page.get("properties", {})
    prop = props.get(prop_name, {})
    if prop_type == "url":
        return prop.get("url")
    elif prop_type == "title":
        title_arr = prop.get("title", [])
        return title_arr[0].get("plain_text", "") if title_arr else None
    return None


def update_payment_status(page_id, status):
    try:
        url = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {
            "properties": {
                "Payment Status": {
                    "select": {"name": status}
                }
            }
        }
        response = requests.patch(url, headers=HEADERS, json=payload, timeout=20)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"[Reconcile] Error updating status for {page_id}: {e}")
        return False


def reconcile_once():
    print(f"[Reconcile] Starting payment reconciliation at {datetime.datetime.utcnow().isoformat()}")
    pages = query_unpaid_jobs()
    changed = 0
    
    for page in pages:
        page_id = page["id"]
        payment_link = get_property_value(page, "Payment Link", "url")
        job_name = get_property_value(page, "Job Name", "title")
        
        if not payment_link:
            continue
        
        if "paypal.com" in payment_link and PAYPAL_ID and PAYPAL_SEC:
            try:
                if "token=" in payment_link:
                    order_id = payment_link.split("token=")[-1].split("&")[0]
                    cap = paypal_capture(order_id)
                    
                    captures = (cap.get("purchase_units", [{}])[0]
                               .get("payments", {})
                               .get("captures", []))
                    
                    if any(v.get("status") == "COMPLETED" for v in captures):
                        if update_payment_status(page_id, "Paid"):
                            print(f"[Reconcile] Marked job '{job_name}' as Paid (PayPal)")
                            changed += 1
                            continue
            except Exception as e:
                print(f"[Reconcile] PayPal capture error for {job_name}: {e}")
    
    if changed:
        try:
            from bot.gmail_client import send_email
            send_email(
                to=os.getenv("ALERT_TO", ""),
                subject="[EchoPilot] Payment Reconciliation Complete",
                body=f"Marked {changed} invoice(s) as Paid via reconciliation at {datetime.datetime.utcnow().isoformat()}"
            )
        except Exception as e:
            print(f"[Reconcile] Alert email error: {e}")
    
    print(f"[Reconcile] Complete. Updated {changed} job(s)")
    return changed
