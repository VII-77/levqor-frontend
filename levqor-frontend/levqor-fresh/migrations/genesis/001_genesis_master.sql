-- 001_genesis_master.sql
-- LEVQOR v8.0 GENESIS - Master Tenant Tables
-- Safe to run: idempotent, no behavior change until TENANCY_MODE switched

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Master tenant registry
CREATE TABLE IF NOT EXISTS tenants (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  ext_id TEXT UNIQUE,       -- human-readable ID (e.g., '000-CORE')
  name TEXT NOT NULL,
  plan TEXT NOT NULL DEFAULT 'enterprise',
  region TEXT NOT NULL DEFAULT 'eu-west-1',
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tenant user mappings
CREATE TABLE IF NOT EXISTS tenant_users (
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  user_id UUID NOT NULL,
  role TEXT NOT NULL DEFAULT 'owner',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (tenant_id, user_id)
);

-- Tenant audit log
CREATE TABLE IF NOT EXISTS tenant_audit (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  event TEXT NOT NULL,
  actor TEXT,
  metadata JSONB,
  ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create indices for performance
CREATE INDEX IF NOT EXISTS idx_tenant_users_tenant ON tenant_users(tenant_id);
CREATE INDEX IF NOT EXISTS idx_tenant_users_user ON tenant_users(user_id);
CREATE INDEX IF NOT EXISTS idx_tenant_audit_tenant ON tenant_audit(tenant_id);
CREATE INDEX IF NOT EXISTS idx_tenant_audit_ts ON tenant_audit(ts DESC);

-- Verify tables created
SELECT 'Genesis master tables created' AS status;
