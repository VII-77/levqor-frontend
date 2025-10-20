#!/usr/bin/env python3
"""Phase 91: Multi-Tenant Core - Tenant Isolation System"""
import os, sys, json
from datetime import datetime

TENANT_DEFAULT_LIMITS = json.loads(os.getenv('TENANT_DEFAULT_LIMITS_JSON', '{"max_jobs":1000,"max_ai_usd":50}'))

def load_tenants():
    if os.path.exists('data/tenants.json'):
        with open('data/tenants.json', 'r') as f:
            return json.load(f)
    return {}

def save_tenants(tenants):
    os.makedirs('data', exist_ok=True)
    with open('data/tenants.json', 'w') as f:
        json.dump(tenants, f, indent=2)

def create_tenant(tenant_id, name, limits=None):
    tenants = load_tenants()
    if tenant_id in tenants:
        return {"ok": False, "error": "Tenant exists"}
    
    tenants[tenant_id] = {
        "name": name,
        "created": datetime.utcnow().isoformat() + "Z",
        "limits": limits or TENANT_DEFAULT_LIMITS,
        "status": "active"
    }
    save_tenants(tenants)
    return {"ok": True, "tenant": tenants[tenant_id]}

def get_tenant_stats():
    tenants = load_tenants()
    return {
        "ok": True,
        "ts": datetime.utcnow().isoformat() + "Z",
        "total_tenants": len(tenants),
        "active_tenants": sum(1 for t in tenants.values() if t.get('status') == 'active')
    }

if __name__ == "__main__":
    result = get_tenant_stats()
    print(json.dumps(result, indent=2))
