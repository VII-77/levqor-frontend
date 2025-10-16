import json
import os
from datetime import datetime, timezone
from bot.gmail_client import GmailClientWrapper
from bot.notion_api import NotionClientWrapper
from bot.google_drive_client import GoogleDriveClientWrapper
from bot import config

def check_notion_health() -> bool:
    """Test if Notion API is working"""
    try:
        wrapper = NotionClientWrapper()
        client = wrapper.get_client()
        # Try to retrieve the queue database
        db = client.databases.retrieve(database_id=config.AUTOMATION_QUEUE_DB_ID)
        return bool(db)
    except Exception as e:
        print(f"❌ Notion health check failed: {e}")
        return False

def check_drive_health() -> bool:
    """Test if Google Drive API is working"""
    try:
        wrapper = GoogleDriveClientWrapper()
        # Try to list files (just 1)
        files = wrapper.list_files(page_size=1)
        return True
    except Exception as e:
        print(f"❌ Drive health check failed: {e}")
        return False

def check_openai_health() -> bool:
    """Test if OpenAI API is configured"""
    try:
        api_key = os.getenv('AI_INTEGRATIONS_OPENAI_API_KEY')
        base_url = os.getenv('AI_INTEGRATIONS_OPENAI_BASE_URL')
        return bool(api_key and base_url)
    except Exception as e:
        print(f"❌ OpenAI health check failed: {e}")
        return False

def get_recent_qa_average() -> float:
    """Get average QA score from recent jobs"""
    try:
        wrapper = NotionClientWrapper()
        client = wrapper.get_client()
        
        # Get recent jobs with QA scores
        results = client.databases.query(
            database_id=config.JOB_LOG_DB_ID,
            filter={
                "and": [
                    {"property": "QA Score", "number": {"is_not_empty": True}},
                    {"property": "Status", "select": {"equals": "Done"}}
                ]
            },
            sorts=[{"timestamp": "created_time", "direction": "descending"}],
            page_size=10
        )
        
        scores = []
        for job in results.get('results', []):
            score = job.get('properties', {}).get('QA Score', {}).get('number')
            if score is not None:
                scores.append(score)
        
        if scores:
            return round(sum(scores) / len(scores), 1)
        else:
            return 0.0
            
    except Exception as e:
        print(f"❌ QA average calculation failed: {e}")
        return 0.0

def generate_supervisor_report() -> dict:
    """Generate comprehensive system health report"""
    
    timestamp = datetime.now(timezone.utc).isoformat()
    
    # Run health checks
    notion_ok = check_notion_health()
    drive_ok = check_drive_health()
    openai_ok = check_openai_health()
    qa_avg = get_recent_qa_average()
    
    # Overall health status
    all_healthy = notion_ok and drive_ok and openai_ok
    status = "Healthy" if all_healthy else "Degraded"
    
    report = {
        "timestamp": timestamp,
        "status": status,
        "services": {
            "notion": "OK" if notion_ok else "FAIL",
            "google_drive": "OK" if drive_ok else "FAIL",
            "openai": "OK" if openai_ok else "FAIL"
        },
        "metrics": {
            "qa_average_recent_10": qa_avg
        },
        "git_commit": os.getenv('CURRENT_COMMIT', 'unknown')
    }
    
    return report

def send_supervisor_email(to_email: str | None = None) -> dict:
    """
    Generate and send supervisor report email
    
    Args:
        to_email: Override recipient (defaults to ALERT_TO env var or authenticated user email)
    
    Returns:
        dict with send status
    """
    try:
        # Generate report
        report = generate_supervisor_report()
        
        # Format email
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        subject = f"[EchoPilot] Supervisor Report — {timestamp}"
        
        # Create readable body
        body = f"""EchoPilot Automation System - Daily Supervisor Report
{'-' * 60}

Timestamp: {report['timestamp']}
Overall Status: {report['status']}
Git Commit: {report['git_commit']}

SERVICE HEALTH:
  • Notion API: {report['services']['notion']}
  • Google Drive: {report['services']['google_drive']}
  • OpenAI API: {report['services']['openai']}

METRICS:
  • Average QA Score (recent 10 jobs): {report['metrics']['qa_average_recent_10']}

{'-' * 60}
Raw JSON Report:

{json.dumps(report, indent=2)}
"""
        
        # Send email via Gmail API
        gmail = GmailClientWrapper()
        
        # Determine recipient
        recipient = to_email or os.getenv('ALERT_TO') or gmail.get_user_email()
        
        result = gmail.send_email(
            to=recipient,
            subject=subject,
            body=body
        )
        
        # Mirror to Telegram (lightweight, non-blocking)
        if result.get('ok'):
            try:
                from bot.telegram_bot import send_telegram
                
                # Create concise Telegram version (truncate if needed)
                telegram_body = f"""📧 <b>Supervisor Report — {timestamp}</b>

<b>Status:</b> {report['status']}
<b>Commit:</b> {report['git_commit'][:8]}

<b>Services:</b>
• Notion: {report['services']['notion']}
• Drive: {report['services']['google_drive']}
• OpenAI: {report['services']['openai']}

<b>QA Average (last 10):</b> {report['metrics']['qa_average_recent_10']}

✅ Full report sent to {recipient}"""
                
                send_telegram(telegram_body)
                print(f"📱 Supervisor report mirrored to Telegram")
            except Exception as tg_error:
                print(f"⚠️ Telegram mirror failed (non-critical): {tg_error}")
        
        return result
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Supervisor email failed: {error_msg}")
        return {
            'ok': False,
            'error': error_msg
        }

def run_supervisor():
    """Main entry point for supervisor report"""
    result = send_supervisor_email()
    
    if result.get('ok'):
        print(f"✅ Supervisor report sent successfully to {result.get('to')}")
    else:
        print(f"❌ Supervisor report failed: {result.get('error')}")
    
    return result

if __name__ == "__main__":
    run_supervisor()
