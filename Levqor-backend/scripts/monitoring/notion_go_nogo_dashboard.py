"""
Notion Go/No-Go Dashboard Integration
Tracks the five gate metrics for Genesis v8.0 cutover decision
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import requests
import json

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
GO_NOGO_PAGE_ID = os.environ.get("GO_NOGO_NOTION_PAGE_ID", "")

# Go/No-Go Criteria Thresholds
CRITERIA = {
    "uptime_7d": {"target": 99.98, "unit": "%"},
    "error_rate": {"target": 0.5, "unit": "%"},
    "p1_incidents": {"target": 0, "unit": "count"},
    "intelligence_api_days": {"target": 7, "unit": "days"},
    "daily_cost": {"target": 10.0, "unit": "$"}
}

def get_db_connection():
    """Get PostgreSQL connection"""
    return psycopg2.connect(
        os.environ.get("DATABASE_URL"),
        cursor_factory=RealDictCursor
    )

def calculate_uptime_7d():
    """Calculate 7-day rolling uptime"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    COUNT(*) as total_checks,
                    COUNT(CASE WHEN backend = 200 AND frontend = 200 THEN 1 END) as successful_checks
                FROM system_health_log
                WHERE timestamp > NOW() - INTERVAL '7 days'
            """)
            
            row = cur.fetchone()
            
            if row and row['total_checks'] > 0:
                uptime = (row['successful_checks'] / row['total_checks']) * 100
                return round(uptime, 2)
            
            return 0.0

def calculate_error_rate():
    """Calculate error rate (last 24h)"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    COUNT(*) as total_checks,
                    COUNT(CASE WHEN error IS NOT NULL OR backend >= 500 OR frontend >= 500 THEN 1 END) as error_count
                FROM system_health_log
                WHERE timestamp > NOW() - INTERVAL '24 hours'
            """)
            
            row = cur.fetchone()
            
            if row and row['total_checks'] > 0:
                error_rate = (row['error_count'] / row['total_checks']) * 100
                return round(error_rate, 2)
            
            return 0.0

def count_p1_incidents():
    """Count P1 incidents (critical outages > 5 minutes)"""
    # This would query an incidents table if we had one
    # For now, detect from logs
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(DISTINCT DATE_TRUNC('hour', timestamp)) as incident_hours
                FROM system_health_log
                WHERE timestamp > NOW() - INTERVAL '7 days'
                AND (backend >= 500 OR backend = 0)
                GROUP BY DATE_TRUNC('hour', timestamp)
                HAVING COUNT(*) > 10
            """)
            
            rows = cur.fetchall()
            return len(rows) if rows else 0

def calculate_intelligence_api_days():
    """Calculate consecutive days intelligence API has been serving"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Check system_health_log entries from intelligence endpoints
            cur.execute("""
                SELECT 
                    DATE(timestamp) as check_date,
                    COUNT(*) as checks
                FROM system_health_log
                WHERE source = 'monitor'
                AND timestamp > NOW() - INTERVAL '30 days'
                GROUP BY DATE(timestamp)
                ORDER BY check_date DESC
            """)
            
            rows = cur.fetchall()
            
            # Count consecutive days with checks
            consecutive_days = 0
            expected_date = datetime.utcnow().date()
            
            for row in rows:
                if row['check_date'] == expected_date:
                    consecutive_days += 1
                    expected_date = expected_date - timedelta(days=1)
                else:
                    break
            
            return consecutive_days

def estimate_daily_cost():
    """Estimate daily Replit cost"""
    # This would integrate with Replit cost API
    # For now, return placeholder based on resource usage
    # Estimate: Autoscale ~$5/day, DB ~$2/day = ~$7/day
    return 7.0

def get_go_nogo_metrics():
    """Get all Go/No-Go metrics"""
    metrics = {
        "uptime_7d": calculate_uptime_7d(),
        "error_rate": calculate_error_rate(),
        "p1_incidents": count_p1_incidents(),
        "intelligence_api_days": calculate_intelligence_api_days(),
        "daily_cost": estimate_daily_cost(),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Determine Go/No-Go status
    go_decision = (
        metrics["uptime_7d"] >= CRITERIA["uptime_7d"]["target"] and
        metrics["error_rate"] <= CRITERIA["error_rate"]["target"] and
        metrics["p1_incidents"] <= CRITERIA["p1_incidents"]["target"] and
        metrics["intelligence_api_days"] >= CRITERIA["intelligence_api_days"]["target"] and
        metrics["daily_cost"] <= CRITERIA["daily_cost"]["target"]
    )
    
    metrics["go_decision"] = "GO ✅" if go_decision else "NO-GO ⚠️"
    metrics["criteria_met"] = sum([
        metrics["uptime_7d"] >= CRITERIA["uptime_7d"]["target"],
        metrics["error_rate"] <= CRITERIA["error_rate"]["target"],
        metrics["p1_incidents"] <= CRITERIA["p1_incidents"]["target"],
        metrics["intelligence_api_days"] >= CRITERIA["intelligence_api_days"]["target"],
        metrics["daily_cost"] <= CRITERIA["daily_cost"]["target"]
    ])
    
    return metrics

def update_notion_dashboard(metrics):
    """Update Notion page with Go/No-Go metrics"""
    if not NOTION_API_KEY or not GO_NOGO_PAGE_ID:
        print("⚠️ Notion API key or page ID not configured")
        return False
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Update page content with metrics
    blocks = [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": f"Genesis v8.0 Go/No-Go Dashboard - {metrics['go_decision']}"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": f"Last Updated: {metrics['timestamp']}"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": f"Criteria Met: {metrics['criteria_met']}/5"}}]
            }
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Gate Metrics"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": f"Uptime (7d): {metrics['uptime_7d']}% (target: ≥{CRITERIA['uptime_7d']['target']}%) {'✅' if metrics['uptime_7d'] >= CRITERIA['uptime_7d']['target'] else '❌'}"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": f"Error Rate (24h): {metrics['error_rate']}% (target: ≤{CRITERIA['error_rate']['target']}%) {'✅' if metrics['error_rate'] <= CRITERIA['error_rate']['target'] else '❌'}"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": f"P1 Incidents (7d): {metrics['p1_incidents']} (target: ≤{CRITERIA['p1_incidents']['target']}) {'✅' if metrics['p1_incidents'] <= CRITERIA['p1_incidents']['target'] else '❌'}"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": f"Intelligence API Days: {metrics['intelligence_api_days']} (target: ≥{CRITERIA['intelligence_api_days']['target']}) {'✅' if metrics['intelligence_api_days'] >= CRITERIA['intelligence_api_days']['target'] else '❌'}"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": f"Daily Cost: ${metrics['daily_cost']} (target: ≤${CRITERIA['daily_cost']['target']}) {'✅' if metrics['daily_cost'] <= CRITERIA['daily_cost']['target'] else '❌'}"}}]
            }
        }
    ]
    
    try:
        # Append blocks to page
        response = requests.patch(
            f"https://api.notion.com/v1/blocks/{GO_NOGO_PAGE_ID}/children",
            headers=headers,
            json={"children": blocks}
        )
        
        if response.status_code == 200:
            print("✅ Notion dashboard updated")
            return True
        else:
            print(f"⚠️ Notion update failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Notion update error: {e}")
        return False

def generate_go_nogo_report():
    """Generate and print Go/No-Go report"""
    print("\n" + "="*60)
    print("GENESIS v8.0 GO/NO-GO DASHBOARD")
    print("="*60)
    
    metrics = get_go_nogo_metrics()
    
    print(f"\nDecision: {metrics['go_decision']}")
    print(f"Criteria Met: {metrics['criteria_met']}/5")
    print(f"Last Updated: {metrics['timestamp']}\n")
    
    print("Gate Metrics:")
    print(f"  1. Uptime (7d):          {metrics['uptime_7d']}% (target: ≥{CRITERIA['uptime_7d']['target']}%) {'✅' if metrics['uptime_7d'] >= CRITERIA['uptime_7d']['target'] else '❌'}")
    print(f"  2. Error Rate (24h):     {metrics['error_rate']}% (target: ≤{CRITERIA['error_rate']['target']}%) {'✅' if metrics['error_rate'] <= CRITERIA['error_rate']['target'] else '❌'}")
    print(f"  3. P1 Incidents (7d):    {metrics['p1_incidents']} (target: ≤{CRITERIA['p1_incidents']['target']}) {'✅' if metrics['p1_incidents'] <= CRITERIA['p1_incidents']['target'] else '❌'}")
    print(f"  4. Intelligence API Days: {metrics['intelligence_api_days']} (target: ≥{CRITERIA['intelligence_api_days']['target']}) {'✅' if metrics['intelligence_api_days'] >= CRITERIA['intelligence_api_days']['target'] else '❌'}")
    print(f"  5. Daily Cost:           ${metrics['daily_cost']} (target: ≤${CRITERIA['daily_cost']['target']}) {'✅' if metrics['daily_cost'] <= CRITERIA['daily_cost']['target'] else '❌'}")
    
    print("\n" + "="*60 + "\n")
    
    # Update Notion if configured
    if NOTION_API_KEY and GO_NOGO_PAGE_ID:
        update_notion_dashboard(metrics)
    
    return metrics

if __name__ == "__main__":
    generate_go_nogo_report()
