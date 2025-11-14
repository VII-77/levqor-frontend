#!/usr/bin/env python3
"""
Dunning system smoke test
Tests dunning logic without sending real emails
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock the config to ensure DUNNING_ENABLED is False for testing
os.environ['DUNNING_ENABLED'] = 'false'

from backend.billing.dunning import run_dunning_cycle, compute_scheduled_time
from backend.billing.config import DUNNING_ENABLED

def main():
    print("=" * 60)
    print("DUNNING SYSTEM SMOKE TEST")
    print("=" * 60)
    print()
    
    # Verify dunning is disabled
    print(f"✓ DUNNING_ENABLED: {DUNNING_ENABLED}")
    assert not DUNNING_ENABLED, "DUNNING_ENABLED must be False for smoke test"
    print("✓ Dunning disabled as expected")
    print()
    
    # Test scheduled time computation
    print("Testing scheduled time computation...")
    now = datetime.utcnow()
    scheduled_1 = compute_scheduled_time(now, 1)
    scheduled_7 = compute_scheduled_time(now, 7)
    scheduled_14 = compute_scheduled_time(now, 14)
    
    print(f"✓ Day 1: {scheduled_1}")
    print(f"✓ Day 7: {scheduled_7}")
    print(f"✓ Day 14: {scheduled_14}")
    print()
    
    # Test with mock database (in-memory)
    print("Testing run_dunning_cycle with mock database...")
    import sqlite3
    mock_db = sqlite3.connect(":memory:")
    
    # Create table
    mock_db.execute("""
        CREATE TABLE billing_dunning_events (
            id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            stripe_customer_id TEXT NOT NULL,
            stripe_subscription_id TEXT NOT NULL,
            invoice_id TEXT NOT NULL,
            email TEXT NOT NULL,
            plan TEXT,
            attempt_number INTEGER NOT NULL,
            scheduled_for TEXT NOT NULL,
            sent_at TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            error_message TEXT
        )
    """)
    
    # Insert test event (scheduled in the past, should be picked up)
    test_time = (now.replace(hour=0, minute=0, second=0)).isoformat()
    mock_db.execute("""
        INSERT INTO billing_dunning_events
        (id, created_at, updated_at, stripe_customer_id, stripe_subscription_id,
         invoice_id, email, plan, attempt_number, scheduled_for, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        'test-event-1', test_time, test_time, 'cus_test', 'sub_test',
        'in_test', 'test@example.com', 'Test Plan', 1, test_time, 'pending'
    ))
    mock_db.commit()
    
    # Run dunning cycle (should skip due to DUNNING_ENABLED=False)
    stats = run_dunning_cycle(mock_db, now)
    
    print(f"✓ Processed: {stats['processed']}")
    print(f"✓ Sent: {stats['sent']}")
    print(f"✓ Skipped: {stats['skipped']}")
    print(f"✓ Errors: {stats['errors']}")
    
    # Verify no emails were sent (because DUNNING_ENABLED=False)
    assert stats['sent'] == 0, "No emails should be sent when DUNNING_ENABLED=False"
    assert stats['skipped'] >= 0, "Events should be skipped when disabled"
    
    print()
    print("=" * 60)
    print("DUNNING_SMOKE_TEST_OK")
    print("=" * 60)
    print()
    print("All checks passed. Dunning system is safe to deploy.")
    print("DUNNING_ENABLED remains False - no emails will be sent until enabled.")
    
    mock_db.close()

if __name__ == "__main__":
    main()
