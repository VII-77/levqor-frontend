#!/usr/bin/env python3
"""
Cross-database metrics aggregation for EchoPilot.
Provides system-wide health and performance metrics.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Optional
from bot.notion_api import NotionClientWrapper


def get_metrics(notion: NotionClientWrapper) -> Dict:
    """
    Aggregate metrics from multiple Notion databases.
    
    Returns:
        {
            "jobs_7d": int,
            "avg_qa_7d": float,
            "revenue_7d": float,
            "roi_30d": float,
            "uptime_pct": float
        }
    """
    now = datetime.utcnow()
    seven_days_ago = now - timedelta(days=7)
    thirty_days_ago = now - timedelta(days=30)
    
    metrics = {
        "jobs_7d": 0,
        "avg_qa_7d": 0.0,
        "revenue_7d": 0.0,
        "roi_30d": 0.0,
        "uptime_pct": 100.0
    }
    
    try:
        client = notion.get_client()
        
        # Get Job Log metrics (last 7 days)
        job_log_db = os.getenv("JOB_LOG_DB_ID")
        if job_log_db:
            
            # Query jobs from last 7 days
            response = client.databases.query(
                database_id=job_log_db,
                filter={
                    "property": "Timestamp",
                    "date": {
                        "after": seven_days_ago.isoformat()
                    }
                }
            )
            
            jobs = response.get("results", [])
            metrics["jobs_7d"] = len(jobs)
            
            # Calculate average QA score
            qa_scores = []
            for job in jobs:
                props = job.get("properties", {})
                
                # Try both "QA Score" and "QA" property names
                qa_prop = props.get("QA Score") or props.get("QA")
                if qa_prop and qa_prop.get("number") is not None:
                    qa_scores.append(qa_prop["number"])
            
            if qa_scores:
                metrics["avg_qa_7d"] = round(sum(qa_scores) / len(qa_scores), 1)
        
        # Get Finance metrics (last 7 days revenue)
        finance_db = os.getenv("NOTION_FINANCE_DB_ID")
        if finance_db:
            try:
                response = client.databases.query(
                    database_id=finance_db,
                    filter={
                        "and": [
                            {
                                "property": "Date",
                                "date": {
                                    "after": seven_days_ago.isoformat()
                                }
                            },
                            {
                                "property": "Paid",
                                "checkbox": {
                                    "equals": True
                                }
                            }
                        ]
                    }
                )
                
                for entry in response.get("results", []):
                    props = entry.get("properties", {})
                    amount_prop = props.get("Amount")
                    if amount_prop and amount_prop.get("number") is not None:
                        metrics["revenue_7d"] += amount_prop["number"]
                
                metrics["revenue_7d"] = round(metrics["revenue_7d"], 2)
            except Exception as e:
                print(f"[Metrics] Finance DB error: {e}")
        
        # Get Cost Dashboard ROI (last 30 days)
        cost_db = os.getenv("NOTION_COST_DASHBOARD_DB_ID")
        if cost_db:
            try:
                response = client.databases.query(
                    database_id=cost_db,
                    filter={
                        "property": "Date",
                        "date": {
                            "after": thirty_days_ago.isoformat()
                        }
                    }
                )
                
                roi_values = []
                for entry in response.get("results", []):
                    props = entry.get("properties", {})
                    roi_prop = props.get("ROI")
                    if roi_prop and roi_prop.get("number") is not None:
                        roi_values.append(roi_prop["number"])
                
                if roi_values:
                    metrics["roi_30d"] = round(sum(roi_values) / len(roi_values), 1)
            except Exception as e:
                print(f"[Metrics] Cost Dashboard error: {e}")
        
        # Calculate uptime from health logs
        metrics["uptime_pct"] = _calculate_uptime()
        
    except Exception as e:
        print(f"[Metrics] Error aggregating metrics: {e}")
    
    return metrics


def write_pulse(notion: NotionClientWrapper, metrics: Dict) -> Optional[str]:
    """
    Write System Pulse entry to Governance Ledger.
    
    Args:
        notion: Notion client wrapper
        metrics: Metrics dictionary from get_metrics()
    
    Returns:
        Page ID of created pulse entry, or None if failed
    """
    governance_db = os.getenv("NOTION_GOVERNANCE_DB_ID")
    if not governance_db:
        print("[Metrics] NOTION_GOVERNANCE_DB_ID not configured")
        return None
    
    try:
        today_utc = datetime.utcnow().strftime("%Y-%m-%d")
        
        notes = (
            f"Jobs {metrics['jobs_7d']} | "
            f"QA {metrics['avg_qa_7d']}% | "
            f"Rev ${metrics['revenue_7d']} | "
            f"ROI {metrics['roi_30d']}% | "
            f"Uptime {metrics['uptime_pct']}%"
        )
        
        properties = {
            "Decision": {
                "title": [{"text": {"content": f"System Pulse {today_utc}"}}]
            },
            "Notes": {
                "rich_text": [{"text": {"content": notes}}]
            },
            "Severity": {
                "select": {"name": "Info"}
            },
            "Source": {
                "select": {"name": "Ops Monitor"}
            },
            "jobs_7d": {"number": metrics["jobs_7d"]},
            "avg_qa_7d": {"number": metrics["avg_qa_7d"]},
            "revenue_7d": {"number": metrics["revenue_7d"]},
            "roi_30d": {"number": metrics["roi_30d"]},
            "uptime_pct": {"number": metrics["uptime_pct"]}
        }
        
        client = notion.get_client()
        response = client.pages.create(
            parent={"database_id": governance_db},
            properties=properties
        )
        
        page_id = response.get("id")
        print(f"[Metrics] System Pulse created: {page_id}")
        return page_id
        
    except Exception as e:
        print(f"[Metrics] Error writing pulse: {e}")
        return None


def _calculate_uptime() -> float:
    """
    Calculate uptime percentage from health logs over last 7 days.
    
    Returns:
        Uptime percentage (0-100)
    """
    health_log_path = "logs/health.ndjson"
    
    if not os.path.exists(health_log_path):
        return 100.0  # Assume healthy if no logs
    
    try:
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        ok_count = 0
        total_count = 0
        
        with open(health_log_path, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                
                try:
                    entry = json.loads(line)
                    timestamp = datetime.fromisoformat(entry.get("timestamp", "").replace("Z", ""))
                    
                    if timestamp < seven_days_ago:
                        continue
                    
                    total_count += 1
                    if entry.get("status") == "ok":
                        ok_count += 1
                        
                except (json.JSONDecodeError, ValueError):
                    continue
        
        if total_count == 0:
            return 100.0
        
        uptime = round(100.0 * ok_count / total_count, 1)
        return uptime
        
    except Exception as e:
        print(f"[Metrics] Error calculating uptime: {e}")
        return 100.0


def log_health_check(status: str = "ok"):
    """
    Append health check result to logs/health.ndjson.
    Keeps only last 7 days of logs.
    
    Args:
        status: Health status ("ok" or "error")
    """
    log_dir = "logs"
    log_path = os.path.join(log_dir, "health.ndjson")
    
    # Create logs directory if needed
    os.makedirs(log_dir, exist_ok=True)
    
    # Append current health check
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": status
    }
    
    try:
        with open(log_path, 'a') as f:
            f.write(json.dumps(entry) + "\n")
        
        # Clean up old entries (keep last 7 days)
        _cleanup_old_health_logs(log_path)
        
    except Exception as e:
        print(f"[Metrics] Error logging health check: {e}")


def _cleanup_old_health_logs(log_path: str):
    """Remove health log entries older than 7 days"""
    try:
        if not os.path.exists(log_path):
            return
        
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        # Read all entries
        entries = []
        with open(log_path, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                
                try:
                    entry = json.loads(line)
                    timestamp = datetime.fromisoformat(entry.get("timestamp", "").replace("Z", ""))
                    
                    if timestamp >= seven_days_ago:
                        entries.append(entry)
                except (json.JSONDecodeError, ValueError):
                    continue
        
        # Rewrite with only recent entries
        with open(log_path, 'w') as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")
                
    except Exception as e:
        print(f"[Metrics] Error cleaning up health logs: {e}")
