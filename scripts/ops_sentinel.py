#!/usr/bin/env python3
"""
Phase 44: OPS Sentinel — System Watchdog
Monitors CPU, RAM, disk, and latency
Logs warnings but does NOT auto-restart (too risky in production)
"""
import os
import sys
import json
import time
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def check_system_health():
    """Check system resources and API latency"""
    try:
        import psutil
        import requests
        
        # CPU check
        cpu_percent = psutil.cpu_percent(interval=2)
        
        # Memory check
        mem = psutil.virtual_memory()
        mem_percent = mem.percent
        
        # Disk check
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        
        # API latency check
        start = time.time()
        try:
            requests.get('http://localhost:5000/', timeout=5)
            latency = time.time() - start
        except:
            latency = 999  # Timeout
        
        # Determine health status
        warnings = []
        if cpu_percent > 85:
            warnings.append(f"High CPU: {cpu_percent:.1f}%")
        if mem_percent > 85:
            warnings.append(f"High Memory: {mem_percent:.1f}%")
        if disk_percent > 85:
            warnings.append(f"High Disk: {disk_percent:.1f}%")
        if latency > 2:
            warnings.append(f"High Latency: {latency:.2f}s")
        
        status = "critical" if warnings else "healthy"
        
        # Log result
        log_entry = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "event": "ops_sentinel",
            "status": status,
            "cpu_percent": cpu_percent,
            "mem_percent": mem_percent,
            "disk_percent": disk_percent,
            "latency_sec": latency,
            "warnings": warnings
        }
        
        os.makedirs('logs', exist_ok=True)
        with open('logs/ops_sentinel.ndjson', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # Send Telegram alert if critical
        if status == "critical":
            send_alert(warnings)
        
        return {
            "ok": True,
            "status": status,
            "metrics": {
                "cpu": cpu_percent,
                "memory": mem_percent,
                "disk": disk_percent,
                "latency": latency
            },
            "warnings": warnings
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def send_alert(warnings):
    """Send Telegram alert for critical issues"""
    try:
        import requests
        
        token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
        
        if not token or not chat_id:
            return
        
        message = f"🔴 *OPS SENTINEL ALERT*\n\n" + "\n".join(f"• {w}" for w in warnings)
        
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"},
            timeout=10
        )
    except:
        pass

if __name__ == "__main__":
    result = check_system_health()
    print(json.dumps(result, indent=2))
