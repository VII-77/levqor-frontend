import threading
import time
import json
from bot.diagnostics import snapshot, post_status_to_notion, run_autocheck


def schedule_hourly_heartbeat():
    """Post system status to Notion Status Board every hour."""
    def loop():
        while True:
            try:
                snap = snapshot()
                # Check if all critical systems are OK
                ok = all(
                    v.get("ok", True) 
                    for k, v in snap.items() 
                    if k != "ts"
                )
                notes = json.dumps(snap, indent=2)[:1800]
                result = post_status_to_notion(ok, notes)
                print(f"[Heartbeat] Posted to Notion: {result}")
            except Exception as e:
                print(f"[Heartbeat] Error: {e}")
                try:
                    post_status_to_notion(False, f"Heartbeat error: {e}")
                except:
                    pass
            
            time.sleep(3600)  # 1 hour
    
    thread = threading.Thread(target=loop, daemon=True, name="DiagHeartbeat")
    thread.start()
    print("✅ Hourly heartbeat diagnostic started")


def schedule_autocheck_6h():
    """Run synthetic end-to-end test every 6 hours."""
    def loop():
        # Wait 5 minutes before first run to let system stabilize
        time.sleep(300)
        
        while True:
            try:
                result = run_autocheck()
                notes = json.dumps(result, indent=2)[:1800]
                post_result = post_status_to_notion(
                    result.get("ok", False), 
                    f"AutoCheck: {notes}"
                )
                print(f"[AutoCheck] Synthetic test: {result}, Posted: {post_result}")
            except Exception as e:
                print(f"[AutoCheck] Error: {e}")
                try:
                    post_status_to_notion(False, f"AutoCheck error: {e}")
                except:
                    pass
            
            time.sleep(6 * 3600)  # 6 hours
    
    thread = threading.Thread(target=loop, daemon=True, name="DiagAutoCheck")
    thread.start()
    print("✅ 6-hour autocheck diagnostic started")
