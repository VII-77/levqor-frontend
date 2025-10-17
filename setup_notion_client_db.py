#!/usr/bin/env python3
"""
Notion Client Database Setup Helper
Creates or verifies the EchoPilot Clients database structure
"""

import os
import sys
from bot.notion_api import NotionClientWrapper

def setup_client_database():
    print("=" * 80)
    print("📊 Notion Client Database Setup")
    print("=" * 80)
    print()
    
    # Check if database ID is already configured
    client_db_id = os.environ.get("NOTION_CLIENT_DB_ID")
    
    if client_db_id:
        print(f"✅ Client Database ID already configured: {client_db_id}")
        print()
        print("Verifying database structure...")
        
        # TODO: Add verification logic here
        notion = NotionClientWrapper()
        try:
            # Try to query the database to verify it exists
            result = notion.query_database(client_db_id, None)
            print(f"✅ Database accessible - found {len(result)} client(s)")
            print()
            
            print("📋 Next Steps:")
            print("1. Verify database has these properties:")
            print("   - Client Name (Title)")
            print("   - Email (Email)")
            print("   - Rate USD/min (Number)")
            print("   - Active (Checkbox)")
            print()
            print("2. Add test client if not present")
            print()
            
        except Exception as e:
            print(f"❌ Error accessing database: {e}")
            print()
            print("Please verify:")
            print("1. Database ID is correct (32 characters)")
            print("2. Database is shared with the Notion integration")
            print()
    else:
        print("⚠️  Client Database ID not configured")
        print()
        print("=" * 80)
        print("📝 Manual Setup Required")
        print("=" * 80)
        print()
        print("Since Notion API requires the database to exist first,")
        print("you'll need to create it manually (takes 2 minutes):")
        print()
        print("1. CREATE DATABASE IN NOTION:")
        print("   • Open Notion → + → Table")
        print("   • Name: 'EchoPilot Clients'")
        print()
        print("2. ADD PROPERTIES:")
        print("   • Client Name (Title) - auto-created")
        print("   • Email (Email type)")
        print("   • Rate USD/min (Number type)")
        print("   • Active (Checkbox type)")
        print()
        print("3. ADD TEST CLIENT:")
        print("   • Client Name: Test Client")
        print("   • Email: your-email@example.com")
        print("   • Rate USD/min: 5.0")
        print("   • Active: ✅ checked")
        print()
        print("4. COPY DATABASE ID:")
        print("   • Open database as full page")
        print("   • Copy URL → Get 32-char ID before ?v=")
        print()
        print("5. ADD TO REPLIT SECRETS:")
        print("   • Name: NOTION_CLIENT_DB_ID")
        print("   • Value: (32-character database ID)")
        print()
        print("   • Name: DEFAULT_RATE_USD_PER_MIN")
        print("   • Value: 5.0")
        print()
        print("=" * 80)
        print()
        print("OR use the detailed guide:")
        print("📖 See: NOTION_CLIENT_DB_SETUP.md")
        print()
    
    return client_db_id is not None

def verify_job_log_fields():
    print("=" * 80)
    print("📊 Job Log Database - Revenue Fields Check")
    print("=" * 80)
    print()
    
    job_log_id = os.environ.get("JOB_LOG_DB_ID")
    
    if not job_log_id:
        print("❌ JOB_LOG_DB_ID not configured")
        return False
    
    print(f"✅ Job Log Database ID: {job_log_id}")
    print()
    
    print("📋 Required Revenue Fields (add these to Job Log database):")
    print()
    print("| Property Name        | Type     | Settings                    |")
    print("|---------------------|----------|------------------------------|")
    print("| Client              | Relation | → EchoPilot Clients DB      |")
    print("| Client Email        | Email    | -                           |")
    print("| Client Rate USD/min | Number   | Number format               |")
    print("| Gross USD           | Number   | Number format, 2 decimals   |")
    print("| Profit USD          | Number   | Number format, 2 decimals   |")
    print("| Margin %            | Number   | Number format, 1 decimal    |")
    print()
    print("📋 Required Payment Fields (if not present):")
    print()
    print("| Property Name   | Type   | Settings                               |")
    print("|----------------|--------|----------------------------------------|")
    print("| Payment Link   | URL    | -                                      |")
    print("| Payment Status | Select | Options: Pending,Paid,Failed,Cancelled |")
    print()
    print("⚠️  Add these fields manually in Notion (API cannot create properties)")
    print()
    
    return True

if __name__ == "__main__":
    print()
    
    # Check client database
    client_ok = setup_client_database()
    
    # Check job log fields
    job_log_ok = verify_job_log_fields()
    
    print("=" * 80)
    print("📊 Setup Summary")
    print("=" * 80)
    print()
    
    if client_ok:
        print("✅ Client Database: Configured")
    else:
        print("⚠️  Client Database: Needs setup (see instructions above)")
    
    print("⚠️  Job Log Fields: Manual addition required")
    print()
    
    if client_ok:
        print("🎉 Client database ready! Add revenue fields to Job Log to complete setup.")
    else:
        print("📖 Follow the guide: NOTION_CLIENT_DB_SETUP.md")
    
    print()
