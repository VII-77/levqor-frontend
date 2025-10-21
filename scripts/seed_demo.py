#!/usr/bin/env python3
"""
EchoPilot Demo Data Seeder
Extra 1: Populates Notion databases with realistic demo data
Run with: python3 scripts/seed_demo.py
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
import random

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from notion_client import Client as NotionClient
except ImportError:
    print("❌ notion-client not installed", file=sys.stderr, flush=True)
    sys.exit(1)

# Configuration
LOG_FILE = Path('logs/seed_demo.ndjson')
LOG_FILE.parent.mkdir(exist_ok=True)

def log_event(event, data=None):
    """Write NDJSON log entry"""
    entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event': event
    }
    if data:
        entry.update(data)
    
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    
    print(json.dumps(entry), flush=True)

def get_notion_client():
    """Initialize Notion client"""
    token = os.getenv('NOTION_TOKEN')
    if not token:
        raise ValueError("NOTION_TOKEN not set")
    
    return NotionClient(auth=token)

def create_demo_clients(notion, client_db_id):
    """Create demo client records (idempotent)"""
    demo_clients = [
        {
            "name": "Acme Corporation",
            "email": "contact@acme.example.com",
            "tier": "Enterprise",
            "status": "Active",
            "mrr": 2500
        },
        {
            "name": "TechStart Inc",
            "email": "hello@techstart.example.com",
            "tier": "Pro",
            "status": "Active",
            "mrr": 500
        },
        {
            "name": "Global Dynamics",
            "email": "info@globaldynamics.example.com",
            "tier": "Enterprise",
            "status": "Active",
            "mrr": 5000
        },
        {
            "name": "SmallBiz LLC",
            "email": "contact@smallbiz.example.com",
            "tier": "Starter",
            "status": "Trial",
            "mrr": 0
        },
        {
            "name": "Innovation Labs",
            "email": "team@innovationlabs.example.com",
            "tier": "Pro",
            "status": "Active",
            "mrr": 750
        }
    ]
    
    created_count = 0
    skipped_count = 0
    
    for client_data in demo_clients:
        try:
            # Check if client already exists
            existing = notion.databases.query(
                database_id=client_db_id,
                filter={
                    "property": "Name",
                    "title": {
                        "equals": client_data["name"]
                    }
                }
            )
            
            if existing['results']:
                log_event('client_exists', {'name': client_data["name"]})
                skipped_count += 1
                continue
            
            # Create Notion page
            notion.pages.create(
                parent={"database_id": client_db_id},
                properties={
                    "Name": {"title": [{"text": {"content": client_data["name"]}}]},
                    "Email": {"email": client_data["email"]},
                    "Tier": {"select": {"name": client_data["tier"]}},
                    "Status": {"select": {"name": client_data["status"]}},
                    "MRR": {"number": client_data["mrr"]}
                }
            )
            created_count += 1
            log_event('client_created', {'name': client_data["name"], 'tier': client_data["tier"]})
        
        except Exception as e:
            log_event('client_creation_error', {'name': client_data["name"], 'error': str(e)})
    
    log_event('clients_summary', {'created': created_count, 'skipped': skipped_count})
    return created_count

def create_demo_automations(notion, queue_db_id):
    """Create demo automation queue items (idempotent)"""
    demo_tasks = [
        {
            "task": "Generate Q4 financial report with revenue breakdown and cost analysis",
            "status": "Pending",
            "priority": "High",
            "client": "Acme Corporation"
        },
        {
            "task": "Create customer onboarding email sequence with welcome materials",
            "status": "In Progress",
            "priority": "Medium",
            "client": "TechStart Inc"
        },
        {
            "task": "Analyze website traffic trends and prepare SEO recommendations",
            "status": "Complete",
            "priority": "Medium",
            "client": "Global Dynamics"
        },
        {
            "task": "Draft product launch announcement for social media channels",
            "status": "Pending",
            "priority": "High",
            "client": "Innovation Labs"
        },
        {
            "task": "Compile customer feedback survey results with sentiment analysis",
            "status": "Complete",
            "priority": "Low",
            "client": "Acme Corporation"
        },
        {
            "task": "Create monthly newsletter with product updates and tips",
            "status": "Pending",
            "priority": "Medium",
            "client": "TechStart Inc"
        }
    ]
    
    created_count = 0
    skipped_count = 0
    
    for task_data in demo_tasks:
        try:
            # Check if task already exists (match first 50 chars)
            existing = notion.databases.query(
                database_id=queue_db_id,
                filter={
                    "property": "Task",
                    "title": {
                        "contains": task_data["task"][:30]  # Use substring match
                    }
                }
            )
            
            if existing['results']:
                log_event('automation_exists', {'task': task_data["task"][:50]})
                skipped_count += 1
                continue
            
            notion.pages.create(
                parent={"database_id": queue_db_id},
                properties={
                    "Task": {"title": [{"text": {"content": task_data["task"]}}]},
                    "Status": {"select": {"name": task_data["status"]}},
                    "Priority": {"select": {"name": task_data["priority"]}},
                    "Client": {"rich_text": [{"text": {"content": task_data["client"]}}]}
                }
            )
            created_count += 1
            log_event('automation_created', {'task': task_data["task"][:50], 'status': task_data["status"]})
        
        except Exception as e:
            log_event('automation_creation_error', {'task': task_data["task"][:50], 'error': str(e)})
    
    log_event('automations_summary', {'created': created_count, 'skipped': skipped_count})
    return created_count

def create_demo_finance(notion, finance_db_id):
    """Create demo finance records (idempotent)"""
    # Generate last 6 months of revenue data
    demo_finance = []
    base_date = datetime.utcnow() - timedelta(days=180)
    
    for i in range(6):
        month_date = base_date + timedelta(days=30 * i)
        revenue = random.randint(8000, 15000)
        costs = int(revenue * random.uniform(0.3, 0.5))
        profit = revenue - costs
        
        demo_finance.append({
            "month": month_date.strftime("%Y-%m"),
            "revenue": revenue,
            "costs": costs,
            "profit": profit,
            "margin": round((profit / revenue) * 100, 1) if revenue > 0 else 0
        })
    
    created_count = 0
    skipped_count = 0
    
    for finance_data in demo_finance:
        try:
            # Check if month already exists
            existing = notion.databases.query(
                database_id=finance_db_id,
                filter={
                    "property": "Month",
                    "title": {
                        "equals": finance_data["month"]
                    }
                }
            )
            
            if existing['results']:
                log_event('finance_exists', {'month': finance_data["month"]})
                skipped_count += 1
                continue
            
            notion.pages.create(
                parent={"database_id": finance_db_id},
                properties={
                    "Month": {"title": [{"text": {"content": finance_data["month"]}}]},
                    "Revenue": {"number": finance_data["revenue"]},
                    "Costs": {"number": finance_data["costs"]},
                    "Profit": {"number": finance_data["profit"]},
                    "Margin": {"number": finance_data["margin"]}
                }
            )
            created_count += 1
            log_event('finance_created', {'month': finance_data["month"], 'revenue': finance_data["revenue"]})
        
        except Exception as e:
            log_event('finance_creation_error', {'month': finance_data["month"], 'error': str(e)})
    
    log_event('finance_summary', {'created': created_count, 'skipped': skipped_count})
    return created_count

def create_demo_growth_metrics(notion, growth_db_id):
    """Create demo growth metrics (idempotent)"""
    # Generate last 30 days of growth data
    demo_metrics = []
    base_date = datetime.utcnow() - timedelta(days=30)
    
    for i in range(30):
        date = base_date + timedelta(days=i)
        signups = random.randint(5, 25)
        activations = int(signups * random.uniform(0.6, 0.9))
        churn = random.randint(0, 3)
        
        demo_metrics.append({
            "date": date.strftime("%Y-%m-%d"),
            "signups": signups,
            "activations": activations,
            "churn": churn,
            "retention": round(((activations - churn) / max(activations, 1)) * 100, 1)
        })
    
    created_count = 0
    skipped_count = 0
    
    # Only create last 7 days to avoid overwhelming the database
    for metric_data in demo_metrics[-7:]:
        try:
            # Check if date already exists
            existing = notion.databases.query(
                database_id=growth_db_id,
                filter={
                    "property": "Date",
                    "title": {
                        "equals": metric_data["date"]
                    }
                }
            )
            
            if existing['results']:
                log_event('growth_metric_exists', {'date': metric_data["date"]})
                skipped_count += 1
                continue
            
            notion.pages.create(
                parent={"database_id": growth_db_id},
                properties={
                    "Date": {"title": [{"text": {"content": metric_data["date"]}}]},
                    "Signups": {"number": metric_data["signups"]},
                    "Activations": {"number": metric_data["activations"]},
                    "Churn": {"number": metric_data["churn"]},
                    "Retention": {"number": metric_data["retention"]}
                }
            )
            created_count += 1
            log_event('growth_metric_created', {'date': metric_data["date"], 'signups': metric_data["signups"]})
        
        except Exception as e:
            log_event('growth_metric_creation_error', {'date': metric_data["date"], 'error': str(e)})
    
    log_event('growth_metrics_summary', {'created': created_count, 'skipped': skipped_count})
    return created_count

def create_demo_partners(notion, partners_db_id):
    """Create demo partner records (idempotent)"""
    demo_partners = [
        {
            "name": "CloudHost Pro",
            "type": "Infrastructure",
            "status": "Active",
            "commission": 15
        },
        {
            "name": "PayGate Solutions",
            "type": "Payment",
            "status": "Active",
            "commission": 10
        },
        {
            "name": "Analytics Plus",
            "type": "Analytics",
            "status": "Active",
            "commission": 20
        },
        {
            "name": "SecureVault",
            "type": "Security",
            "status": "Pending",
            "commission": 12
        }
    ]
    
    created_count = 0
    skipped_count = 0
    
    for partner_data in demo_partners:
        try:
            # Check if partner already exists
            existing = notion.databases.query(
                database_id=partners_db_id,
                filter={
                    "property": "Name",
                    "title": {
                        "equals": partner_data["name"]
                    }
                }
            )
            
            if existing['results']:
                log_event('partner_exists', {'name': partner_data["name"]})
                skipped_count += 1
                continue
            
            notion.pages.create(
                parent={"database_id": partners_db_id},
                properties={
                    "Name": {"title": [{"text": {"content": partner_data["name"]}}]},
                    "Type": {"select": {"name": partner_data["type"]}},
                    "Status": {"select": {"name": partner_data["status"]}},
                    "Commission": {"number": partner_data["commission"]}
                }
            )
            created_count += 1
            log_event('partner_created', {'name': partner_data["name"], 'type': partner_data["type"]})
        
        except Exception as e:
            log_event('partner_creation_error', {'name': partner_data["name"], 'error': str(e)})
    
    log_event('partners_summary', {'created': created_count, 'skipped': skipped_count})
    return created_count

def main():
    """Main seeding logic"""
    log_event('seed_started', {'ok': True})
    
    print("\n🌱 EchoPilot Demo Data Seeder", flush=True)
    print("=" * 50, flush=True)
    
    try:
        # Initialize Notion client
        notion = get_notion_client()
        
        # Get database IDs from environment
        databases = {
            'clients': os.getenv('NOTION_CLIENT_DB_ID'),
            'automation_queue': os.getenv('AUTOMATION_QUEUE_DB_ID'),
            'finance': os.getenv('NOTION_FINANCE_DB_ID'),
            'growth_metrics': os.getenv('NOTION_GROWTH_METRICS_DB_ID'),
            'partners': os.getenv('NOTION_PARTNERS_DB_ID')
        }
        
        # Check which databases are configured
        configured = {k: v for k, v in databases.items() if v}
        missing = [k for k, v in databases.items() if not v]
        
        if missing:
            print(f"\n⚠️  Warning: Missing database IDs for: {', '.join(missing)}", flush=True)
            print(f"   Will seed only configured databases.\n", flush=True)
        
        total_created = 0
        
        # Seed clients
        if 'clients' in configured:
            print("📊 Seeding clients...", flush=True)
            count = create_demo_clients(notion, configured['clients'])
            print(f"   Created {count} demo clients", flush=True)
            total_created += count
        
        # Seed automation queue
        if 'automation_queue' in configured:
            print("⚙️  Seeding automation queue...", flush=True)
            count = create_demo_automations(notion, configured['automation_queue'])
            print(f"   Created {count} demo tasks", flush=True)
            total_created += count
        
        # Seed finance records
        if 'finance' in configured:
            print("💰 Seeding finance records...", flush=True)
            count = create_demo_finance(notion, configured['finance'])
            print(f"   Created {count} finance entries (last 6 months)", flush=True)
            total_created += count
        
        # Seed growth metrics
        if 'growth_metrics' in configured:
            print("📈 Seeding growth metrics...", flush=True)
            count = create_demo_growth_metrics(notion, configured['growth_metrics'])
            print(f"   Created {count} growth metrics (last 7 days)", flush=True)
            total_created += count
        
        # Seed partners
        if 'partners' in configured:
            print("🤝 Seeding partners...", flush=True)
            count = create_demo_partners(notion, configured['partners'])
            print(f"   Created {count} demo partners", flush=True)
            total_created += count
        
        print("=" * 50, flush=True)
        print(f"✅ Demo seeding complete!", flush=True)
        print(f"   Total records created: {total_created}", flush=True)
        print(f"   Databases seeded: {len(configured)}/{len(databases)}", flush=True)
        
        log_event('seed_complete', {
            'ok': True,
            'total_records': total_created,
            'databases_seeded': len(configured)
        })
        
    except Exception as e:
        log_event('seed_error', {'error': str(e), 'type': type(e).__name__})
        print(f"\n❌ Demo seeding failed: {e}", file=sys.stderr, flush=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
