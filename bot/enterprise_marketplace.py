#!/usr/bin/env python3
"""
EchoPilot Enterprise Marketplace (Phase 126)
Partner integration marketplace with revenue sharing
"""

import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

def log_marketplace_event(event_type, details=None):
    """Log marketplace events"""
    log_entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event_type': event_type,
        'details': details or {}
    }
    
    log_file = Path('logs/marketplace.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

# Marketplace listings
MARKETPLACE_LISTINGS = {
    'premium_ai_pack': {
        'id': 'premium_ai_pack',
        'name': 'Premium AI Pack',
        'description': 'Access to GPT-4, Claude 3, and Gemini Pro',
        'provider': 'EchoPilot',
        'category': 'ai_models',
        'price_usd': 99.00,
        'revenue_share': 0.0,
        'status': 'active'
    },
    'enterprise_support': {
        'id': 'enterprise_support',
        'name': 'Enterprise Support',
        'description': '24/7 support with 1-hour SLA',
        'provider': 'EchoPilot',
        'category': 'support',
        'price_usd': 499.00,
        'revenue_share': 0.0,
        'status': 'active'
    },
    'custom_workflows': {
        'id': 'custom_workflows',
        'name': 'Custom Workflow Builder',
        'description': 'Professional workflow design service',
        'provider': 'Partner: FlowCraft',
        'category': 'services',
        'price_usd': 299.00,
        'revenue_share': 0.30,
        'status': 'active'
    },
    'compliance_suite': {
        'id': 'compliance_suite',
        'name': 'Compliance Suite Pro',
        'description': 'GDPR, SOC2, HIPAA compliance automation',
        'provider': 'Partner: ComplianceAI',
        'category': 'compliance',
        'price_usd': 799.00,
        'revenue_share': 0.25,
        'status': 'active'
    }
}

def get_marketplace_listings(category=None):
    """Get marketplace listings"""
    listings = MARKETPLACE_LISTINGS.copy()
    
    if category:
        listings = {
            k: v for k, v in listings.items()
            if v.get('category') == category
        }
    
    return {
        'listings': list(listings.values()),
        'total': len(listings),
        'categories': list(set(l['category'] for l in listings.values()))
    }

def purchase_listing(listing_id, tenant_id, quantity=1):
    """Purchase a marketplace listing"""
    if listing_id not in MARKETPLACE_LISTINGS:
        return {
            'purchased': False,
            'error': 'Listing not found'
        }
    
    listing = MARKETPLACE_LISTINGS[listing_id]
    
    total_price = listing['price_usd'] * quantity
    revenue_share_amount = total_price * listing.get('revenue_share', 0.0)
    echopilot_revenue = total_price - revenue_share_amount
    
    purchase = {
        'purchase_id': f"PUR_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        'listing_id': listing_id,
        'tenant_id': tenant_id,
        'quantity': quantity,
        'total_price_usd': total_price,
        'revenue_share_usd': revenue_share_amount,
        'echopilot_revenue_usd': echopilot_revenue,
        'purchased_at': datetime.utcnow().isoformat() + 'Z',
        'status': 'completed'
    }
    
    log_marketplace_event('purchase_completed', purchase)
    
    return {
        'purchased': True,
        **purchase
    }

def get_revenue_report():
    """Get marketplace revenue report"""
    try:
        log_file = Path('logs/marketplace.ndjson')
        if not log_file.exists():
            return {
                'total_revenue': 0.0,
                'partner_share': 0.0,
                'echopilot_revenue': 0.0,
                'purchase_count': 0
            }
        
        stats = {
            'total': 0.0,
            'partner_share': 0.0,
            'echopilot': 0.0,
            'purchases': 0,
            'by_listing': defaultdict(lambda: {
                'count': 0,
                'revenue': 0.0
            })
        }
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get('event_type') == 'purchase_completed':
                        details = entry.get('details', {})
                        
                        stats['total'] += details.get('total_price_usd', 0.0)
                        stats['partner_share'] += details.get('revenue_share_usd', 0.0)
                        stats['echopilot'] += details.get('echopilot_revenue_usd', 0.0)
                        stats['purchases'] += 1
                        
                        listing_id = details.get('listing_id')
                        stats['by_listing'][listing_id]['count'] += 1
                        stats['by_listing'][listing_id]['revenue'] += details.get('total_price_usd', 0.0)
                        
                except:
                    continue
        
        return {
            'total_revenue': round(stats['total'], 2),
            'partner_share': round(stats['partner_share'], 2),
            'echopilot_revenue': round(stats['echopilot'], 2),
            'purchase_count': stats['purchases'],
            'by_listing': dict(stats['by_listing'])
        }
        
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    # Test marketplace
    print("Testing Enterprise Marketplace...")
    
    print("\n1. Get listings")
    listings = get_marketplace_listings()
    print(f"  Total listings: {listings['total']}")
    print(f"  Categories: {listings['categories']}")
    
    print("\n2. Purchase listings")
    purchase_listing('premium_ai_pack', 'tenant_a', quantity=1)
    purchase_listing('custom_workflows', 'tenant_b', quantity=2)
    
    print("\n3. Get revenue report")
    report = get_revenue_report()
    print(json.dumps(report, indent=2))
    
    print("\n✓ Enterprise Marketplace tests complete")
