#!/usr/bin/env python3
"""
Final Transition Validation (STEP 14)
Comprehensive validation before v2.0.0-stable tag
"""

import requests
import json
import os
from datetime import datetime

def run_final_validation():
    """Run comprehensive final validation"""
    
    results = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'version': '2.0.0',
        'codename': 'Quantum',
        'validations': [],
        'passed': 0,
        'failed': 0,
        'warnings': []
    }
    
    base_url = os.getenv('BASE_URL', 'http://localhost:5000')
    dashboard_key = os.getenv('DASHBOARD_KEY', '')
    
    print("=" * 70)
    print("  ECHOPILOT FINAL TRANSITION VALIDATION")
    print("  Version: 2.0.0 'Quantum'")
    print("=" * 70)
    print()
    
    # Validation checks
    checks = [
        {
            'name': 'Platform Status',
            'endpoint': '/api/platform/status',
            'method': 'GET',
            'auth': False,
            'expect': {'phases_complete': 130}
        },
        {
            'name': 'Health Endpoint',
            'endpoint': '/api/health',
            'method': 'GET',
            'auth': False,
            'expect': {'ok': True}
        },
        {
            'name': 'Integrations Hub',
            'endpoint': '/api/integrations/catalog',
            'method': 'GET',
            'auth': True,
            'expect': {'ok': True}
        },
        {
            'name': 'Marketplace',
            'endpoint': '/api/marketplace/listings',
            'method': 'GET',
            'auth': True,
            'expect': {'ok': True}
        },
        {
            'name': 'Multi-Region',
            'endpoint': '/api/regions/status',
            'method': 'GET',
            'auth': True,
            'expect': {'ok': True}
        },
        {
            'name': 'Analytics',
            'endpoint': '/api/analytics/usage?days=7',
            'method': 'GET',
            'auth': True,
            'expect': {'ok': True}
        },
        {
            'name': 'Phase Report',
            'endpoint': '/api/platform/phase-report',
            'method': 'GET',
            'auth': True,
            'expect': {'completion_status': 'ALL_COMPLETE'}
        },
    ]
    
    for check in checks:
        headers = {'X-Dash-Key': dashboard_key} if check.get('auth') else {}
        
        try:
            response = requests.get(
                f"{base_url}{check['endpoint']}",
                headers=headers,
                timeout=10
            )
            
            data = response.json() if response.status_code == 200 else {}
            
            # Verify expected values
            passed = response.status_code == 200
            for key, expected_value in check.get('expect', {}).items():
                if data.get(key) != expected_value:
                    passed = False
            
            validation = {
                'name': check['name'],
                'endpoint': check['endpoint'],
                'status': 'PASS' if passed else 'FAIL',
                'http_code': response.status_code,
                'response_time_ms': int(response.elapsed.total_seconds() * 1000)
            }
            
            results['validations'].append(validation)
            
            if passed:
                results['passed'] += 1
                print(f"✅ {check['name']}: PASS ({response.status_code}, {validation['response_time_ms']}ms)")
            else:
                results['failed'] += 1
                print(f"❌ {check['name']}: FAIL ({response.status_code})")
                
        except Exception as e:
            results['validations'].append({
                'name': check['name'],
                'endpoint': check['endpoint'],
                'status': 'ERROR',
                'error': str(e)
            })
            results['failed'] += 1
            print(f"❌ {check['name']}: ERROR - {str(e)[:50]}")
    
    # Additional checks
    print()
    print("=" * 70)
    print("  INFRASTRUCTURE CHECKS")
    print("=" * 70)
    
    # Check environment
    env_vars = [
        'NOTION_CLIENT_DB_ID',
        'AI_INTEGRATIONS_OPENAI_API_KEY',
        'TELEGRAM_BOT_TOKEN',
        'DATABASE_URL'
    ]
    
    env_status = all(os.getenv(var) for var in env_vars)
    if env_status:
        print("✅ Environment Variables: ALL PRESENT")
        results['passed'] += 1
    else:
        print("❌ Environment Variables: MISSING")
        results['failed'] += 1
    
    # Check files
    required_files = [
        'static/manifest.json',
        'static/sw.js',
        'templates/offline.html',
        'bot/echopilot_os.py',
        'scripts/daily_health_check.py',
        'docs/LTO_OPERATIONS.md'
    ]
    
    files_status = all(os.path.exists(f) for f in required_files)
    if files_status:
        print("✅ Required Files: ALL PRESENT")
        results['passed'] += 1
    else:
        print("❌ Required Files: MISSING")
        results['failed'] += 1
    
    # Final status
    print()
    print("=" * 70)
    print("  FINAL VALIDATION SUMMARY")
    print("=" * 70)
    print(f"  Total Checks: {results['passed'] + results['failed']}")
    print(f"  ✅ Passed: {results['passed']}")
    print(f"  ❌ Failed: {results['failed']}")
    
    if results['failed'] == 0:
        results['overall_status'] = 'READY_FOR_PRODUCTION'
        print()
        print("  🎉 ALL VALIDATIONS PASSED")
        print("  ✅ Platform ready for v2.0.0-stable tag")
    else:
        results['overall_status'] = 'VALIDATION_FAILED'
        print()
        print("  ⚠️  VALIDATION FAILED")
        print(f"  Please review {results['failed']} failed check(s)")
    
    print("=" * 70)
    
    # Save results
    output_file = 'logs/FINAL_VALIDATION_COMPLETE.txt'
    with open(output_file, 'w') as f:
        f.write(json.dumps(results, indent=2))
    
    print(f"\n📄 Full report saved to: {output_file}\n")
    
    return results

if __name__ == '__main__':
    results = run_final_validation()
    exit(0 if results['overall_status'] == 'READY_FOR_PRODUCTION' else 1)
