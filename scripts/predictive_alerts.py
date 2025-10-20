#!/usr/bin/env python3
"""
Predictive Alerts - Phase 31
Monitors for concerning patterns and sends Telegram alerts
"""
import os
import json
import datetime
import requests
from pathlib import Path

ALERT_COOLDOWN_FILE = "logs/alert_cooldown.json"
COOLDOWN_MINUTES = 30

def load_cooldown():
    """Load cooldown timestamps"""
    if os.path.exists(ALERT_COOLDOWN_FILE):
        with open(ALERT_COOLDOWN_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cooldown(data):
    """Save cooldown timestamps"""
    with open(ALERT_COOLDOWN_FILE, 'w') as f:
        json.dump(data, f)

def can_send_alert(alert_type):
    """Check if we can send this alert type (cooldown check)"""
    cooldowns = load_cooldown()
    if alert_type in cooldowns:
        last_sent = datetime.datetime.fromisoformat(cooldowns[alert_type])
        age_minutes = (datetime.datetime.utcnow() - last_sent).total_seconds() / 60
        return age_minutes >= COOLDOWN_MINUTES
    return True

def mark_alert_sent(alert_type):
    """Mark that we sent this alert type"""
    cooldowns = load_cooldown()
    cooldowns[alert_type] = datetime.datetime.utcnow().isoformat()
    save_cooldown(cooldowns)

def send_telegram_alert(message):
    """Send alert to Telegram"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print(f"⚠️ Telegram not configured, would send: {message}")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": f"🚨 EchoPilot Alert\n\n{message}",
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Failed to send Telegram alert: {e}")
        return False

def check_and_alert():
    """Run all predictive checks and send alerts if needed"""
    alerts_sent = []
    
    # Check 1: Tick gaps (inline check to avoid import issues)
    def detect_tick_gaps():
        """Detect if there are >3 consecutive tick gaps >70s"""
        try:
            if not os.path.exists("logs/scheduler.log"):
                return False
            
            with open("logs/scheduler.log", 'r') as f:
                lines = f.readlines()
            
            tick_times = []
            for line in reversed(lines[-50:]):  # Check last 50 lines
                if '"event": "tick"' in line:
                    try:
                        data = json.loads(line)
                        tick_time = datetime.datetime.fromisoformat(data['ts'].replace('Z', '+00:00'))
                        tick_times.append(tick_time)
                    except:
                        continue
            
            if len(tick_times) < 4:
                return False
            
            tick_times.sort()
            consecutive_gaps = 0
            
            for i in range(len(tick_times) - 1):
                gap = (tick_times[i+1] - tick_times[i]).total_seconds()
                if gap > 70:
                    consecutive_gaps += 1
                    if consecutive_gaps >= 3:
                        return True
                else:
                    consecutive_gaps = 0
            
            return False
        except Exception:
            return False
    
    if detect_tick_gaps():
        if can_send_alert('tick_gaps'):
            message = "⚠️ Detected >3 consecutive tick gaps >70s. Scheduler may be unstable."
            if send_telegram_alert(message):
                mark_alert_sent('tick_gaps')
                alerts_sent.append('tick_gaps')
    
    # Check 2: Disk usage
    import shutil
    try:
        usage = shutil.disk_usage("/")
        percent = (usage.used / usage.total) * 100
        if percent > 85:
            if can_send_alert('disk_usage'):
                message = f"💾 Disk usage at {percent:.1f}%. Consider cleanup."
                if send_telegram_alert(message):
                    mark_alert_sent('disk_usage')
                    alerts_sent.append('disk_usage')
    except:
        pass
    
    # Check 3: Self-heal high activity
    try:
        if os.path.exists("logs/self_heal.log"):
            with open("logs/self_heal.log", 'r') as f:
                lines = f.readlines()
                # Count retries in last 24h
                recent_retries = 0
                cutoff = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
                for line in lines[-100:]:  # Check last 100 lines
                    try:
                        data = json.loads(line)
                        if 'retried_count' in data:
                            ts = datetime.datetime.fromisoformat(data.get('ts', '').replace('Z', ''))
                            if ts > cutoff:
                                recent_retries += data['retried_count']
                    except:
                        continue
                
                if recent_retries > 3:
                    if can_send_alert('self_heal_high'):
                        message = f"🔧 Self-heal retried {recent_retries} jobs in 24h. Check job queue."
                        if send_telegram_alert(message):
                            mark_alert_sent('self_heal_high')
                            alerts_sent.append('self_heal_high')
    except:
        pass
    
    return alerts_sent

if __name__ == "__main__":
    alerts = check_and_alert()
    print(json.dumps({
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "alerts_sent": alerts
    }))
