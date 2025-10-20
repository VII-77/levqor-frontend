#!/usr/bin/env python3
"""
Telemetry Collector - Aggregates real-time metrics from all autonomous systems
Used by /api/ops/telemetry endpoint for Operational Dashboard
"""
import json
import os
import glob
import psutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

def get_scheduler_health():
    """Get scheduler health status"""
    try:
        pid_file = Path('logs/scheduler.pid')
        if not pid_file.exists():
            return {"status": "down", "error": "PID file missing"}
        
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        # Check if process exists
        try:
            os.kill(pid, 0)
            process_alive = True
        except OSError:
            return {"status": "down", "error": f"Process {pid} not running"}
        
        # Check heartbeat age
        scheduler_log = Path('logs/scheduler.log')
        if scheduler_log.exists():
            with open(scheduler_log, 'r') as f:
                lines = f.readlines()
                if lines:
                    try:
                        last_line = json.loads(lines[-1])
                        if 'ts' in last_line:
                            ts = datetime.fromisoformat(last_line['ts'].replace('Z', '+00:00'))
                            age_seconds = (datetime.now(timezone.utc) - ts).total_seconds()
                            
                            if age_seconds < 60:
                                return {
                                    "status": "healthy",
                                    "pid": pid,
                                    "heartbeat_age_seconds": round(age_seconds, 1),
                                    "last_tick": last_line.get('tick', 0)
                                }
                            else:
                                return {
                                    "status": "stale",
                                    "pid": pid,
                                    "heartbeat_age_seconds": round(age_seconds, 1),
                                    "warning": "Heartbeat stale"
                                }
                    except:
                        pass
        
        return {"status": "unknown", "pid": pid}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_finance_metrics():
    """Get live finance metrics"""
    try:
        # Read recent finance logs
        finance_log = Path('logs/finance.ndjson')
        if not finance_log.exists():
            return {"status": "no_data", "total_revenue": 0, "failed_payments": 0}
        
        with open(finance_log, 'r') as f:
            lines = f.readlines()[-100:]  # Last 100 entries
        
        total_revenue = 0
        failed_payments = 0
        revenue_24h = 0
        cutoff_24h = datetime.now(timezone.utc) - timedelta(hours=24)
        
        for line in lines:
            try:
                entry = json.loads(line)
                if entry.get('event') == 'payment_success':
                    amount = entry.get('amount_usd', 0)
                    total_revenue += amount
                    
                    if 'ts' in entry:
                        ts = datetime.fromisoformat(entry['ts'].replace('Z', '+00:00'))
                        if ts > cutoff_24h:
                            revenue_24h += amount
                
                elif entry.get('event') == 'payment_failed':
                    failed_payments += 1
            except:
                continue
        
        return {
            "status": "ok",
            "total_revenue_usd": round(total_revenue, 2),
            "revenue_24h_usd": round(revenue_24h, 2),
            "failed_payments_total": failed_payments,
            "sample_count": len(lines)
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_slo_status():
    """Get current SLO compliance"""
    try:
        slo_report = Path('logs/slo_report.json')
        if not slo_report.exists():
            return {"status": "no_data", "note": "SLO report not yet generated"}
        
        with open(slo_report, 'r') as f:
            data = json.load(f)
        
        return {
            "status": data.get('overall_status', 'UNKNOWN'),
            "breaches": data.get('breaches', []),
            "availability_pct": data.get('slos', {}).get('availability', {}).get('actual_pct', 0),
            "p95_latency_ms": data.get('slos', {}).get('p95_latency', {}).get('actual_ms', 0),
            "webhook_success_pct": data.get('slos', {}).get('webhook_success', {}).get('actual_pct', 0),
            "error_budget_remaining_pct": data.get('slos', {}).get('availability', {}).get('error_budget', {}).get('remaining_pct', 100)
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_security_alerts():
    """Get recent security and threat alerts"""
    try:
        alerts = []
        alert_files = glob.glob('logs/*alert*.ndjson') + glob.glob('logs/production_alerts.ndjson')
        
        cutoff = datetime.now(timezone.utc) - timedelta(hours=1)
        
        for alert_file in alert_files:
            try:
                with open(alert_file, 'r') as f:
                    lines = f.readlines()[-50:]  # Last 50 alerts
                
                for line in lines:
                    try:
                        alert = json.loads(line)
                        if 'ts' in alert:
                            ts = datetime.fromisoformat(alert.get('ts', '').replace('Z', '+00:00'))
                            if ts > cutoff:
                                alerts.append({
                                    "ts": alert.get('ts'),
                                    "severity": alert.get('severity', 'INFO'),
                                    "event": alert.get('event', 'unknown'),
                                    "source": Path(alert_file).name
                                })
                    except:
                        continue
            except:
                continue
        
        # Count by severity
        critical = sum(1 for a in alerts if a.get('severity') == 'CRITICAL')
        warning = sum(1 for a in alerts if a.get('severity') == 'WARNING')
        
        return {
            "status": "ok",
            "alerts_1h": len(alerts),
            "critical": critical,
            "warning": warning,
            "info": len(alerts) - critical - warning,
            "threshold_status": "OK" if len(alerts) < 10 else "HIGH"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_system_metrics():
    """Get system resource metrics"""
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_percent": round(cpu_percent, 1),
            "memory_percent": round(memory.percent, 1),
            "disk_percent": round(disk.percent, 1),
            "status": "healthy" if cpu_percent < 80 and memory.percent < 80 else "stressed"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_automation_count():
    """Count active automation scripts and tasks"""
    try:
        scripts = len(glob.glob('scripts/*.py'))
        
        # Count scheduled tasks from scheduler
        scheduler_funcs = 0
        try:
            with open('scripts/exec_scheduler.py', 'r') as f:
                content = f.read()
                scheduler_funcs = content.count('def run_')
        except:
            pass
        
        return {
            "total_scripts": scripts,
            "scheduled_tasks": scheduler_funcs,
            "status": "ok"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_governance_status():
    """Get governance KPI status"""
    try:
        governance_log = Path('logs/governance_loop.ndjson')
        if not governance_log.exists():
            return {"status": "no_data", "compliance_index": 0}
        
        with open(governance_log, 'r') as f:
            lines = f.readlines()
            if not lines:
                return {"status": "no_data", "compliance_index": 0}
            
            latest = json.loads(lines[-1])
            return {
                "status": latest.get('status', 'UNKNOWN'),
                "compliance_index": latest.get('compliance_index', 0),
                "okr_status": latest.get('okr_status', {}),
                "last_check": latest.get('ts')
            }
    except Exception as e:
        return {"status": "pending", "note": "Governance loop not yet run"}

def collect_telemetry():
    """Collect all telemetry data"""
    telemetry = {
        "ts": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "overall_health": "green",
        "autonomy": "verified",
        "components": {
            "scheduler": get_scheduler_health(),
            "finance": get_finance_metrics(),
            "slo": get_slo_status(),
            "security": get_security_alerts(),
            "system": get_system_metrics(),
            "automation": get_automation_count(),
            "governance": get_governance_status()
        }
    }
    
    # Determine overall health
    scheduler_ok = telemetry["components"]["scheduler"]["status"] in ["healthy", "unknown"]
    slo_ok = telemetry["components"]["slo"]["status"] in ["OK", "no_data"]
    security_ok = telemetry["components"]["security"].get("alerts_1h", 0) < 10
    system_ok = telemetry["components"]["system"]["status"] == "healthy"
    
    if not scheduler_ok:
        telemetry["overall_health"] = "red"
        telemetry["autonomy"] = "degraded"
    elif not (slo_ok and security_ok and system_ok):
        telemetry["overall_health"] = "yellow"
        telemetry["autonomy"] = "operational"
    else:
        telemetry["overall_health"] = "green"
        telemetry["autonomy"] = "verified"
    
    return telemetry

if __name__ == '__main__':
    telemetry = collect_telemetry()
    print(json.dumps(telemetry, indent=2))
