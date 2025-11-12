-- 002_seed_core.sql
-- LEVQOR v8.0 GENESIS - Seed Legacy "000-CORE" Tenant
-- Maps all existing users to core tenant for backward compatibility

-- Insert core tenant (idempotent)
WITH core AS (
  INSERT INTO tenants (ext_id, name, plan, region, status)
  VALUES ('000-CORE','Levqor Core','enterprise','eu-west-1','active')
  ON CONFLICT (ext_id) DO UPDATE SET name=EXCLUDED.name
  RETURNING id
)
-- Map all existing users to core tenant
INSERT INTO tenant_users (tenant_id, user_id, role)
SELECT 
  (SELECT id FROM core), 
  u.id::uuid, 
  'owner'
FROM users u
WHERE u.id IS NOT NULL
ON CONFLICT DO NOTHING;

-- Audit the seeding
INSERT INTO tenant_audit (tenant_id, event, actor, metadata)
SELECT 
  id,
  'tenant_seeded',
  'system',
  jsonb_build_object(
    'source', 'genesis_migration',
    'timestamp', NOW(),
    'users_mapped', (SELECT COUNT(*) FROM tenant_users WHERE tenant_id = id)
  )
FROM tenants
WHERE ext_id = '000-CORE';

-- Verify seeding
SELECT 
  t.ext_id,
  t.name,
  t.status,
  (SELECT COUNT(*) FROM tenant_users WHERE tenant_id = t.id) as user_count
FROM tenants t
WHERE t.ext_id = '000-CORE';
