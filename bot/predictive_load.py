#!/usr/bin/env python3
"""
EchoPilot Predictive Load & Staff Hints (Phase 124)
ML-based load forecasting and staffing recommendations
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

def log_load_metrics(queue_size, active_jobs, cpu_pct, memory_pct):
    """Log system load metrics for prediction"""
    log_entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'queue_size': queue_size,
        'active_jobs': active_jobs,
        'cpu_pct': cpu_pct,
        'memory_pct': memory_pct
    }
    
    log_file = Path('logs/load_metrics.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def predict_load(hours_ahead=24):
    """Predict system load for next N hours"""
    try:
        log_file = Path('logs/load_metrics.ndjson')
        if not log_file.exists():
            return {
                'prediction': 'low',
                'confidence': 0.0,
                'note': 'Insufficient data'
            }
        
        # Get historical load data
        cutoff = datetime.utcnow() - timedelta(days=7)
        hourly_loads = defaultdict(list)
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry['ts'].replace('Z', '+00:00'))
                    
                    if entry_time < cutoff:
                        continue
                    
                    hour = entry_time.hour
                    hourly_loads[hour].append({
                        'queue_size': entry.get('queue_size', 0),
                        'cpu_pct': entry.get('cpu_pct', 0),
                        'memory_pct': entry.get('memory_pct', 0)
                    })
                except:
                    continue
        
        # Predict for target hour
        target_hour = (datetime.utcnow() + timedelta(hours=hours_ahead)).hour
        
        if target_hour not in hourly_loads or not hourly_loads[target_hour]:
            return {
                'prediction': 'unknown',
                'confidence': 0.0,
                'note': f'No historical data for hour {target_hour}'
            }
        
        # Calculate average metrics for that hour
        samples = hourly_loads[target_hour]
        avg_queue = sum(s['queue_size'] for s in samples) / len(samples)
        avg_cpu = sum(s['cpu_pct'] for s in samples) / len(samples)
        avg_memory = sum(s['memory_pct'] for s in samples) / len(samples)
        
        # Classify load
        if avg_queue > 50 or avg_cpu > 80:
            load_level = 'high'
        elif avg_queue > 20 or avg_cpu > 50:
            load_level = 'medium'
        else:
            load_level = 'low'
        
        confidence = min(len(samples) / 10, 1.0)
        
        return {
            'target_hour': target_hour,
            'hours_ahead': hours_ahead,
            'prediction': load_level,
            'confidence': round(confidence, 2),
            'metrics': {
                'avg_queue_size': round(avg_queue, 1),
                'avg_cpu_pct': round(avg_cpu, 1),
                'avg_memory_pct': round(avg_memory, 1)
            },
            'sample_count': len(samples)
        }
        
    except Exception as e:
        return {'error': str(e)}

def get_staffing_recommendation():
    """Get AI-powered staffing hints"""
    try:
        # Get current and predicted load
        current_metrics = get_current_load()
        predicted_load = predict_load(hours_ahead=4)
        
        queue_size = current_metrics.get('queue_size', 0)
        prediction = predicted_load.get('prediction', 'unknown')
        
        # Generate recommendation
        if queue_size > 100 or prediction == 'high':
            recommendation = {
                'action': 'scale_up',
                'workers_recommended': 3,
                'priority': 'high',
                'reason': 'High current load or predicted spike'
            }
        elif queue_size > 50 or prediction == 'medium':
            recommendation = {
                'action': 'monitor',
                'workers_recommended': 2,
                'priority': 'medium',
                'reason': 'Moderate load, consider scaling'
            }
        else:
            recommendation = {
                'action': 'maintain',
                'workers_recommended': 1,
                'priority': 'low',
                'reason': 'Load within normal range'
            }
        
        return {
            'recommendation': recommendation,
            'current_load': current_metrics,
            'predicted_load': predicted_load
        }
        
    except Exception as e:
        return {'error': str(e)}

def get_current_load():
    """Get current system load"""
    try:
        log_file = Path('logs/load_metrics.ndjson')
        if not log_file.exists():
            return {'queue_size': 0, 'active_jobs': 0, 'cpu_pct': 0, 'memory_pct': 0}
        
        # Get most recent entry
        with open(log_file, 'r') as f:
            lines = list(f)
        
        if not lines:
            return {'queue_size': 0, 'active_jobs': 0, 'cpu_pct': 0, 'memory_pct': 0}
        
        latest = json.loads(lines[-1])
        return {
            'queue_size': latest.get('queue_size', 0),
            'active_jobs': latest.get('active_jobs', 0),
            'cpu_pct': latest.get('cpu_pct', 0),
            'memory_pct': latest.get('memory_pct', 0),
            'timestamp': latest.get('ts')
        }
        
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    # Test predictive load
    print("Testing Predictive Load...")
    
    print("\n1. Logging load metrics")
    log_load_metrics(queue_size=15, active_jobs=3, cpu_pct=45, memory_pct=60)
    log_load_metrics(queue_size=25, active_jobs=5, cpu_pct=62, memory_pct=70)
    log_load_metrics(queue_size=8, active_jobs=2, cpu_pct=30, memory_pct=55)
    
    print("\n2. Get current load")
    current = get_current_load()
    print(json.dumps(current, indent=2))
    
    print("\n3. Predict load (4 hours ahead)")
    prediction = predict_load(hours_ahead=4)
    print(json.dumps(prediction, indent=2))
    
    print("\n4. Get staffing recommendation")
    staffing = get_staffing_recommendation()
    print(json.dumps(staffing, indent=2))
    
    print("\n✓ Predictive Load tests complete")
