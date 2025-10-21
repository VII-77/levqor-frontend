#!/usr/bin/env python3
"""
EchoPilot Autonomous SLA Tracker
Tracks daily uptime percentage from telemetry data
Runs every 15 minutes to build SLA history
"""

import json
import time
import datetime
import os

TELEMETRY_FILE = "logs/os_telemetry_cache.json"
SLA_HISTORY_FILE = "logs/os_sla_history.json"

def pct(a, b):
    """Calculate percentage"""
    return round((a / b) * 100, 2) if b else 0

def main():
    """Track SLA uptime based on telemetry status"""
    
    # Check if telemetry data exists
    if not os.path.exists(TELEMETRY_FILE):
        print(f"⚠️  Telemetry file not found: {TELEMETRY_FILE}")
        return
    
    # Read current telemetry status
    try:
        with open(TELEMETRY_FILE, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading telemetry: {e}")
        return
    
    status = data.get("status", "fail")
    today = datetime.date.today().isoformat()
    
    # Load existing history
    hist = {}
    if os.path.exists(SLA_HISTORY_FILE):
        try:
            with open(SLA_HISTORY_FILE, 'r') as f:
                hist = json.load(f)
        except Exception:
            hist = {}
    
    # Update today's counts
    day = hist.get(today, {"ok": 0, "fail": 0, "checks": 0})
    day["checks"] += 1
    
    if status.lower() == "ok":
        day["ok"] += 1
    else:
        day["fail"] += 1
    
    hist[today] = day
    
    # Save updated history
    try:
        with open(SLA_HISTORY_FILE, 'w') as f:
            json.dump(hist, f, indent=2)
    except Exception as e:
        print(f"❌ Error saving SLA history: {e}")
        return
    
    # Calculate and display uptime
    uptime = pct(day["ok"], day["ok"] + day["fail"])
    
    print(f"📊 {today} uptime: {uptime}% ({day['ok']}/{day['checks']} checks OK)")
    
    # Alert if uptime drops below threshold
    if uptime < 99.0 and day["checks"] > 10:
        print(f"⚠️  WARNING: Daily uptime below 99% threshold!")

if __name__ == "__main__":
    main()
