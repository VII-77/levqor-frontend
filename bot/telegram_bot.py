import os
import requests
import time
import json
from threading import Thread
from typing import Callable, Optional

class TelegramBot:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}" if self.bot_token else None
        self.enabled = bool(self.bot_token and self.chat_id)
    
    def send_message(self, message: str) -> bool:
        """Send a message to the configured Telegram chat"""
        if not self.enabled:
            print("⚠️  Telegram not configured - message not sent")
            return False
        
        try:
            # Truncate to Telegram's message limit
            truncated_msg = message[:4000]
            
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": truncated_msg,
                    "parse_mode": "HTML"
                },
                timeout=15
            )
            
            if response.status_code == 200:
                print(f"📨 Telegram message sent (status: {response.status_code})")
                return True
            else:
                print(f"⚠️  Telegram send failed: {response.status_code} - {response.text[:100]}")
                return False
                
        except Exception as e:
            print(f"❌ Telegram send error: {e}")
            return False
    
    def send_alert(self, title: str, body: str) -> bool:
        """Send a formatted alert message"""
        message = f"🚨 <b>{title}</b>\n\n{body}"
        return self.send_message(message)
    
    def poll_commands(
        self, 
        get_status_fn: Optional[Callable] = None,
        get_health_fn: Optional[Callable] = None,
        trigger_report_fn: Optional[Callable] = None
    ):
        """Poll for Telegram commands in background thread"""
        if not self.enabled:
            print("⚠️  Telegram bot disabled - no token/chat_id configured")
            return
        
        offset = 0
        print("🤖 Telegram bot listening for commands...")
        
        while True:
            try:
                response = requests.get(
                    f"{self.api_url}/getUpdates",
                    params={"timeout": 30, "offset": offset + 1},
                    timeout=40
                )
                
                data = response.json()
                
                for update in data.get("result", []):
                    offset = update["update_id"]
                    message = update.get("message", {})
                    text = message.get("text", "").strip()
                    
                    if not text:
                        continue
                    
                    cmd = text.lower()
                    
                    # Handle commands
                    if cmd in ("/start", "/help"):
                        help_text = """🤖 <b>EchoPilot Bot Ready</b>

Available commands:
/status - Check bot status
/health - System health check
/report - Trigger supervisor report
/help - Show this message"""
                        self.send_message(help_text)
                    
                    elif cmd == "/status":
                        if get_status_fn:
                            status = get_status_fn()
                            self.send_message(f"📊 <b>Status</b>\n\n{status}")
                        else:
                            self.send_message("Status check not available")
                    
                    elif cmd == "/health":
                        if get_health_fn:
                            health = get_health_fn()
                            self.send_message(f"💚 <b>Health Check</b>\n\n{health}")
                        else:
                            self.send_message("Health check not available")
                    
                    elif cmd == "/report":
                        if trigger_report_fn:
                            self.send_message("📧 Generating supervisor report...")
                            result = trigger_report_fn()
                            if result.get('ok'):
                                self.send_message(f"✅ Report sent to {result.get('to')}")
                            else:
                                self.send_message(f"❌ Report failed: {result.get('error')}")
                        else:
                            self.send_message("Report function not available")
                    
                    else:
                        self.send_message(f"❓ Unknown command: {text}\n\nUse /help to see available commands")
                
            except Exception as e:
                print(f"Telegram poll error: {e}")
                time.sleep(5)
            
            time.sleep(1)


# Global instance
telegram_bot = TelegramBot()

# Convenience functions
def send_telegram(message: str) -> bool:
    """Send a message via Telegram"""
    return telegram_bot.send_message(message)

def send_telegram_alert(title: str, body: str) -> bool:
    """Send a formatted alert via Telegram"""
    return telegram_bot.send_alert(title, body)

def start_telegram_listener(get_status_fn=None, get_health_fn=None, trigger_report_fn=None):
    """Start Telegram command listener in background thread"""
    if not telegram_bot.enabled:
        print("⚠️  Telegram bot disabled - set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
        return None
    
    thread = Thread(
        target=telegram_bot.poll_commands,
        kwargs={
            "get_status_fn": get_status_fn,
            "get_health_fn": get_health_fn,
            "trigger_report_fn": trigger_report_fn
        },
        daemon=True
    )
    thread.start()
    return thread
