#!/usr/bin/env python3
"""
Create EchoPilot Clients Database in Notion
"""

import os
from bot.notion_api import NotionClientWrapper

def create_clients_database():
    print("=" * 80)
    print("📊 Creating EchoPilot Clients Database in Notion")
    print("=" * 80)
    print()
    
    notion = NotionClientWrapper()
    client = notion.get_client()
    
    # Search for a suitable parent page or use workspace
    print("🔍 Searching for workspace pages...")
    
    try:
        # Search for pages to find a suitable parent
        search_results = client.search(
            filter={"property": "object", "value": "page"}
        ).get("results", [])
        
        if search_results:
            print(f"✅ Found {len(search_results)} pages in workspace")
            print()
            
            # Use the first page as parent, or let user choose
            parent_page = search_results[0]
            parent_id = parent_page["id"]
            parent_title = parent_page.get("properties", {}).get("title", {})
            
            # Try to get page title
            page_name = "Workspace"
            if parent_title and parent_title.get("title"):
                page_name = parent_title["title"][0]["plain_text"] if parent_title["title"] else "Workspace"
            
            print(f"📍 Creating database under: {page_name}")
            print()
        else:
            print("⚠️  No pages found, will try to create at workspace level")
            parent_id = None
    except Exception as e:
        print(f"⚠️  Could not search pages: {e}")
        print("Will attempt to create at workspace level")
        parent_id = None
        print()
    
    # Define the database schema
    print("🏗️  Creating database with schema...")
    print()
    
    database_properties = {
        "Client Name": {"title": {}},
        "Email": {"email": {}},
        "Rate USD/min": {"number": {"format": "number"}},
        "Active": {"checkbox": {}}
    }
    
    try:
        # Create the database
        if parent_id:
            new_database = client.databases.create(
                parent={"type": "page_id", "page_id": parent_id},
                title=[{"type": "text", "text": {"content": "EchoPilot Clients"}}],
                properties=database_properties
            )
        else:
            # Try workspace parent
            new_database = client.databases.create(
                parent={"type": "workspace", "workspace": True},
                title=[{"type": "text", "text": {"content": "EchoPilot Clients"}}],
                properties=database_properties
            )
        
        database_id = new_database["id"]
        
        print("✅ Database created successfully!")
        print(f"📋 Database ID: {database_id}")
        print()
        
        # Add a test client
        print("👤 Adding test client...")
        
        test_client = client.pages.create(
            parent={"database_id": database_id},
            properties={
                "Client Name": {"title": [{"text": {"content": "Test Client"}}]},
                "Email": {"email": "test@example.com"},
                "Rate USD/min": {"number": 5.0},
                "Active": {"checkbox": True}
            }
        )
        
        print("✅ Test client added!")
        print()
        
        print("=" * 80)
        print("🎉 SUCCESS! Database Created")
        print("=" * 80)
        print()
        print("📋 Database Details:")
        print(f"   Name: EchoPilot Clients")
        print(f"   ID: {database_id}")
        print()
        print("✅ Properties created:")
        print("   • Client Name (Title)")
        print("   • Email (Email)")
        print("   • Rate USD/min (Number)")
        print("   • Active (Checkbox)")
        print()
        print("✅ Test client added:")
        print("   • Name: Test Client")
        print("   • Email: test@example.com")
        print("   • Rate: $5.00/min")
        print("   • Active: ✅")
        print()
        print("=" * 80)
        print("📱 NEXT STEP: Add to Replit Secrets")
        print("=" * 80)
        print()
        print("In Replit app → Tap ⋮ → Secrets → Add:")
        print()
        print(f"Secret Name: NOTION_CLIENT_DB_ID")
        print(f"Secret Value: {database_id}")
        print()
        print("Secret Name: DEFAULT_RATE_USD_PER_MIN")
        print("Secret Value: 5.0")
        print()
        print("🔄 The bot will auto-restart when you add the secrets!")
        print()
        
        return database_id
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        print()
        print("=" * 80)
        print("📝 Alternative: Manual Setup")
        print("=" * 80)
        print()
        print("If automatic creation failed, create manually:")
        print()
        print("1. Open Notion → + → Table → 'EchoPilot Clients'")
        print("2. Add properties: Client Name, Email, Rate USD/min, Active")
        print("3. Copy database ID from URL")
        print("4. Add to Replit Secrets: NOTION_CLIENT_DB_ID")
        print()
        print("📖 See: NOTION_CLIENT_DB_SETUP.md for detailed guide")
        print()
        return None

if __name__ == "__main__":
    database_id = create_clients_database()
    
    if database_id:
        print("✅ All done! Add the database ID to Replit Secrets to activate!")
    else:
        print("⚠️  See instructions above for manual setup")
    
    print()
