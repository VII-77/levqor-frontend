import time
import schedule
from datetime import datetime
from typing import Dict
from bot import config

class EchoPilotBot:
    def __init__(self):
        self.is_running = False
        self.health_status = "Initializing"
        self.demo_mode = config.DEMO_MODE
    
    def health_check(self) -> Dict:
        try:
            if self.demo_mode:
                return {
                    'status': 'Demo Mode', 
                    'message': 'Running in DEMO mode - configure real Notion databases for production'
                }
            
            if not config.AUTOMATION_QUEUE_DB_ID:
                return {'status': 'Error', 'message': 'AUTOMATION_QUEUE_DB_ID not configured'}
            if not config.AUTOMATION_LOG_DB_ID:
                return {'status': 'Error', 'message': 'AUTOMATION_LOG_DB_ID not configured'}
            if not config.JOB_LOG_DB_ID:
                return {'status': 'Error', 'message': 'JOB_LOG_DB_ID not configured'}
            
            return {'status': 'Healthy', 'message': 'All systems operational'}
        except Exception as e:
            return {'status': 'Error', 'message': str(e)}
    
    def poll_and_process_demo(self):
        """Demo polling - simulates bot activity"""
        print(f"[{datetime.now().isoformat()}] 🔄 Demo Mode: Polling for tasks...")
        print("   📊 No real Notion databases configured")
        print("   ✅ Bot is running correctly in demo mode")
        print("   💡 To enable production mode: configure real database IDs")
        self.health_status = "Running (Demo)"
    
    def poll_and_process(self):
        """Real polling for production mode"""
        try:
            from bot.processor import TaskProcessor
            from bot.notion_api import NotionClientWrapper
            
            notion = NotionClientWrapper()
            processor = TaskProcessor()
            
            print(f"[{datetime.now().isoformat()}] Polling for triggered tasks...")
            
            tasks = notion.get_triggered_tasks()
            
            if tasks:
                print(f"Found {len(tasks)} triggered task(s)")
                
                for task in tasks:
                    result = processor.process_task(task)
                    if result['success']:
                        print(f"✅ Completed: {result['task_name']} (QA: {result['qa_score']}%)")
                    else:
                        print(f"❌ Failed: {result['task_name']} - {result.get('error', 'Unknown error')}")
            else:
                print("No triggered tasks found")
            
            self.health_status = "Running"
            
        except Exception as e:
            print(f"Error in poll cycle: {e}")
            self.health_status = f"Error: {str(e)}"
    
    def run(self):
        print("=" * 80)
        print("🤖 EchoPilot AI Automation Bot Starting...")
        print("=" * 80)
        
        health = self.health_check()
        print(f"\nHealth Check: {health['status']} - {health['message']}")
        
        if health['status'] == 'Demo Mode':
            print("\n" + "🎮 DEMO MODE ACTIVE" + "\n")
            print("The bot is running in demo mode for testing.")
            print("\n📋 TO ENABLE PRODUCTION MODE:\n")
            print("1. Get your 3 Notion database IDs:")
            print("   • Open each database in Notion")
            print("   • Copy the ID from the URL")
            print("\n2. Add them to Replit Secrets (🔒 tab):")
            print("   • AUTOMATION_QUEUE_DB_ID")
            print("   • AUTOMATION_LOG_DB_ID")
            print("   • JOB_LOG_DB_ID")
            print("\n3. Restart this workflow\n")
            print("=" * 80 + "\n")
            
            self.is_running = True
            schedule.every(config.POLL_INTERVAL_SECONDS).seconds.do(self.poll_and_process_demo)
            self.poll_and_process_demo()
            
        elif health['status'] == 'Error':
            print("\n⚠️  Configuration Error!")
            print("Please set the following environment variables:")
            print("  - AUTOMATION_QUEUE_DB_ID")
            print("  - AUTOMATION_LOG_DB_ID")
            print("  - JOB_LOG_DB_ID")
            return
        
        else:
            print(f"\n✅ Bot initialized successfully!")
            print(f"📊 Polling interval: {config.POLL_INTERVAL_SECONDS} seconds")
            print(f"🎯 QA Target Score: {config.QA_TARGET_SCORE}%")
            print("\n" + "=" * 80 + "\n")
            
            self.is_running = True
            schedule.every(config.POLL_INTERVAL_SECONDS).seconds.do(self.poll_and_process)
            self.poll_and_process()
        
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    bot = EchoPilotBot()
    bot.run()
