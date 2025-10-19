#!/usr/bin/env python3
"""
Daily System Pulse scheduler.
Triggers pulse generation at 06:30 UTC daily with idempotency.
"""

import os
import requests
from datetime import datetime
from typing import Optional


def should_run_pulse() -> bool:
    """
    Check if pulse should run today.
    Uses tmp/last_pulse_utc.txt for idempotency.
    
    Returns:
        True if pulse hasn't run today, False otherwise
    """
    now = datetime.utcnow()
    today_utc = now.strftime("%Y-%m-%d")
    
    # Check if we've run today already
    pulse_tracker = "tmp/last_pulse_utc.txt"
    
    try:
        os.makedirs("tmp", exist_ok=True)
        
        if os.path.exists(pulse_tracker):
            with open(pulse_tracker, 'r') as f:
                last_run = f.read().strip()
                
            if last_run == today_utc:
                return False  # Already ran today
        
        return True
        
    except Exception as e:
        print(f"[Pulse Scheduler] Error checking last run: {e}")
        return False


def mark_pulse_complete():
    """Mark today's pulse as complete"""
    today_utc = datetime.utcnow().strftime("%Y-%m-%d")
    pulse_tracker = "tmp/last_pulse_utc.txt"
    
    try:
        os.makedirs("tmp", exist_ok=True)
        with open(pulse_tracker, 'w') as f:
            f.write(today_utc)
    except Exception as e:
        print(f"[Pulse Scheduler] Error marking complete: {e}")


def trigger_pulse() -> Optional[dict]:
    """
    Trigger pulse endpoint via internal HTTP call.
    
    Returns:
        Response dict or None if failed
    """
    try:
        base_url = os.getenv('REPLIT_DOMAINS', 'localhost').split(',')[0]
        if not base_url.startswith('http'):
            base_url = f"https://{base_url}"
        
        token = os.getenv('HEALTH_TOKEN', '')
        url = f"{base_url}/pulse?token={token}"
        
        # Internal HTTP call with short timeout
        response = requests.post(url, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"[Pulse Scheduler] ✅ Pulse created: {result.get('id')}")
            return result
        else:
            print(f"[Pulse Scheduler] ❌ Failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"[Pulse Scheduler] Error triggering pulse: {e}")
        return None


def check_and_run_pulse():
    """
    Check if it's time to run pulse (06:30 UTC) and execute if needed.
    This is called periodically from the main bot loop.
    """
    now = datetime.utcnow()
    
    # Only run between 06:30 and 06:45 UTC
    if not (6 <= now.hour < 7 and 30 <= now.minute < 45):
        return
    
    # Check idempotency
    if not should_run_pulse():
        return
    
    print(f"[Pulse Scheduler] 🎯 Triggering daily System Pulse at {now.isoformat()}Z")
    
    result = trigger_pulse()
    
    if result and result.get('ok'):
        mark_pulse_complete()
        print("[Pulse Scheduler] ✅ Daily pulse complete")
        print(f"[Pulse Scheduler] Metrics: {result.get('metrics')}")
    else:
        print("[Pulse Scheduler] ⚠️  Pulse failed, will retry tomorrow")
