#!/usr/bin/env python3
"""
EchoPilot Executive Scheduler
Runs automated tasks on schedule without cron.
"""

import os
import sys
import time
import json
import signal
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Configuration from environment
SCHED_BRIEF_UTC = os.getenv('SCHED_BRIEF_UTC', '08:00')
SCHED_REPORT_UTC = os.getenv('SCHED_REPORT_UTC', '09:00')
SCHED_SELFHEAL_EVERY_HOURS = int(os.getenv('SCHED_SELFHEAL_EVERY_HOURS', '6'))
DASHBOARD_KEY = os.getenv('DASHBOARD_KEY', '')
BASE_URL = 'http://localhost:5000'

# Debounce: don't run same task twice within 55 minutes
DEBOUNCE_MINUTES = 55
last_run = {}

# Logging
log_file = Path('logs/scheduler.log')
log_file.parent.mkdir(exist_ok=True)

running = True

def signal_handler(signum, frame):
    """Handle SIGTERM for graceful shutdown"""
    global running
    log_event('shutdown', {'signal': signum})
    running = False
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

def log_event(task, data):
    """Log NDJSON to logs/scheduler.log"""
    entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'task': task,
        **data
    }
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    print(f"[{entry['ts']}] {task}: {data.get('ok', data.get('status', 'N/A'))}")

def should_run(task_name):
    """Check if task should run based on debounce"""
    if task_name not in last_run:
        return True
    
    elapsed = datetime.utcnow() - last_run[task_name]
    return elapsed.total_seconds() > (DEBOUNCE_MINUTES * 60)

def mark_run(task_name):
    """Mark task as run"""
    last_run[task_name] = datetime.utcnow()

def call_api(method, endpoint, description):
    """Call API with retries"""
    if not DASHBOARD_KEY:
        log_event(description, {'ok': False, 'error': 'DASHBOARD_KEY not set'})
        return False
    
    url = f"{BASE_URL}{endpoint}"
    headers = {'X-Dash-Key': DASHBOARD_KEY}
    
    for attempt in range(3):
        try:
            if method == 'POST':
                resp = requests.post(url, headers=headers, timeout=30)
            else:
                resp = requests.get(url, headers=headers, timeout=30)
            
            if resp.status_code == 200:
                data = resp.json()
                log_data = {'ok': True, 'status': resp.status_code}
                
                # Extract useful info
                if 'json_path' in data:
                    log_data['paths'] = [data.get('json_path'), data.get('html_path')]
                elif 'saved_to' in data:
                    log_data['paths'] = [data.get('saved_to')]
                elif 'retried_count' in data:
                    log_data['retried_count'] = data.get('retried_count')
                
                log_event(description, log_data)
                return True
            else:
                error_msg = f"HTTP {resp.status_code}"
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                log_event(description, {'ok': False, 'error': error_msg})
                return False
        
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            log_event(description, {'ok': False, 'error': str(e)})
            return False
    
    return False

def parse_time(time_str):
    """Parse HH:MM to (hour, minute)"""
    try:
        parts = time_str.split(':')
        return int(parts[0]), int(parts[1])
    except:
        return 0, 0

def is_time_match(target_hour, target_minute):
    """Check if current UTC time matches target"""
    now = datetime.utcnow()
    return now.hour == target_hour and now.minute == target_minute

def run_scheduled_tasks():
    """Check and run scheduled tasks"""
    
    # 1) CEO Brief at SCHED_BRIEF_UTC
    brief_hour, brief_minute = parse_time(SCHED_BRIEF_UTC)
    if is_time_match(brief_hour, brief_minute) and should_run('ceo_brief'):
        call_api('POST', '/api/exec/brief', 'ceo_brief')
        mark_run('ceo_brief')
    
    # 2) Daily Report at SCHED_REPORT_UTC
    report_hour, report_minute = parse_time(SCHED_REPORT_UTC)
    if is_time_match(report_hour, report_minute) and should_run('daily_report'):
        # Warm cache with metrics calls
        call_api('GET', '/api/finance-metrics', 'finance_metrics_cache')
        call_api('GET', '/api/metrics-summary', 'metrics_summary_cache')
        mark_run('daily_report')
    
    # 3) Self-Heal every SCHED_SELFHEAL_EVERY_HOURS
    if should_run('self_heal'):
        # Check if enough hours have passed since last run
        if 'self_heal' not in last_run or \
           (datetime.utcnow() - last_run['self_heal']).total_seconds() >= (SCHED_SELFHEAL_EVERY_HOURS * 3600):
            call_api('POST', '/api/self-heal', 'self_heal')
            mark_run('self_heal')

def main():
    """Main scheduler loop"""
    log_event('startup', {
        'ok': True,
        'config': {
            'brief_time': SCHED_BRIEF_UTC,
            'report_time': SCHED_REPORT_UTC,
            'selfheal_hours': SCHED_SELFHEAL_EVERY_HOURS,
            'base_url': BASE_URL
        }
    })
    
    print(f"🤖 EchoPilot Executive Scheduler Started")
    print(f"   CEO Brief: {SCHED_BRIEF_UTC} UTC")
    print(f"   Daily Report: {SCHED_REPORT_UTC} UTC")
    print(f"   Self-Heal: Every {SCHED_SELFHEAL_EVERY_HOURS} hours")
    print(f"   Logs: {log_file}")
    print(f"   Press Ctrl+C to stop")
    print()
    
    # Initial self-heal run on startup
    if DASHBOARD_KEY:
        call_api('POST', '/api/self-heal', 'self_heal_startup')
        mark_run('self_heal')
    
    while running:
        try:
            run_scheduled_tasks()
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            log_event('shutdown', {'ok': True, 'reason': 'KeyboardInterrupt'})
            break
        except Exception as e:
            log_event('error', {'ok': False, 'error': str(e)})
            time.sleep(60)
    
    log_event('stopped', {'ok': True})
    print("✅ Scheduler stopped")

if __name__ == '__main__':
    main()
