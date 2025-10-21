#!/usr/bin/env python3
"""
EchoPilot Partner/Affiliate Portal (Phase 129)
Partner management with revenue sharing and analytics
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

def register_partner(partner_name, partner_email, tier='standard'):
    """Register new partner"""
    import uuid
    
    partner_id = f"PTR_{str(uuid.uuid4())[:8].upper()}"
    
    # Commission tiers
    commission_rates = {
        'standard': 0.15,   # 15%
        'premium': 0.20,    # 20%
        'elite': 0.30       # 30%
    }
    
    partner = {
        'partner_id': partner_id,
        'name': partner_name,
        'email': partner_email,
        'tier': tier,
        'commission_rate': commission_rates.get(tier, 0.15),
        'registered_at': datetime.utcnow().isoformat() + 'Z',
        'status': 'active',
        'api_key': f"pk_{str(uuid.uuid4())[:16]}"
    }
    
    # Log registration
    log_file = Path('logs/partner_portal.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps({
            'ts': datetime.utcnow().isoformat() + 'Z',
            'event_type': 'partner_registered',
            **partner
        }) + '\n')
    
    return partner

def track_partner_sale(partner_id, sale_amount, customer_id):
    """Track partner-referred sale"""
    import uuid
    
    # Get partner commission rate
    partner_info = get_partner_info(partner_id)
    commission_rate = partner_info.get('commission_rate', 0.15)
    commission_amount = sale_amount * commission_rate
    
    sale = {
        'sale_id': str(uuid.uuid4())[:8],
        'partner_id': partner_id,
        'customer_id': customer_id,
        'sale_amount': sale_amount,
        'commission_rate': commission_rate,
        'commission_amount': commission_amount,
        'sale_date': datetime.utcnow().isoformat() + 'Z',
        'payout_status': 'pending'
    }
    
    # Log sale
    log_file = Path('logs/partner_portal.ndjson')
    with open(log_file, 'a') as f:
        f.write(json.dumps({
            'ts': datetime.utcnow().isoformat() + 'Z',
            'event_type': 'partner_sale',
            **sale
        }) + '\n')
    
    return sale

def get_partner_info(partner_id):
    """Get partner information"""
    try:
        log_file = Path('logs/partner_portal.ndjson')
        if not log_file.exists():
            return {'error': 'Partner not found'}
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if (entry.get('event_type') == 'partner_registered' and
                        entry.get('partner_id') == partner_id):
                        return entry
                except:
                    continue
        
        return {'error': 'Partner not found'}
        
    except Exception as e:
        return {'error': str(e)}

def get_partner_dashboard(partner_id, days=30):
    """Get partner performance dashboard"""
    try:
        log_file = Path('logs/partner_portal.ndjson')
        if not log_file.exists():
            return {
                'total_sales': 0,
                'total_commission': 0.0,
                'sales': []
            }
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        stats = {
            'sales_count': 0,
            'total_revenue': 0.0,
            'total_commission': 0.0,
            'sales': []
        }
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    
                    if entry.get('event_type') != 'partner_sale':
                        continue
                    
                    if entry.get('partner_id') != partner_id:
                        continue
                    
                    entry_time = datetime.fromisoformat(entry['ts'].replace('Z', '+00:00'))
                    if entry_time < cutoff:
                        continue
                    
                    stats['sales_count'] += 1
                    stats['total_revenue'] += entry.get('sale_amount', 0.0)
                    stats['total_commission'] += entry.get('commission_amount', 0.0)
                    stats['sales'].append({
                        'sale_id': entry.get('sale_id'),
                        'amount': entry.get('sale_amount'),
                        'commission': entry.get('commission_amount'),
                        'date': entry.get('sale_date')
                    })
                    
                except:
                    continue
        
        # Get partner info
        partner_info = get_partner_info(partner_id)
        
        return {
            'partner_id': partner_id,
            'partner_name': partner_info.get('name', 'Unknown'),
            'tier': partner_info.get('tier', 'standard'),
            'commission_rate': partner_info.get('commission_rate', 0.15),
            'period_days': days,
            'total_sales': stats['sales_count'],
            'total_revenue': round(stats['total_revenue'], 2),
            'total_commission': round(stats['total_commission'], 2),
            'pending_payout': round(stats['total_commission'], 2),
            'recent_sales': stats['sales'][-10:]
        }
        
    except Exception as e:
        return {'error': str(e)}

def get_all_partners_summary():
    """Get summary of all partners"""
    try:
        log_file = Path('logs/partner_portal.ndjson')
        if not log_file.exists():
            return {'partners': [], 'total': 0}
        
        partners = []
        partner_sales = defaultdict(lambda: {
            'sales': 0,
            'revenue': 0.0,
            'commission': 0.0
        })
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    
                    if entry.get('event_type') == 'partner_registered':
                        partners.append({
                            'partner_id': entry.get('partner_id'),
                            'name': entry.get('name'),
                            'tier': entry.get('tier'),
                            'status': entry.get('status')
                        })
                    
                    elif entry.get('event_type') == 'partner_sale':
                        pid = entry.get('partner_id')
                        partner_sales[pid]['sales'] += 1
                        partner_sales[pid]['revenue'] += entry.get('sale_amount', 0.0)
                        partner_sales[pid]['commission'] += entry.get('commission_amount', 0.0)
                        
                except:
                    continue
        
        # Merge partner info with sales
        for partner in partners:
            pid = partner['partner_id']
            partner.update(partner_sales[pid])
        
        # Sort by revenue
        partners.sort(key=lambda x: x.get('revenue', 0.0), reverse=True)
        
        return {
            'partners': partners,
            'total': len(partners),
            'total_sales': sum(p.get('sales', 0) for p in partners),
            'total_revenue': round(sum(p.get('revenue', 0.0) for p in partners), 2),
            'total_commission': round(sum(p.get('commission', 0.0) for p in partners), 2)
        }
        
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    # Test partner portal
    print("Testing Partner Portal...")
    
    print("\n1. Register partners")
    p1 = register_partner('Acme Solutions', 'sales@acme.com', 'premium')
    p2 = register_partner('Beta Corp', 'partner@beta.com', 'standard')
    print(f"  Partner 1: {p1['partner_id']} ({p1['commission_rate']*100}%)")
    print(f"  Partner 2: {p2['partner_id']} ({p2['commission_rate']*100}%)")
    
    print("\n2. Track sales")
    track_partner_sale(p1['partner_id'], 500.0, 'cust_001')
    track_partner_sale(p1['partner_id'], 750.0, 'cust_002')
    track_partner_sale(p2['partner_id'], 300.0, 'cust_003')
    
    print("\n3. Get partner dashboard")
    dashboard = get_partner_dashboard(p1['partner_id'])
    print(json.dumps(dashboard, indent=2))
    
    print("\n4. Get all partners summary")
    summary = get_all_partners_summary()
    print(f"  Total partners: {summary['total']}")
    print(f"  Total revenue: ${summary['total_revenue']}")
    print(f"  Total commission: ${summary['total_commission']}")
    
    print("\n✓ Partner Portal tests complete")
