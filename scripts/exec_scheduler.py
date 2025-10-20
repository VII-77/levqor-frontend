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
    """Run production alerts monitoring - webhook failures, payment errors, revenue dips"""
    import subprocess
    try:
        result = subprocess.run(['python3', 'scripts/production_alerts.py'], 
                              capture_output=True, text=True, check=False, timeout=30)
        if result.returncode == 0:
            log_event('production_alerts', {'ok': True, 'status': 'alerts_checked'})
        else:
            log_event('production_alerts_error', {'ok': False, 'error': result.stderr})
    except Exception as e:
        log_event('production_alerts_error', {'error': str(e)})

def run_slo_guard():
    """Run SLO compliance guard - Phase 51"""
    import subprocess
    try:
        result = subprocess.run(['python3', 'scripts/slo_guard.py'], 
                              capture_output=True, text=True, check=False, timeout=30)
        if result.returncode == 0:
            log_event('alerts_run_slo', {'ok': True, 'status': 'slo_checked'})
        else:
            log_event('slo_guard_error', {'ok': False, 'error': result.stderr})
    except Exception as e:
        log_event('slo_guard_error', {'error': str(e)})

def run_ops_sentinel():
    """Run ops sentinel system watchdog"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/ops_sentinel.py'], check=False, timeout=30)
    except Exception as e:
        log_event('ops_sentinel_error', {'error': str(e)})

def run_revenue_intelligence():
    """Run revenue intelligence analysis"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/revenue_intelligence.py'], check=False, timeout=60)
    except Exception as e:
        log_event('revenue_intelligence_error', {'error': str(e)})

def run_finance_reconcile():
    """Run finance reconciliation"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/finance_reconciler.py'], check=False, timeout=60)
    except Exception as e:
        log_event('finance_reconcile_error', {'error': str(e)})

def run_auto_governance():
    """Run auto-governance checks"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/auto_governance.py'], check=False, timeout=30)
    except Exception as e:
        log_event('auto_governance_error', {'error': str(e)})

def run_observability():
    """Run observability snapshot"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/observability_snapshot.py'], check=False, timeout=30)
    except Exception as e:
        log_event('observability_error', {'error': str(e)})

def run_payout_recon():
    """Run payout reconciliation"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/payout_recon.py'], check=False, timeout=60)
    except Exception as e:
        log_event('payout_recon_error', {'error': str(e)})

def run_churn_ai():
    """Run churn risk analysis"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/churn_ai.py'], check=False, timeout=60)
    except Exception as e:
        log_event('churn_ai_error', {'error': str(e)})

def run_slo_guard():
    """Run SLO compliance check"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/slo_guard.py'], check=False, timeout=30)
    except Exception as e:
        log_event('slo_guard_error', {'error': str(e)})

def run_support_inbox():
    """Fetch support inbox digest"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/support_inbox.py'], check=False, timeout=30)
    except Exception as e:
        log_event('support_inbox_error', {'error': str(e)})

def run_cost_tracker():
    """Run infrastructure cost tracking"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/cost_tracker.py'], check=False, timeout=30)
    except Exception as e:
        log_event('cost_tracker_error', {'error': str(e)})

def run_incident_scan():
    """Scan for incidents"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/incident_autoresponder.py'], check=False, timeout=30)
    except Exception as e:
        log_event('incident_scan_error', {'error': str(e)})

def run_payment_recon_nightly():
    """Run nightly payment reconciliation backup"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/payment_recon_nightly.py'], check=False, timeout=30)
    except Exception as e:
        log_event('payment_recon_nightly_error', {'error': str(e)})

def run_slo_monitor():
    """Run SLO monitoring"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/slo_monitor.py'], check=False, timeout=30)
    except Exception as e:
        log_event('slo_monitor_error', {'error': str(e)})

def run_daily_backup():
    """Run daily backup"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/backup_daily.py'], check=False, timeout=60)
    except Exception as e:
        log_event('daily_backup_error', {'error': str(e)})

def run_predictive_scaling():
    """Run predictive scaling analysis"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/predictive_scaling.py'], check=False, timeout=30)
    except Exception as e:
        log_event('predictive_scaling_error', {'error': str(e)})

def run_smart_retries():
    """Run smart retries test"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/smart_retries.py'], check=False, timeout=30)
    except Exception as e:
        log_event('smart_retries_error', {'error': str(e)})

def run_email_reports():
    """Generate daily email reports"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/email_reports_v2.py'], check=False, timeout=30)
    except Exception as e:
        log_event('email_reports_error', {'error': str(e)})

def run_ai_incident_summaries():
    """Generate AI incident summaries"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/ai_incident_summaries.py'], check=False, timeout=30)
    except Exception as e:
        log_event('ai_incident_summaries_error', {'error': str(e)})

def run_slo_budget():
    """Compute SLO budget and error rates"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/slo_budget.py'], check=False, timeout=30)
    except Exception as e:
        log_event('slo_budget_error', {'error': str(e)})

def run_incident_pager():
    """Run incident pager check"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/incident_pager.py'], check=False, timeout=30)
    except Exception as e:
        log_event('incident_pager_error', {'error': str(e)})

def run_cost_guardrails():
    """Check cost guardrails"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/cost_guardrails.py'], check=False, timeout=30)
    except Exception as e:
        log_event('cost_guardrails_error', {'error': str(e)})

def run_autoscale_workers():
    """Run autoscale decision engine"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/autoscale_workers.py'], check=False, timeout=30)
    except Exception as e:
        log_event('autoscale_workers_error', {'error': str(e)})

# ==================== PHASE 81-100 RUN FUNCTIONS ====================

def run_dr_backups():
    """Create DR backups"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/dr_backups.py'], check=False, timeout=60)
    except Exception as e:
        log_event('dr_backups_error', {'error': str(e)})

def run_finops_reports():
    """Generate FinOps reports"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/finops_reports.py'], check=False, timeout=30)
    except Exception as e:
        log_event('finops_reports_error', {'error': str(e)})

def run_warehouse_sync():
    """Sync to data warehouse"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/warehouse_sync.py'], check=False, timeout=60)
    except Exception as e:
        log_event('warehouse_sync_error', {'error': str(e)})

def run_analytics_hub():
    """Run analytics hub"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/analytics_hub.py'], check=False, timeout=30)
    except Exception as e:
        log_event('analytics_hub_error', {'error': str(e)})

def run_predictive_maint():
    """Run predictive maintenance"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/predictive_maintenance.py'], check=False, timeout=30)
    except Exception as e:
        log_event('predictive_maint_error', {'error': str(e)})

def run_compliance_v2():
    """Check compliance status"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/compliance_suite_v2.py'], check=False, timeout=30)
    except Exception as e:
        log_event('compliance_v2_error', {'error': str(e)})

def run_governance_ai():
    """Get governance AI recommendations"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/governance_ai.py'], check=False, timeout=30)
    except Exception as e:
        log_event('governance_ai_error', {'error': str(e)})

def run_anomaly_detect():
    """Detect anomalies"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/anomaly_detection.py'], check=False, timeout=30)
    except Exception as e:
        log_event('anomaly_detect_error', {'error': str(e)})

def run_security_scan():
    """Run security scan"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/security_scan.py'], check=False, timeout=60)
    except Exception as e:
        log_event('security_scan_error', {'error': str(e)})

def run_training_audit():
    """Run AI training audit"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/training_audit.py'], check=False, timeout=30)
    except Exception as e:
        log_event('training_audit_error', {'error': str(e)})

def run_adaptive_optimizer():
    """Run adaptive optimizer"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/adaptive_optimizer.py'], check=False, timeout=30)
    except Exception as e:
        log_event('adaptive_optimizer_error', {'error': str(e)})

def run_self_heal_v2():
    """Run self-heal v2"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/self_heal_v2.py'], check=False, timeout=30)
    except Exception as e:
        log_event('self_heal_v2_error', {'error': str(e)})

def run_continuous_learning():
    """Run continuous learning engine"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/continuous_learning.py'], check=False, timeout=30)
    except Exception as e:
        log_event('continuous_learning_error', {'error': str(e)})

def run_enterprise_validator():
    """Run enterprise validation"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/enterprise_validator.py'], check=False, timeout=60)
    except Exception as e:
        log_event('enterprise_validator_error', {'error': str(e)})

def run_enterprise_report():
    """Generate enterprise report"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/final_enterprise_report.py'], check=False, timeout=60)
    except Exception as e:
        log_event('enterprise_report_error', {'error': str(e)})

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
    
    # 9b) SLO Guard - Every 15 minutes (Phase 51)
    if 'slo_guard' not in last_run or \
       (datetime.utcnow() - last_run['slo_guard']).total_seconds() >= (15 * 60):
        run_slo_guard()
        mark_run('slo_guard')
    
    # ==================== PHASES 41-50: AUTONOMOUS ENTERPRISE ====================
    
    # 10) Ops Sentinel - Every 3 minutes
    if 'ops_sentinel' not in last_run or \
       (datetime.utcnow() - last_run['ops_sentinel']).total_seconds() >= (3 * 60):
        run_ops_sentinel()
        mark_run('ops_sentinel')
    
    # 11) Revenue Intelligence - Every 30 minutes
    if 'revenue_intelligence' not in last_run or \
       (datetime.utcnow() - last_run['revenue_intelligence']).total_seconds() >= (30 * 60):
        run_revenue_intelligence()
        mark_run('revenue_intelligence')
    
    # 12) Finance Reconciliation - Every 6 hours
    if 'finance_reconcile' not in last_run or \
       (datetime.utcnow() - last_run['finance_reconcile']).total_seconds() >= (6 * 3600):
        run_finance_reconcile()
        mark_run('finance_reconcile')
    
    # 13) Auto-Governance - Every hour
    if is_time_match(datetime.utcnow().hour, 0) and should_run('auto_governance'):
        run_auto_governance()
        mark_run('auto_governance')
    
    # 14) Observability Snapshot - Every hour (Phase 53)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('observability'):
        run_observability()
        mark_run('observability')
    
    # ==================== PHASES 56-60: REPORTS & MONITORING ====================
    
    # 15) Payout Reconciliation - Every 6 hours (Phase 57)
    if 'payout_recon' not in last_run or \
       (datetime.utcnow() - last_run['payout_recon']).total_seconds() >= (6 * 3600):
        run_payout_recon()
        mark_run('payout_recon')
    
    # 16) Churn AI - Every 2 hours (Phase 58)
    if 'churn_ai' not in last_run or \
       (datetime.utcnow() - last_run['churn_ai']).total_seconds() >= (2 * 3600):
        run_churn_ai()
        mark_run('churn_ai')
    
    # 17) SLO Guard - Every 10 minutes (Phase 59)
    if 'slo_guard' not in last_run or \
       (datetime.utcnow() - last_run['slo_guard']).total_seconds() >= (10 * 60):
        run_slo_guard()
        mark_run('slo_guard')
    
    # ==================== PHASES 61-65: SUPPORT & INFRASTRUCTURE ====================
    
    # 18) Support Inbox - Every hour (Phase 61)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('support_inbox'):
        run_support_inbox()
        mark_run('support_inbox')
    
    # 19) Cost Tracker - Daily at 01:10 UTC (Phase 64)
    if is_time_match(1, 10) and should_run('cost_tracker'):
        run_cost_tracker()
        mark_run('cost_tracker')
    
    # 20) Incident Scanner - Every 5 minutes (Phase 65)
    if 'incident_scan' not in last_run or \
       (datetime.utcnow() - last_run['incident_scan']).total_seconds() >= (5 * 60):
        run_incident_scan()
        mark_run('incident_scan')
    
    # ==================== PHASES 66-70: PAYMENTS, MONITORING & BACKUPS ====================
    
    # 21) Payment Recon Nightly - Daily at 23:50 UTC (Phase 67)
    if is_time_match(23, 50) and should_run('payment_recon_nightly'):
        run_payment_recon_nightly()
        mark_run('payment_recon_nightly')
    
    # 22) SLO Monitor - Every hour (Phase 68)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('slo_monitor'):
        run_slo_monitor()
        mark_run('slo_monitor')
    
    # 23) Daily Backup - Daily at 00:30 UTC (Phase 70)
    if is_time_match(0, 30) and should_run('daily_backup'):
        run_daily_backup()
        mark_run('daily_backup')
    
    # ==================== PHASES 71-75: PREDICTIVE, SMART RETRIES & AI ====================
    
    # 24) Predictive Scaling - Every hour (Phase 71)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('predictive_scaling'):
        run_predictive_scaling()
        mark_run('predictive_scaling')
    
    # 25) AI Incident Summaries - Every 30 minutes (Phase 75)
    if 'ai_incident_summaries' not in last_run or \
       (datetime.utcnow() - last_run['ai_incident_summaries']).total_seconds() >= (30 * 60):
        run_ai_incident_summaries()
        mark_run('ai_incident_summaries')
    
    # 26) Smart Retries Test - Every 6 hours (Phase 72)
    if 'smart_retries' not in last_run or \
       (datetime.utcnow() - last_run['smart_retries']).total_seconds() >= (6 * 3600):
        run_smart_retries()
        mark_run('smart_retries')
    
    # 27) Email Reports - Daily at 07:45 UTC (Phase 73)
    if is_time_match(7, 45) and should_run('email_reports'):
        run_email_reports()
        mark_run('email_reports')
    
    # ==================== PHASES 76-80: SLOs, PAGER, PORTAL, COSTS & SCALE ====================
    
    # 28) SLO Budget - Every 15 minutes (Phase 76)
    if 'slo_budget' not in last_run or \
       (datetime.utcnow() - last_run['slo_budget']).total_seconds() >= (15 * 60):
        run_slo_budget()
        mark_run('slo_budget')
    
    # 29) Incident Pager - Every 5 minutes (Phase 77)
    if 'incident_pager' not in last_run or \
       (datetime.utcnow() - last_run['incident_pager']).total_seconds() >= (5 * 60):
        run_incident_pager()
        mark_run('incident_pager')
    
    # 30) Cost Guardrails - Every hour (Phase 79)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('cost_guardrails'):
        run_cost_guardrails()
        mark_run('cost_guardrails')
    
    # 31) Autoscale Workers - Every 10 minutes (Phase 80)
    if 'autoscale_workers' not in last_run or \
       (datetime.utcnow() - last_run['autoscale_workers']).total_seconds() >= (10 * 60):
        run_autoscale_workers()
        mark_run('autoscale_workers')
    
    # ==================== PHASES 81-100: ENTERPRISE EXPANSION FINALE ====================
    
    # 32) DR Backups - Daily at 02:30 UTC (Phase 83)
    if is_time_match(2, 30) and should_run('dr_backups'):
        run_dr_backups()
        mark_run('dr_backups')
    
    # 33) FinOps Reports - Daily at 04:00 UTC (Phase 85)
    if is_time_match(4, 0) and should_run('finops_reports'):
        run_finops_reports()
        mark_run('finops_reports')
    
    # 34) Warehouse Sync - Every 6 hours (Phase 86)
    if 'warehouse_sync' not in last_run or \
       (datetime.utcnow() - last_run['warehouse_sync']).total_seconds() >= (6 * 3600):
        run_warehouse_sync()
        mark_run('warehouse_sync')
    
    # 35) Analytics Hub - Every hour (Phase 87)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('analytics_hub'):
        run_analytics_hub()
        mark_run('analytics_hub')
    
    # 36) Predictive Maintenance - Every 2 hours (Phase 88)
    if 'predictive_maint' not in last_run or \
       (datetime.utcnow() - last_run['predictive_maint']).total_seconds() >= (2 * 3600):
        run_predictive_maint()
        mark_run('predictive_maint')
    
    # 37) Compliance V2 - Daily at 05:00 UTC (Phase 89)
    if is_time_match(5, 0) and should_run('compliance_v2'):
        run_compliance_v2()
        mark_run('compliance_v2')
    
    # 38) Governance AI - Every 3 hours (Phase 90)
    if 'governance_ai' not in last_run or \
       (datetime.utcnow() - last_run['governance_ai']).total_seconds() >= (3 * 3600):
        run_governance_ai()
        mark_run('governance_ai')
    
    # 39) Anomaly Detection - Every 30 minutes (Phase 93)
    if 'anomaly_detect' not in last_run or \
       (datetime.utcnow() - last_run['anomaly_detect']).total_seconds() >= (30 * 60):
        run_anomaly_detect()
        mark_run('anomaly_detect')
    
    # 40) Security Scan - Daily at 06:00 UTC (Phase 95)
    if is_time_match(6, 0) and should_run('security_scan'):
        run_security_scan()
        mark_run('security_scan')
    
    # 41) Training Audit - Weekly (Monday 02:00 UTC) (Phase 97)
    if now.weekday() == 0 and is_time_match(2, 0) and should_run('training_audit'):
        run_training_audit()
        mark_run('training_audit')
    
    # 42) Adaptive Optimizer - Every 4 hours (Phase 98)
    if 'adaptive_optimizer' not in last_run or \
       (datetime.utcnow() - last_run['adaptive_optimizer']).total_seconds() >= (4 * 3600):
        run_adaptive_optimizer()
        mark_run('adaptive_optimizer')
    
    # 43) Self-Heal V2 - Every 6 hours (Phase 99)
    if 'self_heal_v2' not in last_run or \
       (datetime.utcnow() - last_run['self_heal_v2']).total_seconds() >= (6 * 3600):
        run_self_heal_v2()
        mark_run('self_heal_v2')
    
    # 44) Continuous Learning - Every 12 hours (Phase 100)
    if 'continuous_learning' not in last_run or \
       (datetime.utcnow() - last_run['continuous_learning']).total_seconds() >= (12 * 3600):
        run_continuous_learning()
        mark_run('continuous_learning')
    
    # 45) Enterprise Validator - Every hour (Phase 100B)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('enterprise_validator'):
        run_enterprise_validator()
        mark_run('enterprise_validator')
    
    # 46) Enterprise Report - Daily at 08:00 UTC (Phase 100C)
    if is_time_match(8, 0) and should_run('enterprise_report'):
        run_enterprise_report()
        mark_run('enterprise_report')
    
    # ==================== PHASE 101: OPERATIONAL DASHBOARD ====================
    
    # 47) Governance Loop - Every 15 minutes (Phase 101)
    if 'governance_loop' not in last_run or \
       (datetime.utcnow() - last_run['governance_loop']).total_seconds() >= (15 * 60):
        run_governance_loop()
        mark_run('governance_loop')
    
    # 48) Predictive Maintenance - Every hour (Phase 101)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('predictive_maintenance'):
        run_predictive_maintenance()
        mark_run('predictive_maintenance')

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
    print(f"   --- Phases 41-50: Autonomous Enterprise ---", flush=True)
    print(f"   Ops Sentinel: Every 3 minutes", flush=True)
    print(f"   Revenue Intelligence: Every 30 minutes", flush=True)
    print(f"   Finance Reconcile: Every 6 hours", flush=True)
    print(f"   Auto-Governance: Every hour", flush=True)
    print(f"   --- Phases 51-55: Post-Live Hardening ---", flush=True)
    print(f"   Observability Snapshot: Every hour", flush=True)
    print(f"   --- Phases 56-60: Reports & Monitoring ---", flush=True)
    print(f"   Payout Reconciliation: Every 6 hours", flush=True)
    print(f"   Churn AI: Every 2 hours", flush=True)
    print(f"   SLO Guard: Every 10 minutes", flush=True)
    print(f"   --- Phases 61-65: Support & Infrastructure ---", flush=True)
    print(f"   Support Inbox: Every hour", flush=True)
    print(f"   Cost Tracker: Daily at 01:10 UTC", flush=True)
    print(f"   Incident Scanner: Every 5 minutes", flush=True)
    print(f"   --- Phases 66-70: Payments, Monitoring & Backups ---", flush=True)
    print(f"   Payment Recon Nightly: Daily at 23:50 UTC", flush=True)
    print(f"   SLO Monitor: Every hour", flush=True)
    print(f"   Daily Backup: Daily at 00:30 UTC", flush=True)
    print(f"   --- Phases 71-75: Predictive, Smart Retries & AI ---", flush=True)
    print(f"   Predictive Scaling: Every hour", flush=True)
    print(f"   AI Incident Summaries: Every 30 minutes", flush=True)
    print(f"   Smart Retries Test: Every 6 hours", flush=True)
    print(f"   Email Reports: Daily at 07:45 UTC", flush=True)
    print(f"   --- Phases 76-80: SLOs, Pager, Portal, Costs & Scale ---", flush=True)
    print(f"   SLO Budget: Every 15 minutes", flush=True)
    print(f"   Incident Pager: Every 5 minutes", flush=True)
    print(f"   Cost Guardrails: Every hour", flush=True)
    print(f"   Autoscale Workers: Every 10 minutes", flush=True)
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

def run_governance_loop():
    """Run governance loop (SLO compliance check) - Phase 101"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/governance_loop.py'], check=False, timeout=30)
    except Exception as e:
        log_event('governance_loop_error', {'error': str(e)})

def run_predictive_maintenance():
    """Run predictive maintenance AI - Phase 101"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/predictive_maintenance.py'], check=False, timeout=60)
    except Exception as e:
        log_event('predictive_maintenance_error', {'error': str(e)})
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
    """Run production alerts monitoring - webhook failures, payment errors, revenue dips"""
    import subprocess
    try:
        result = subprocess.run(['python3', 'scripts/production_alerts.py'], 
                              capture_output=True, text=True, check=False, timeout=30)
        if result.returncode == 0:
            log_event('production_alerts', {'ok': True, 'status': 'alerts_checked'})
        else:
            log_event('production_alerts_error', {'ok': False, 'error': result.stderr})
    except Exception as e:
        log_event('production_alerts_error', {'error': str(e)})

def run_slo_guard():
    """Run SLO compliance guard - Phase 51"""
    import subprocess
    try:
        result = subprocess.run(['python3', 'scripts/slo_guard.py'], 
                              capture_output=True, text=True, check=False, timeout=30)
        if result.returncode == 0:
            log_event('alerts_run_slo', {'ok': True, 'status': 'slo_checked'})
        else:
            log_event('slo_guard_error', {'ok': False, 'error': result.stderr})
    except Exception as e:
        log_event('slo_guard_error', {'error': str(e)})

def run_ops_sentinel():
    """Run ops sentinel system watchdog"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/ops_sentinel.py'], check=False, timeout=30)
    except Exception as e:
        log_event('ops_sentinel_error', {'error': str(e)})

def run_revenue_intelligence():
    """Run revenue intelligence analysis"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/revenue_intelligence.py'], check=False, timeout=60)
    except Exception as e:
        log_event('revenue_intelligence_error', {'error': str(e)})

def run_finance_reconcile():
    """Run finance reconciliation"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/finance_reconciler.py'], check=False, timeout=60)
    except Exception as e:
        log_event('finance_reconcile_error', {'error': str(e)})

def run_auto_governance():
    """Run auto-governance checks"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/auto_governance.py'], check=False, timeout=30)
    except Exception as e:
        log_event('auto_governance_error', {'error': str(e)})

def run_observability():
    """Run observability snapshot"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/observability_snapshot.py'], check=False, timeout=30)
    except Exception as e:
        log_event('observability_error', {'error': str(e)})

def run_payout_recon():
    """Run payout reconciliation"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/payout_recon.py'], check=False, timeout=60)
    except Exception as e:
        log_event('payout_recon_error', {'error': str(e)})

def run_churn_ai():
    """Run churn risk analysis"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/churn_ai.py'], check=False, timeout=60)
    except Exception as e:
        log_event('churn_ai_error', {'error': str(e)})

def run_slo_guard():
    """Run SLO compliance check"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/slo_guard.py'], check=False, timeout=30)
    except Exception as e:
        log_event('slo_guard_error', {'error': str(e)})

def run_support_inbox():
    """Fetch support inbox digest"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/support_inbox.py'], check=False, timeout=30)
    except Exception as e:
        log_event('support_inbox_error', {'error': str(e)})

def run_cost_tracker():
    """Run infrastructure cost tracking"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/cost_tracker.py'], check=False, timeout=30)
    except Exception as e:
        log_event('cost_tracker_error', {'error': str(e)})

def run_incident_scan():
    """Scan for incidents"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/incident_autoresponder.py'], check=False, timeout=30)
    except Exception as e:
        log_event('incident_scan_error', {'error': str(e)})

def run_payment_recon_nightly():
    """Run nightly payment reconciliation backup"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/payment_recon_nightly.py'], check=False, timeout=30)
    except Exception as e:
        log_event('payment_recon_nightly_error', {'error': str(e)})

def run_slo_monitor():
    """Run SLO monitoring"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/slo_monitor.py'], check=False, timeout=30)
    except Exception as e:
        log_event('slo_monitor_error', {'error': str(e)})

def run_daily_backup():
    """Run daily backup"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/backup_daily.py'], check=False, timeout=60)
    except Exception as e:
        log_event('daily_backup_error', {'error': str(e)})

def run_predictive_scaling():
    """Run predictive scaling analysis"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/predictive_scaling.py'], check=False, timeout=30)
    except Exception as e:
        log_event('predictive_scaling_error', {'error': str(e)})

def run_smart_retries():
    """Run smart retries test"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/smart_retries.py'], check=False, timeout=30)
    except Exception as e:
        log_event('smart_retries_error', {'error': str(e)})

def run_email_reports():
    """Generate daily email reports"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/email_reports_v2.py'], check=False, timeout=30)
    except Exception as e:
        log_event('email_reports_error', {'error': str(e)})

def run_ai_incident_summaries():
    """Generate AI incident summaries"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/ai_incident_summaries.py'], check=False, timeout=30)
    except Exception as e:
        log_event('ai_incident_summaries_error', {'error': str(e)})

def run_slo_budget():
    """Compute SLO budget and error rates"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/slo_budget.py'], check=False, timeout=30)
    except Exception as e:
        log_event('slo_budget_error', {'error': str(e)})

def run_incident_pager():
    """Run incident pager check"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/incident_pager.py'], check=False, timeout=30)
    except Exception as e:
        log_event('incident_pager_error', {'error': str(e)})

def run_cost_guardrails():
    """Check cost guardrails"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/cost_guardrails.py'], check=False, timeout=30)
    except Exception as e:
        log_event('cost_guardrails_error', {'error': str(e)})

def run_autoscale_workers():
    """Run autoscale decision engine"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/autoscale_workers.py'], check=False, timeout=30)
    except Exception as e:
        log_event('autoscale_workers_error', {'error': str(e)})

# ==================== PHASE 81-100 RUN FUNCTIONS ====================

def run_dr_backups():
    """Create DR backups"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/dr_backups.py'], check=False, timeout=60)
    except Exception as e:
        log_event('dr_backups_error', {'error': str(e)})

def run_finops_reports():
    """Generate FinOps reports"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/finops_reports.py'], check=False, timeout=30)
    except Exception as e:
        log_event('finops_reports_error', {'error': str(e)})

def run_warehouse_sync():
    """Sync to data warehouse"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/warehouse_sync.py'], check=False, timeout=60)
    except Exception as e:
        log_event('warehouse_sync_error', {'error': str(e)})

def run_analytics_hub():
    """Run analytics hub"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/analytics_hub.py'], check=False, timeout=30)
    except Exception as e:
        log_event('analytics_hub_error', {'error': str(e)})

def run_predictive_maint():
    """Run predictive maintenance"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/predictive_maintenance.py'], check=False, timeout=30)
    except Exception as e:
        log_event('predictive_maint_error', {'error': str(e)})

def run_compliance_v2():
    """Check compliance status"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/compliance_suite_v2.py'], check=False, timeout=30)
    except Exception as e:
        log_event('compliance_v2_error', {'error': str(e)})

def run_governance_ai():
    """Get governance AI recommendations"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/governance_ai.py'], check=False, timeout=30)
    except Exception as e:
        log_event('governance_ai_error', {'error': str(e)})

def run_anomaly_detect():
    """Detect anomalies"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/anomaly_detection.py'], check=False, timeout=30)
    except Exception as e:
        log_event('anomaly_detect_error', {'error': str(e)})

def run_security_scan():
    """Run security scan"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/security_scan.py'], check=False, timeout=60)
    except Exception as e:
        log_event('security_scan_error', {'error': str(e)})

def run_training_audit():
    """Run AI training audit"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/training_audit.py'], check=False, timeout=30)
    except Exception as e:
        log_event('training_audit_error', {'error': str(e)})

def run_adaptive_optimizer():
    """Run adaptive optimizer"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/adaptive_optimizer.py'], check=False, timeout=30)
    except Exception as e:
        log_event('adaptive_optimizer_error', {'error': str(e)})

def run_self_heal_v2():
    """Run self-heal v2"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/self_heal_v2.py'], check=False, timeout=30)
    except Exception as e:
        log_event('self_heal_v2_error', {'error': str(e)})

def run_continuous_learning():
    """Run continuous learning engine"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/continuous_learning.py'], check=False, timeout=30)
    except Exception as e:
        log_event('continuous_learning_error', {'error': str(e)})

def run_enterprise_validator():
    """Run enterprise validation"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/enterprise_validator.py'], check=False, timeout=60)
    except Exception as e:
        log_event('enterprise_validator_error', {'error': str(e)})

def run_enterprise_report():
    """Generate enterprise report"""
    import subprocess
    try:
        subprocess.run(['python3', 'scripts/final_enterprise_report.py'], check=False, timeout=60)
    except Exception as e:
        log_event('enterprise_report_error', {'error': str(e)})

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
    
    # 9b) SLO Guard - Every 15 minutes (Phase 51)
    if 'slo_guard' not in last_run or \
       (datetime.utcnow() - last_run['slo_guard']).total_seconds() >= (15 * 60):
        run_slo_guard()
        mark_run('slo_guard')
    
    # ==================== PHASES 41-50: AUTONOMOUS ENTERPRISE ====================
    
    # 10) Ops Sentinel - Every 3 minutes
    if 'ops_sentinel' not in last_run or \
       (datetime.utcnow() - last_run['ops_sentinel']).total_seconds() >= (3 * 60):
        run_ops_sentinel()
        mark_run('ops_sentinel')
    
    # 11) Revenue Intelligence - Every 30 minutes
    if 'revenue_intelligence' not in last_run or \
       (datetime.utcnow() - last_run['revenue_intelligence']).total_seconds() >= (30 * 60):
        run_revenue_intelligence()
        mark_run('revenue_intelligence')
    
    # 12) Finance Reconciliation - Every 6 hours
    if 'finance_reconcile' not in last_run or \
       (datetime.utcnow() - last_run['finance_reconcile']).total_seconds() >= (6 * 3600):
        run_finance_reconcile()
        mark_run('finance_reconcile')
    
    # 13) Auto-Governance - Every hour
    if is_time_match(datetime.utcnow().hour, 0) and should_run('auto_governance'):
        run_auto_governance()
        mark_run('auto_governance')
    
    # 14) Observability Snapshot - Every hour (Phase 53)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('observability'):
        run_observability()
        mark_run('observability')
    
    # ==================== PHASES 56-60: REPORTS & MONITORING ====================
    
    # 15) Payout Reconciliation - Every 6 hours (Phase 57)
    if 'payout_recon' not in last_run or \
       (datetime.utcnow() - last_run['payout_recon']).total_seconds() >= (6 * 3600):
        run_payout_recon()
        mark_run('payout_recon')
    
    # 16) Churn AI - Every 2 hours (Phase 58)
    if 'churn_ai' not in last_run or \
       (datetime.utcnow() - last_run['churn_ai']).total_seconds() >= (2 * 3600):
        run_churn_ai()
        mark_run('churn_ai')
    
    # 17) SLO Guard - Every 10 minutes (Phase 59)
    if 'slo_guard' not in last_run or \
       (datetime.utcnow() - last_run['slo_guard']).total_seconds() >= (10 * 60):
        run_slo_guard()
        mark_run('slo_guard')
    
    # ==================== PHASES 61-65: SUPPORT & INFRASTRUCTURE ====================
    
    # 18) Support Inbox - Every hour (Phase 61)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('support_inbox'):
        run_support_inbox()
        mark_run('support_inbox')
    
    # 19) Cost Tracker - Daily at 01:10 UTC (Phase 64)
    if is_time_match(1, 10) and should_run('cost_tracker'):
        run_cost_tracker()
        mark_run('cost_tracker')
    
    # 20) Incident Scanner - Every 5 minutes (Phase 65)
    if 'incident_scan' not in last_run or \
       (datetime.utcnow() - last_run['incident_scan']).total_seconds() >= (5 * 60):
        run_incident_scan()
        mark_run('incident_scan')
    
    # ==================== PHASES 66-70: PAYMENTS, MONITORING & BACKUPS ====================
    
    # 21) Payment Recon Nightly - Daily at 23:50 UTC (Phase 67)
    if is_time_match(23, 50) and should_run('payment_recon_nightly'):
        run_payment_recon_nightly()
        mark_run('payment_recon_nightly')
    
    # 22) SLO Monitor - Every hour (Phase 68)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('slo_monitor'):
        run_slo_monitor()
        mark_run('slo_monitor')
    
    # 23) Daily Backup - Daily at 00:30 UTC (Phase 70)
    if is_time_match(0, 30) and should_run('daily_backup'):
        run_daily_backup()
        mark_run('daily_backup')
    
    # ==================== PHASES 71-75: PREDICTIVE, SMART RETRIES & AI ====================
    
    # 24) Predictive Scaling - Every hour (Phase 71)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('predictive_scaling'):
        run_predictive_scaling()
        mark_run('predictive_scaling')
    
    # 25) AI Incident Summaries - Every 30 minutes (Phase 75)
    if 'ai_incident_summaries' not in last_run or \
       (datetime.utcnow() - last_run['ai_incident_summaries']).total_seconds() >= (30 * 60):
        run_ai_incident_summaries()
        mark_run('ai_incident_summaries')
    
    # 26) Smart Retries Test - Every 6 hours (Phase 72)
    if 'smart_retries' not in last_run or \
       (datetime.utcnow() - last_run['smart_retries']).total_seconds() >= (6 * 3600):
        run_smart_retries()
        mark_run('smart_retries')
    
    # 27) Email Reports - Daily at 07:45 UTC (Phase 73)
    if is_time_match(7, 45) and should_run('email_reports'):
        run_email_reports()
        mark_run('email_reports')
    
    # ==================== PHASES 76-80: SLOs, PAGER, PORTAL, COSTS & SCALE ====================
    
    # 28) SLO Budget - Every 15 minutes (Phase 76)
    if 'slo_budget' not in last_run or \
       (datetime.utcnow() - last_run['slo_budget']).total_seconds() >= (15 * 60):
        run_slo_budget()
        mark_run('slo_budget')
    
    # 29) Incident Pager - Every 5 minutes (Phase 77)
    if 'incident_pager' not in last_run or \
       (datetime.utcnow() - last_run['incident_pager']).total_seconds() >= (5 * 60):
        run_incident_pager()
        mark_run('incident_pager')
    
    # 30) Cost Guardrails - Every hour (Phase 79)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('cost_guardrails'):
        run_cost_guardrails()
        mark_run('cost_guardrails')
    
    # 31) Autoscale Workers - Every 10 minutes (Phase 80)
    if 'autoscale_workers' not in last_run or \
       (datetime.utcnow() - last_run['autoscale_workers']).total_seconds() >= (10 * 60):
        run_autoscale_workers()
        mark_run('autoscale_workers')
    
    # ==================== PHASES 81-100: ENTERPRISE EXPANSION FINALE ====================
    
    # 32) DR Backups - Daily at 02:30 UTC (Phase 83)
    if is_time_match(2, 30) and should_run('dr_backups'):
        run_dr_backups()
        mark_run('dr_backups')
    
    # 33) FinOps Reports - Daily at 04:00 UTC (Phase 85)
    if is_time_match(4, 0) and should_run('finops_reports'):
        run_finops_reports()
        mark_run('finops_reports')
    
    # 34) Warehouse Sync - Every 6 hours (Phase 86)
    if 'warehouse_sync' not in last_run or \
       (datetime.utcnow() - last_run['warehouse_sync']).total_seconds() >= (6 * 3600):
        run_warehouse_sync()
        mark_run('warehouse_sync')
    
    # 35) Analytics Hub - Every hour (Phase 87)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('analytics_hub'):
        run_analytics_hub()
        mark_run('analytics_hub')
    
    # 36) Predictive Maintenance - Every 2 hours (Phase 88)
    if 'predictive_maint' not in last_run or \
       (datetime.utcnow() - last_run['predictive_maint']).total_seconds() >= (2 * 3600):
        run_predictive_maint()
        mark_run('predictive_maint')
    
    # 37) Compliance V2 - Daily at 05:00 UTC (Phase 89)
    if is_time_match(5, 0) and should_run('compliance_v2'):
        run_compliance_v2()
        mark_run('compliance_v2')
    
    # 38) Governance AI - Every 3 hours (Phase 90)
    if 'governance_ai' not in last_run or \
       (datetime.utcnow() - last_run['governance_ai']).total_seconds() >= (3 * 3600):
        run_governance_ai()
        mark_run('governance_ai')
    
    # 39) Anomaly Detection - Every 30 minutes (Phase 93)
    if 'anomaly_detect' not in last_run or \
       (datetime.utcnow() - last_run['anomaly_detect']).total_seconds() >= (30 * 60):
        run_anomaly_detect()
        mark_run('anomaly_detect')
    
    # 40) Security Scan - Daily at 06:00 UTC (Phase 95)
    if is_time_match(6, 0) and should_run('security_scan'):
        run_security_scan()
        mark_run('security_scan')
    
    # 41) Training Audit - Weekly (Monday 02:00 UTC) (Phase 97)
    if now.weekday() == 0 and is_time_match(2, 0) and should_run('training_audit'):
        run_training_audit()
        mark_run('training_audit')
    
    # 42) Adaptive Optimizer - Every 4 hours (Phase 98)
    if 'adaptive_optimizer' not in last_run or \
       (datetime.utcnow() - last_run['adaptive_optimizer']).total_seconds() >= (4 * 3600):
        run_adaptive_optimizer()
        mark_run('adaptive_optimizer')
    
    # 43) Self-Heal V2 - Every 6 hours (Phase 99)
    if 'self_heal_v2' not in last_run or \
       (datetime.utcnow() - last_run['self_heal_v2']).total_seconds() >= (6 * 3600):
        run_self_heal_v2()
        mark_run('self_heal_v2')
    
    # 44) Continuous Learning - Every 12 hours (Phase 100)
    if 'continuous_learning' not in last_run or \
       (datetime.utcnow() - last_run['continuous_learning']).total_seconds() >= (12 * 3600):
        run_continuous_learning()
        mark_run('continuous_learning')
    
    # 45) Enterprise Validator - Every hour (Phase 100B)
    if is_time_match(datetime.utcnow().hour, 0) and should_run('enterprise_validator'):
        run_enterprise_validator()
        mark_run('enterprise_validator')
    
    # 46) Enterprise Report - Daily at 08:00 UTC (Phase 100C)
    if is_time_match(8, 0) and should_run('enterprise_report'):
        run_enterprise_report()
        mark_run('enterprise_report')

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
    print(f"   --- Phases 41-50: Autonomous Enterprise ---", flush=True)
    print(f"   Ops Sentinel: Every 3 minutes", flush=True)
    print(f"   Revenue Intelligence: Every 30 minutes", flush=True)
    print(f"   Finance Reconcile: Every 6 hours", flush=True)
    print(f"   Auto-Governance: Every hour", flush=True)
    print(f"   --- Phases 51-55: Post-Live Hardening ---", flush=True)
    print(f"   Observability Snapshot: Every hour", flush=True)
    print(f"   --- Phases 56-60: Reports & Monitoring ---", flush=True)
    print(f"   Payout Reconciliation: Every 6 hours", flush=True)
    print(f"   Churn AI: Every 2 hours", flush=True)
    print(f"   SLO Guard: Every 10 minutes", flush=True)
    print(f"   --- Phases 61-65: Support & Infrastructure ---", flush=True)
    print(f"   Support Inbox: Every hour", flush=True)
    print(f"   Cost Tracker: Daily at 01:10 UTC", flush=True)
    print(f"   Incident Scanner: Every 5 minutes", flush=True)
    print(f"   --- Phases 66-70: Payments, Monitoring & Backups ---", flush=True)
    print(f"   Payment Recon Nightly: Daily at 23:50 UTC", flush=True)
    print(f"   SLO Monitor: Every hour", flush=True)
    print(f"   Daily Backup: Daily at 00:30 UTC", flush=True)
    print(f"   --- Phases 71-75: Predictive, Smart Retries & AI ---", flush=True)
    print(f"   Predictive Scaling: Every hour", flush=True)
    print(f"   AI Incident Summaries: Every 30 minutes", flush=True)
    print(f"   Smart Retries Test: Every 6 hours", flush=True)
    print(f"   Email Reports: Daily at 07:45 UTC", flush=True)
    print(f"   --- Phases 76-80: SLOs, Pager, Portal, Costs & Scale ---", flush=True)
    print(f"   SLO Budget: Every 15 minutes", flush=True)
    print(f"   Incident Pager: Every 5 minutes", flush=True)
    print(f"   Cost Guardrails: Every hour", flush=True)
    print(f"   Autoscale Workers: Every 10 minutes", flush=True)
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
