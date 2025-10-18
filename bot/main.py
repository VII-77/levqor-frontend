import time
import schedule
import json
import threading
from datetime import datetime
from typing import Dict
from bot import config
from bot.git_utils import get_git_info, check_git_clean
from bot.schema_validator import SchemaValidator
from bot.alerting import AlertManager
from bot.metrics import MetricsCollector

class EchoPilotBot:
    def __init__(self):
        self.is_running = False
        self.health_status = "Initializing"
        self.demo_mode = config.DEMO_MODE
        self.commit, self.branch, self.is_dirty = get_git_info()
        self.alert_manager = AlertManager()
        self.metrics = MetricsCollector()
        self.last_alert_ts = None
    
    def health_check(self) -> Dict:
        try:
            if self.demo_mode:
                return {
                    'status': 'Demo Mode', 
                    'message': 'Running in DEMO mode - configure real Notion databases for production',
                    'commit': self.commit,
                    'model': 'gpt-4o',
                    'rate_limit_headroom': 'N/A',
                    'last_alert_ts': self.last_alert_ts
                }
            
            if not config.AUTOMATION_QUEUE_DB_ID:
                return {'status': 'Error', 'message': 'AUTOMATION_QUEUE_DB_ID not configured'}
            if not config.AUTOMATION_LOG_DB_ID:
                return {'status': 'Error', 'message': 'AUTOMATION_LOG_DB_ID not configured'}
            if not config.JOB_LOG_DB_ID:
                return {'status': 'Error', 'message': 'JOB_LOG_DB_ID not configured'}
            
            return {
                'status': 'Healthy',
                'message': 'All systems operational',
                'commit': self.commit,
                'branch': self.branch,
                'model': 'gpt-4o',
                'rate_limit_headroom': 'OK',
                'last_alert_ts': self.last_alert_ts
            }
        except Exception as e:
            return {'status': 'Error', 'message': str(e), 'commit': self.commit}
    
    def poll_and_process_demo(self):
        print(f"[{datetime.now().isoformat()}] 🔄 Demo Mode: Polling for tasks...")
        print(f"   📊 Commit: {self.commit}")
        print("   ✅ Bot is running correctly in demo mode")
        print("   💡 To enable production mode: configure real database IDs")
        self.health_status = "Running (Demo)"
    
    def poll_and_process(self):
        try:
            from bot.processor import TaskProcessor
            from bot.notion_api import NotionClientWrapper
            
            notion = NotionClientWrapper()
            processor = TaskProcessor(
                commit=self.commit,
                alert_manager=self.alert_manager,
                metrics=self.metrics
            )
            
            print(f"[{datetime.now().isoformat()}] Polling for triggered tasks... (commit: {self.commit[:8]})")
            
            tasks = notion.get_triggered_tasks()
            
            if tasks:
                print(f"Found {len(tasks)} triggered task(s)")
                
                for task in tasks:
                    result = processor.process_task(task)
                    if result['success']:
                        print(f"✅ Completed: {result['task_name']} (QA: {result['qa_score']}%)")
                    else:
                        print(f"❌ Failed: {result['task_name']} - {result.get('error', 'Unknown error')}")
                
                alert_sent = self.alert_manager.check_and_alert(self.commit, notion)
                if alert_sent:
                    self.last_alert_ts = datetime.now().isoformat()
                    print(f"⚠️  Alert sent for consecutive failures")
            else:
                print("No triggered tasks found")
            
            self.health_status = "Running"
            
        except Exception as e:
            print(f"Error in poll cycle: {e}")
            self.health_status = f"Error: {str(e)}"
    
    def run(self):
        print("=" * 80)
        print("🤖 EchoPilot AI Automation Bot Starting...")
        print(f"📝 Commit: {self.commit}")
        print(f"🌿 Branch: {self.branch}")
        print("=" * 80)
        
        if not config.DEMO_MODE:
            try:
                check_git_clean()
            except Exception as e:
                print(f"\n❌ Git Check Failed: {e}")
                print("Exiting...")
                return
        
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
            
            # Start diagnostic schedulers for live monitoring
            try:
                from bot.scheduler_diag import schedule_hourly_heartbeat, schedule_autocheck_6h
                schedule_hourly_heartbeat()
                schedule_autocheck_6h()
            except Exception as e:
                print(f"⚠️  Diagnostic schedulers not started: {e}")
            
            # Start daily supervisor email report
            try:
                from bot.supervisor_report import send_supervisor_email
                def daily_supervisor():
                    print(f"[{datetime.now().isoformat()}] 📧 Sending daily supervisor report...")
                    result = send_supervisor_email()
                    if result.get('ok'):
                        print(f"✅ Supervisor report sent to {result.get('to')}")
                    else:
                        print(f"❌ Supervisor report failed: {result.get('error')}")
                
                # Schedule for 6:45 UTC daily
                schedule.every().day.at("06:45").do(daily_supervisor)
                print("📧 Daily supervisor email scheduled for 06:45 UTC")
            except Exception as e:
                print(f"⚠️  Supervisor email scheduler not started: {e}")
            
            # Start daily executive report (PDF)
            try:
                from bot.executive_report import run_exec_report
                def daily_exec_report():
                    print(f"[{datetime.now().isoformat()}] 📊 Generating daily executive report...")
                    try:
                        summary = run_exec_report()
                        print(f"✅ Executive report sent: {summary['total']} jobs, ${summary['sum_gross']:.2f} gross")
                    except Exception as e:
                        print(f"❌ Executive report failed: {e}")
                
                # Schedule for 6:55 UTC daily
                schedule.every().day.at("06:55").do(daily_exec_report)
                print("📊 Daily executive report scheduled for 06:55 UTC")
            except Exception as e:
                print(f"⚠️  Executive report scheduler not started: {e}")
            
            # Start Telegram bot command listener
            try:
                from bot.telegram_bot import start_telegram_listener, send_telegram
                from bot.supervisor_report import send_supervisor_email
                
                def get_status():
                    return f"✅ EchoPilot Running\n📊 Polling: Every 60s\n🎯 QA Target: {config.QA_TARGET_SCORE}%\n📝 Commit: {self.commit[:8]}\n🌿 Branch: {self.branch}"
                
                def get_health():
                    health = self.health_check()
                    return f"Status: {health['status']}\n{health['message']}\nCommit: {health.get('commit', 'unknown')[:8]}"
                
                def trigger_report():
                    return send_supervisor_email()
                
                thread = start_telegram_listener(
                    get_status_fn=get_status,
                    get_health_fn=get_health,
                    trigger_report_fn=trigger_report
                )
                
                if thread:
                    print("🤖 Telegram bot listener started")
                    # Send startup notification
                    send_telegram("🚀 <b>EchoPilot Bot Started</b>\n\nBot is live and monitoring!\nUse /help for commands.")
            except Exception as e:
                print(f"⚠️  Telegram bot not started: {e}")
            
            # Start auto-operator monitoring (every 5 minutes)
            try:
                from bot.auto_operator import run_auto_operator_once
                
                def auto_operator_loop():
                    while self.is_running:
                        try:
                            run_auto_operator_once()
                        except Exception as e:
                            print(f"[AutoOperator] error: {e}")
                        time.sleep(300)  # 5 minutes
                
                operator_thread = threading.Thread(target=auto_operator_loop, daemon=True)
                operator_thread.start()
                print("🔧 Auto-operator monitoring started (checks every 5min)")
            except Exception as e:
                print(f"⚠️  Auto-operator not started: {e}")
            
            # Start nightly payment reconciliation (2:10 UTC daily)
            try:
                from bot.reconcile_payments import reconcile_once
                
                def reconciliation_scheduler():
                    while self.is_running:
                        now = datetime.now()
                        if now.hour == 2 and now.minute == 10:
                            try:
                                changed = reconcile_once()
                                print(f"[Reconcile] Completed. Updated {changed} job(s)")
                            except Exception as e:
                                print(f"[Reconcile] Error: {e}")
                            time.sleep(70)
                        time.sleep(20)
                
                reconcile_thread = threading.Thread(target=reconciliation_scheduler, daemon=True)
                reconcile_thread.start()
                print("💰 Payment reconciliation scheduled (2:10 UTC daily)")
            except Exception as e:
                print(f"⚠️  Payment reconciliation not started: {e}")
            
            # Start weekly compliance maintenance (Sundays at 03:00 UTC)
            try:
                from bot.compliance_tools import compute_p95_latency, backup_config
                
                def weekly_maintenance():
                    while self.is_running:
                        now = datetime.now()
                        # Sunday = 6, at 03:00 UTC
                        if now.weekday() == 6 and now.hour == 3 and now.minute == 0:
                            try:
                                print("[Maintenance] Running weekly p95 latency computation...")
                                p95 = compute_p95_latency()
                                if p95:
                                    print(f"[Maintenance] p95 latency: {p95}s")
                                
                                print("[Maintenance] Creating config backup...")
                                backup_path = backup_config()
                                print(f"[Maintenance] Backup created: {backup_path}")
                            except Exception as e:
                                print(f"[Maintenance] Error: {e}")
                            time.sleep(70)  # Sleep after running to avoid duplicate runs
                        time.sleep(60)  # Check every minute
                
                maintenance_thread = threading.Thread(target=weekly_maintenance, daemon=True)
                maintenance_thread.start()
                print("🔧 Weekly compliance maintenance scheduled (Sundays 03:00 UTC)")
            except Exception as e:
                print(f"⚠️  Weekly maintenance not started: {e}")
            
            # Start resilience scheduler (payment scan + job replay)
            try:
                from bot.stripe_events_poller import poll_and_fix
                from bot.replay_failed_jobs import replay_once
                
                def resilience_scheduler():
                    while self.is_running:
                        now = datetime.now()
                        
                        # Every 15 minutes: Stripe payment reconciliation
                        if now.minute % 15 == 0:
                            try:
                                fixed = poll_and_fix()
                                if fixed > 0:
                                    print(f"[Resilience] Payment scan: Fixed {fixed} missed payment(s)")
                            except Exception as e:
                                print(f"[Resilience] Payment scan error: {e}")
                            time.sleep(70)  # Sleep after running to avoid duplicate runs
                        
                        # Daily at 02:20 UTC: Replay failed jobs
                        if now.hour == 2 and now.minute == 20:
                            try:
                                replayed = replay_once()
                                if replayed > 0:
                                    print(f"[Resilience] Job replay: Replayed {replayed} failed job(s)")
                            except Exception as e:
                                print(f"[Resilience] Job replay error: {e}")
                            time.sleep(70)  # Sleep after running
                        
                        time.sleep(60)  # Check every minute
                
                resilience_thread = threading.Thread(target=resilience_scheduler, daemon=True)
                resilience_thread.start()
                print("🔄 Resilience scheduler started (payment scan every 15min, job replay daily 02:20 UTC)")
            except Exception as e:
                print(f"⚠️  Resilience scheduler not started: {e}")
            
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
