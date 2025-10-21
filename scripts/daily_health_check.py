#!/usr/bin/env python3
"""
Daily Health Check (STEP 4)
Comprehensive system health verification
Runs daily at 08:00 UTC
"""

import requests
import json
from datetime import datetime
import os

def daily_health_check():
    """Run comprehensive daily health check"""
    base_url = os.getenv('BASE_URL', 'http://localhost:5000')
    
    results = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'checks': [],
        'status': 'HEALTHY',
        'failures': 0
    }
    
    # Critical endpoints to check
    checks = [
        ('/api/health', 'Health Endpoint'),
        ('/api/platform/status', 'Platform Status'),
        ('/api/status/summary', 'Status Summary'),
    ]
    
    print(f"{'='*70}")
    print(f"  DAILY HEALTH CHECK - {results['timestamp']}")
    print(f"{'='*70}\n")
    
    for endpoint, name in checks:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            status = 'PASS' if response.status_code == 200 else 'FAIL'
            
            check_result = {
                'endpoint': endpoint,
                'name': name,
                'status': status,
                'http_code': response.status_code,
                'response_time_ms': int(response.elapsed.total_seconds() * 1000)
            }
            
            results['checks'].append(check_result)
            
            icon = '✅' if status == 'PASS' else '❌'
            print(f"{icon} {name}: {status} ({response.status_code}) - {check_result['response_time_ms']}ms")
            
            if status == 'FAIL':
                results['failures'] += 1
                results['status'] = 'DEGRADED'
                
        except Exception as e:
            results['checks'].append({
                'endpoint': endpoint,
                'name': name,
                'status': 'ERROR',
                'error': str(e)
            })
            results['failures'] += 1
            results['status'] = 'CRITICAL'
            print(f"❌ {name}: ERROR - {str(e)[:50]}")
    
    # Save results
    with open('logs/daily_health.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"  OVERALL STATUS: {results['status']}")
    print(f"  Checks Passed: {len(results['checks']) - results['failures']}/{len(results['checks'])}")
    print(f"  Report saved: logs/daily_health.json")
    print(f"{'='*70}\n")
    
    # Telegram alert if failures
    if results['failures'] > 0:
        send_telegram_alert(results)
    
    return results

def send_telegram_alert(results):
    """Send Telegram alert for health check failures"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        print("⚠️  Telegram not configured - skipping alert")
        return
    
    message = f"""🚨 *EchoPilot Health Check Alert*

Status: {results['status']}
Failures: {results['failures']}
Timestamp: {results['timestamp']}

Failed Checks:"""
    
    for check in results['checks']:
        if check.get('status') in ['FAIL', 'ERROR']:
            message += f"\n• {check['name']}: {check.get('status')}"
    
    try:
        requests.post(
            f'https://api.telegram.org/bot{token}/sendMessage',
            json={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            },
            timeout=10
        )
        print("✅ Telegram alert sent")
    except Exception as e:
        print(f"❌ Telegram alert failed: {e}")

if __name__ == '__main__':
    daily_health_check()
