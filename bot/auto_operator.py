"""
Auto-Operator: Self-healing monitoring and escalation system
Monitors EchoPilot health, metrics, and stuck jobs every 5 minutes
"""
import os
import time
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, List
from bot.diagnostics import snapshot, check_openai_ping, get_recent_job_metrics, post_status_to_notion
from bot.notion_api import NotionClientWrapper
from bot.config import JOB_LOG_DB_ID
from bot.alerting import AlertManager
from bot.constants import QC_PASS_THRESHOLD


def check_stuck_jobs(minutes: int = 30) -> List[Dict]:
    """
    Find jobs that are not 'Done' and haven't been edited in N minutes
    These might be stuck in Processing or other non-terminal states
    """
    if not JOB_LOG_DB_ID:
        return []
    
    try:
        wrapper = NotionClientWrapper()
        client = wrapper.get_client()
        
        cutoff = (datetime.utcnow() - timedelta(minutes=minutes)).isoformat() + "Z"
        
        # Query for jobs not Done and last edited before cutoff
        results = client.databases.query(
            database_id=JOB_LOG_DB_ID,
            filter={
                "and": [
                    {
                        "property": "Status",
                        "select": {
                            "does_not_equal": "Done"
                        }
                    },
                    {
                        "timestamp": "last_edited_time",
                        "last_edited_time": {
                            "before": cutoff
                        }
                    }
                ]
            },
            page_size=50
        )
        
        return results.get("results", [])
    except Exception as e:
        print(f"[AutoOperator] Error checking stuck jobs: {e}")
        return []


def check_health_integrations() -> Dict[str, Any]:
    """
    Check health of all critical integrations
    Returns dict with ok/error status for each
    """
    health = {
        "openai": None,
        "notion": None,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    # OpenAI check
    openai_result = check_openai_ping()
    health["openai"] = openai_result.get("ok", False)
    
    # Notion check - if we can query, it's working
    try:
        from bot.notion_api import NotionClientWrapper
        wrapper = NotionClientWrapper()
        client = wrapper.get_client()
        if JOB_LOG_DB_ID:
            client.databases.retrieve(database_id=JOB_LOG_DB_ID)
            health["notion"] = True
        else:
            health["notion"] = None  # Not configured
    except Exception as e:
        print(f"[AutoOperator] Notion check failed: {e}")
        health["notion"] = False
    
    return health


def analyze_metrics() -> Dict[str, Any]:
    """
    Analyze recent job metrics for quality and completion issues
    """
    metrics = get_recent_job_metrics()
    
    analysis = {
        "total_24h": metrics.get("total_24h", 0),
        "done_24h": metrics.get("done_24h", 0),
        "low_qa_count": metrics.get("low_qa_count", 0),
        "avg_qa_24h": metrics.get("avg_qa_24h", 0.0),
        "ok": metrics.get("ok", False)
    }
    
    # Add warnings
    warnings = []
    
    if analysis["total_24h"] >= 10 and analysis["done_24h"] == 0:
        warnings.append("No completed jobs in last 24h despite activity")
    
    if analysis["avg_qa_24h"] > 0 and analysis["avg_qa_24h"] < 75:
        warnings.append(f"Quality dropping: avg {analysis['avg_qa_24h']}% (threshold {QC_PASS_THRESHOLD}%)")
    
    if analysis["total_24h"] > 0:
        done_rate = (analysis["done_24h"] / analysis["total_24h"]) * 100
        if done_rate < 50:
            warnings.append(f"Low completion rate: {done_rate:.1f}%")
    
    analysis["warnings"] = warnings
    
    return analysis


def run_auto_operator_once() -> Tuple[bool, Dict[str, Any]]:
    """
    Run one cycle of auto-operator checks
    Returns (ok: bool, report: dict)
    """
    print(f"[AutoOperator] Running health check at {datetime.utcnow().isoformat()}Z")
    
    # Gather all monitoring data
    health = check_health_integrations()
    metrics_analysis = analyze_metrics()
    stuck_jobs = check_stuck_jobs(minutes=30)
    
    # Build report
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "health": health,
        "metrics": metrics_analysis,
        "stuck_jobs_count": len(stuck_jobs),
        "overall_ok": True,
        "issues": []
    }
    
    # Check for critical issues
    if health.get("openai") is False:
        report["issues"].append("❌ OpenAI integration offline")
        report["overall_ok"] = False
    
    if health.get("notion") is False:
        report["issues"].append("❌ Notion integration offline")
        report["overall_ok"] = False
    
    if len(stuck_jobs) > 0:
        report["issues"].append(f"⚠️ {len(stuck_jobs)} job(s) stuck >30 minutes")
        report["overall_ok"] = False
    
    # Add metric warnings as issues
    for warning in metrics_analysis.get("warnings", []):
        report["issues"].append(f"⚠️ {warning}")
        if "No completed jobs" in warning or "Quality dropping" in warning:
            report["overall_ok"] = False
    
    # Post status to Notion Status Board
    try:
        summary = f"Health: OpenAI={'✅' if health['openai'] else '❌'} Notion={'✅' if health['notion'] else '❌'}\n"
        summary += f"Jobs 24h: {metrics_analysis['total_24h']} total, {metrics_analysis['done_24h']} done\n"
        summary += f"QA avg: {metrics_analysis['avg_qa_24h']}%, Low QA: {metrics_analysis['low_qa_count']}\n"
        summary += f"Stuck jobs: {len(stuck_jobs)}\n"
        
        if report["issues"]:
            summary += "\nIssues:\n" + "\n".join(report["issues"])
        else:
            summary += "\n✅ All systems operational"
        
        post_status_to_notion(report["overall_ok"], summary)
    except Exception as e:
        print(f"[AutoOperator] Failed to post status: {e}")
    
    # Escalate critical issues
    if not report["overall_ok"]:
        try:
            escalate_issues(report)
        except Exception as e:
            print(f"[AutoOperator] Failed to escalate: {e}")
    
    return report["overall_ok"], report


def escalate_issues(report: Dict[str, Any]) -> None:
    """
    Escalate critical issues via email and Telegram
    """
    if not report.get("issues"):
        return
    
    title = f"EchoPilot Auto-Operator Alert"
    details = f"Timestamp: {report['timestamp']}\n\n"
    details += "ISSUES DETECTED:\n"
    details += "\n".join(f"  • {issue}" for issue in report["issues"])
    details += f"\n\nMetrics:\n"
    details += f"  • Total jobs (24h): {report['metrics']['total_24h']}\n"
    details += f"  • Done jobs: {report['metrics']['done_24h']}\n"
    details += f"  • Avg QA: {report['metrics']['avg_qa_24h']}%\n"
    details += f"  • Stuck jobs: {report['stuck_jobs_count']}\n"
    
    # Try to send email alert
    try:
        from bot.gmail_client import GmailClientWrapper
        alert_to = os.getenv("ALERT_TO", "")
        if alert_to:
            gmail = GmailClientWrapper()
            gmail.send_email(
                to=alert_to,
                subject=f"🚨 {title}",
                body=details
            )
            print(f"[AutoOperator] Alert email sent to {alert_to}")
    except Exception as e:
        print(f"[AutoOperator] Failed to send email alert: {e}")
    
    # Try Telegram alert
    try:
        from bot.telegram_bot import send_telegram
        send_telegram(f"🚨 {title}\n\n{details}")
        print(f"[AutoOperator] Alert sent via Telegram")
    except Exception as e:
        print(f"[AutoOperator] Failed to send Telegram alert: {e}")


def get_operator_report() -> Dict[str, Any]:
    """
    Get a quick operator report (for web endpoint)
    """
    ok, report = run_auto_operator_once()
    return report
