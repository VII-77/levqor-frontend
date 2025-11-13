-- Phase 6.4: Database-backed feature flags and generic KV store

-- Feature flags table
CREATE TABLE IF NOT EXISTS feature_flags (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Generic key-value store for runtime config
CREATE TABLE IF NOT EXISTS kv (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_kv_key ON kv(key);
CREATE INDEX IF NOT EXISTS idx_flags_key ON feature_flags(key);
