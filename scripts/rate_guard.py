#!/usr/bin/env python3
"""
Rate Guard - Phase 32
IP ban system for rate limit violations
Temporary bans (10 minutes) after 3 consecutive 429 responses
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

BAN_FILE = "logs/ip_bans.json"
BAN_DURATION_MINUTES = 10
STRIKE_THRESHOLD = 3
STRIKE_WINDOW_MINUTES = 5

os.makedirs("logs", exist_ok=True)

def load_bans():
    """Load current ban list"""
    if os.path.exists(BAN_FILE):
        try:
            with open(BAN_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"bans": {}, "strikes": {}}
    return {"bans": {}, "strikes": {}}

def save_bans(data):
    """Save ban list"""
    with open(BAN_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def is_banned(ip):
    """Check if IP is currently banned"""
    data = load_bans()
    
    if ip in data["bans"]:
        ban_until = datetime.fromisoformat(data["bans"][ip])
        if datetime.utcnow() < ban_until:
            return True, ban_until
        else:
            # Ban expired, remove it
            del data["bans"][ip]
            save_bans(data)
            return False, None
    
    return False, None

def add_strike(ip):
    """Add a strike to IP and check if ban needed"""
    data = load_bans()
    now = datetime.utcnow()
    
    # Initialize strikes for IP if not exists
    if ip not in data["strikes"]:
        data["strikes"][ip] = []
    
    # Add current strike
    data["strikes"][ip].append(now.isoformat())
    
    # Remove old strikes (outside window)
    cutoff = now - timedelta(minutes=STRIKE_WINDOW_MINUTES)
    data["strikes"][ip] = [
        ts for ts in data["strikes"][ip]
        if datetime.fromisoformat(ts) > cutoff
    ]
    
    # Check if ban threshold reached
    if len(data["strikes"][ip]) >= STRIKE_THRESHOLD:
        # Ban the IP
        ban_until = now + timedelta(minutes=BAN_DURATION_MINUTES)
        data["bans"][ip] = ban_until.isoformat()
        data["strikes"][ip] = []  # Clear strikes after ban
        save_bans(data)
        return True, ban_until
    
    save_bans(data)
    return False, None

def clear_strike(ip):
    """Clear strikes for IP (on successful request)"""
    data = load_bans()
    if ip in data["strikes"]:
        del data["strikes"][ip]
        save_bans(data)

def get_ban_stats():
    """Get current ban statistics"""
    data = load_bans()
    now = datetime.utcnow()
    
    # Count active bans
    active_bans = 0
    for ip, ban_until_str in data["bans"].items():
        ban_until = datetime.fromisoformat(ban_until_str)
        if now < ban_until:
            active_bans += 1
    
    # Count IPs with strikes
    ips_with_strikes = len(data["strikes"])
    
    return {
        "active_bans": active_bans,
        "ips_with_strikes": ips_with_strikes,
        "total_tracked_ips": len(data["bans"]) + len(data["strikes"])
    }

def cleanup_old_bans():
    """Remove expired bans from storage"""
    data = load_bans()
    now = datetime.utcnow()
    
    # Filter out expired bans
    active_bans = {
        ip: ban_until
        for ip, ban_until in data["bans"].items()
        if datetime.fromisoformat(ban_until) > now
    }
    
    removed_count = len(data["bans"]) - len(active_bans)
    data["bans"] = active_bans
    save_bans(data)
    
    return removed_count

if __name__ == "__main__":
    # CLI interface for testing
    import sys
    
    if len(sys.argv) < 2:
        print(json.dumps(get_ban_stats(), indent=2))
        exit(0)
    
    command = sys.argv[1]
    
    if command == "check" and len(sys.argv) > 2:
        ip = sys.argv[2]
        banned, until = is_banned(ip)
        print(json.dumps({
            "ip": ip,
            "banned": banned,
            "ban_until": until.isoformat() if until else None
        }, indent=2))
    
    elif command == "strike" and len(sys.argv) > 2:
        ip = sys.argv[2]
        banned, until = add_strike(ip)
        print(json.dumps({
            "ip": ip,
            "strike_added": True,
            "banned": banned,
            "ban_until": until.isoformat() if until else None
        }, indent=2))
    
    elif command == "clear" and len(sys.argv) > 2:
        ip = sys.argv[2]
        clear_strike(ip)
        print(json.dumps({"ip": ip, "strikes_cleared": True}, indent=2))
    
    elif command == "cleanup":
        removed = cleanup_old_bans()
        print(json.dumps({"removed_expired_bans": removed}, indent=2))
    
    elif command == "stats":
        print(json.dumps(get_ban_stats(), indent=2))
    
    else:
        print("Usage: rate_guard.py [check|strike|clear|cleanup|stats] [ip]")
        exit(1)
