#!/usr/bin/env python3
"""
EchoPilot Analytics & Product Insights (Phase 111)
Deep usage analytics with DAU/WAU/MAU, feature usage, and funnels
"""

import os
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

def log_event(event_type, user_id=None, feature=None, metadata=None):
    """Log analytics event to NDJSON"""
    event = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "user_id": user_id or "anonymous",
        "feature": feature,
        "metadata": metadata or {}
    }
    
    log_file = Path("logs/analytics_events.ndjson")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, "a") as f:
        f.write(json.dumps(event) + "\n")
    
    return event

def get_analytics_summary(days=30):
    """
    Calculate DAU/WAU/MAU, feature usage, and funnel metrics
    Returns comprehensive analytics summary
    """
    now = datetime.utcnow()
    cutoff = now - timedelta(days=days)
    
    # Data structures
    daily_users = defaultdict(set)
    weekly_users = defaultdict(set)
    monthly_users = set()
    feature_counts = defaultdict(int)
    funnel_steps = defaultdict(int)
    
    # Read all events
    events_file = Path("logs/analytics_events.ndjson")
    
    if not events_file.exists():
        return {
            "period_days": days,
            "dau": 0,
            "wau": 0,
            "mau": 0,
            "feature_usage": {},
            "funnel_steps": {},
            "total_events": 0
        }
    
    total_events = 0
    
    with open(events_file, "r") as f:
        for line in f:
            try:
                event = json.loads(line.strip())
                event_time = datetime.fromisoformat(event["ts"].replace("Z", ""))
                
                # Skip events outside window
                if event_time < cutoff:
                    continue
                
                total_events += 1
                user_id = event.get("user_id", "anonymous")
                feature = event.get("feature")
                event_type = event.get("event_type")
                
                # Track daily users
                day_key = event_time.strftime("%Y-%m-%d")
                daily_users[day_key].add(user_id)
                
                # Track weekly users
                week_key = event_time.strftime("%Y-W%W")
                weekly_users[week_key].add(user_id)
                
                # Track monthly users
                monthly_users.add(user_id)
                
                # Track feature usage
                if feature:
                    feature_counts[feature] += 1
                
                # Track funnel steps
                if event_type in ["page_view", "action", "conversion"]:
                    funnel_steps[event_type] += 1
                    
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
    
    # Calculate averages
    avg_dau = sum(len(users) for users in daily_users.values()) / max(len(daily_users), 1)
    avg_wau = sum(len(users) for users in weekly_users.values()) / max(len(weekly_users), 1)
    mau = len(monthly_users)
    
    return {
        "ts": now.isoformat() + "Z",
        "period_days": days,
        "dau": round(avg_dau, 1),
        "wau": round(avg_wau, 1),
        "mau": mau,
        "feature_usage": dict(sorted(feature_counts.items(), key=lambda x: x[1], reverse=True)),
        "funnel_steps": dict(funnel_steps),
        "total_events": total_events,
        "unique_days": len(daily_users),
        "unique_weeks": len(weekly_users)
    }

def rollup_analytics():
    """
    Daily analytics rollup job
    Aggregates raw events into daily summaries
    """
    summary = get_analytics_summary(days=30)
    
    # Write rollup
    rollup_file = Path("logs/analytics.ndjson")
    rollup_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(rollup_file, "a") as f:
        f.write(json.dumps(summary) + "\n")
    
    return summary

if __name__ == "__main__":
    # Run rollup when executed directly
    result = rollup_analytics()
    print(json.dumps(result, indent=2))
