import os
import json
import datetime
import pathlib
import statistics
import requests
from bot.alert_mailer import send_alert

NOTION_KEY = os.getenv("NOTION_API_KEY", "")
JOB_DB = os.getenv("JOB_LOG_DB_ID", "")
STATUS_DB = os.getenv("NOTION_STATUS_DB_ID", "")
DSR_DB = os.getenv("NOTION_DSR_DB_ID", "")

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}


def compute_p95_latency():
    """
    Compute p95 latency from recent job metrics
    Reads from metrics.csv or Job Log database
    Returns p95 latency in seconds
    """
    try:
        metrics_file = pathlib.Path("metrics.csv")
        
        if metrics_file.exists():
            lines = metrics_file.read_text(encoding="utf-8").splitlines()[-200:]
            durations = []
            for line in lines:
                if line.count(",") >= 2:
                    try:
                        duration = float(line.split(",", 2)[1])
                        durations.append(duration)
                    except (ValueError, IndexError):
                        continue
            
            if not durations:
                print("[p95] No valid duration data found in metrics.csv")
                return None
            
            durations.sort()
            idx = max(0, int(len(durations) * 0.95) - 1)
            p95 = round(durations[idx], 2)
            
            send_alert(
                "[EchoPilot] Weekly Latency Metric",
                f"p95 Latency: {p95}s from {len(durations)} jobs\nTimestamp: {datetime.datetime.utcnow().isoformat()}Z"
            )
            
            print(f"[p95] Computed: {p95}s from {len(durations)} jobs")
            return p95
        
        else:
            print("[p95] metrics.csv not found, using Notion Job Log")
            
            response = requests.post(
                f"https://api.notion.com/v1/databases/{JOB_DB}/query",
                headers=HEADERS,
                json={"page_size": 100, "sorts": [{"timestamp": "created_time", "direction": "descending"}]},
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json().get("results", [])
            durations = []
            
            for page in results:
                props = page.get("properties", {})
                duration_prop = props.get("Duration (sec)", {}) or props.get("Run Time (sec)", {})
                
                if duration_prop.get("type") == "number":
                    duration = duration_prop.get("number")
                    if duration is not None:
                        durations.append(duration)
            
            if not durations:
                print("[p95] No duration data found in Notion")
                return None
            
            durations.sort()
            idx = max(0, int(len(durations) * 0.95) - 1)
            p95 = round(durations[idx], 2)
            
            send_alert(
                "[EchoPilot] Weekly Latency Metric",
                f"p95 Latency: {p95}s from {len(durations)} jobs (from Notion)\nTimestamp: {datetime.datetime.utcnow().isoformat()}Z"
            )
            
            print(f"[p95] Computed: {p95}s from {len(durations)} jobs")
            return p95
            
    except Exception as e:
        error_msg = f"Error computing p95 latency: {e}"
        print(f"[p95] {error_msg}")
        send_alert("[EchoPilot] p95 Metric Error", error_msg)
        return None


def mark_refund(job_id: str, reason: str = "Client refund"):
    """
    Mark a job as refunded in Notion
    
    Args:
        job_id: Notion page ID of the job
        reason: Reason for refund
    
    Returns:
        bool: True if successful
    """
    try:
        update_data = {
            "properties": {}
        }
        
        if "Payment Status" in []:
            update_data["properties"]["Payment Status"] = {"select": {"name": "Cancelled"}}
        
        update_data["properties"]["Notes"] = {"rich_text": [{"text": {"content": reason}}]}
        
        response = requests.patch(
            f"https://api.notion.com/v1/pages/{job_id}",
            headers=HEADERS,
            json=update_data,
            timeout=20
        )
        
        success = response.status_code == 200
        
        if success:
            send_alert(
                "[EchoPilot] Refund Processed",
                f"Job ID: {job_id}\nReason: {reason}\nStatus: Cancelled\nTimestamp: {datetime.datetime.utcnow().isoformat()}Z"
            )
            print(f"[Refund] Marked {job_id} as refunded: {reason}")
        else:
            print(f"[Refund] Failed to update {job_id}: {response.text}")
        
        return success
        
    except Exception as e:
        error_msg = f"Error marking refund for {job_id}: {e}"
        print(f"[Refund] {error_msg}")
        send_alert("[EchoPilot] Refund Error", error_msg)
        return False


def create_dsr_ticket(correlation_id: str, email: str, action: str = "Erase", notes: str = ""):
    """
    Create a Data Subject Request (DSR) ticket in Notion
    
    Args:
        correlation_id: Unique identifier for the request
        email: Email address of the data subject
        action: Action type (Access, Erase, Restrict)
        notes: Additional notes
    
    Returns:
        bool: True if successful
    """
    if not DSR_DB:
        print("[DSR] NOTION_DSR_DB_ID not configured")
        return False
    
    try:
        body = {
            "parent": {"database_id": DSR_DB},
            "properties": {
                "Correlation ID": {"title": [{"text": {"content": correlation_id}}]},
                "Email": {"email": email},
                "Action": {"select": {"name": action}},
                "Status": {"select": {"name": "New"}},
                "Notes": {"rich_text": [{"text": {"content": notes}}]}
            }
        }
        
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=HEADERS,
            json=body,
            timeout=20
        )
        
        success = response.status_code == 200
        
        if success:
            send_alert(
                "[EchoPilot] DSR Ticket Created",
                f"Correlation ID: {correlation_id}\nEmail: {email}\nAction: {action}\nNotes: {notes}\nTimestamp: {datetime.datetime.utcnow().isoformat()}Z"
            )
            print(f"[DSR] Created ticket: {correlation_id} - {action}")
        else:
            print(f"[DSR] Failed to create ticket: {response.text}")
        
        return success
        
    except Exception as e:
        error_msg = f"Error creating DSR ticket: {e}"
        print(f"[DSR] {error_msg}")
        send_alert("[EchoPilot] DSR Error", error_msg)
        return False


def backup_config():
    """
    Create a backup snapshot of critical environment configuration
    
    Returns:
        str: Path to backup file
    """
    try:
        dest = pathlib.Path("backups/config")
        dest.mkdir(parents=True, exist_ok=True)
        
        backup_file = dest / f"env_backup_{datetime.date.today()}.json"
        
        keep_keys = [
            "AI_INTEGRATIONS_OPENAI_API_KEY",
            "STRIPE_SECRET_KEY",
            "TELEGRAM_BOT_TOKEN",
            "PAYMENT_CURRENCY",
            "DEFAULT_RATE_USD_PER_MIN",
            "COST_GPT_IN_PER_1K_USD",
            "COST_GPT_OUT_PER_1K_USD",
            "AUTOMATION_QUEUE_DB_ID",
            "JOB_LOG_DB_ID",
            "AUTOMATION_LOG_DB_ID"
        ]
        
        snapshot = {k: ("SET" if os.getenv(k) else None) for k in keep_keys}
        snapshot["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
        snapshot["backup_date"] = str(datetime.date.today())
        
        backup_file.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
        
        send_alert(
            "[EchoPilot] Config Backup Created",
            f"Backup file: {backup_file.name}\nTimestamp: {snapshot['timestamp']}\nKeys tracked: {len(keep_keys)}"
        )
        
        print(f"[Backup] Config snapshot created: {backup_file}")
        return str(backup_file)
        
    except Exception as e:
        error_msg = f"Error creating config backup: {e}"
        print(f"[Backup] {error_msg}")
        send_alert("[EchoPilot] Backup Error", error_msg)
        return ""
