#!/usr/bin/env python3
"""
Fix Automation Queue Database Schema
Adds the missing Trigger checkbox property
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.notion_api import get_notion_client

def fix_automation_queue_schema():
    """Add the Trigger checkbox property to existing database"""
    
    print("="*70)
    print("FIX AUTOMATION QUEUE SCHEMA")
    print("="*70)
    
    # Get Notion client
    try:
        notion = get_notion_client()
        print("✅ Connected to Notion")
    except Exception as e:
        print(f"❌ Failed to connect to Notion: {e}")
        return False
    
    # Get database ID
    db_id = os.getenv('AUTOMATION_QUEUE_DB_ID')
    if not db_id:
        print("❌ AUTOMATION_QUEUE_DB_ID environment variable not set")
        return False
    
    print(f"✅ Database ID: {db_id}")
    
    try:
        # First, check current schema
        print("\n🔍 Checking current database schema...")
        db_info = notion.databases.retrieve(database_id=db_id)
        props = db_info.get('properties', {})
        
        print(f"   Found {len(props)} properties:")
        for prop_name, prop_data in props.items():
            prop_type = prop_data.get('type', 'unknown')
            print(f"   - {prop_name}: {prop_type}")
        
        # Check if Trigger exists and what type it is
        if 'Trigger' in props:
            trigger_type = props['Trigger'].get('type')
            print(f"\n✅ 'Trigger' property exists (type: {trigger_type})")
            
            if trigger_type == 'checkbox':
                print("   ✅ Already correct type (checkbox)!")
                print("   No changes needed!")
                return True
            else:
                print(f"   ⚠️  Currently {trigger_type}, need to change to checkbox")
                print("   ⚠️  Notion doesn't allow changing property types via API")
                print("   📝 Manual fix needed:")
                print("   1. Open database: https://notion.so/" + db_id.replace("-", ""))
                print("   2. Click on 'Trigger' column header")
                print("   3. Delete the 'Trigger' property")
                print("   4. Add new property: Name='Trigger', Type='Checkbox'")
                return False
        else:
            # Add the Trigger checkbox property
            print("\n🔨 Adding 'Trigger' checkbox property...")
            
            notion.databases.update(
                database_id=db_id,
                properties={
                    "Trigger": {
                        "checkbox": {}
                    }
                }
            )
            
            print("✅ Successfully added 'Trigger' checkbox property!")
            print("\n🎉 Database schema fixed!")
            return True
            
    except Exception as e:
        print(f"❌ Failed to fix schema: {e}")
        return False

if __name__ == "__main__":
    success = fix_automation_queue_schema()
    
    if success:
        print("\n" + "="*70)
        print("✅ SUCCESS!")
        print("="*70)
        print("\nThe database schema is now correct!")
        print("Restart the EchoPilot Bot workflow and the errors should be gone!")
    else:
        print("\n" + "="*70)
        print("⚠️  MANUAL FIX NEEDED")
        print("="*70)
        sys.exit(1)
