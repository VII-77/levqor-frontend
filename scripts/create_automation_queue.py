#!/usr/bin/env python3
"""
Create Automation Queue Database in Notion
This is the core database needed for task processing
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.notion_api import get_notion_client

def create_automation_queue_database():
    """Create the Automation Queue database in Notion"""
    
    print("="*70)
    print("CREATE AUTOMATION QUEUE DATABASE")
    print("="*70)
    
    # Get Notion client
    try:
        notion = get_notion_client()
        print("✅ Connected to Notion")
    except Exception as e:
        print(f"❌ Failed to connect to Notion: {e}")
        return None
    
    # Get parent page ID
    parent_page_id = os.getenv('NOTION_PARENT_PAGE_ID')
    if not parent_page_id:
        print("❌ NOTION_PARENT_PAGE_ID environment variable not set")
        print("   Please set it to a page ID in your Notion workspace")
        return None
    
    print(f"✅ Parent page ID: {parent_page_id}")
    
    # Define database schema - MUST match what the code expects!
    properties = {
        "Task": {
            "title": {}
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "Pending", "color": "gray"},
                    {"name": "InProgress", "color": "blue"},
                    {"name": "Completed", "color": "green"},
                    {"name": "Failed", "color": "red"}
                ]
            }
        },
        "Trigger": {
            "checkbox": {}
        },
        "Priority": {
            "select": {
                "options": [
                    {"name": "Low", "color": "gray"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "High", "color": "orange"},
                    {"name": "Critical", "color": "red"}
                ]
            }
        },
        "Assigned To": {
            "rich_text": {}
        },
        "Details": {
            "rich_text": {}
        },
        "Result": {
            "rich_text": {}
        },
        "Created": {
            "created_time": {}
        },
        "Updated": {
            "last_edited_time": {}
        }
    }
    
    # Create database
    try:
        print("\n🔨 Creating 'Automation Queue' database...")
        response = notion.databases.create(
            parent={"page_id": parent_page_id},
            title=[{"type": "text", "text": {"content": "Automation Queue"}}],
            properties=properties
        )
        
        database_id = response['id']
        print(f"✅ Successfully created Automation Queue database!")
        print(f"   Database ID: {database_id}")
        print(f"\n📝 Add this to your Secrets:")
        print(f"   AUTOMATION_QUEUE_DB_ID={database_id}")
        print(f"\n⚠️  IMPORTANT: Share this database with your Notion integration:")
        print(f"   1. Open the database in Notion")
        print(f"   2. Click '...' menu → 'Connections'")
        print(f"   3. Add your integration and confirm")
        
        return database_id
        
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        print(f"\nTroubleshooting:")
        print(f"  1. Make sure NOTION_PARENT_PAGE_ID points to a valid page")
        print(f"  2. Make sure your Notion integration has access to that page")
        print(f"  3. Check that your Notion token is valid")
        return None

if __name__ == "__main__":
    database_id = create_automation_queue_database()
    
    if database_id:
        print("\n" + "="*70)
        print("✅ SUCCESS!")
        print("="*70)
        print("\nNext steps:")
        print("1. Open Notion and find the new 'Automation Queue' database")
        print("2. Share it with your integration (••• → Connections)")
        print("3. Add the database ID to your Secrets")
        print("4. Restart the EchoPilot Bot workflow")
        print("\nWithin 60 seconds, the error should disappear!")
    else:
        print("\n" + "="*70)
        print("❌ FAILED")
        print("="*70)
        sys.exit(1)
