import json
import os
from datetime import datetime
from pathlib import Path


USAGE_FILE = "data/usage_quota.json"
FREE_DAILY_LIMIT = 1


def _get_usage_data():
    """Load usage quota data"""
    if not os.path.exists(USAGE_FILE):
        return {}
    try:
        with open(USAGE_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def _save_usage_data(data):
    """Save usage quota data"""
    os.makedirs(os.path.dirname(USAGE_FILE), exist_ok=True)
    with open(USAGE_FILE, 'w') as f:
        json.dump(data, f)


def check_quota(user_or_ip: str, connector: str, plan: str = "free") -> None:
    """
    Check quota for connector usage.
    Raises: 402 error dict if quota exceeded
    """
    if plan == "pro":
        return
    
    today = datetime.utcnow().strftime("%Y-%m-%d")
    usage = _get_usage_data()
    
    key = f"{user_or_ip}:{connector}:{today}"
    current_count = usage.get(key, 0)
    
    if current_count >= FREE_DAILY_LIMIT:
        raise ValueError(json.dumps({
            "error": "rate_limited",
            "message": f"Free plan: {FREE_DAILY_LIMIT} {connector} call/day. Upgrade for unlimited.",
            "upgrade": "/pricing"
        }))
    
    usage[key] = current_count + 1
    _save_usage_data(usage)


def get_connector_stats(connector: str = None, days: int = 7):
    """Get usage stats for connectors"""
    usage = _get_usage_data()
    stats = {}
    
    for key, count in usage.items():
        parts = key.split(':')
        if len(parts) != 3:
            continue
        
        _, conn, _ = parts
        if connector and conn != connector:
            continue
        
        stats[conn] = stats.get(conn, 0) + count
    
    return stats
