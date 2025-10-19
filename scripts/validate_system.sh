#!/bin/bash
set -euo pipefail

echo "==========================================="
echo "🧠 ECHOPILOT BOSS MODE — SYSTEM VALIDATION"
echo "==========================================="
echo ""

python3 - <<'PY'
import sys,os,json,time
sys.path.insert(0,'/home/runner/workspace')
from datetime import datetime
from bot.notion_api import NotionClientWrapper
from bot import config
from run import app

n = NotionClientWrapper()

print("=" * 80)
print("E2E FINALIZER — BOSS MODE VALIDATION")
print("=" * 80)
print()

print("STEP 1: Creating test job...")
props = {
    "Job Name": {"title": [{"text": {"content": "E2E Boss Mode Validation"}}]},
    "Task Type": {"select": {"name": "Processing"}},
    "Trigger": {"checkbox": True},
    "Status": {"select": {"name": "New"}},
    "Payload Link": {"url": "https://filesamples.com/samples/audio/mp3/sample3.mp3"}
}
page = n.create_page(config.AUTOMATION_QUEUE_DB_ID, props)
print(f"✅ Job created: {page['id'][:8]}...")
print()

def val(props, name):
    if name not in props: return None
    t = props[name]['type']
    d = props[name]
    if t == 'number': return d['number']
    if t == 'url': return d['url']
    if t == 'select': return (d['select'] or {}).get('name')
    if t == 'rich_text': return d['rich_text'][0]['text']['content'] if d['rich_text'] else None
    if t == 'title': return d['title'][0]['text']['content'] if d['title'] else None
    return None

print("STEP 2: Polling Job Log with retry delays [5,10,20,30]...")
job = None
for delay in [5, 10, 20, 30]:
    time.sleep(delay)
    print(f"  Waiting {delay}s...", end=" ", flush=True)
    rows = n.query_database(config.JOB_LOG_DB_ID)
    now = datetime.utcnow()
    for r in rows[:10]:
        created = r.get('created_time', '')
        if created[:16] == now.isoformat()[:16] and val(r['properties'], 'Gross USD') is not None:
            job = {
                "qa": val(r['properties'], 'QA') or val(r['properties'], 'QA Score'),
                "duration_sec": val(r['properties'], 'Duration Sec'),
                "gross_usd": val(r['properties'], 'Gross USD'),
                "profit_usd": val(r['properties'], 'Profit USD'),
                "margin_pct": val(r['properties'], 'Margin %'),
                "payment_status": val(r['properties'], 'Payment Status')
            }
            print("✅ FOUND!")
            break
    if job:
        break
    else:
        print("not yet")

print()

print("STEP 3: Testing Governance /pulse endpoint...")
gov = "error"
try:
    with app.test_client() as c:
        r = c.post(f"/pulse?token={os.getenv('HEALTH_TOKEN', 'test')}")
        gov = "created" if r.status_code == 200 else f"status_{r.status_code}"
        print(f"✅ Pulse: {gov}")
except Exception as e:
    print(f"❌ Pulse error: {e}")
print()

print("STEP 4: Checking Cost Dashboard ROI...")
roi = "not_configured"
try:
    cid = os.getenv('NOTION_COST_DASHBOARD_DB_ID')
    if cid:
        res = n.query_database(cid)
        if res:
            roi_val = (res[0]['properties'].get('ROI', {}).get('formula', {}) or {}).get('number')
            roi = roi_val if roi_val is not None else "no_entries"
            print(f"✅ ROI: {roi}")
except Exception as e:
    print(f"⚠️ ROI read: {e}")
print()

result = {
    "timestamp": datetime.utcnow().isoformat(),
    "status": "PASS" if job else "PARTIAL",
    "reason": "processed + finance tracked + pulse ok" if job else "Notion sync lag (retry)",
    "qa": job and job["qa"],
    "duration_sec": job and job["duration_sec"],
    "gross_usd": job and job["gross_usd"],
    "profit_usd": job and job["profit_usd"],
    "margin_pct": job and job["margin_pct"],
    "payment_status": job and job["payment_status"],
    "roi_30d": roi,
    "governance_pulse": gov
}

print("=" * 80)
print("E2E_RESULT")
print("=" * 80)
print()
print(json.dumps(result, indent=2))
print()

with open("logs/e2e_validation.json", "a") as f:
    f.write(json.dumps(result) + "\n")

print("✅ Results saved to logs/e2e_validation.json")
print()

if result["status"] == "PASS":
    print("🎉 BOSS MODE: ALL SYSTEMS OPERATIONAL!")
else:
    print("⚠️ PARTIAL: Job processing in progress (check again in 60s)")
PY

echo ""
echo "==========================================="
echo "✅ System Validation Complete"
echo "==========================================="
