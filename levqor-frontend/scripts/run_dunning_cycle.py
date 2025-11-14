#!/usr/bin/env python3
"""
Manual dunning cycle runner
Execute dunning email sends for scheduled events

Usage:
    python scripts/run_dunning_cycle.py
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import after path setup
from backend.billing.dunning import run_dunning_cycle
from backend.billing.config import DUNNING_ENABLED
import sqlite3

def main():
    print(f"Dunning Cycle Runner - {datetime.utcnow().isoformat()}")
    print(f"DUNNING_ENABLED: {DUNNING_ENABLED}")
    print()
    
    if not DUNNING_ENABLED:
        print("WARNING: DUNNING_ENABLED is False")
        print("No emails will be sent, but events will be processed in dry-run mode")
        print()
    
    # Get database connection
    db_path = os.environ.get("SQLITE_PATH", "levqor.db")
    print(f"Database: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"ERROR: Database not found at {db_path}")
        sys.exit(1)
    
    db = sqlite3.connect(db_path)
    
    # Check if dunning table exists
    cursor = db.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='billing_dunning_events'
    """)
    
    if not cursor.fetchone():
        print("ERROR: billing_dunning_events table does not exist")
        print("Please run migration: db/migrations/008_add_billing_dunning_events.sql")
        sys.exit(1)
    
    # Run dunning cycle
    print("Running dunning cycle...")
    now_utc = datetime.utcnow()
    
    stats = run_dunning_cycle(db, now_utc)
    
    print()
    print("=" * 60)
    print("DUNNING CYCLE COMPLETE")
    print("=" * 60)
    print(f"Processed: {stats['processed']}")
    print(f"Sent:      {stats['sent']}")
    print(f"Skipped:   {stats['skipped']}")
    print(f"Errors:    {stats['errors']}")
    print()
    
    if stats['errors'] > 0:
        print("⚠️  Some events had errors. Check logs for details.")
        sys.exit(1)
    
    if stats['sent'] > 0:
        print(f"✓ Successfully sent {stats['sent']} dunning emails")
    elif stats['skipped'] > 0:
        print(f"✓ Skipped {stats['skipped']} events (dunning disabled)")
    else:
        print("✓ No pending events to process")
    
    db.close()

if __name__ == "__main__":
    main()
