#!/usr/bin/env python3
"""
Setup Automation Queue Database in Notion
Creates the automation queue database with all required properties
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.notion_api import get_notion_client

def create_automation_queue_database():
    """Create Automation Queue database in Notion"""
    
    notion = get_notion_client()
    parent_page_id = os.getenv('NOTION_PARENT_PAGE_ID')
    
    if not parent_page_id:
        print("❌ NOTION_PARENT_PAGE_ID not found in environment")
        print("   Please set this to your Notion workspace page ID")
        return None
    
    print("🔧 Creating Automation Queue database...")
    
    # Define database properties
    properties = {
        "Task Name": {
            "title": {}
        },
        "Trigger": {
            "checkbox": {}
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "Pending", "color": "gray"},
                    {"name": "In Progress", "color": "blue"},
                    {"name": "Completed", "color": "green"},
                    {"name": "Failed", "color": "red"},
                    {"name": "Cancelled", "color": "orange"}
                ]
            }
        },
        "Priority": {
            "select": {
                "options": [
                    {"name": "High", "color": "red"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "Low", "color": "gray"}
                ]
            }
        },
        "Assigned To": {
            "rich_text": {}
        },
        "Description": {
            "rich_text": {}
        },
        "Due Date": {
            "date": {}
        },
        "Created": {
            "created_time": {}
        },
        "Last Modified": {
            "last_edited_time": {}
        }
    }
    
    try:
        # Create the database
        response = notion.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            title=[
                {
                    "type": "text",
                    "text": {"content": "Automation Queue"}
                }
            ],
            properties=properties
        )
        
        database_id = response['id']
        print(f"✅ Automation Queue database created!")
        print(f"📋 Database ID: {database_id}")
        print()
        print("=" * 70)
        print("NEXT STEP: Add this to your Replit Secrets")
        print("=" * 70)
        print(f"Secret name:  AUTOMATION_QUEUE_DB_ID")
        print(f"Secret value: {database_id}")
        print()
        print("Instructions:")
        print("1. Click the lock icon 🔒 in the left sidebar")
        print("2. Click 'New secret'")
        print("3. Enter the name and value above")
        print("4. Click 'Add secret'")
        print("5. Restart the workflow")
        print()
        
        return database_id
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        print()
        print("Common issues:")
        print("- Make sure your Notion integration has access to the parent page")
        print("- Verify NOTION_PARENT_PAGE_ID is correct")
        return None

if __name__ == "__main__":
    print("=" * 70)
    print("Automation Queue Database Setup")
    print("=" * 70)
    print()
    
    db_id = create_automation_queue_database()
    
    if db_id:
        print("✅ Setup complete!")
        sys.exit(0)
    else:
        print("❌ Setup failed")
        sys.exit(1)
