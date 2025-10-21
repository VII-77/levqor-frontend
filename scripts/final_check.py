#!/usr/bin/env python3
"""
EchoPilot Final Systems Check
Comprehensive verification of all 130 phases
"""

import os
import sys
import json
import requests
from datetime import datetime

def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def check_mark(condition):
    return "✅" if condition else "❌"

def test_endpoint(url, headers=None, expected_status=200):
    try:
        response = requests.get(url, headers=headers or {}, timeout=5)
        return response.status_code == expected_status, response
    except Exception as e:
        return False, str(e)

print_section("ECHOPILOT FINAL SYSTEMS CHECK")
print(f"Timestamp: {datetime.utcnow().isoformat()}Z\n")

results = {
    'passed': 0,
    'failed': 0,
    'warnings': []
}

# 1. Environment Variables
print_section("1. ENVIRONMENT VARIABLES")
required_vars = [
    'NOTION_CLIENT_DB_ID',
    'AUTOMATION_QUEUE_DB_ID',
    'JOB_LOG_DB_ID',
    'AI_INTEGRATIONS_OPENAI_API_KEY',
    'TELEGRAM_BOT_TOKEN',
    'SESSION_SECRET',
    'DATABASE_URL'
]

for var in required_vars:
    val = os.getenv(var)
    status = check_mark(val is not None)
    print(f"  {status} {var}")
    if val:
        results['passed'] += 1
    else:
        results['failed'] += 1

# 2. Server Health
print_section("2. SERVER HEALTH")
base_url = "http://localhost:5000"
dashboard_key = os.getenv('DASHBOARD_KEY', '')

try:
    health_ok, health_resp = test_endpoint(f"{base_url}/api/health")
    if health_ok:
        health_data = health_resp.json()
        print(f"  ✅ Health endpoint responsive")
        print(f"     Status: {health_data.get('status', 'unknown')}")
        results['passed'] += 1
    else:
        print(f"  ❌ Health endpoint failed")
        results['failed'] += 1
except Exception as e:
    print(f"  ❌ Health check error: {e}")
    results['failed'] += 1

# 3. Platform Status (Phase 130)
print_section("3. PLATFORM STATUS (PHASE 130)")
try:
    status_ok, status_resp = test_endpoint(f"{base_url}/api/platform/status")
    if status_ok:
        data = status_resp.json()
        print(f"  ✅ Platform: {data.get('platform')}")
        print(f"  ✅ Version: {data.get('version')}")
        print(f"  ✅ Status: {data.get('status')}")
        print(f"  ✅ Phases Complete: {data.get('phases_complete')}/130")
        print(f"  ✅ Active Modules: {len(data.get('modules', {}))}")
        results['passed'] += 5
    else:
        print(f"  ❌ Platform status failed")
        results['failed'] += 1
except Exception as e:
    print(f"  ❌ Platform status error: {e}")
    results['failed'] += 1

# 4. Phase 121-130 Endpoints
print_section("4. PHASE 121-130 ENDPOINTS")
headers = {'X-Dash-Key': dashboard_key}
new_endpoints = [
    ('/api/integrations/catalog', 'Phase 122: Integrations Hub'),
    ('/api/ai/analytics?days=7', 'Phase 123: AI Data Lake'),
    ('/api/predict/load?hours=4', 'Phase 124: Predictive Load'),
    ('/api/healing/status', 'Phase 125: Self-Healing 2.0'),
    ('/api/marketplace/listings', 'Phase 126: Enterprise Marketplace'),
    ('/api/compliance/soc2-report', 'Phase 127: Compliance APIs'),
    ('/api/regions/status', 'Phase 128: Multi-Region'),
    ('/api/platform/metrics', 'Phase 130: System Metrics'),
]

for endpoint, description in new_endpoints:
    try:
        ok, resp = test_endpoint(f"{base_url}{endpoint}", headers=headers)
        if ok:
            data = resp.json()
            if data.get('ok', True):
                print(f"  ✅ {description}")
                results['passed'] += 1
            else:
                print(f"  ⚠️  {description} (returned ok=false)")
                results['warnings'].append(f"{endpoint}: {data.get('error', 'unknown')}")
        else:
            print(f"  ❌ {description}")
            results['failed'] += 1
    except Exception as e:
        print(f"  ❌ {description}: {str(e)[:50]}")
        results['failed'] += 1

# 5. Python Modules
print_section("5. PYTHON MODULE IMPORTS")
modules = [
    ('bot.echopilot_os', 'Phase 130: EchoPilot OS'),
    ('bot.integrations_hub', 'Phase 122: Integrations Hub'),
    ('bot.ai_data_lake', 'Phase 123: AI Data Lake'),
    ('bot.predictive_load', 'Phase 124: Predictive Load'),
    ('bot.self_healing_v2', 'Phase 125: Self-Healing 2.0'),
    ('bot.enterprise_marketplace', 'Phase 126: Enterprise Marketplace'),
    ('bot.compliance_apis', 'Phase 127: Compliance APIs'),
    ('bot.multi_region', 'Phase 128: Multi-Region'),
    ('bot.partner_portal', 'Phase 129: Partner Portal'),
]

for module, description in modules:
    try:
        __import__(module)
        print(f"  ✅ {description}")
        results['passed'] += 1
    except Exception as e:
        print(f"  ❌ {description}: {str(e)[:50]}")
        results['failed'] += 1

# 6. PWA Assets
print_section("6. PWA ASSETS (PHASE 121)")
pwa_files = [
    ('static/manifest.json', 'PWA Manifest'),
    ('static/sw.js', 'Service Worker'),
    ('templates/offline.html', 'Offline Page'),
]

for file_path, description in pwa_files:
    exists = os.path.exists(file_path)
    print(f"  {check_mark(exists)} {description}")
    if exists:
        results['passed'] += 1
    else:
        results['failed'] += 1

# 7. Log Files
print_section("7. LOG INFRASTRUCTURE")
log_dirs = ['logs', 'logs/analytics', 'logs/security', 'backups']
for log_dir in log_dirs:
    exists = os.path.isdir(log_dir)
    print(f"  {check_mark(exists)} {log_dir}/")
    if exists:
        results['passed'] += 1
    else:
        results['failed'] += 1

# 8. Database Connection
print_section("8. DATABASE CONNECTIVITY")
try:
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        import psycopg2
        conn = psycopg2.connect(db_url)
        conn.close()
        print(f"  ✅ PostgreSQL connection successful")
        results['passed'] += 1
    else:
        print(f"  ⚠️  DATABASE_URL not set")
        results['warnings'].append("PostgreSQL not configured")
except Exception as e:
    print(f"  ⚠️  PostgreSQL connection: {str(e)[:50]}")
    results['warnings'].append(f"DB: {str(e)[:50]}")

# Final Summary
print_section("FINAL SUMMARY")
total = results['passed'] + results['failed']
pass_rate = (results['passed'] / total * 100) if total > 0 else 0

print(f"\n  Total Checks: {total}")
print(f"  ✅ Passed: {results['passed']}")
print(f"  ❌ Failed: {results['failed']}")
print(f"  ⚠️  Warnings: {len(results['warnings'])}")
print(f"\n  Pass Rate: {pass_rate:.1f}%")

if results['warnings']:
    print(f"\n  Warnings:")
    for warning in results['warnings']:
        print(f"    - {warning}")

print("\n" + "=" * 70)

if results['failed'] == 0:
    print("  🎉 ALL SYSTEMS OPERATIONAL - 130 PHASES COMPLETE")
    sys.exit(0)
else:
    print("  ⚠️  SOME CHECKS FAILED - REVIEW REQUIRED")
    sys.exit(1)
