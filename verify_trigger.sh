#!/bin/bash
echo "🔍 Verifying trigger checkbox status..."
echo ""
python3 << 'EOF'
from bot.notion_api import NotionClientWrapper
import os

notion = NotionClientWrapper()
queue_id = os.getenv('AUTOMATION_QUEUE_DB_ID')
triggered = notion.get_triggered_tasks()

if triggered:
    props = triggered[0].get('properties', {})
    name_prop = props.get('Task Name', {}).get('title', [])
    name = name_prop[0].get('text', {}).get('content', 'Unnamed') if name_prop else 'Unnamed'
    
    print("=" * 70)
    print("✅ SUCCESS! TRIGGER IS CHECKED!")
    print("=" * 70)
    print(f"\nTask: {name}")
    print(f"Trigger: ✅ CHECKED")
    print(f"\n🚀 Bot will process this task within 60 seconds!")
    print(f"   Watch for the AI-generated result in Notion...")
    print("=" * 70)
else:
    print("=" * 70)
    print("❌ TRIGGER STILL NOT CHECKED")
    print("=" * 70)
    print("\nThe checkbox is still empty. Please:")
    print("1. Open the task in Notion")
    print("2. Click the Trigger checkbox")
    print("3. Make sure you see a checkmark ✅")
    print("4. Refresh and verify it's still checked")
    print("=" * 70)
EOF
