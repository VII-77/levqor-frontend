#!/usr/bin/env python3
"""
Quick Setup - Configure EchoPilot with database IDs
"""

import os
import sys

def save_to_secrets(queue_id, log_id, job_id):
    """Save database IDs to .env file"""
    with open('.env', 'w') as f:
        f.write(f"# EchoPilot Database Configuration\n")
        f.write(f"AUTOMATION_QUEUE_DB_ID={queue_id}\n")
        f.write(f"AUTOMATION_LOG_DB_ID={log_id}\n")
        f.write(f"JOB_LOG_DB_ID={job_id}\n")
    print("\n✅ Configuration saved to .env file!")

def validate_id(db_id):
    """Basic validation for Notion database ID"""
    # Notion IDs are 32 characters (UUID without hyphens) or 36 with hyphens
    clean_id = db_id.replace('-', '')
    return len(clean_id) == 32 and clean_id.isalnum()

def main():
    print("\n" + "=" * 80)
    print("🚀 ECHOPILOT QUICK SETUP")
    print("=" * 80 + "\n")
    
    print("This script will configure your Notion database IDs.\n")
    
    print("📋 You need 3 database IDs from Notion:\n")
    print("   1. Automation Queue Database")
    print("   2. Automation Log Database")
    print("   3. EchoPilot Job Log Database\n")
    
    print("🔍 HOW TO GET DATABASE IDs:\n")
    print("   1. Open each database in Notion (full page view)")
    print("   2. Look at the URL: https://notion.so/workspace/DATABASE_ID?v=...")
    print("   3. Copy the 32-character ID between the last / and ?\n")
    print("   Example ID: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6\n")
    print("=" * 80 + "\n")
    
    # Option 1: Manual input
    print("📝 ENTER YOUR DATABASE IDs:\n")
    
    queue_id = input("Automation Queue Database ID: ").strip()
    log_id = input("Automation Log Database ID: ").strip()
    job_id = input("Job Log Database ID: ").strip()
    
    print("\n🔍 Validating IDs...\n")
    
    if not all([queue_id, log_id, job_id]):
        print("❌ Error: All database IDs are required!")
        sys.exit(1)
    
    # Basic validation
    valid = True
    if not validate_id(queue_id):
        print(f"⚠️  Warning: Queue ID format looks incorrect: {queue_id}")
        valid = False
    if not validate_id(log_id):
        print(f"⚠️  Warning: Log ID format looks incorrect: {log_id}")
        valid = False
    if not validate_id(job_id):
        print(f"⚠️  Warning: Job ID format looks incorrect: {job_id}")
        valid = False
    
    if not valid:
        proceed = input("\nIDs look unusual. Proceed anyway? (y/n): ").strip().lower()
        if proceed != 'y':
            print("❌ Setup cancelled.")
            sys.exit(1)
    
    # Save configuration
    save_to_secrets(queue_id, log_id, job_id)
    
    print("\n" + "=" * 80)
    print("✅ SETUP COMPLETE!")
    print("=" * 80 + "\n")
    
    print("📋 Configuration Summary:")
    print(f"   AUTOMATION_QUEUE_DB_ID = {queue_id}")
    print(f"   AUTOMATION_LOG_DB_ID = {log_id}")
    print(f"   JOB_LOG_DB_ID = {job_id}\n")
    
    print("🔐 IMPORTANT - Add these to Replit Secrets:")
    print("   1. Click the 🔒 'Secrets' tab in Replit")
    print("   2. Add each of the 3 database IDs as secrets")
    print("   3. Or the bot will use the .env file automatically\n")
    
    print("🚀 NEXT STEPS:")
    print("   1. Restart the 'EchoPilot Bot' workflow")
    print("   2. The bot will start processing tasks automatically")
    print("   3. Check the console for 'Health Check: Healthy' message\n")
    
    print("✅ Your EchoPilot bot is ready to go!\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
