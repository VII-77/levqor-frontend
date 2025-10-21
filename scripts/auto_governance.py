#!/usr/bin/env python3
"""
EchoPilot AI Governance Advisor
Phase 110: Automated governance, compliance, and security recommendations
Uses GPT-4o-mini to analyze system metrics and provide actionable insights
Runs every 12 hours via scheduler
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# OpenAI client
try:
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv('AI_INTEGRATIONS_OPENAI_API_KEY'),
        base_url=os.getenv('AI_INTEGRATIONS_OPENAI_BASE_URL')
    )
except ImportError:
    print("❌ OpenAI library not installed", file=sys.stderr, flush=True)
    sys.exit(1)

# Configuration
LOG_FILE = Path('logs/governance_advisor.ndjson')
LOG_FILE.parent.mkdir(exist_ok=True)

REPORT_FILE = Path('logs/governance_report.json')

def log_event(event, data=None):
    """Write NDJSON log entry"""
    entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event': event
    }
    if data:
        entry.update(data)
    
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    
    print(json.dumps(entry), flush=True)

def collect_system_metrics():
    """
    Collect metrics from various log files for governance analysis
    """
    metrics = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'slo_status': None,
        'security_issues': [],
        'data_quality': {},
        'cost_trends': {},
        'compliance_flags': []
    }
    
    # 1. SLO Health
    try:
        slo_log = Path('logs/slo_guard.ndjson')
        if slo_log.exists():
            with open(slo_log) as f:
                lines = f.readlines()
                if lines:
                    last_slo = json.loads(lines[-1])
                    metrics['slo_status'] = {
                        'error_budget_used': last_slo.get('error_budget_used', 0),
                        'availability': last_slo.get('availability_pct', 100),
                        'p95_latency': last_slo.get('p95_latency_ms', 0),
                        'p99_latency': last_slo.get('p99_latency_ms', 0)
                    }
    except Exception as e:
        log_event('slo_collection_error', {'error': str(e)})
    
    # 2. Security Events
    try:
        security_log = Path('logs/security_scanner.ndjson')
        if security_log.exists():
            with open(security_log) as f:
                lines = f.readlines()[-50:]  # Last 50 events
                for line in lines:
                    event = json.loads(line)
                    if event.get('event') == 'vulnerability_found':
                        metrics['security_issues'].append({
                            'severity': event.get('severity'),
                            'type': event.get('vuln_type'),
                            'timestamp': event.get('ts')
                        })
    except Exception as e:
        log_event('security_collection_error', {'error': str(e)})
    
    # 3. Data Quality Metrics
    try:
        warehouse_log = Path('logs/warehouse_sync.ndjson')
        if warehouse_log.exists():
            with open(warehouse_log) as f:
                lines = f.readlines()
                if lines:
                    last_sync = json.loads(lines[-1])
                    if last_sync.get('event') == 'sync_complete':
                        metrics['data_quality'] = {
                            'last_sync': last_sync.get('ts'),
                            'records_synced': last_sync.get('total_records', 0),
                            'duration_seconds': last_sync.get('duration_seconds', 0),
                            'errors': last_sync.get('errors', 0)
                        }
    except Exception as e:
        log_event('warehouse_collection_error', {'error': str(e)})
    
    # 4. Cost Trends
    try:
        job_log = Path('logs/job_log.ndjson')
        if job_log.exists():
            with open(job_log) as f:
                lines = f.readlines()[-100:]  # Last 100 lines
                total_cost = 0
                total_tokens = 0
                completed_jobs = 0
                
                for line in lines:
                    job = json.loads(line)
                    if job.get('event') == 'job_complete':
                        total_cost += job.get('cost_usd', 0)
                        total_tokens += job.get('tokens_total', 0)
                        completed_jobs += 1
                
                metrics['cost_trends'] = {
                    'recent_jobs': completed_jobs,  # Only count completed jobs
                    'total_cost_usd': round(total_cost, 4),
                    'total_tokens': total_tokens,
                    'avg_cost_per_job': round(total_cost / max(completed_jobs, 1), 4)  # Divide by completed jobs
                }
    except Exception as e:
        log_event('cost_collection_error', {'error': str(e)})
    
    # 5. Compliance Flags
    try:
        # Check for GDPR compliance indicators
        if metrics['data_quality'].get('last_sync'):
            last_sync_dt = datetime.fromisoformat(metrics['data_quality']['last_sync'].replace('Z', ''))
            hours_since_sync = (datetime.utcnow() - last_sync_dt).total_seconds() / 3600
            if hours_since_sync > 48:
                metrics['compliance_flags'].append({
                    'type': 'data_staleness',
                    'severity': 'medium',
                    'message': f'Data warehouse not synced in {int(hours_since_sync)} hours'
                })
        
        # Check for error budget violations
        if metrics['slo_status'] and metrics['slo_status']['error_budget_used'] > 0.8:
            metrics['compliance_flags'].append({
                'type': 'slo_violation',
                'severity': 'high',
                'message': f"SLO error budget at {metrics['slo_status']['error_budget_used']*100:.1f}%"
            })
        
        # Check for security vulnerabilities
        high_severity = [s for s in metrics['security_issues'] if s.get('severity') == 'high']
        if high_severity:
            metrics['compliance_flags'].append({
                'type': 'security_vulnerability',
                'severity': 'critical',
                'message': f'{len(high_severity)} high-severity vulnerabilities detected'
            })
    
    except Exception as e:
        log_event('compliance_collection_error', {'error': str(e)})
    
    return metrics

def generate_governance_recommendations(metrics):
    """
    Use GPT-4o-mini to generate governance recommendations
    """
    log_event('generating_recommendations', {'ok': True})
    
    # Prepare context for AI
    context = f"""You are an AI governance advisor for EchoPilot, an enterprise automation platform.

Analyze the following system metrics and provide actionable governance recommendations:

**SLO Status:**
{json.dumps(metrics.get('slo_status'), indent=2)}

**Security Issues (last 50 events):**
{len(metrics.get('security_issues', []))} issues detected
High severity: {len([s for s in metrics.get('security_issues', []) if s.get('severity') == 'high'])}

**Data Quality:**
{json.dumps(metrics.get('data_quality'), indent=2)}

**Cost Trends (last 100 jobs):**
{json.dumps(metrics.get('cost_trends'), indent=2)}

**Compliance Flags:**
{json.dumps(metrics.get('compliance_flags'), indent=2)}

Provide your recommendations in the following JSON format:
{{
  "priority": "low|medium|high|critical",
  "summary": "Brief 1-sentence summary",
  "recommendations": [
    {{
      "category": "security|compliance|cost|performance|data_quality",
      "priority": "low|medium|high",
      "title": "Short title",
      "description": "Detailed recommendation",
      "action_items": ["Specific action 1", "Specific action 2"]
    }}
  ],
  "alerts": [
    {{
      "severity": "low|medium|high|critical",
      "message": "Alert message",
      "category": "security|compliance|cost|performance"
    }}
  ]
}}

Focus on:
1. GDPR/CCPA compliance
2. Security vulnerabilities
3. Cost optimization
4. SLO adherence
5. Data quality and governance
"""
    
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': 'You are an expert AI governance advisor specializing in compliance, security, and operational excellence.'},
                {'role': 'user', 'content': context}
            ],
            temperature=0.3,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if not content:
            raise ValueError("AI returned empty response")
        
        recommendations = json.loads(content)
        
        log_event('recommendations_generated', {
            'priority': recommendations.get('priority'),
            'num_recommendations': len(recommendations.get('recommendations', [])),
            'num_alerts': len(recommendations.get('alerts', []))
        })
        
        return recommendations
    
    except Exception as e:
        log_event('recommendations_error', {'error': str(e), 'type': type(e).__name__})
        
        # Return fallback recommendations
        return {
            'priority': 'low',
            'summary': 'AI governance advisor encountered an error, using fallback mode',
            'recommendations': [
                {
                    'category': 'system',
                    'priority': 'medium',
                    'title': 'Review governance advisor logs',
                    'description': f'Governance advisor failed with error: {str(e)}',
                    'action_items': ['Check logs/governance_advisor.ndjson', 'Verify OpenAI API key']
                }
            ],
            'alerts': []
        }

def send_critical_alerts(recommendations):
    """
    Send Telegram alerts for critical findings
    """
    critical_alerts = [a for a in recommendations.get('alerts', []) if a.get('severity') == 'critical']
    
    if not critical_alerts:
        return
    
    try:
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        telegram_chat = os.getenv('TELEGRAM_CHAT_ID')
        
        if not telegram_token or not telegram_chat:
            log_event('telegram_not_configured', {'ok': False})
            return
        
        import requests
        
        for alert in critical_alerts:
            message = f"""🚨 CRITICAL GOVERNANCE ALERT

Category: {alert.get('category', 'unknown').upper()}
Severity: {alert.get('severity', 'unknown').upper()}

{alert.get('message', 'No details available')}

Action required immediately.
"""
            
            requests.post(
                f'https://api.telegram.org/bot{telegram_token}/sendMessage',
                json={
                    'chat_id': telegram_chat,
                    'text': message
                },
                timeout=5
            )
            
            log_event('critical_alert_sent', {
                'category': alert.get('category'),
                'severity': alert.get('severity')
            })
    
    except Exception as e:
        log_event('alert_send_error', {'error': str(e)})

def save_governance_report(metrics, recommendations):
    """
    Save governance report to disk
    """
    report = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'metrics': metrics,
        'recommendations': recommendations,
        'metadata': {
            'advisor_version': '1.0.0',
            'model': 'gpt-4o-mini'
        }
    }
    
    with open(REPORT_FILE, 'w') as f:
        json.dump(report, f, indent=2)
    
    log_event('report_saved', {'path': str(REPORT_FILE)})

def main():
    """Main governance advisor logic"""
    log_event('advisor_started', {'ok': True})
    
    try:
        # 1. Collect system metrics
        log_event('collecting_metrics', {'ok': True})
        metrics = collect_system_metrics()
        
        # 2. Generate AI recommendations
        recommendations = generate_governance_recommendations(metrics)
        
        # 3. Send critical alerts
        send_critical_alerts(recommendations)
        
        # 4. Save report
        save_governance_report(metrics, recommendations)
        
        # Summary
        print(f"\n✅ AI Governance Advisor:", flush=True)
        print(f"   Priority: {recommendations.get('priority', 'unknown').upper()}", flush=True)
        print(f"   Summary: {recommendations.get('summary', 'No summary available')}", flush=True)
        print(f"   Recommendations: {len(recommendations.get('recommendations', []))}", flush=True)
        print(f"   Alerts: {len(recommendations.get('alerts', []))}", flush=True)
        print(f"   Report saved: {REPORT_FILE}", flush=True)
        
        # Show high-priority recommendations
        for rec in recommendations.get('recommendations', []):
            if rec.get('priority') in ['high', 'critical']:
                print(f"\n   🔴 {rec.get('title', 'Untitled')}", flush=True)
                print(f"      Category: {rec.get('category', 'unknown')}", flush=True)
                print(f"      {rec.get('description', 'No description')}", flush=True)
        
        log_event('advisor_complete', {
            'ok': True,
            'priority': recommendations.get('priority'),
            'num_recommendations': len(recommendations.get('recommendations', [])),
            'num_alerts': len(recommendations.get('alerts', []))
        })
        
    except Exception as e:
        log_event('advisor_error', {'error': str(e), 'type': type(e).__name__})
        print(f"❌ Governance advisor failed: {e}", file=sys.stderr, flush=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
