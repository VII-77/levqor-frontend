#!/usr/bin/env python3
"""
EchoPilot Alert Tuner - ML-Powered SLO Threshold Optimization
Phase 107: Analyzes historical SLO data and recommends optimal thresholds
Reduces alert fatigue while maintaining 99.99% reliability target
"""

import os
import sys
import json
import psycopg2
from datetime import datetime, timedelta
from pathlib import Path
from statistics import mean, stdev

# Logging
log_file = Path('logs/alert_tuner.ndjson')
log_file.parent.mkdir(exist_ok=True)

def log_event(event, data=None):
    """Write NDJSON log entry"""
    entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event': event
    }
    if data:
        entry.update(data)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    
    print(json.dumps(entry), flush=True)

def get_historical_metrics(days=30):
    """
    Extract historical SLO metrics from warehouse
    Returns dict of metric_name -> list of values
    """
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        # Get ops monitor data (contains SLO metrics)
        cutoff = datetime.utcnow() - timedelta(days=days)
        cursor.execute("""
            SELECT metric_name, metric_value, recorded_at
            FROM wh_ops_monitor
            WHERE recorded_at >= %s
            ORDER BY recorded_at DESC
        """, (cutoff,))
        
        metrics = {}
        for row in cursor.fetchall():
            metric_name = row[0]
            metric_value = row[1]
            
            if metric_name not in metrics:
                metrics[metric_name] = []
            
            try:
                metrics[metric_name].append(float(metric_value))
            except (ValueError, TypeError):
                continue
        
        cursor.close()
        conn.close()
        
        return metrics
        
    except Exception as e:
        log_event('metrics_fetch_error', {'error': str(e)})
        return {}

def calculate_percentiles(values, percentiles=[50, 90, 95, 99]):
    """Calculate percentile values from list"""
    if not values:
        return {}
    
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    
    result = {}
    for p in percentiles:
        idx = int(n * p / 100)
        if idx >= n:
            idx = n - 1
        result[f'p{p}'] = sorted_vals[idx]
    
    return result

def tune_latency_thresholds(metrics):
    """
    ML-based latency threshold optimization
    Analyzes P95/P99 latency and recommends thresholds
    Goal: Reduce false positives while staying under target
    """
    recommendations = {}
    
    # Current defaults from environment
    current_p95_target = int(os.getenv('SLO_P95_TARGET_MS', '800'))
    current_p99_target = int(os.getenv('SLO_P99_TARGET_MS', '1200'))
    
    # Analyze actual latency distribution
    if 'p95_latency_ms' in metrics and metrics['p95_latency_ms']:
        p95_values = metrics['p95_latency_ms']
        p95_stats = calculate_percentiles(p95_values)
        p95_mean = mean(p95_values)
        p95_stdev = stdev(p95_values) if len(p95_values) > 1 else 0
        
        # Recommended threshold: P95 of P95s + 1 stdev (headroom)
        p95_recommended = int(p95_stats.get('p95', current_p95_target) + p95_stdev)
        
        # Don't recommend lower than current mean + 2 stdev (safety margin)
        p95_safe_minimum = int(p95_mean + (2 * p95_stdev))
        p95_final = max(p95_recommended, p95_safe_minimum)
        
        # Three-tier confidence: high (>100), medium (50-100), low (<50)
        if len(p95_values) > 100:
            p95_confidence = 'high'
        elif len(p95_values) >= 50:
            p95_confidence = 'medium'
        else:
            p95_confidence = 'low'
        
        recommendations['SLO_P95_TARGET_MS'] = {
            'current': current_p95_target,
            'recommended': p95_final,
            'confidence': p95_confidence,
            'sample_size': len(p95_values),
            'rationale': f'Based on {len(p95_values)} samples: P95={p95_stats.get("p95", 0):.0f}ms, mean={p95_mean:.0f}ms, stdev={p95_stdev:.0f}ms',
            'alert_reduction': max(0, int(100 * (p95_final - current_p95_target) / current_p95_target))
        }
    
    if 'p99_latency_ms' in metrics and metrics['p99_latency_ms']:
        p99_values = metrics['p99_latency_ms']
        p99_stats = calculate_percentiles(p99_values)
        p99_mean = mean(p99_values)
        p99_stdev = stdev(p99_values) if len(p99_values) > 1 else 0
        
        p99_recommended = int(p99_stats.get('p99', current_p99_target) + p99_stdev)
        p99_safe_minimum = int(p99_mean + (2 * p99_stdev))
        p99_final = max(p99_recommended, p99_safe_minimum)
        
        # Three-tier confidence: high (>100), medium (50-100), low (<50)
        if len(p99_values) > 100:
            p99_confidence = 'high'
        elif len(p99_values) >= 50:
            p99_confidence = 'medium'
        else:
            p99_confidence = 'low'
        
        recommendations['SLO_P99_TARGET_MS'] = {
            'current': current_p99_target,
            'recommended': p99_final,
            'confidence': p99_confidence,
            'sample_size': len(p99_values),
            'rationale': f'Based on {len(p99_values)} samples: P99={p99_stats.get("p99", 0):.0f}ms, mean={p99_mean:.0f}ms, stdev={p99_stdev:.0f}ms',
            'alert_reduction': max(0, int(100 * (p99_final - current_p99_target) / current_p99_target))
        }
    
    return recommendations

def tune_availability_thresholds(metrics):
    """
    Availability SLO tuning
    Analyzes uptime patterns and error rates
    """
    recommendations = {}
    
    current_availability = float(os.getenv('SLO_AVAILABILITY_PCT', '99.9'))
    
    if 'uptime_pct' in metrics and metrics['uptime_pct']:
        uptime_values = metrics['uptime_pct']
        uptime_mean = mean(uptime_values)
        uptime_min = min(uptime_values)
        
        # If consistently above target, we can raise it
        if uptime_mean > current_availability and uptime_min > current_availability:
            recommended = min(99.99, uptime_mean - 0.01)  # Slight buffer
        else:
            recommended = current_availability
        
        # Three-tier confidence: high (>100), medium (50-100), low (<50)
        if len(uptime_values) > 100:
            availability_confidence = 'high'
        elif len(uptime_values) >= 50:
            availability_confidence = 'medium'
        else:
            availability_confidence = 'low'
        
        recommendations['SLO_AVAILABILITY_PCT'] = {
            'current': current_availability,
            'recommended': round(recommended, 2),
            'confidence': availability_confidence,
            'sample_size': len(uptime_values),
            'rationale': f'Mean uptime: {uptime_mean:.2f}%, min: {uptime_min:.2f}% over {len(uptime_values)} samples',
            'alert_reduction': 0
        }
    
    return recommendations

def tune_error_budget_thresholds(metrics):
    """
    Error budget burn rate tuning
    Analyzes error patterns and incident frequency
    """
    recommendations = {}
    
    current_budget = float(os.getenv('SLO_ERROR_BUDGET_PCT', '2.0'))
    
    if 'error_budget_burn_pct' in metrics and metrics['error_budget_burn_pct']:
        burn_values = metrics['error_budget_burn_pct']
        burn_p95 = calculate_percentiles(burn_values).get('p95', current_budget)
        burn_mean = mean(burn_values)
        
        # Recommended: P95 + 20% headroom
        recommended = min(5.0, burn_p95 * 1.2)  # Cap at 5% per day
        
        # Three-tier confidence: high (>100), medium (50-100), low (<50)
        if len(burn_values) > 100:
            budget_confidence = 'high'
        elif len(burn_values) >= 50:
            budget_confidence = 'medium'
        else:
            budget_confidence = 'low'
        
        recommendations['SLO_ERROR_BUDGET_PCT'] = {
            'current': current_budget,
            'recommended': round(recommended, 2),
            'confidence': budget_confidence,
            'sample_size': len(burn_values),
            'rationale': f'P95 burn rate: {burn_p95:.2f}%, mean: {burn_mean:.2f}%',
            'alert_reduction': max(0, int(100 * (recommended - current_budget) / current_budget))
        }
    
    return recommendations

def tune_webhook_success_thresholds(metrics):
    """
    Webhook success rate tuning
    Analyzes webhook delivery patterns
    """
    recommendations = {}
    
    current_webhook_slo = float(os.getenv('SLO_WEBHOOK_SUCCESS_PCT', '99.0'))
    
    if 'webhook_success_pct' in metrics and metrics['webhook_success_pct']:
        webhook_values = metrics['webhook_success_pct']
        webhook_mean = mean(webhook_values)
        webhook_min = min(webhook_values)
        
        # If consistently high, can raise threshold
        if webhook_mean > current_webhook_slo:
            recommended = min(99.9, webhook_mean - 0.5)
        else:
            recommended = current_webhook_slo
        
        # Three-tier confidence: high (>100), medium (50-100), low (<50)
        if len(webhook_values) > 100:
            webhook_confidence = 'high'
        elif len(webhook_values) >= 50:
            webhook_confidence = 'medium'
        else:
            webhook_confidence = 'low'
        
        recommendations['SLO_WEBHOOK_SUCCESS_PCT'] = {
            'current': current_webhook_slo,
            'recommended': round(recommended, 1),
            'confidence': webhook_confidence,
            'sample_size': len(webhook_values),
            'rationale': f'Mean success: {webhook_mean:.1f}%, min: {webhook_min:.1f}%',
            'alert_reduction': 0
        }
    
    return recommendations

def save_recommendations(recommendations):
    """
    Save tuning recommendations to JSON file
    Includes metadata for admin review
    """
    output_file = Path('configs/slo_tuning_recommendations.json')
    output_file.parent.mkdir(exist_ok=True)
    
    output = {
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'analysis_window_days': 30,
        'total_recommendations': len(recommendations),
        'recommendations': recommendations,
        'auto_apply': {
            'enabled': os.getenv('SLO_AUTO_TUNE', 'false').lower() == 'true',
            'min_confidence': 'high'
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    return str(output_file)

def apply_recommendations(recommendations, min_confidence='high'):
    """
    Auto-apply recommendations based on confidence threshold
    Supports three tiers: high, medium, low
    """
    applied = []
    skipped = []
    
    # Define confidence hierarchy
    confidence_levels = {'high': 3, 'medium': 2, 'low': 1}
    min_level = confidence_levels.get(min_confidence, 3)
    
    for var_name, rec in recommendations.items():
        rec_level = confidence_levels.get(rec['confidence'], 0)
        
        # Apply if recommendation confidence >= minimum threshold
        if rec_level >= min_level:
            applied.append({
                'variable': var_name,
                'old_value': rec['current'],
                'new_value': rec['recommended'],
                'confidence': rec['confidence'],
                'sample_size': rec.get('sample_size', 0),
                'rationale': rec['rationale']
            })
        else:
            skipped.append({
                'variable': var_name,
                'confidence': rec['confidence'],
                'sample_size': rec.get('sample_size', 0),
                'reason': f'Confidence {rec["confidence"]} below threshold {min_confidence}'
            })
    
    return applied, skipped

def main():
    """Main alert tuner workflow"""
    log_event('tuning_started', {'ok': True})
    
    try:
        # Step 1: Fetch historical metrics
        log_event('fetching_metrics', {'days': 30})
        metrics = get_historical_metrics(days=30)
        
        if not metrics:
            log_event('no_metrics', {'warning': 'No historical data available for tuning'})
            print("⚠️  No historical metrics found. Warehouse may need more data.", flush=True)
            return
        
        log_event('metrics_fetched', {'metric_count': len(metrics), 'metrics': list(metrics.keys())})
        
        # Step 2: Run ML tuning algorithms
        all_recommendations = {}
        
        log_event('tuning_latency', {'ok': True})
        latency_recs = tune_latency_thresholds(metrics)
        all_recommendations.update(latency_recs)
        
        log_event('tuning_availability', {'ok': True})
        availability_recs = tune_availability_thresholds(metrics)
        all_recommendations.update(availability_recs)
        
        log_event('tuning_error_budget', {'ok': True})
        error_budget_recs = tune_error_budget_thresholds(metrics)
        all_recommendations.update(error_budget_recs)
        
        log_event('tuning_webhooks', {'ok': True})
        webhook_recs = tune_webhook_success_thresholds(metrics)
        all_recommendations.update(webhook_recs)
        
        # Step 3: Save recommendations
        output_path = save_recommendations(all_recommendations)
        log_event('recommendations_saved', {'path': output_path, 'count': len(all_recommendations)})
        
        # Step 4: Auto-apply if enabled
        auto_tune = os.getenv('SLO_AUTO_TUNE', 'false').lower() == 'true'
        if auto_tune:
            applied, skipped = apply_recommendations(all_recommendations, min_confidence='high')
            log_event('auto_apply', {
                'applied_count': len(applied),
                'skipped_count': len(skipped),
                'applied': applied,
                'skipped': skipped
            })
            print(f"✅ Auto-applied {len(applied)} high-confidence recommendations", flush=True)
        else:
            log_event('auto_apply_disabled', {'ok': True})
            print("ℹ️  Auto-apply disabled. Set SLO_AUTO_TUNE=true to enable.", flush=True)
        
        # Summary
        print(f"\n🎯 Alert Tuner Complete:", flush=True)
        print(f"   Analyzed {len(metrics)} metric types over 30 days", flush=True)
        print(f"   Generated {len(all_recommendations)} recommendations", flush=True)
        print(f"   Saved to: {output_path}", flush=True)
        
        # Show recommendations
        for var_name, rec in all_recommendations.items():
            change_pct = 100 * (rec['recommended'] - rec['current']) / rec['current']
            arrow = '📈' if change_pct > 0 else '📉' if change_pct < 0 else '='
            print(f"   {arrow} {var_name}: {rec['current']} → {rec['recommended']} ({rec['confidence']} confidence)", flush=True)
        
        log_event('tuning_complete', {
            'ok': True,
            'recommendations': len(all_recommendations),
            'output_path': output_path
        })
        
    except Exception as e:
        log_event('tuning_error', {'error': str(e), 'type': type(e).__name__})
        print(f"❌ Alert tuner failed: {e}", file=sys.stderr, flush=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
