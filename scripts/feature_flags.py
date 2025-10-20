#!/usr/bin/env python3
"""
Phase 62: Feature Flags
Dynamic feature toggle system
"""
import os
import sys
import json
import threading
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

FLAG_FILE = 'configs/flags.json'
_lock = threading.Lock()

def get_flags():
    """Get all feature flags"""
    try:
        with open(FLAG_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def get_flag(key, default=False):
    """Get single feature flag"""
    flags = get_flags()
    return flags.get(key, default)

def set_flag(key, value):
    """Set feature flag"""
    with _lock:
        flags = get_flags()
        flags[key] = value
        
        os.makedirs('configs', exist_ok=True)
        with open(FLAG_FILE, 'w') as f:
            json.dump(flags, f, indent=2)
        
        # Log change
        log_entry = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "event": "flag_changed",
            "key": key,
            "value": value
        }
        
        os.makedirs('logs', exist_ok=True)
        with open('logs/feature_flags.ndjson', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return flags

def list_flags():
    """List all flags with their status"""
    flags = get_flags()
    return {
        "ok": True,
        "count": len(flags),
        "flags": flags
    }

if __name__ == "__main__":
    result = list_flags()
    print(json.dumps(result, indent=2))
