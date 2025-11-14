-- Migration: Add billing_dunning_events table for Stripe payment dunning system
-- Version: 008
-- Date: 2025-11-14
-- Description: Tracks scheduled and sent dunning emails for failed subscription payments

-- Billing dunning events table
CREATE TABLE IF NOT EXISTS billing_dunning_events (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    stripe_customer_id TEXT NOT NULL,
    stripe_subscription_id TEXT NOT NULL,
    invoice_id TEXT NOT NULL,
    email TEXT NOT NULL,
    plan TEXT,
    attempt_number INTEGER NOT NULL CHECK(attempt_number IN (1, 2, 3)),
    scheduled_for TEXT NOT NULL,
    sent_at TEXT,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'sent', 'skipped', 'error')),
    error_message TEXT
);

-- Indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_dunning_events_customer ON billing_dunning_events(stripe_customer_id);
CREATE INDEX IF NOT EXISTS idx_dunning_events_subscription ON billing_dunning_events(stripe_subscription_id);
CREATE INDEX IF NOT EXISTS idx_dunning_events_invoice ON billing_dunning_events(invoice_id);
CREATE INDEX IF NOT EXISTS idx_dunning_events_status ON billing_dunning_events(status);
CREATE INDEX IF NOT EXISTS idx_dunning_events_scheduled ON billing_dunning_events(scheduled_for, status);

-- Trigger to auto-update updated_at timestamp
CREATE TRIGGER IF NOT EXISTS update_dunning_events_timestamp 
AFTER UPDATE ON billing_dunning_events
BEGIN
    UPDATE billing_dunning_events SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- Comments (SQLite doesn't support COMMENT ON COLUMN, so documenting here)
-- id: UUID primary key
-- created_at: ISO8601 timestamp when event was created
-- updated_at: ISO8601 timestamp of last modification
-- stripe_customer_id: Stripe customer identifier (cus_xxx)
-- stripe_subscription_id: Stripe subscription identifier (sub_xxx)
-- invoice_id: Stripe invoice that failed payment (in_xxx)
-- email: Customer email address for dunning notification
-- plan: Human-readable subscription plan name (e.g., "Growth Monthly")
-- attempt_number: Email sequence number (1=Day 1, 2=Day 7, 3=Day 14)
-- scheduled_for: ISO8601 timestamp when email should be sent
-- sent_at: ISO8601 timestamp when email was actually sent (NULL if not sent)
-- status: Current state (pending, sent, skipped, error)
-- error_message: Error details if send failed (NULL if no error)
