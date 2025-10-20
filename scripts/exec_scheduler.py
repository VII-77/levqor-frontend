#!/usr/bin/env python3
"""
EchoPilot Executive Scheduler
Runs automated tasks on schedule without cron.
Hardened with persistent daemon mode, signal handling, and heartbeat ticks.
"""

import os
import sys
import time
import json
import signal
import requests
import atexit
import threading
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
pid_file = Path('logs/scheduler.pid')

running = True
my_pid = os.getpid()

def cleanup_pid_file():
    """Remove PID file if it matches our PID"""
    try:
        if pid_file.exists():
            current_pid = int(pid_file.read_text().strip())
            if current_pid == my_pid:
                pid_file.unlink()
                log_event('cleanup', {'removed_pid': my_pid})
    except Exception as e:
        print(f"Warning: Failed to clean PID file: {e}", file=sys.stderr, flush=True)

def signal_handler(signum, frame):
    """Handle SIGTERM/SIGINT for graceful shutdown"""
    global running
    log_event('shutdown', {'signal': signum, 'pid': my_pid})
    running = False
    cleanup_pid_file()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
atexit.register(cleanup_pid_file)

def log_event(event, data=None):
    """Log NDJSON to logs/scheduler.log and stdout"""
    entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event': event,
    }
    if data:
        entry.update(data)
    
    # Write to log file
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')
        f.flush()
        os.fsync(f.fileno())
    
    # Print to stdout
    print(json.dumps(entry), flush=True)

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
    except Exception:
        return 0, 0

def is_time_match(target_hour, target_minute):
    """Check if current UTC time matches target"""
    now = datetime.utcnow()
    return now.hour == target_hour and now.minute == target_minute

def calculate_next_run_times():
    """Calculate next run times for all scheduled tasks"""
    now = datetime.utcnow()
    
    # CEO Brief
    brief_hour, brief_minute = parse_time(SCHED_BRIEF_UTC)
    brief_next = now.replace(hour=brief_hour, minute=brief_minute, second=0, microsecond=0)
    if brief_next <= now:
        brief_next += timedelta(days=1)
    
    # Daily Report
    report_hour, report_minute = parse_time(SCHED_REPORT_UTC)
    report_next = now.replace(hour=report_hour, minute=report_minute, second=0, microsecond=0)
    if report_next <= now:
        report_next += timedelta(days=1)
    
    # Self-Heal (next 6-hour interval)
    if 'self_heal' in last_run:
        selfheal_next = last_run['self_heal'] + timedelta(hours=SCHED_SELFHEAL_EVERY_HOURS)
    else:
        selfheal_next = now + timedelta(hours=SCHED_SELFHEAL_EVERY_HOURS)
    
    return {
        'brief': brief_next.isoformat() + 'Z',
        'report': report_next.isoformat() + 'Z',
        'selfheal': selfheal_next.isoformat() + 'Z'
    }

def run_production_alerts():
    """Run production alerts monitoring"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/production_alerts.py'], check=False, timeout=30)
    except Exception as e:
        log_event('production_alerts_error', {'error': str(e)})

def run_scheduled_tasks():
    """Check and run scheduled tasks"""
    
    # 0) Health Probe at 07:55 UTC daily (before CEO Brief)
    if is_time_match(7, 55) and should_run('health_probe'):
        call_api('GET', '/api/system-health', 'health_probe')
        mark_run('health_probe')
    
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
    
    # 4) Predictive Alerts (check every hour)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('predictive_alerts'):
        try:
            import subprocess
            subprocess.run(['python3', 'scripts/predictive_alerts.py'], timeout=15)
            mark_run('predictive_alerts')
        except Exception:
            pass
    
    # ==================== ENTERPRISE EXPANSION TASKS (Phase 33-40) ====================
    
    # 5) Pricing AI Optimization - Daily at 03:00 UTC
    if is_time_match(3, 0) and should_run('pricing_ai'):
        call_api('POST', '/api/pricing/optimize', 'pricing_ai_optimization')
        mark_run('pricing_ai')
    
    # 6) Weekly Audit Pack - Mondays at 00:30 UTC
    now = datetime.utcnow()
    if now.weekday() == 0 and is_time_match(0, 30) and should_run('weekly_audit'):
        call_api('GET', '/api/audit/report', 'weekly_audit_report')
        mark_run('weekly_audit')
    
    # 7) Replica Sync - Every 2 hours
    if should_run('replica_sync'):
        if 'replica_sync' not in last_run or \
           (datetime.utcnow() - last_run['replica_sync']).total_seconds() >= (2 * 3600):
            call_api('POST', '/api/regions/sync', 'replica_sync')
            mark_run('replica_sync')
    
    # 8) AI Ops Brain - Every 12 hours
    if should_run('ops_brain'):
        if 'ops_brain' not in last_run or \
           (datetime.utcnow() - last_run['ops_brain']).total_seconds() >= (12 * 3600):
            call_api('POST', '/api/brain/decide', 'ai_ops_brain')
            mark_run('ops_brain')
    
    # 9) Production Alerts - Every 5 minutes
    if 'production_alerts' not in last_run or \
       (datetime.utcnow() - last_run['production_alerts']).total_seconds() >= (5 * 60):
        run_production_alerts()
        mark_run('production_alerts')

def write_pid():
    """Write PID to file with fsync"""
    pid_file.write_text(str(my_pid))
    # Ensure it's written to disk
    with open(pid_file, 'r') as f:
        os.fsync(f.fileno())

def main():
    """Main scheduler loop with persistence"""
    global running
    
    # Write PID file
    write_pid()
    
    log_event('startup', {
        'ok': True,
        'pid': my_pid,
        'config': {
            'brief_time': SCHED_BRIEF_UTC,
            'report_time': SCHED_REPORT_UTC,
            'selfheal_hours': SCHED_SELFHEAL_EVERY_HOURS,
            'base_url': BASE_URL
        }
    })
    
    print(f"🤖 EchoPilot Executive Scheduler Started (PID: {my_pid})", flush=True)
    print(f"   CEO Brief: {SCHED_BRIEF_UTC} UTC", flush=True)
    print(f"   Daily Report: {SCHED_REPORT_UTC} UTC", flush=True)
    print(f"   Self-Heal: Every {SCHED_SELFHEAL_EVERY_HOURS} hours", flush=True)
    print(f"   Pricing AI: Daily at 03:00 UTC", flush=True)
    print(f"   Audit Pack: Weekly (Monday 00:30 UTC)", flush=True)
    print(f"   Replica Sync: Every 2 hours", flush=True)
    print(f"   AI Ops Brain: Every 12 hours", flush=True)
    print(f"   Production Alerts: Every 5 minutes", flush=True)
    print(f"   Logs: {log_file}", flush=True)
    print(f"   PID: {pid_file}", flush=True)
    print(flush=True)
    
    # Initial self-heal run on startup (in background thread to avoid blocking)
    def startup_self_heal():
        """Run startup self-heal in background"""
        if DASHBOARD_KEY:
            call_api('POST', '/api/self-heal', 'self_heal_startup')
            mark_run('self_heal')
    
    # Start self-heal in background thread so it doesn't block main loop
    if DASHBOARD_KEY:
        heal_thread = threading.Thread(target=startup_self_heal, daemon=True)
        heal_thread.start()
    
    # Main loop with heartbeat
    tick_count = 0
    while True:
        try:
            # Run scheduled tasks
            run_scheduled_tasks()
            
            # Heartbeat tick every minute
            tick_count += 1
            next_runs = calculate_next_run_times()
            log_event('tick', {
                'tick': tick_count,
                'next': next_runs
            })
            
            # Sleep for 60 seconds
            time.sleep(60)
            
        except KeyboardInterrupt:
            log_event('shutdown', {'ok': True, 'reason': 'KeyboardInterrupt'})
            break
        except Exception as e:
            log_event('error', {'ok': False, 'error': str(e), 'tick': tick_count})
            # Keep running despite errors
            time.sleep(60)
    
    cleanup_pid_file()
    log_event('stopped', {'ok': True, 'ticks': tick_count})
    print("✅ Scheduler stopped", flush=True)

if __name__ == '__main__':
    main()
