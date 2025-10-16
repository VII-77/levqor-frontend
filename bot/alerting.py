import os
import time
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict

class AlertManager:
    def __init__(self):
        self.consecutive_failures = defaultdict(int)
        self.failure_timestamps = defaultdict(list)
        self.last_alert_time = {}
        self.alert_webhook_url = os.getenv('ALERT_WEBHOOK_URL', '')
        self.email_alerts_enabled = bool(os.getenv('ALERT_TO'))
        self.telegram_alerts_enabled = bool(os.getenv('TELEGRAM_BOT_TOKEN') and os.getenv('TELEGRAM_CHAT_ID'))
    
    def record_failure(self, task_name: str, task_type: str):
        self.consecutive_failures[task_name] += 1
        self.consecutive_failures[f"type:{task_type}"] += 1
        self.failure_timestamps[task_name].append(datetime.now())
        
        self.failure_timestamps[task_name] = [
            ts for ts in self.failure_timestamps[task_name]
            if ts > datetime.now() - timedelta(hours=24)
        ]
    
    def reset_failures(self, task_name: str):
        self.consecutive_failures[task_name] = 0
    
    def check_and_alert(self, commit: str, notion_logger) -> bool:
        now = datetime.now()
        alert_triggered = False
        
        for key, count in self.consecutive_failures.items():
            if count >= 3:
                last_alert = self.last_alert_time.get(key, datetime.min)
                if now - last_alert > timedelta(hours=1):
                    failures_24h = len([
                        ts for ts in self.failure_timestamps.get(key.replace('type:', ''), [])
                        if ts > now - timedelta(hours=24)
                    ])
                    
                    summary = f"Consecutive failures for {key}: {count} (24h: {failures_24h})"
                    
                    notion_logger.log_activity(
                        task_name="Alert",
                        status="Warning",
                        message=f"Alert triggered: {summary}",
                        details=f"Commit: {commit}"
                    )
                    
                    # Send webhook alert
                    if self.alert_webhook_url:
                        try:
                            payload = {
                                'ts': now.isoformat(),
                                'commit': commit,
                                'key': key,
                                'consecutive_failures': count,
                                'failures_24h': failures_24h,
                                'summary': summary
                            }
                            requests.post(
                                self.alert_webhook_url,
                                json=payload,
                                timeout=5
                            )
                        except Exception as e:
                            print(f"Failed to send webhook: {e}")
                    
                    # Send email alert
                    if self.email_alerts_enabled:
                        try:
                            from bot.gmail_client import GmailClientWrapper
                            gmail = GmailClientWrapper()
                            
                            subject = f"[EchoPilot] ALERT: Consecutive Failures Detected"
                            body = f"""EchoPilot Alert: Consecutive Failures
{'=' * 60}

Alert Key: {key}
Consecutive Failures: {count}
Failures in Last 24h: {failures_24h}
Timestamp: {now.isoformat()}
Git Commit: {commit}

Summary:
{summary}

{'=' * 60}
Action Required: Please investigate the automation queue and logs.
"""
                            
                            gmail.send_email(
                                to=os.getenv('ALERT_TO', ''),
                                subject=subject,
                                body=body
                            )
                            print(f"📧 Alert email sent for {key}")
                        except Exception as e:
                            print(f"Failed to send alert email: {e}")
                    
                    # Send Telegram alert
                    if self.telegram_alerts_enabled:
                        try:
                            from bot.telegram_bot import send_telegram_alert
                            
                            alert_title = "ALERT: Consecutive Failures"
                            alert_body = f"""Alert Key: {key}
Consecutive Failures: {count}
Failures (24h): {failures_24h}
Timestamp: {now.strftime('%Y-%m-%d %H:%M:%S')}
Commit: {commit[:8]}

{summary}

⚠️ Action Required: Check automation queue and logs."""
                            
                            send_telegram_alert(alert_title, alert_body)
                            print(f"📱 Alert sent to Telegram for {key}")
                        except Exception as e:
                            print(f"Failed to send Telegram alert: {e}")
                    
                    self.last_alert_time[key] = now
                    alert_triggered = True
        
        return alert_triggered
