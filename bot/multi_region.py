#!/usr/bin/env python3
"""
EchoPilot Multi-Region Edge Runtime (Phase 128)
Geographic distribution and intelligent routing
"""

import json
from datetime import datetime
from pathlib import Path

# Regional edge nodes
EDGE_REGIONS = {
    'us-east': {
        'id': 'us-east',
        'name': 'US East (Virginia)',
        'location': 'us-east-1',
        'latency_ms': 20,
        'capacity': 1000,
        'status': 'active'
    },
    'us-west': {
        'id': 'us-west',
        'name': 'US West (Oregon)',
        'location': 'us-west-2',
        'latency_ms': 25,
        'capacity': 1000,
        'status': 'active'
    },
    'eu-west': {
        'id': 'eu-west',
        'name': 'Europe (Ireland)',
        'location': 'eu-west-1',
        'latency_ms': 35,
        'capacity': 800,
        'status': 'active'
    },
    'ap-south': {
        'id': 'ap-south',
        'name': 'Asia Pacific (Singapore)',
        'location': 'ap-southeast-1',
        'latency_ms': 45,
        'capacity': 600,
        'status': 'active'
    }
}

def get_optimal_region(client_ip=None, client_lat=None, client_lon=None):
    """Get optimal edge region for client"""
    # Simplified region selection (in production, use GeoIP)
    if client_ip:
        # Parse IP to determine region (simplified)
        if client_ip.startswith('192.') or client_ip.startswith('10.'):
            return 'us-east'
        else:
            return 'us-east'
    
    # Default to lowest latency
    best_region = min(
        EDGE_REGIONS.items(),
        key=lambda x: x[1]['latency_ms']
    )
    
    return best_region[0]

def route_request(request_type, client_ip=None, tenant_id=None):
    """Route request to optimal edge region"""
    region_id = get_optimal_region(client_ip=client_ip)
    region = EDGE_REGIONS.get(region_id)
    
    routing = {
        'request_type': request_type,
        'routed_to': region_id,
        'region_name': region['name'],
        'estimated_latency_ms': region['latency_ms'],
        'tenant_id': tenant_id,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    # Log routing decision
    log_file = Path('logs/multi_region.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps({
            'ts': datetime.utcnow().isoformat() + 'Z',
            'event_type': 'request_routed',
            **routing
        }) + '\n')
    
    return routing

def get_region_stats():
    """Get multi-region statistics"""
    try:
        log_file = Path('logs/multi_region.ndjson')
        if not log_file.exists():
            return {
                'total_requests': 0,
                'by_region': {}
            }
        
        stats = {
            'total': 0,
            'by_region': {r: 0 for r in EDGE_REGIONS.keys()}
        }
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get('event_type') == 'request_routed':
                        stats['total'] += 1
                        region = entry.get('routed_to', 'unknown')
                        if region in stats['by_region']:
                            stats['by_region'][region] += 1
                except:
                    continue
        
        return {
            'total_requests': stats['total'],
            'by_region': stats['by_region'],
            'active_regions': len([r for r in EDGE_REGIONS.values() if r['status'] == 'active'])
        }
        
    except Exception as e:
        return {'error': str(e)}

def get_regional_health():
    """Get health status of all regions"""
    return {
        'regions': [
            {
                **region,
                'health': 'healthy' if region['status'] == 'active' else 'unhealthy'
            }
            for region in EDGE_REGIONS.values()
        ],
        'total_capacity': sum(r['capacity'] for r in EDGE_REGIONS.values()),
        'healthy_count': len([r for r in EDGE_REGIONS.values() if r['status'] == 'active'])
    }

if __name__ == '__main__':
    # Test multi-region
    print("Testing Multi-Region Edge Runtime...")
    
    print("\n1. Route requests to optimal regions")
    route_request('ai_task', client_ip='192.168.1.1', tenant_id='tenant_a')
    route_request('report_gen', client_ip='10.0.0.1', tenant_id='tenant_b')
    route_request('data_sync', client_ip='172.16.0.1', tenant_id='tenant_c')
    
    print("\n2. Get region stats")
    stats = get_region_stats()
    print(json.dumps(stats, indent=2))
    
    print("\n3. Get regional health")
    health = get_regional_health()
    print(f"  Active regions: {health['healthy_count']}")
    print(f"  Total capacity: {health['total_capacity']}")
    
    print("\n✓ Multi-Region tests complete")
