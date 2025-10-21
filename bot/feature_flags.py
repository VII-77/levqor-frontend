"""
EchoPilot Feature Flags - A/B Testing & Progressive Rollout System
Phase 108: Hot-reload cache, rollout percentages, environment filtering
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from threading import Lock

# Feature flag configuration
FLAGS_FILE = Path('configs/flags.json')
LOG_FILE = Path('logs/feature_flags.ndjson')

# Hot-reload cache
_cache = {}
_cache_lock = Lock()
_last_modified = None

def log_flag_event(event, data=None):
    """Write NDJSON log entry for flag operations"""
    LOG_FILE.parent.mkdir(exist_ok=True)
    
    entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event': event
    }
    if data:
        entry.update(data)
    
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def _load_flags():
    """Load feature flags from disk with hot-reload check"""
    global _cache, _last_modified
    
    if not FLAGS_FILE.exists():
        log_flag_event('flags_missing', {'error': 'flags.json not found'})
        return {}
    
    # Check if file was modified
    current_mtime = FLAGS_FILE.stat().st_mtime
    
    with _cache_lock:
        # Return cache if file unchanged
        if _last_modified == current_mtime and _cache:
            return _cache
        
        # Reload from disk
        try:
            with open(FLAGS_FILE, 'r') as f:
                data = json.load(f)
            
            _cache = data.get('flags', {})
            _last_modified = current_mtime
            
            log_flag_event('flags_reloaded', {
                'ok': True,
                'flag_count': len(_cache),
                'mtime': current_mtime
            })
            
            return _cache
            
        except Exception as e:
            log_flag_event('flags_load_error', {'error': str(e)})
            return _cache  # Return stale cache on error

def is_enabled(flag_name, user_id=None, environment=None):
    """
    Check if feature flag is enabled for user
    
    Args:
        flag_name: Name of feature flag
        user_id: Optional user ID for rollout percentage check
        environment: Optional environment (development/production)
    
    Returns:
        bool: True if flag is enabled for this user
    """
    flags = _load_flags()
    
    if flag_name not in flags:
        log_flag_event('flag_check', {
            'flag': flag_name,
            'result': False,
            'reason': 'not_found'
        })
        return False
    
    flag = flags[flag_name]
    
    # Check if flag is enabled globally
    if not flag.get('enabled', False):
        return False
    
    # Check environment filter
    if environment:
        allowed_envs = flag.get('environments', [])
        if allowed_envs and environment not in allowed_envs:
            return False
    
    # Check rollout percentage
    rollout_pct = flag.get('rollout_pct', 100)
    
    if rollout_pct < 100 and user_id:
        # Use hash of user_id + flag_name for consistent bucketing
        bucket_key = f"{user_id}:{flag_name}"
        hash_val = int(hashlib.md5(bucket_key.encode()).hexdigest(), 16)
        bucket = hash_val % 100
        
        if bucket >= rollout_pct:
            return False
    
    return True

def get_flag(flag_name):
    """Get full flag configuration"""
    flags = _load_flags()
    return flags.get(flag_name)

def get_all_flags():
    """Get all feature flags"""
    return _load_flags()

def set_flag(flag_name, enabled=None, rollout_pct=None, environments=None, description=None):
    """
    Update feature flag configuration
    
    Args:
        flag_name: Name of feature flag
        enabled: Enable/disable flag
        rollout_pct: Rollout percentage (0-100)
        environments: List of allowed environments
        description: Flag description
    """
    if not FLAGS_FILE.exists():
        log_flag_event('set_flag_error', {'error': 'flags.json not found'})
        return False
    
    try:
        with open(FLAGS_FILE, 'r') as f:
            data = json.load(f)
        
        flags = data.get('flags', {})
        
        # Create or update flag
        if flag_name not in flags:
            flags[flag_name] = {
                'enabled': False,
                'rollout_pct': 0,
                'description': '',
                'environments': [],
                'created_at': datetime.utcnow().isoformat() + 'Z'
            }
        
        flag = flags[flag_name]
        old_config = flag.copy()
        
        # Update fields
        if enabled is not None:
            flag['enabled'] = enabled
        if rollout_pct is not None:
            flag['rollout_pct'] = max(0, min(100, rollout_pct))
        if environments is not None:
            flag['environments'] = environments
        if description is not None:
            flag['description'] = description
        
        flag['updated_at'] = datetime.utcnow().isoformat() + 'Z'
        
        # Update metadata
        data['meta']['last_updated'] = datetime.utcnow().isoformat() + 'Z'
        
        # Write back to disk
        with open(FLAGS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Clear cache to force reload
        global _last_modified
        with _cache_lock:
            _last_modified = None
        
        log_flag_event('flag_updated', {
            'ok': True,
            'flag': flag_name,
            'old': old_config,
            'new': flag
        })
        
        return True
        
    except Exception as e:
        log_flag_event('set_flag_error', {
            'flag': flag_name,
            'error': str(e)
        })
        return False

def delete_flag(flag_name):
    """Delete feature flag"""
    if not FLAGS_FILE.exists():
        return False
    
    try:
        with open(FLAGS_FILE, 'r') as f:
            data = json.load(f)
        
        flags = data.get('flags', {})
        
        if flag_name not in flags:
            return False
        
        deleted_config = flags.pop(flag_name)
        
        # Update metadata
        data['meta']['last_updated'] = datetime.utcnow().isoformat() + 'Z'
        
        # Write back to disk
        with open(FLAGS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Clear cache
        global _last_modified
        with _cache_lock:
            _last_modified = None
        
        log_flag_event('flag_deleted', {
            'ok': True,
            'flag': flag_name,
            'config': deleted_config
        })
        
        return True
        
    except Exception as e:
        log_flag_event('delete_flag_error', {
            'flag': flag_name,
            'error': str(e)
        })
        return False

def get_environment():
    """Get current environment from REPL_SLUG or default to development"""
    repl_slug = os.getenv('REPL_SLUG', '')
    
    if 'production' in repl_slug.lower() or os.getenv('ENVIRONMENT') == 'production':
        return 'production'
    else:
        return 'development'

def evaluate_for_user(user_id):
    """
    Evaluate all flags for a specific user
    Returns dict of flag_name -> enabled status
    """
    flags = _load_flags()
    environment = get_environment()
    
    result = {}
    for flag_name in flags:
        result[flag_name] = is_enabled(flag_name, user_id=user_id, environment=environment)
    
    return result
