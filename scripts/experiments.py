#!/usr/bin/env python3
"""
Phase 63: Experiments (A/B Testing)
User assignment and experiment logging
"""
import os
import sys
import json
import hashlib
import time
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

EXP_FILE = 'configs/experiments.json'

def get_experiments():
    """Get all experiment configs"""
    try:
        with open(EXP_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def assign_variant(user, experiment):
    """
    Assign user to experiment variant using consistent hashing
    
    Args:
        user: User identifier (email, user_id, etc)
        experiment: Experiment name
    
    Returns:
        Variant assignment
    """
    try:
        experiments = get_experiments()
        exp_config = experiments.get(experiment)
        
        if not exp_config:
            return {
                "ok": False,
                "error": "unknown_experiment"
            }
        
        variants = exp_config.get('variants', ['A', 'B'])
        salt = exp_config.get('salt', 'DEFAULT')
        
        # Consistent hashing to assign variant
        hash_input = f"{user}{salt}".encode()
        hash_value = int(hashlib.sha256(hash_input).hexdigest(), 16)
        variant_index = hash_value % len(variants)
        variant = variants[variant_index]
        
        # Log assignment
        log_assignment(user, experiment, variant)
        
        return {
            "ok": True,
            "user": user,
            "experiment": experiment,
            "variant": variant,
            "description": exp_config.get('description', '')
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def log_assignment(user, experiment, variant):
    """Log experiment assignment"""
    log_entry = {
        "ts": time.time(),
        "ts_iso": datetime.utcnow().isoformat() + "Z",
        "event": "assignment",
        "user": user,
        "experiment": experiment,
        "variant": variant
    }
    
    os.makedirs('logs', exist_ok=True)
    with open('logs/experiments.ndjson', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def log_event(payload):
    """Log experiment event (conversion, click, etc)"""
    log_entry = {
        "ts": time.time(),
        "ts_iso": datetime.utcnow().isoformat() + "Z",
        **payload
    }
    
    os.makedirs('logs', exist_ok=True)
    with open('logs/experiments.ndjson', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    return {"ok": True}

if __name__ == "__main__":
    # Test assignment
    result = assign_variant("test@example.com", "pricing_v2")
    print(json.dumps(result, indent=2))
