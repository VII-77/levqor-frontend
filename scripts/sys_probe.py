#!/usr/bin/env python3
"""
System Probe - Phase 32
Monitors CPU, RAM, Disk usage for live operations
"""
import psutil
import shutil
import json
import time
import os
from datetime import datetime

LOG_FILE = "logs/sys_probe.log"
os.makedirs("logs", exist_ok=True)

def log_event(event):
    """Append NDJSON event to sys probe log"""
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")

def get_system_metrics():
    """Collect system resource metrics"""
    try:
        # CPU usage (1 second sample)
        cpu_percent = round(psutil.cpu_percent(interval=1), 1)
        
        # Memory usage
        mem = psutil.virtual_memory()
        mem_percent = round(mem.percent, 1)
        mem_available_mb = round(mem.available / (1024 * 1024), 1)
        
        # Disk usage
        disk = shutil.disk_usage("/")
        disk_percent = round((disk.used / disk.total) * 100, 1)
        disk_free_gb = round(disk.free / (1024 ** 3), 2)
        
        # Process count
        process_count = len(psutil.pids())
        
        return {
            "cpu": cpu_percent,
            "mem": mem_percent,
            "mem_available_mb": mem_available_mb,
            "disk": disk_percent,
            "disk_free_gb": disk_free_gb,
            "process_count": process_count
        }
    except Exception as e:
        return {
            "cpu": 0,
            "mem": 0,
            "mem_available_mb": 0,
            "disk": 0,
            "disk_free_gb": 0,
            "process_count": 0,
            "error": str(e)
        }

def check_health_status(metrics):
    """Determine if system is healthy based on thresholds"""
    issues = []
    
    # CPU threshold: 80%
    if metrics.get("cpu", 0) > 80:
        issues.append(f"High CPU usage: {metrics['cpu']}%")
    
    # Memory threshold: 85%
    if metrics.get("mem", 0) > 85:
        issues.append(f"High memory usage: {metrics['mem']}%")
    
    # Disk threshold: 85%
    if metrics.get("disk", 0) > 85:
        issues.append(f"High disk usage: {metrics['disk']}%")
    
    # Low memory warning: <100MB available
    if metrics.get("mem_available_mb", 0) < 100:
        issues.append(f"Low available memory: {metrics['mem_available_mb']}MB")
    
    # Low disk warning: <1GB free
    if metrics.get("disk_free_gb", 0) < 1.0:
        issues.append(f"Low disk space: {metrics['disk_free_gb']}GB")
    
    ok = len(issues) == 0
    return ok, issues

def main():
    """Run system probe and log results"""
    ts = datetime.utcnow().isoformat() + "Z"
    
    # Collect metrics
    metrics = get_system_metrics()
    
    # Check health
    ok, issues = check_health_status(metrics)
    
    # Build event
    event = {
        "ts": ts,
        "ok": ok,
        "metrics": metrics,
        "issues": issues
    }
    
    # Log to file
    log_event(event)
    
    # Output to stdout
    print(json.dumps(event, indent=2))
    
    return 0 if ok else 1

if __name__ == "__main__":
    exit(main())
