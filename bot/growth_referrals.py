#!/usr/bin/env python3
"""
EchoPilot Growth & Marketing Referral 2.0 (Phase 120)
Advanced referral tracking with payout management and analytics
"""

import json
import csv
import io
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

def log_referral_event(event_type, details=None):
    """Log referral events"""
    log_entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event_type': event_type,
        'details': details or {}
    }
    
    log_file = Path('logs/referrals.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def create_referral(referrer_id, campaign='default'):
    """Create new referral link"""
    import uuid
    
    referral_code = str(uuid.uuid4())[:8].upper()
    
    referral = {
        'referral_code': referral_code,
        'referrer_id': referrer_id,
        'campaign': campaign,
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'clicks': 0,
        'signups': 0,
        'conversions': 0,
        'revenue_usd': 0.0,
        'payout_usd': 0.0,
        'payout_status': 'pending'
    }
    
    log_referral_event('referral_created', referral)
    
    return referral

def track_referral_click(referral_code):
    """Track click on referral link"""
    log_referral_event('referral_click', {
        'referral_code': referral_code,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    })
    
    return {'tracked': True}

def track_referral_signup(referral_code, user_id):
    """Track signup from referral"""
    log_referral_event('referral_signup', {
        'referral_code': referral_code,
        'user_id': user_id,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    })
    
    return {'tracked': True}

def track_referral_conversion(referral_code, user_id, revenue_usd):
    """Track conversion (paid subscription) from referral"""
    # Calculate commission (default 20%)
    commission_rate = 0.20
    payout_usd = revenue_usd * commission_rate
    
    log_referral_event('referral_conversion', {
        'referral_code': referral_code,
        'user_id': user_id,
        'revenue_usd': revenue_usd,
        'payout_usd': payout_usd,
        'commission_rate': commission_rate,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    })
    
    return {
        'tracked': True,
        'payout_usd': payout_usd
    }

def get_referral_stats(referrer_id=None, days=30):
    """Get referral statistics"""
    try:
        log_file = Path('logs/referrals.ndjson')
        if not log_file.exists():
            return {
                'referrals': [],
                'total_clicks': 0,
                'total_signups': 0,
                'total_conversions': 0,
                'total_revenue': 0.0,
                'total_payout': 0.0
            }
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        # Aggregate by referral code
        referrals = defaultdict(lambda: {
            'clicks': 0,
            'signups': 0,
            'conversions': 0,
            'revenue_usd': 0.0,
            'payout_usd': 0.0
        })
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry['ts'].replace('Z', '+00:00'))
                    
                    if entry_time < cutoff:
                        continue
                    
                    event_type = entry.get('event_type')
                    details = entry.get('details', {})
                    
                    # Filter by referrer if specified
                    if referrer_id and details.get('referrer_id') != referrer_id:
                        continue
                    
                    ref_code = details.get('referral_code')
                    if not ref_code:
                        continue
                    
                    # Track metrics
                    if event_type == 'referral_created':
                        referrals[ref_code]['referrer_id'] = details.get('referrer_id')
                        referrals[ref_code]['campaign'] = details.get('campaign', 'default')
                        referrals[ref_code]['created_at'] = entry['ts']
                    
                    elif event_type == 'referral_click':
                        referrals[ref_code]['clicks'] += 1
                    
                    elif event_type == 'referral_signup':
                        referrals[ref_code]['signups'] += 1
                    
                    elif event_type == 'referral_conversion':
                        referrals[ref_code]['conversions'] += 1
                        referrals[ref_code]['revenue_usd'] += details.get('revenue_usd', 0.0)
                        referrals[ref_code]['payout_usd'] += details.get('payout_usd', 0.0)
                        
                except:
                    continue
        
        # Convert to list
        referral_list = [
            {'referral_code': code, **data}
            for code, data in referrals.items()
        ]
        
        # Sort by revenue descending
        referral_list.sort(key=lambda x: x.get('revenue_usd', 0.0), reverse=True)
        
        # Calculate totals
        totals = {
            'referrals': referral_list,
            'total_referrals': len(referral_list),
            'total_clicks': sum(r.get('clicks', 0) for r in referral_list),
            'total_signups': sum(r.get('signups', 0) for r in referral_list),
            'total_conversions': sum(r.get('conversions', 0) for r in referral_list),
            'total_revenue': round(sum(r.get('revenue_usd', 0.0) for r in referral_list), 2),
            'total_payout': round(sum(r.get('payout_usd', 0.0) for r in referral_list), 2)
        }
        
        return totals
        
    except Exception as e:
        log_referral_event('stats_error', {'error': str(e)})
        return {'error': str(e)}

def export_payouts_csv(min_payout_usd=10.0):
    """Export referral payouts to CSV"""
    try:
        stats = get_referral_stats(days=365)  # Last year
        
        # Filter to payouts >= minimum
        payouts = [
            r for r in stats.get('referrals', [])
            if r.get('payout_usd', 0.0) >= min_payout_usd
        ]
        
        # Create CSV
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            'referral_code', 'referrer_id', 'campaign',
            'signups', 'conversions', 'revenue_usd', 'payout_usd'
        ])
        
        writer.writeheader()
        for payout in payouts:
            writer.writerow({
                'referral_code': payout.get('referral_code', ''),
                'referrer_id': payout.get('referrer_id', ''),
                'campaign': payout.get('campaign', ''),
                'signups': payout.get('signups', 0),
                'conversions': payout.get('conversions', 0),
                'revenue_usd': payout.get('revenue_usd', 0.0),
                'payout_usd': payout.get('payout_usd', 0.0)
            })
        
        csv_content = output.getvalue()
        output.close()
        
        log_referral_event('payout_export', {
            'payout_count': len(payouts),
            'total_payout_usd': sum(p.get('payout_usd', 0.0) for p in payouts)
        })
        
        return csv_content
        
    except Exception as e:
        log_referral_event('export_error', {'error': str(e)})
        return None

if __name__ == '__main__':
    # Test referral system
    print("Testing referral system...")
    
    print("\n1. Creating referral")
    referral = create_referral('user123', campaign='spring2025')
    print(f"  Referral code: {referral['referral_code']}")
    
    print("\n2. Tracking events")
    track_referral_click(referral['referral_code'])
    track_referral_signup(referral['referral_code'], 'new_user_1')
    track_referral_conversion(referral['referral_code'], 'new_user_1', 50.0)
    
    print("\n3. Getting stats")
    stats = get_referral_stats(referrer_id='user123')
    print(json.dumps(stats, indent=2))
    
    print("\n4. Exporting CSV")
    csv_data = export_payouts_csv(min_payout_usd=1.0)
    if csv_data:
        print(f"  CSV length: {len(csv_data)} chars")
        print("  Preview:")
        print(csv_data[:200])
    
    print("\n✓ Referral tests complete")
