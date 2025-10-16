#!/usr/bin/env python3
"""Quick script to check if a task has been created in the database."""

from bot.notion_api import NotionClientWrapper
import os
from datetime import datetime

def check_tasks():
    print("=" * 70)
    print(f"🔍 TASK CHECK - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 70)
    
    notion = NotionClientWrapper()
    queue_id = os.getenv('AUTOMATION_QUEUE_DB_ID')
    
    # Get all tasks
    all_tasks = notion.query_database(queue_id)
    triggered_tasks = notion.get_triggered_tasks()
    
    print(f"\n📊 DATABASE STATUS:")
    print(f"   Total tasks: {len(all_tasks)}")
    print(f"   Triggered tasks (ready to process): {len(triggered_tasks)}")
    
    if triggered_tasks:
        print(f"\n✅ SUCCESS! Found {len(triggered_tasks)} triggered task(s):")
        print("-" * 70)
        for i, task in enumerate(triggered_tasks, 1):
            props = task.get('properties', {})
            name = props.get('Task Name', {}).get('title', [{}])[0].get('text', {}).get('content', 'Unnamed')
            desc = props.get('Description', {}).get('rich_text', [{}])[0].get('text', {}).get('content', 'No description')[:60]
            task_type = props.get('Task Type', {}).get('select', {}).get('name', 'Other')
            
            print(f"\n   Task {i}: {name}")
            print(f"   Type: {task_type}")
            print(f"   Description: {desc}...")
            print(f"   Trigger: ✅ CHECKED")
        
        print("\n" + "=" * 70)
        print("🚀 YOUR BOT WILL PROCESS THIS TASK WITHIN 60 SECONDS!")
        print("=" * 70)
        print("\n💡 Watch the bot logs to see it processing...")
        
    elif all_tasks:
        print(f"\n⚠️  Found {len(all_tasks)} task(s) but NONE have Trigger checked:")
        print("-" * 70)
        for i, task in enumerate(all_tasks, 1):
            props = task.get('properties', {})
            name = props.get('Task Name', {}).get('title', [{}])[0].get('text', {}).get('content', 'Unnamed')
            trigger = props.get('Trigger', {}).get('checkbox', False)
            
            print(f"\n   Task {i}: {name}")
            print(f"   Trigger: {'✅ CHECKED' if trigger else '☐ NOT CHECKED ← FIX THIS!'}")
        
        print("\n" + "=" * 70)
        print("❌ ACTION REQUIRED: Check the Trigger box on your task!")
        print("=" * 70)
    else:
        print(f"\n⚠️  DATABASE IS STILL EMPTY")
        print("-" * 70)
        print("   No tasks found in the database.")
        print("   Please create a task in Notion and try again.")
        print("=" * 70)

if __name__ == "__main__":
    check_tasks()
