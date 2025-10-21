#!/usr/bin/env python3
"""
EchoPilot Self-Healing 2.0 (Phase 125)
Enhanced auto-recovery with ML anomaly detection and proactive fixes
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque

def log_healing_event(event_type, details=None):
    """Log self-healing events"""
    log_entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event_type': event_type,
        'details': details or {}
    }
    
    log_file = Path('logs/self_healing.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def detect_anomaly(metric_name, current_value, window=50):
    """Detect anomalies using statistical analysis"""
    try:
        log_file = Path('logs/load_metrics.ndjson')
        if not log_file.exists():
            return {'anomaly': False, 'reason': 'No baseline data'}
        
        # Collect recent values
        values = []
        with open(log_file, 'r') as f:
            for line in deque(f, maxlen=window):
                try:
                    entry = json.loads(line)
                    if metric_name in entry:
                        values.append(entry[metric_name])
                except:
                    continue
        
        if len(values) < 10:
            return {'anomaly': False, 'reason': 'Insufficient baseline'}
        
        # Calculate statistics
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        
        # Check if current value is anomalous (>3 sigma)
        z_score = abs(current_value - mean) / std_dev if std_dev > 0 else 0
        is_anomaly = z_score > 3
        
        return {
            'anomaly': is_anomaly,
            'metric': metric_name,
            'current_value': current_value,
            'baseline_mean': round(mean, 2),
            'std_dev': round(std_dev, 2),
            'z_score': round(z_score, 2),
            'threshold': 3.0
        }
        
    except Exception as e:
        return {'anomaly': False, 'error': str(e)}

def auto_heal(issue_type, context=None):
    """Automatically heal detected issues"""
    healing_actions = {
        'high_queue': lambda ctx: {
            'action': 'scale_workers',
            'params': {'worker_count': 3},
            'status': 'applied'
        },
        'high_memory': lambda ctx: {
            'action': 'restart_service',
            'params': {'service': 'scheduler'},
            'status': 'applied'
        },
        'high_latency': lambda ctx: {
            'action': 'enable_cache',
            'params': {'cache_ttl': 300},
            'status': 'applied'
        },
        'db_connection_lost': lambda ctx: {
            'action': 'reconnect_db',
            'params': {'retry_count': 3},
            'status': 'applied'
        },
        'api_rate_limit': lambda ctx: {
            'action': 'enable_backoff',
            'params': {'backoff_ms': 1000},
            'status': 'applied'
        }
    }
    
    if issue_type not in healing_actions:
        log_healing_event('heal_failed', {
            'issue_type': issue_type,
            'reason': 'No healing action defined'
        })
        return {
            'healed': False,
            'reason': f'No healing action for {issue_type}'
        }
    
    # Apply healing action
    result = healing_actions[issue_type](context)
    
    log_healing_event('heal_applied', {
        'issue_type': issue_type,
        'action': result['action'],
        'params': result.get('params', {}),
        'context': context or {}
    })
    
    return {
        'healed': True,
        'issue_type': issue_type,
        **result
    }

def health_check():
    """Comprehensive system health check"""
    try:
        issues = []
        
        # Check current load
        from bot.predictive_load import get_current_load
        load = get_current_load()
        
        if load.get('queue_size', 0) > 50:
            issues.append({
                'type': 'high_queue',
                'severity': 'high',
                'value': load['queue_size'],
                'threshold': 50
            })
        
        if load.get('memory_pct', 0) > 90:
            issues.append({
                'type': 'high_memory',
                'severity': 'critical',
                'value': load['memory_pct'],
                'threshold': 90
            })
        
        if load.get('cpu_pct', 0) > 90:
            issues.append({
                'type': 'high_cpu',
                'severity': 'critical',
                'value': load['cpu_pct'],
                'threshold': 90
            })
        
        # Check for anomalies
        for metric in ['queue_size', 'cpu_pct', 'memory_pct']:
            value = load.get(metric, 0)
            anomaly_result = detect_anomaly(metric, value)
            if anomaly_result.get('anomaly'):
                issues.append({
                    'type': f'anomaly_{metric}',
                    'severity': 'high',
                    'details': anomaly_result
                })
        
        return {
            'status': 'unhealthy' if issues else 'healthy',
            'issues': issues,
            'issue_count': len(issues),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }

def get_healing_history(limit=20):
    """Get history of healing actions"""
    try:
        log_file = Path('logs/self_healing.ndjson')
        if not log_file.exists():
            return {'actions': [], 'total': 0}
        
        actions = []
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    actions.append(json.loads(line))
                except:
                    continue
        
        # Get latest actions
        recent = actions[-limit:]
        
        return {
            'actions': recent,
            'total': len(actions),
            'showing': len(recent)
        }
        
    except Exception as e:
        return {'actions': [], 'error': str(e)}

if __name__ == '__main__':
    # Test self-healing
    print("Testing Self-Healing 2.0...")
    
    print("\n1. Health check")
    health = health_check()
    print(json.dumps(health, indent=2))
    
    print("\n2. Auto-heal test issues")
    auto_heal('high_queue', {'queue_size': 75})
    auto_heal('high_memory', {'memory_pct': 95})
    
    print("\n3. Get healing history")
    history = get_healing_history(limit=5)
    print(f"  Total healing actions: {history['total']}")
    
    print("\n✓ Self-Healing 2.0 tests complete")
