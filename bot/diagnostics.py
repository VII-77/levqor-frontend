import os
import json
import time
import requests
from datetime import datetime
from typing import Dict, Any

# Environment variables
NOTION_STATUS_DB_ID = os.getenv("NOTION_STATUS_DB_ID", "")
AUTOMATION_QUEUE_DB_ID = os.getenv("AUTOMATION_QUEUE_DB_ID", "")
AUTOMATION_LOG_DB_ID = os.getenv("AUTOMATION_LOG_DB_ID", "")
JOB_LOG_DB_ID = os.getenv("JOB_LOG_DB_ID", "")


def check_openai_ping() -> Dict[str, Any]:
    """Quick ping to OpenAI API to verify connectivity."""
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=os.getenv("AI_INTEGRATIONS_OPENAI_API_KEY"),
            base_url=os.getenv("AI_INTEGRATIONS_OPENAI_BASE_URL")
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Reply exactly: ping-ok"},
                {"role": "user", "content": "ping"}
            ],
            timeout=20
        )
        content = response.choices[0].message.content or ""
        ok = "ping-ok" in content.lower()
        return {"ok": ok, "status": "success"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def check_notion_read(db_id: str, name: str) -> Dict[str, Any]:
    """Check if we can read from a Notion database."""
    if not db_id:
        return {"ok": False, "reason": f"{name} not configured"}
    try:
        from bot.notion_api import NotionClientWrapper
        wrapper = NotionClientWrapper()
        client = wrapper.get_client()
        db = client.databases.retrieve(database_id=db_id)
        return {"ok": True, "db_title": db.get("title", [{}])[0].get("plain_text", "Unknown")}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_recent_job_metrics() -> Dict[str, Any]:
    """Get metrics from recent jobs in Job Log database."""
    total = done = low = 0
    qa_sum = 0.0
    
    try:
        from bot.notion_api import NotionClientWrapper
        from datetime import timedelta
        from bot.constants import QC_PASS_THRESHOLD
        wrapper = NotionClientWrapper()
        client = wrapper.get_client()
        
        # Get last 24 hours of jobs
        yesterday = (datetime.utcnow() - timedelta(hours=24)).isoformat()
        
        results = client.databases.query(
            database_id=JOB_LOG_DB_ID,
            filter={
                "timestamp": "created_time",
                "created_time": {"on_or_after": yesterday}
            },
            page_size=100
        )
        
        for page in results.get("results", []):
            props = page.get("properties", {})
            
            # Get QA Score
            qa_prop = props.get("QA Score", {})
            if qa_prop.get("type") == "number" and qa_prop.get("number") is not None:
                qa = qa_prop["number"]
                qa_sum += qa
                if qa < QC_PASS_THRESHOLD:
                    low += 1
            
            # Get Status
            status_prop = props.get("Status", {})
            if status_prop.get("type") == "select":
                status = status_prop.get("select", {}).get("name", "")
                if status == "Done":
                    done += 1
            
            total += 1
        
        avg = (qa_sum / total) if total > 0 else 0.0
        return {
            "ok": True,
            "total_24h": total,
            "done_24h": done,
            "low_qa_count": low,
            "avg_qa_24h": round(avg, 1)
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "total_24h": 0, "done_24h": 0, "low_qa_count": 0, "avg_qa_24h": 0.0}


def snapshot() -> Dict[str, Any]:
    """Generate complete system health snapshot."""
    snap = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "openai_ping": check_openai_ping(),
        "notion_queue": check_notion_read(AUTOMATION_QUEUE_DB_ID, "Queue DB"),
        "notion_log": check_notion_read(AUTOMATION_LOG_DB_ID, "Log DB"),
        "notion_joblog": check_notion_read(JOB_LOG_DB_ID, "Job Log DB"),
        "metrics": get_recent_job_metrics()
    }
    return snap


def post_status_to_notion(ok: bool, notes: str) -> Dict[str, Any]:
    """Post heartbeat status to Notion Status Board."""
    if not NOTION_STATUS_DB_ID:
        return {"ok": False, "reason": "NOTION_STATUS_DB_ID not configured"}
    
    try:
        from bot.notion_api import NotionClientWrapper
        from bot.git_utils import get_git_info
        
        wrapper = NotionClientWrapper()
        client = wrapper.get_client()
        metrics = get_recent_job_metrics()
        commit, branch, _ = get_git_info()
        
        payload = {
            "parent": {"database_id": NOTION_STATUS_DB_ID},
            "properties": {
                "Name": {"title": [{"text": {"content": "Heartbeat"}}]},
                "When": {"date": {"start": datetime.utcnow().isoformat() + "Z"}},
                "OK": {"checkbox": ok},
                "Jobs (24h)": {"number": metrics.get("total_24h", 0)},
                "Avg QA (24h)": {"number": metrics.get("avg_qa_24h", 0.0)},
                "Low-QA Count": {"number": metrics.get("low_qa_count", 0)},
                "Commit": {"rich_text": [{"text": {"content": commit[:40]}}]},
                "Branch": {"rich_text": [{"text": {"content": branch[:100]}}]},
                "Notes": {"rich_text": [{"text": {"content": notes[:1900]}}]}
            }
        }
        
        response = client.pages.create(**payload)
        return {"ok": True, "page_id": response["id"]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def synthetic_bot_job() -> Dict[str, Any]:
    """Create a synthetic test job in the queue to verify end-to-end processing."""
    if not AUTOMATION_QUEUE_DB_ID:
        return {"ok": False, "reason": "AUTOMATION_QUEUE_DB_ID not configured"}
    
    try:
        from bot.notion_api import NotionClientWrapper
        wrapper = NotionClientWrapper()
        client = wrapper.get_client()
        
        title = f"[SYNTHETIC TEST] {datetime.utcnow():%Y-%m-%d %H:%M:%SZ}"
        description = "Automated diagnostic test job - please process and verify system health"
        
        payload = {
            "parent": {"database_id": AUTOMATION_QUEUE_DB_ID},
            "properties": {
                "Task Name": {"title": [{"text": {"content": title}}]},
                "Description": {"rich_text": [{"text": {"content": description}}]},
                "Trigger": {"checkbox": True},
                "Status": {"select": {"name": "New"}},
                "Task Type": {"select": {"name": "Research"}}
            }
        }
        
        response = client.pages.create(**payload)
        return {"ok": True, "page_id": response["id"], "mode": "bot"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def run_autocheck() -> Dict[str, Any]:
    """Run synthetic end-to-end test."""
    return synthetic_bot_job()
