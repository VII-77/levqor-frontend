#!/usr/bin/env python3
"""
EchoPilot Tenantization Hardening (Phase 116)
Middleware and utilities for tenant isolation and cross-tenant access prevention
"""

import json
from datetime import datetime
from pathlib import Path
from functools import wraps
from flask import request, g, jsonify

def log_tenant_event(event_type, details=None):
    """Log tenant-related security events"""
    log_entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event_type': event_type,
        'details': details or {}
    }
    
    log_file = Path('logs/tenant_security.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def extract_tenant_id():
    """
    Extract tenant_id from request context
    Sources (in priority order):
    1. X-Tenant-ID header
    2. tenant_id query parameter
    3. Bearer token claims (if present)
    4. Default to 'default' tenant
    """
    # Check header first
    tenant_id = request.headers.get('X-Tenant-ID')
    if tenant_id:
        return tenant_id.strip()
    
    # Check query parameter
    tenant_id = request.args.get('tenant_id')
    if tenant_id:
        return tenant_id.strip()
    
    # Check if we have a decoded JWT token with tenant claim
    if hasattr(g, 'jwt_claims') and g.jwt_claims:
        tenant_id = g.jwt_claims.get('tenant_id')
        if tenant_id:
            return tenant_id
    
    # Default tenant for backward compatibility
    return 'default'

def set_tenant_context():
    """
    Middleware to extract and set tenant context on Flask g object
    Call this early in request processing
    """
    g.tenant_id = extract_tenant_id()
    g.tenant_verified = False
    
    # Log tenant access
    log_tenant_event('tenant_access', {
        'tenant_id': g.tenant_id,
        'path': request.path,
        'method': request.method,
        'ip': request.remote_addr
    })

def require_tenant(allowed_tenants=None):
    """
    Decorator to enforce tenant access control on endpoints
    
    Args:
        allowed_tenants: List of allowed tenant IDs, or None for any authenticated tenant
    
    Usage:
        @app.route('/api/data')
        @require_tenant(['tenant_a', 'tenant_b'])
        def get_data():
            # Only tenant_a and tenant_b can access
            return jsonify(data)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'tenant_id'):
                set_tenant_context()
            
            tenant_id = g.tenant_id
            
            # Check if tenant is allowed
            if allowed_tenants and tenant_id not in allowed_tenants:
                log_tenant_event('tenant_access_denied', {
                    'tenant_id': tenant_id,
                    'allowed_tenants': allowed_tenants,
                    'path': request.path,
                    'method': request.method
                })
                
                return jsonify({
                    'ok': False,
                    'error': 'Access denied: tenant not authorized',
                    'tenant_id': tenant_id
                }), 403
            
            # Mark tenant as verified
            g.tenant_verified = True
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def check_cross_tenant_access(resource_tenant_id, action='access'):
    """
    Check if current tenant can access resource from another tenant
    
    Args:
        resource_tenant_id: Tenant ID that owns the resource
        action: Action being performed (access, modify, delete)
    
    Returns:
        (allowed: bool, reason: str)
    """
    if not hasattr(g, 'tenant_id'):
        set_tenant_context()
    
    current_tenant = g.tenant_id
    
    # Same tenant - always allowed
    if current_tenant == resource_tenant_id:
        return True, 'same_tenant'
    
    # Default tenant has read-only access to all tenants (for admin purposes)
    if current_tenant == 'default' and action == 'access':
        log_tenant_event('cross_tenant_admin_access', {
            'admin_tenant': current_tenant,
            'resource_tenant': resource_tenant_id,
            'action': action
        })
        return True, 'admin_access'
    
    # All other cross-tenant access denied
    log_tenant_event('cross_tenant_access_denied', {
        'requesting_tenant': current_tenant,
        'resource_tenant': resource_tenant_id,
        'action': action,
        'path': request.path
    })
    
    return False, 'cross_tenant_denied'

def filter_by_tenant(items, tenant_field='tenant_id'):
    """
    Filter list of items to only include those belonging to current tenant
    
    Args:
        items: List of dicts/objects with tenant_id field
        tenant_field: Name of the tenant ID field (default: 'tenant_id')
    
    Returns:
        Filtered list
    """
    if not hasattr(g, 'tenant_id'):
        set_tenant_context()
    
    current_tenant = g.tenant_id
    
    filtered = []
    for item in items:
        # Handle dict
        if isinstance(item, dict):
            item_tenant = item.get(tenant_field)
        # Handle object with attribute
        elif hasattr(item, tenant_field):
            item_tenant = getattr(item, tenant_field)
        else:
            # Skip items without tenant info
            continue
        
        # Include if same tenant or default tenant (admin)
        if item_tenant == current_tenant or current_tenant == 'default':
            filtered.append(item)
    
    return filtered

def get_tenant_stats():
    """Get tenant access statistics from logs"""
    try:
        log_file = Path('logs/tenant_security.ndjson')
        if not log_file.exists():
            return {
                'total_events': 0,
                'tenants': {},
                'denied_access': 0
            }
        
        stats = {
            'total_events': 0,
            'tenants': {},
            'denied_access': 0,
            'cross_tenant_denied': 0
        }
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    stats['total_events'] += 1
                    
                    event_type = entry.get('event_type')
                    tenant_id = entry.get('details', {}).get('tenant_id', 'unknown')
                    
                    # Count by tenant
                    if tenant_id not in stats['tenants']:
                        stats['tenants'][tenant_id] = 0
                    stats['tenants'][tenant_id] += 1
                    
                    # Count denials
                    if 'denied' in event_type:
                        stats['denied_access'] += 1
                    if 'cross_tenant' in event_type and 'denied' in event_type:
                        stats['cross_tenant_denied'] += 1
                        
                except:
                    continue
        
        return stats
        
    except Exception as e:
        return {
            'error': str(e),
            'total_events': 0
        }

if __name__ == '__main__':
    # Test tenant extraction and validation
    print("Testing tenancy utilities...")
    
    # Simulate request context
    class MockRequest:
        def __init__(self):
            self.headers = {'X-Tenant-ID': 'test_tenant'}
            self.args = {}
            self.path = '/test'
            self.method = 'GET'
            self.remote_addr = '127.0.0.1'
    
    class MockG:
        pass
    
    # Test cross-tenant check
    print("\nTest 1: Same tenant access")
    g = MockG()
    g.tenant_id = 'tenant_a'
    allowed, reason = check_cross_tenant_access('tenant_a', 'access')
    print(f"  Allowed: {allowed}, Reason: {reason}")
    
    print("\nTest 2: Cross-tenant access (denied)")
    allowed, reason = check_cross_tenant_access('tenant_b', 'access')
    print(f"  Allowed: {allowed}, Reason: {reason}")
    
    print("\nTest 3: Admin access")
    g.tenant_id = 'default'
    allowed, reason = check_cross_tenant_access('tenant_a', 'access')
    print(f"  Allowed: {allowed}, Reason: {reason}")
    
    print("\nTest 4: Filter by tenant")
    items = [
        {'id': 1, 'tenant_id': 'tenant_a', 'name': 'Item A'},
        {'id': 2, 'tenant_id': 'tenant_b', 'name': 'Item B'},
        {'id': 3, 'tenant_id': 'tenant_a', 'name': 'Item C'},
    ]
    g.tenant_id = 'tenant_a'
    filtered = filter_by_tenant(items)
    print(f"  Original: {len(items)} items, Filtered: {len(filtered)} items")
    
    print("\n✓ Tenancy tests complete")
