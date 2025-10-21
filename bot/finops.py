#!/usr/bin/env python3
"""
EchoPilot FinOps Cost & Profitability (Phase 117)
Track revenue, costs, margins, and profitability per tenant and globally
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

def log_finops_event(event_type, details=None):
    """Log FinOps events"""
    log_entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event_type': event_type,
        'details': details or {}
    }
    
    log_file = Path('logs/finops.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def get_ai_costs(tenant_id=None, days=30):
    """Calculate AI costs from job logs"""
    try:
        log_file = Path('logs/job_performance.ndjson')
        if not log_file.exists():
            return {'total_cost': 0.0, 'job_count': 0}
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        total_cost = 0.0
        job_count = 0
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry['ts'].replace('Z', '+00:00'))
                    
                    if entry_time < cutoff:
                        continue
                    
                    # Filter by tenant if specified
                    if tenant_id and entry.get('tenant_id') != tenant_id:
                        continue
                    
                    cost = entry.get('total_cost_usd', 0.0)
                    if cost > 0:
                        total_cost += cost
                        job_count += 1
                        
                except:
                    continue
        
        return {
            'total_cost': round(total_cost, 2),
            'job_count': job_count,
            'avg_cost_per_job': round(total_cost / job_count, 4) if job_count > 0 else 0.0
        }
        
    except Exception as e:
        log_finops_event('ai_cost_calc_error', {'error': str(e)})
        return {'total_cost': 0.0, 'job_count': 0, 'error': str(e)}

def get_stripe_revenue(tenant_id=None, days=30):
    """Calculate revenue from Stripe payments"""
    try:
        log_file = Path('logs/payment_reconciliation.ndjson')
        if not log_file.exists():
            return {'total_revenue': 0.0, 'payment_count': 0}
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        total_revenue = 0.0
        payment_count = 0
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    
                    if entry.get('event_type') != 'payment_success':
                        continue
                    
                    entry_time = datetime.fromisoformat(entry['ts'].replace('Z', '+00:00'))
                    if entry_time < cutoff:
                        continue
                    
                    # Filter by tenant if specified
                    if tenant_id and entry.get('details', {}).get('tenant_id') != tenant_id:
                        continue
                    
                    amount = entry.get('details', {}).get('amount_usd', 0.0)
                    if amount > 0:
                        total_revenue += amount
                        payment_count += 1
                        
                except:
                    continue
        
        return {
            'total_revenue': round(total_revenue, 2),
            'payment_count': payment_count,
            'avg_revenue_per_payment': round(total_revenue / payment_count, 2) if payment_count > 0 else 0.0
        }
        
    except Exception as e:
        log_finops_event('revenue_calc_error', {'error': str(e)})
        return {'total_revenue': 0.0, 'payment_count': 0, 'error': str(e)}

def get_infrastructure_costs(days=30):
    """Estimate infrastructure costs (simplified)"""
    # Rough estimates per day
    REPLIT_VM_COST_PER_DAY = 0.50  # Reserved VM estimate
    DATABASE_COST_PER_DAY = 0.10   # Postgres estimate
    
    total_cost = (REPLIT_VM_COST_PER_DAY + DATABASE_COST_PER_DAY) * days
    
    return {
        'total_cost': round(total_cost, 2),
        'breakdown': {
            'compute': round(REPLIT_VM_COST_PER_DAY * days, 2),
            'database': round(DATABASE_COST_PER_DAY * days, 2)
        }
    }

def calculate_profitability(revenue, costs):
    """Calculate profit margins and metrics"""
    total_revenue = revenue.get('total_revenue', 0.0)
    total_costs = sum([
        costs.get('ai', {}).get('total_cost', 0.0),
        costs.get('infrastructure', {}).get('total_cost', 0.0)
    ])
    
    profit = total_revenue - total_costs
    margin = (profit / total_revenue * 100) if total_revenue > 0 else 0.0
    
    return {
        'profit': round(profit, 2),
        'margin_pct': round(margin, 2),
        'total_revenue': total_revenue,
        'total_costs': round(total_costs, 2),
        'roi': round((profit / total_costs * 100) if total_costs > 0 else 0.0, 2)
    }

def get_finops_summary(tenant_id=None, days=30):
    """
    Get comprehensive FinOps summary with revenue, costs, and profitability
    
    Args:
        tenant_id: Filter by specific tenant (None for all)
        days: Analysis window in days
    
    Returns:
        dict with revenue, costs, profit, and metrics
    """
    try:
        # Get revenue
        revenue = get_stripe_revenue(tenant_id=tenant_id, days=days)
        
        # Get costs
        ai_costs = get_ai_costs(tenant_id=tenant_id, days=days)
        infra_costs = get_infrastructure_costs(days=days) if not tenant_id else {'total_cost': 0.0, 'breakdown': {}}
        
        costs = {
            'ai': ai_costs,
            'infrastructure': infra_costs
        }
        
        # Calculate profitability
        profitability = calculate_profitability(revenue, costs)
        
        # Build summary
        summary = {
            'ts': datetime.utcnow().isoformat() + 'Z',
            'tenant_id': tenant_id or 'all',
            'period_days': days,
            'revenue': revenue,
            'costs': costs,
            'profitability': profitability
        }
        
        # Log summary generation
        log_finops_event('summary_generated', {
            'tenant_id': tenant_id or 'all',
            'days': days,
            'profit': profitability['profit']
        })
        
        return summary
        
    except Exception as e:
        log_finops_event('summary_error', {'error': str(e)})
        raise

def get_tenant_breakdown(days=30):
    """Get cost and revenue breakdown by tenant"""
    try:
        # Get all AI costs by tenant
        log_file = Path('logs/job_performance.ndjson')
        if not log_file.exists():
            return {'tenants': {}}
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        tenant_data = defaultdict(lambda: {'costs': 0.0, 'jobs': 0})
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry['ts'].replace('Z', '+00:00'))
                    
                    if entry_time < cutoff:
                        continue
                    
                    tenant_id = entry.get('tenant_id', 'default')
                    cost = entry.get('total_cost_usd', 0.0)
                    
                    tenant_data[tenant_id]['costs'] += cost
                    tenant_data[tenant_id]['jobs'] += 1
                    
                except:
                    continue
        
        # Sort by cost descending
        sorted_tenants = dict(sorted(
            tenant_data.items(),
            key=lambda x: x[1]['costs'],
            reverse=True
        ))
        
        return {
            'tenants': {
                tid: {
                    'costs_usd': round(data['costs'], 2),
                    'job_count': data['jobs'],
                    'avg_cost_per_job': round(data['costs'] / data['jobs'], 4) if data['jobs'] > 0 else 0.0
                }
                for tid, data in sorted_tenants.items()
            },
            'total_tenants': len(sorted_tenants)
        }
        
    except Exception as e:
        log_finops_event('tenant_breakdown_error', {'error': str(e)})
        return {'tenants': {}, 'error': str(e)}

if __name__ == '__main__':
    # Test FinOps calculations
    print("Testing FinOps...")
    
    print("\n1. Global Summary (30 days)")
    summary = get_finops_summary(days=30)
    print(json.dumps(summary, indent=2))
    
    print("\n2. Tenant Breakdown")
    breakdown = get_tenant_breakdown(days=30)
    print(json.dumps(breakdown, indent=2))
    
    print("\n✓ FinOps tests complete")
