#!/usr/bin/env python3
"""
EchoPilot AI Data Lake & Prompt Analytics (Phase 123)
Track prompt performance, token usage, and AI model effectiveness
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

def log_prompt_execution(prompt, model, tokens_used, cost_usd, latency_ms, response_quality=None):
    """Log AI prompt execution for analytics"""
    import hashlib
    
    # Create prompt fingerprint for tracking
    prompt_hash = hashlib.md5(prompt[:100].encode()).hexdigest()[:8]
    
    log_entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'prompt_hash': prompt_hash,
        'prompt_length': len(prompt),
        'model': model,
        'tokens_used': tokens_used,
        'cost_usd': cost_usd,
        'latency_ms': latency_ms,
        'response_quality': response_quality
    }
    
    log_file = Path('logs/ai_data_lake.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def get_prompt_analytics(days=7):
    """Get prompt performance analytics"""
    try:
        log_file = Path('logs/ai_data_lake.ndjson')
        if not log_file.exists():
            return {
                'total_prompts': 0,
                'total_tokens': 0,
                'total_cost': 0.0,
                'avg_latency_ms': 0.0
            }
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        stats = {
            'prompts': 0,
            'tokens': 0,
            'cost': 0.0,
            'latencies': [],
            'by_model': defaultdict(lambda: {
                'count': 0,
                'tokens': 0,
                'cost': 0.0,
                'latencies': []
            }),
            'by_quality': defaultdict(int)
        }
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry['ts'].replace('Z', '+00:00'))
                    
                    if entry_time < cutoff:
                        continue
                    
                    stats['prompts'] += 1
                    stats['tokens'] += entry.get('tokens_used', 0)
                    stats['cost'] += entry.get('cost_usd', 0.0)
                    stats['latencies'].append(entry.get('latency_ms', 0))
                    
                    # By model
                    model = entry.get('model', 'unknown')
                    stats['by_model'][model]['count'] += 1
                    stats['by_model'][model]['tokens'] += entry.get('tokens_used', 0)
                    stats['by_model'][model]['cost'] += entry.get('cost_usd', 0.0)
                    stats['by_model'][model]['latencies'].append(entry.get('latency_ms', 0))
                    
                    # By quality
                    quality = entry.get('response_quality')
                    if quality:
                        stats['by_quality'][quality] += 1
                        
                except:
                    continue
        
        # Calculate aggregates
        avg_latency = sum(stats['latencies']) / len(stats['latencies']) if stats['latencies'] else 0.0
        
        # Calculate per-model averages
        by_model_summary = {}
        for model, data in stats['by_model'].items():
            by_model_summary[model] = {
                'count': data['count'],
                'total_tokens': data['tokens'],
                'total_cost': round(data['cost'], 2),
                'avg_latency_ms': round(sum(data['latencies']) / len(data['latencies']), 2) if data['latencies'] else 0.0,
                'avg_cost_per_prompt': round(data['cost'] / data['count'], 4) if data['count'] > 0 else 0.0
            }
        
        return {
            'period_days': days,
            'total_prompts': stats['prompts'],
            'total_tokens': stats['tokens'],
            'total_cost': round(stats['cost'], 2),
            'avg_latency_ms': round(avg_latency, 2),
            'avg_cost_per_prompt': round(stats['cost'] / stats['prompts'], 4) if stats['prompts'] > 0 else 0.0,
            'by_model': by_model_summary,
            'quality_distribution': dict(stats['by_quality'])
        }
        
    except Exception as e:
        return {'error': str(e)}

def get_top_prompts(limit=10, days=7):
    """Get most frequently used prompts"""
    try:
        log_file = Path('logs/ai_data_lake.ndjson')
        if not log_file.exists():
            return {'prompts': []}
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        prompt_stats = defaultdict(lambda: {
            'count': 0,
            'total_cost': 0.0,
            'total_tokens': 0,
            'avg_latency': []
        })
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry['ts'].replace('Z', '+00:00'))
                    
                    if entry_time < cutoff:
                        continue
                    
                    prompt_hash = entry.get('prompt_hash')
                    prompt_stats[prompt_hash]['count'] += 1
                    prompt_stats[prompt_hash]['total_cost'] += entry.get('cost_usd', 0.0)
                    prompt_stats[prompt_hash]['total_tokens'] += entry.get('tokens_used', 0)
                    prompt_stats[prompt_hash]['avg_latency'].append(entry.get('latency_ms', 0))
                    
                except:
                    continue
        
        # Sort by count
        top_prompts = sorted(
            [
                {
                    'prompt_hash': h,
                    'execution_count': data['count'],
                    'total_cost': round(data['total_cost'], 2),
                    'total_tokens': data['total_tokens'],
                    'avg_latency_ms': round(sum(data['avg_latency']) / len(data['avg_latency']), 2) if data['avg_latency'] else 0.0
                }
                for h, data in prompt_stats.items()
            ],
            key=lambda x: x['execution_count'],
            reverse=True
        )[:limit]
        
        return {
            'prompts': top_prompts,
            'period_days': days
        }
        
    except Exception as e:
        return {'prompts': [], 'error': str(e)}

def get_model_comparison():
    """Compare AI model performance"""
    try:
        log_file = Path('logs/ai_data_lake.ndjson')
        if not log_file.exists():
            return {'models': []}
        
        model_stats = defaultdict(lambda: {
            'prompts': 0,
            'tokens': 0,
            'cost': 0.0,
            'latencies': []
        })
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    model = entry.get('model', 'unknown')
                    
                    model_stats[model]['prompts'] += 1
                    model_stats[model]['tokens'] += entry.get('tokens_used', 0)
                    model_stats[model]['cost'] += entry.get('cost_usd', 0.0)
                    model_stats[model]['latencies'].append(entry.get('latency_ms', 0))
                    
                except:
                    continue
        
        # Build comparison
        comparison = []
        for model, data in model_stats.items():
            comparison.append({
                'model': model,
                'total_prompts': data['prompts'],
                'total_tokens': data['tokens'],
                'total_cost': round(data['cost'], 2),
                'avg_cost_per_prompt': round(data['cost'] / data['prompts'], 4) if data['prompts'] > 0 else 0.0,
                'avg_latency_ms': round(sum(data['latencies']) / len(data['latencies']), 2) if data['latencies'] else 0.0,
                'cost_efficiency': round(data['tokens'] / data['cost'], 2) if data['cost'] > 0 else 0.0
            })
        
        # Sort by total prompts
        comparison.sort(key=lambda x: x['total_prompts'], reverse=True)
        
        return {'models': comparison}
        
    except Exception as e:
        return {'models': [], 'error': str(e)}

if __name__ == '__main__':
    # Test AI data lake
    print("Testing AI Data Lake...")
    
    print("\n1. Logging prompt executions")
    log_prompt_execution("Analyze customer feedback", "gpt-4o", 1500, 0.03, 850, "good")
    log_prompt_execution("Generate report summary", "gpt-4o-mini", 500, 0.005, 420, "excellent")
    log_prompt_execution("Analyze customer feedback", "gpt-4o", 1480, 0.029, 820, "good")
    
    print("\n2. Get prompt analytics (7 days)")
    analytics = get_prompt_analytics(days=7)
    print(json.dumps(analytics, indent=2))
    
    print("\n3. Get top prompts")
    top = get_top_prompts(limit=5)
    print(json.dumps(top, indent=2))
    
    print("\n4. Get model comparison")
    comparison = get_model_comparison()
    print(json.dumps(comparison, indent=2))
    
    print("\n✓ AI Data Lake tests complete")
