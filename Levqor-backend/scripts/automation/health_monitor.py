#!/usr/bin/env python3
"""
Health & Uptime Monitoring Script
Runs every 6 hours via APScheduler
Pings levqor.ai and api.levqor.ai/health
Logs to Notion if non-200 response
"""
import os
import sys
import time
import requests
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from server.notion_helper import NotionHelper, notion_title, notion_rich_text, notion_number, notion_select, notion_date

ENDPOINTS = [
    {"name": "Frontend", "url": "https://levqor.ai"},
    {"name": "Backend Health", "url": "https://api.levqor.ai/health"},
    {"name": "Public Metrics", "url": "https://api.levqor.ai/public/metrics"},
]

def check_health():
    """Check health of all endpoints and return results"""
    results = []
    
    for endpoint in ENDPOINTS:
        start_time = time.time()
        try:
            response = requests.get(endpoint["url"], timeout=10)
            latency_ms = int((time.time() - start_time) * 1000)
            
            result = {
                "name": endpoint["name"],
                "url": endpoint["url"],
                "status_code": response.status_code,
                "latency_ms": latency_ms,
                "healthy": response.status_code == 200,
                "timestamp": datetime.utcnow().isoformat(),
            }
            results.append(result)
            
            # Log issues
            if response.status_code != 200:
                print(f"⚠️ {endpoint['name']} returned {response.status_code}")
            else:
                print(f"✅ {endpoint['name']} OK ({latency_ms}ms)")
                
        except Exception as e:
            print(f"❌ {endpoint['name']} FAILED: {str(e)}")
            results.append({
                "name": endpoint["name"],
                "url": endpoint["url"],
                "status_code": 0,
                "latency_ms": 0,
                "healthy": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            })
    
    return results

def log_to_notion(results):
    """Log health check results to Notion (if configured)"""
    unhealthy = [r for r in results if not r["healthy"]]
    
    if unhealthy:
        print(f"\n🚨 ALERT: {len(unhealthy)} endpoint(s) unhealthy")
        for result in unhealthy:
            print(f"  - {result['name']}: {result.get('status_code', 'ERROR')}")
    else:
        print(f"\n✅ All {len(results)} endpoints healthy")
    
    db_id = os.getenv("NOTION_HEALTH_DB_ID", "").strip()
    
    if not db_id:
        print("ℹ️  NOTION_HEALTH_DB_ID not configured, skipping Notion logging")
        print("   Add your database ID to Secrets to enable Notion integration")
        return unhealthy
    
    try:
        notion = NotionHelper()
        logged_count = 0
        
        for result in results:
            status = "Healthy" if result["healthy"] else ("Down" if result["status_code"] == 0 else "Degraded")
            notes = result.get("error", "") if not result["healthy"] else ""
            
            properties = {
                "Name": notion_title(result["name"]),
                "Timestamp": notion_date(result["timestamp"]),
                "Endpoint": notion_rich_text(result["url"]),
                "Status": notion_select(status),
                "Latency": notion_number(result["latency_ms"]),
                "Notes": notion_rich_text(notes) if notes else notion_rich_text(""),
            }
            
            notion.create_page(db_id, properties)
            logged_count += 1
        
        print(f"✅ Health check logged to Notion ({logged_count} entries added)")
        
    except Exception as e:
        print(f"⚠️  Notion logging failed: {str(e)}")
        print("   Health check completed, but not logged to Notion")
    
    return unhealthy

if __name__ == "__main__":
    print(f"🔍 Health Check - {datetime.utcnow().isoformat()}")
    results = check_health()
    alerts = log_to_notion(results)
    
    # Return exit code based on health
    exit_code = 1 if alerts else 0
    exit(exit_code)
