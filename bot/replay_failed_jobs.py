import os
import datetime
import requests

NOTION_KEY = os.getenv("NOTION_API_KEY", "")
JOB_DB = os.getenv("AUTOMATION_QUEUE_DB_ID", "")
LOOKBACK_DAYS = int(os.getenv("REPLAY_LOOKBACK_DAYS", "14"))
BATCH_SIZE = int(os.getenv("REPLAY_MAX_PER_RUN", "10"))

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}


def find_failed():
    """
    Find jobs with Status = Failed-Final from the past month
    
    Returns:
        list: Failed job pages
    """
    if not NOTION_KEY or not JOB_DB:
        print("[Replay] Missing Notion configuration")
        return []
    
    try:
        query = {
            "filter": {
                "and": [
                    {"property": "Status", "select": {"equals": "Failed-Final"}},
                    {"timestamp": "last_edited_time", "last_edited_time": {"past_month": {}}}
                ]
            },
            "sorts": [{"timestamp": "last_edited_time", "direction": "descending"}],
            "page_size": BATCH_SIZE
        }
        
        response = requests.post(
            f"https://api.notion.com/v1/databases/{JOB_DB}/query",
            headers=HEADERS,
            json=query,
            timeout=20
        )
        response.raise_for_status()
        
        results = response.json().get("results", [])
        print(f"[Replay] Found {len(results)} Failed-Final jobs")
        return results
        
    except Exception as e:
        print(f"[Replay] Error finding failed jobs: {e}")
        return []


def reset_to_retry(page_id):
    """
    Reset a failed job back to Running status with Trigger enabled
    
    Args:
        page_id: Notion page ID
    """
    try:
        patch = {
            "properties": {
                "Status": {"select": {"name": "Running"}},
                "Trigger": {"checkbox": True},
                "Notes": {"rich_text": [{"text": {"content": "Auto-replay initiated"}}]}
            }
        }
        
        response = requests.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers=HEADERS,
            json=patch,
            timeout=20
        )
        response.raise_for_status()
        print(f"[Replay] Reset job {page_id} for retry")
        return True
        
    except Exception as e:
        print(f"[Replay] Error resetting job {page_id}: {e}")
        return False


def replay_once():
    """
    Find Failed-Final jobs and reset them for retry
    
    Returns:
        int: Number of jobs replayed
    """
    try:
        items = find_failed()
        
        if not items:
            print("[Replay] No failed jobs to replay")
            return 0
        
        count = 0
        for item in items:
            page_id = item.get("id")
            if page_id and reset_to_retry(page_id):
                count += 1
        
        if count > 0:
            print(f"[Replay] ✅ Replayed {count} failed job(s)")
        
        return count
        
    except Exception as e:
        print(f"[Replay] Error during replay: {e}")
        return 0
