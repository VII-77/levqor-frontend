import time
import schedule
from datetime import datetime
from processor import TaskProcessor
from notion_client import NotionClientWrapper
import config

class EchoPilotBot:
    def __init__(self):
        self.processor = TaskProcessor()
        self.notion = NotionClientWrapper()
        self.is_running = False
        self.health_status = "Initializing"
    
    def health_check(self) -> Dict:
        try:
            if not config.AUTOMATION_QUEUE_DB_ID:
                return {'status': 'Error', 'message': 'AUTOMATION_QUEUE_DB_ID not configured'}
            if not config.AUTOMATION_LOG_DB_ID:
                return {'status': 'Error', 'message': 'AUTOMATION_LOG_DB_ID not configured'}
            if not config.JOB_LOG_DB_ID:
                return {'status': 'Error', 'message': 'JOB_LOG_DB_ID not configured'}
            
            self.notion.get_client()
            
            return {'status': 'Healthy', 'message': 'All systems operational'}
        except Exception as e:
            return {'status': 'Error', 'message': str(e)}
    
    def poll_and_process(self):
        try:
            print(f"[{datetime.now().isoformat()}] Polling for triggered tasks...")
            
            tasks = self.notion.get_triggered_tasks()
            
            if tasks:
                print(f"Found {len(tasks)} triggered task(s)")
                
                for task in tasks:
                    result = self.processor.process_task(task)
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
        print("=" * 60)
        print("🤖 EchoPilot AI Automation Bot Starting...")
        print("=" * 60)
        
        health = self.health_check()
        print(f"Health Check: {health['status']} - {health['message']}")
        
        if health['status'] == 'Error':
            print("\n⚠️  Configuration Error!")
            print("Please set the following environment variables:")
            print("  - AUTOMATION_QUEUE_DB_ID")
            print("  - AUTOMATION_LOG_DB_ID")
            print("  - JOB_LOG_DB_ID")
            print("\nGet database IDs from Notion:")
            print("1. Open each database in Notion")
            print("2. Copy the database ID from the URL")
            print("3. Add to Replit Secrets")
            return
        
        print(f"\n✅ Bot initialized successfully!")
        print(f"📊 Polling interval: {config.POLL_INTERVAL_SECONDS} seconds")
        print(f"🎯 QA Target Score: {config.QA_TARGET_SCORE}%")
        print("\n" + "=" * 60 + "\n")
        
        self.is_running = True
        
        schedule.every(config.POLL_INTERVAL_SECONDS).seconds.do(self.poll_and_process)
        
        self.poll_and_process()
        
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    from typing import Dict
    bot = EchoPilotBot()
    bot.run()
