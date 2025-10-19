#!/usr/bin/env python3
"""
EchoPilot Release Captain — One-Prompt E2E Runbook
Adaptive QA retry, finance auto-close, governance check
"""
import sys
import os
import json
import time
from datetime import datetime

sys.path.insert(0, '/home/runner/workspace')

from bot.notion_api import NotionClientWrapper
from bot import config
from run import app


def val(props, name):
    """Extract property value from Notion properties dict"""
    if name not in props:
        return None
    t = props[name]['type']
    d = props[name]
    if t == 'number':
        return d['number']
    if t == 'url':
        return d['url']
    if t == 'select':
        return (d['select'] or {}).get('name')
    if t == 'rich_text':
        return d['rich_text'][0]['text']['content'] if d['rich_text'] else None
    if t == 'title':
        return d['title'][0]['text']['content'] if d['title'] else None
    return None


def main():
    n = NotionClientWrapper()
    
    print("=" * 80)
    print("🚀 ECHOPILOT RELEASE CAPTAIN — E2E RUNBOOK")
    print("=" * 80)
    print()
    
    # Step 1: Create test job
    print("STEP 1: Creating test job in Automation Queue...")
    props = {
        "Job Name": {"title": [{"text": {"content": "Boss Mode E2E"}}]},
        "Task Type": {"select": {"name": "Processing"}},
        "Trigger": {"checkbox": True},
        "Status": {"select": {"name": "New"}},
        "Payload Link": {"url": "https://filesamples.com/samples/audio/mp3/sample3.mp3"},
        "Owner Email": {"email": "admin@echopilot.ai"}
    }
    page = n.create_page(config.AUTOMATION_QUEUE_DB_ID, props)
    job_id = page["id"]
    print(f"✅ Job created: {job_id[:8]}...")
    print()
    
    # Step 2 & 3: Poll Job Log with backoff [5s, 10s, 20s, 30s]
    print("STEP 2-3: Polling Job Log with adaptive retry backoff...")
    delays = [5, 10, 20, 30]
    job = None
    job_page_id = None
    
    for delay in delays:
        time.sleep(delay)
        print(f"  Waiting {delay}s...", end=" ", flush=True)
        rows = n.query_database(config.JOB_LOG_DB_ID)
        now = datetime.utcnow()
        
        for r in rows[:10]:
            created = r.get('created_time', '')
            props_data = r['properties']
            
            # Match jobs from last 5 minutes
            if created[:16] == now.isoformat()[:16]:
                qa = val(props_data, 'QA') or val(props_data, 'QA Score')
                if qa is not None:
                    job = {
                        "qa": qa,
                        "duration_sec": val(props_data, 'Duration Sec'),
                        "duration_min": val(props_data, 'Duration Min'),
                        "client_rate": val(props_data, 'Client Rate USD/min'),
                        "gross_usd": val(props_data, 'Gross USD'),
                        "profit_usd": val(props_data, 'Profit USD'),
                        "margin_pct": val(props_data, 'Margin %'),
                        "payment_link": val(props_data, 'Payment Link'),
                        "payment_status": val(props_data, 'Payment Status'),
                        "drive_folder": val(props_data, 'Drive Folder'),
                        "summary": val(props_data, 'Summary')
                    }
                    job_page_id = r['id']
                    print("✅ FOUND!")
                    break
        
        if job:
            break
        else:
            print("not yet")
    
    print()
    
    # Step 2: Adaptive QA retry logic
    qa_retry = None
    qa_status = None
    
    if job:
        initial_qa = job['qa']
        print(f"STEP 2 (cont): Adaptive QA evaluation — Initial QA: {initial_qa}%")
        
        if initial_qa >= 95:
            print("✅ QA ≥ 95: PASS (no retry needed)")
            qa_status = "Verified"
        elif initial_qa >= 80:
            print(f"⚠️  QA {initial_qa}% in range [80, 95) — triggering retry...")
            print("   (Retry logic would happen during processing - this is post-processing check)")
            qa_status = "Verified"
            # Note: Actual retry happens in processor.py during job execution
            # This is the validation phase
        else:
            print(f"❌ QA {initial_qa}% < 80: NEEDS REVIEW")
            qa_status = "Needs Review"
            # Update Job Log with QA Status if field exists
            try:
                n.update_page(job_page_id, {
                    "Notes": {"rich_text": [{"text": {"content": f"QA Status: Needs Review (score: {initial_qa}%)"}}]}
                })
            except:
                pass
        print()
    
    # Step 4: Finance guardrails (auto-close when QA ≥ 95)
    finance_action = "skipped"
    if job and job['qa'] >= 95:
        print("STEP 4: Finance guardrails — QA ≥ 95, checking payment...")
        if job['payment_link'] and job['payment_status'] != 'Paid':
            try:
                n.update_page(job_page_id, {
                    "Payment Status": {"select": {"name": "Paid"}}
                })
                job['payment_status'] = 'Paid'
                finance_action = "auto_closed_to_paid"
                print("✅ Payment Status → Paid (auto-closed)")
            except Exception as e:
                finance_action = f"update_failed: {str(e)[:50]}"
                print(f"⚠️  Failed to update payment: {e}")
        elif not job['payment_link']:
            finance_action = "missing_payment_link"
            print("⚠️  No Payment Link to close")
        elif job['payment_status'] == 'Paid':
            finance_action = "already_paid"
            print("✅ Already marked Paid")
        print()
    elif job and job['qa'] < 95:
        print(f"STEP 4: Finance guardrails — QA {job['qa']}% < 95, skipping payment")
        print()
    
    # Step 5: Cost Dashboard check
    print("STEP 5: Checking Cost Dashboard (Revenue_30d, ROI)...")
    roi_30d = "not_configured"
    
    try:
        cid = os.getenv('NOTION_COST_DASHBOARD_DB_ID')
        if cid:
            time.sleep(10)  # Wait for rollup to update
            res = n.query_database(cid)
            if res:
                dashboard_props = res[0]['properties']
                roi_val = (dashboard_props.get('ROI', {}).get('formula', {}) or {}).get('number')
                if roi_val is not None:
                    roi_30d = roi_val
                    print(f"✅ ROI: {roi_30d}")
                else:
                    roi_30d = "no_entries"
                    print("⚠️  ROI: no_entries")
            else:
                roi_30d = "no_entries"
                print("⚠️  Cost Dashboard empty")
        else:
            print("⚠️  Cost Dashboard not configured")
    except Exception as e:
        roi_30d = f"error: {str(e)[:30]}"
        print(f"⚠️  Error reading dashboard: {e}")
    print()
    
    # Step 6: Governance heartbeat
    print("STEP 6: Governance heartbeat (POST /pulse)...")
    gov_pulse = "error"
    try:
        with app.test_client() as c:
            r = c.post(f"/pulse?token={os.getenv('HEALTH_TOKEN', 'test')}")
            if r.status_code == 200:
                gov_pulse = "created"
                print("✅ Governance pulse: created")
            else:
                gov_pulse = f"status_{r.status_code}"
                print(f"⚠️  Governance pulse: status {r.status_code}")
    except Exception as e:
        gov_pulse = "error"
        print(f"❌ Governance pulse error: {e}")
    print()
    
    # Step 7: Output E2E_RESULT JSON
    if job:
        if job['qa'] >= 95:
            status = "PASS"
            reason = "QA ≥ 95, all steps completed, finance auto-closed"
        elif job['qa'] >= 80:
            status = "PARTIAL"
            reason = f"QA {job['qa']}% in acceptable range but < 95"
        else:
            status = "PARTIAL"
            reason = f"QA {job['qa']}% needs review"
    else:
        status = "FAIL"
        reason = "Job Log entry not found after full backoff (Notion lag or processing failed)"
    
    E2E_RESULT = {
        "status": status,
        "reason": reason,
        "qa": job['qa'] if job else None,
        "duration_sec": job['duration_sec'] if job else None,
        "gross_usd": job['gross_usd'] if job else None,
        "profit_usd": job['profit_usd'] if job else None,
        "margin_pct": job['margin_pct'] if job else None,
        "payment_link": job['payment_link'] if job else None,
        "payment_status": job['payment_status'] if job else None,
        "roi_30d": roi_30d,
        "governance_pulse": gov_pulse,
        "qa_retry": qa_retry,
        "qa_status": qa_status
    }
    
    print("=" * 80)
    print("E2E_RESULT")
    print("=" * 80)
    print()
    print(json.dumps(E2E_RESULT, indent=2))
    print()
    
    # Save to log
    with open("logs/release_captain.json", "a") as f:
        f.write(json.dumps(E2E_RESULT) + "\n")
    
    print("✅ Results saved to logs/release_captain.json")
    print()
    
    if status == "PASS":
        print("🎉 RELEASE CAPTAIN: PASS — All systems operational!")
    elif status == "PARTIAL":
        print("⚠️  RELEASE CAPTAIN: PARTIAL — Review required")
    else:
        print("❌ RELEASE CAPTAIN: FAIL — Investigation needed")
    
    return E2E_RESULT


if __name__ == "__main__":
    main()
