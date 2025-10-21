#!/usr/bin/env python3
"""
EchoPilot Auto-Scaler (Phase 113)
Predicts CPU/RAM/queue load and recommends scaling actions
"""

import os
import sys
import json
import psutil
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque

def log_event(event_type, details=None):
    """Log autoscaler events"""
    log_entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event_type': event_type,
        'details': details or {}
    }
    
    log_file = Path('logs/autoscaler.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def get_system_metrics():
    """Get current CPU, memory, and disk usage"""
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
        'load_avg': os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0
    }

def get_queue_depth():
    """Get automation queue depth from logs"""
    try:
        # Read recent queue logs
        queue_log = Path('logs/automation_queue.ndjson')
        if not queue_log.exists():
            return 0
        
        with open(queue_log, 'r') as f:
            lines = deque(f, maxlen=100)  # Last 100 entries
        
        if not lines:
            return 0
        
        # Count pending items
        pending = 0
        for line in lines:
            try:
                entry = json.loads(line)
                if entry.get('status') == 'pending':
                    pending += 1
            except:
                continue
        
        return pending
        
    except Exception as e:
        log_event('queue_depth_error', {'error': str(e)})
        return 0

def predict_load_trend(metrics_history):
    """Simple linear regression to predict load trend"""
    if len(metrics_history) < 2:
        return 0.0
    
    # Calculate slope of CPU usage over time
    x_sum = sum(range(len(metrics_history)))
    y_sum = sum(m['cpu_percent'] for m in metrics_history)
    xy_sum = sum(i * m['cpu_percent'] for i, m in enumerate(metrics_history))
    x_sq_sum = sum(i * i for i in range(len(metrics_history)))
    
    n = len(metrics_history)
    slope = (n * xy_sum - x_sum * y_sum) / (n * x_sq_sum - x_sum * x_sum)
    
    return slope

def analyze_scaling_need(metrics, queue_depth, trend):
    """Determine if scaling action is needed"""
    recommendations = []
    
    # High CPU threshold
    if metrics['cpu_percent'] > 80:
        recommendations.append({
            'action': 'scale_up',
            'reason': f"CPU usage high: {metrics['cpu_percent']:.1f}%",
            'priority': 'high'
        })
    elif metrics['cpu_percent'] < 20 and trend < 0:
        recommendations.append({
            'action': 'scale_down',
            'reason': f"CPU usage low: {metrics['cpu_percent']:.1f}%",
            'priority': 'low'
        })
    
    # High memory threshold
    if metrics['memory_percent'] > 85:
        recommendations.append({
            'action': 'scale_up',
            'reason': f"Memory usage high: {metrics['memory_percent']:.1f}%",
            'priority': 'high'
        })
    
    # Queue backlog
    if queue_depth > 50:
        recommendations.append({
            'action': 'scale_up',
            'reason': f"Queue backlog: {queue_depth} items",
            'priority': 'medium'
        })
    elif queue_depth == 0 and metrics['cpu_percent'] < 30:
        recommendations.append({
            'action': 'scale_down',
            'reason': "Queue empty and low CPU usage",
            'priority': 'low'
        })
    
    # Positive trend
    if trend > 5:
        recommendations.append({
            'action': 'scale_up',
            'reason': f"CPU trend increasing: +{trend:.2f}%/min",
            'priority': 'medium'
        })
    
    return recommendations

def load_metrics_history():
    """Load recent metrics from autoscaler log"""
    try:
        log_file = Path('logs/autoscaler.ndjson')
        if not log_file.exists():
            return []
        
        with open(log_file, 'r') as f:
            lines = deque(f, maxlen=60)  # Last 60 metrics (60 minutes)
        
        metrics = []
        for line in lines:
            try:
                entry = json.loads(line)
                if entry.get('event_type') == 'metrics_snapshot':
                    metrics.append(entry.get('details', {}).get('metrics', {}))
            except:
                continue
        
        return metrics[-10:]  # Last 10 data points
        
    except Exception as e:
        log_event('history_load_error', {'error': str(e)})
        return []

def run_autoscaler():
    """Main autoscaler routine"""
    try:
        # Collect current metrics
        metrics = get_system_metrics()
        queue_depth = get_queue_depth()
        
        # Log metrics snapshot
        log_event('metrics_snapshot', {
            'metrics': metrics,
            'queue_depth': queue_depth
        })
        
        # Load historical data
        history = load_metrics_history()
        trend = predict_load_trend(history)
        
        # Analyze scaling needs
        recommendations = analyze_scaling_need(metrics, queue_depth, trend)
        
        # Log recommendations
        if recommendations:
            log_event('scaling_recommendations', {
                'recommendations': recommendations,
                'metrics': metrics,
                'queue_depth': queue_depth,
                'trend': trend
            })
        
        # Build report
        report = {
            'ts': datetime.utcnow().isoformat() + 'Z',
            'metrics': metrics,
            'queue_depth': queue_depth,
            'trend': trend,
            'recommendations': recommendations,
            'status': 'ok'
        }
        
        print(json.dumps(report, indent=2))
        return 0
        
    except Exception as e:
        log_event('autoscaler_error', {'error': str(e)})
        print(json.dumps({
            'ts': datetime.utcnow().isoformat() + 'Z',
            'status': 'error',
            'error': str(e)
        }, indent=2))
        return 1

if __name__ == '__main__':
    sys.exit(run_autoscaler())
