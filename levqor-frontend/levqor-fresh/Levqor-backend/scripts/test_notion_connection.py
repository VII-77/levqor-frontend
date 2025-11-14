#!/usr/bin/env python3
"""
Test Notion Integration Connection
Verifies that Notion API is accessible and database IDs are configured
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_notion_connection():
    """Test Notion API connection"""
    print("🔍 Testing Notion Integration...\n")
    
    # Check required environment variables
    print("1️⃣  Checking environment variables...")
    hostname = os.getenv("REPLIT_CONNECTORS_HOSTNAME")
    repl_identity = os.getenv("REPL_IDENTITY")
    web_renewal = os.getenv("WEB_REPL_RENEWAL")
    
    if not hostname:
        print("❌ REPLIT_CONNECTORS_HOSTNAME not found")
        return False
    
    if not repl_identity and not web_renewal:
        print("❌ No REPL_IDENTITY or WEB_REPL_RENEWAL found")
        return False
    
    print("✅ Environment variables OK")
    
    # Check database IDs
    print("\n2️⃣  Checking database IDs...")
    health_db = os.getenv("NOTION_HEALTH_DB_ID", "").strip()
    cost_db = os.getenv("NOTION_COST_DB_ID", "").strip()
    pulse_db = os.getenv("NOTION_PULSE_DB_ID", "").strip()
    
    db_status = []
    if health_db:
        print(f"✅ NOTION_HEALTH_DB_ID configured ({len(health_db)} chars)")
        db_status.append(True)
    else:
        print("⚠️  NOTION_HEALTH_DB_ID not configured")
        db_status.append(False)
    
    if cost_db:
        print(f"✅ NOTION_COST_DB_ID configured ({len(cost_db)} chars)")
        db_status.append(True)
    else:
        print("⚠️  NOTION_COST_DB_ID not configured")
        db_status.append(False)
    
    if pulse_db:
        print(f"✅ NOTION_PULSE_DB_ID configured ({len(pulse_db)} chars)")
        db_status.append(True)
    else:
        print("⚠️  NOTION_PULSE_DB_ID not configured")
        db_status.append(False)
    
    # Test API connection
    print("\n3️⃣  Testing Notion API connection...")
    try:
        from server.notion_helper import NotionHelper
        
        notion = NotionHelper()
        access_token = notion._get_access_token()
        
        if access_token:
            print(f"✅ Successfully authenticated with Notion")
            print(f"   Token length: {len(access_token)} characters")
        else:
            print("❌ Failed to get access token")
            return False
            
    except Exception as e:
        print(f"❌ Notion API connection failed: {str(e)}")
        return False
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    if all(db_status):
        print("✅ All database IDs configured")
        print("✅ Notion API connection successful")
        print("\n🎉 Notion integration is ready to use!")
        print("\nNext steps:")
        print("1. Test automation scripts:")
        print("   python3 scripts/automation/health_monitor.py")
        print("   python3 scripts/automation/cost_collector.py")
        print("   python3 scripts/automation/weekly_pulse.py")
        print("\n2. Check Notion databases for new entries")
        return True
    else:
        configured = sum(db_status)
        total = len(db_status)
        print(f"⚠️  {configured}/{total} database IDs configured")
        print("✅ Notion API connection successful")
        print("\n📝 TODO: Add missing database IDs to Replit Secrets:")
        if not health_db:
            print("   - NOTION_HEALTH_DB_ID")
        if not cost_db:
            print("   - NOTION_COST_DB_ID")
        if not pulse_db:
            print("   - NOTION_PULSE_DB_ID")
        print("\nSee NOTION-SETUP-GUIDE.md for instructions")
        return False

if __name__ == "__main__":
    success = test_notion_connection()
    exit(0 if success else 1)
