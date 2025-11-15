#!/usr/bin/env python3
"""
Database Stability Test
Tests PostgreSQL connection reliability over 20 iterations

This script does NOT modify business data. It only:
- Performs lightweight SELECT queries
- Tests connection and commit stability
"""

import sys
import os
import time
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Flask app and db from run.py
from run import app
from app import db
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, DatabaseError

# Test configuration
ITERATIONS = 20
SLEEP_BETWEEN = 0.5  # seconds


def test_db_connection():
    """
    Test a single DB connection attempt.
    Returns: (success: bool, error_type: str or None, error_msg: str or None)
    """
    try:
        with app.app_context():
            # Perform a lightweight query
            result = db.session.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            
            if row and row[0] == 1:
                return (True, None, None)
            else:
                return (False, "UnexpectedResult", "SELECT 1 did not return 1")
                
    except OperationalError as e:
        error_msg = str(e)
        
        # Categorize error type
        if "SSL connection has been closed unexpectedly" in error_msg:
            error_type = "SSL_CLOSED"
        elif "timeout" in error_msg.lower():
            error_type = "TIMEOUT"
        elif "could not connect" in error_msg.lower():
            error_type = "CONNECTION_FAILED"
        else:
            error_type = "OPERATIONAL_ERROR"
            
        return (False, error_type, error_msg)
        
    except DatabaseError as e:
        return (False, "DATABASE_ERROR", str(e))
        
    except Exception as e:
        return (False, "UNKNOWN_ERROR", str(e))


def run_stability_test():
    """
    Run N iterations of DB connection tests.
    Returns: dict with test results
    """
    print("=" * 70)
    print("DATABASE STABILITY TEST")
    print("=" * 70)
    print()
    print(f"Testing PostgreSQL connection reliability...")
    print(f"Iterations: {ITERATIONS}")
    print(f"Delay between tests: {SLEEP_BETWEEN}s")
    print()
    print("Starting tests...")
    print()
    
    results = {
        'total': ITERATIONS,
        'successful': 0,
        'failed': 0,
        'errors': {},
        'attempts': []
    }
    
    for i in range(1, ITERATIONS + 1):
        start_time = time.time()
        success, error_type, error_msg = test_db_connection()
        elapsed = (time.time() - start_time) * 1000  # ms
        
        # Record result
        attempt = {
            'iteration': i,
            'success': success,
            'elapsed_ms': round(elapsed, 2),
            'error_type': error_type,
            'timestamp': datetime.utcnow().isoformat()
        }
        results['attempts'].append(attempt)
        
        if success:
            results['successful'] += 1
            status = f"✅ PASS ({elapsed:.1f}ms)"
        else:
            results['failed'] += 1
            
            # Track error types
            if error_type not in results['errors']:
                results['errors'][error_type] = {
                    'count': 0,
                    'example': error_msg
                }
            results['errors'][error_type]['count'] += 1
            
            status = f"❌ FAIL - {error_type}"
        
        # Print progress
        print(f"  [{i:2d}/{ITERATIONS}] {status}")
        
        # Sleep between iterations (except last one)
        if i < ITERATIONS:
            time.sleep(SLEEP_BETWEEN)
    
    return results


def analyze_results(results):
    """
    Analyze test results and determine stability classification.
    Returns: (classification: str, summary: dict)
    """
    success_rate = (results['successful'] / results['total']) * 100
    
    # Classify based on success rate
    if success_rate == 100:
        classification = "STABLE"
        verdict = "Database connection is STABLE - safe for production webhooks"
    elif success_rate >= 95:
        classification = "MOSTLY_STABLE"
        verdict = "Database connection is MOSTLY STABLE - acceptable with retry logic"
    elif success_rate >= 80:
        classification = "FLAKY"
        verdict = "Database connection is FLAKY - retry logic REQUIRED"
    else:
        classification = "UNRELIABLE"
        verdict = "Database connection is UNRELIABLE - NOT safe for production"
    
    summary = {
        'classification': classification,
        'verdict': verdict,
        'success_rate': round(success_rate, 1),
        'total_attempts': results['total'],
        'successful': results['successful'],
        'failed': results['failed']
    }
    
    return classification, summary


def print_summary(results, classification, summary):
    """Print human-readable summary"""
    print()
    print("=" * 70)
    print("TEST RESULTS")
    print("=" * 70)
    print()
    print(f"Total Attempts:    {results['total']}")
    print(f"Successful:        {results['successful']} ({summary['success_rate']}%)")
    print(f"Failed:            {results['failed']}")
    print()
    
    if results['errors']:
        print("Error Breakdown:")
        for error_type, info in results['errors'].items():
            print(f"  - {error_type}: {info['count']} occurrences")
            print(f"    Example: {info['example'][:80]}...")
        print()
    
    print("=" * 70)
    print(f"CLASSIFICATION: {classification}")
    print("=" * 70)
    print()
    print(summary['verdict'])
    print()
    
    if classification == "STABLE":
        print("✅ RECOMMENDATION: Safe to proceed with webhook testing")
        print("   No retry logic needed at this time.")
    elif classification == "MOSTLY_STABLE":
        print("⚠️  RECOMMENDATION: Add simple retry logic (1-2 retries)")
        print("   This will handle occasional transient failures.")
    elif classification == "FLAKY":
        print("⚠️  RECOMMENDATION: Add robust retry logic (3 retries)")
        print("   Also consider connection pool pre-ping.")
    else:
        print("❌ RECOMMENDATION: DO NOT use for production webhooks yet")
        print("   Investigate database connection issues first.")
    
    print()


def save_report(results, classification, summary):
    """Save detailed report to markdown file"""
    report_path = "DB-STABILITY-REPORT.md"
    
    with open(report_path, 'w') as f:
        f.write("# Database Stability Test Report\n")
        f.write(f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n")
        
        # Executive summary at top
        f.write("## OVERALL VERDICT\n\n")
        f.write(f"**Classification:** {classification}\n\n")
        f.write(f"> {summary['verdict']}\n\n")
        f.write(f"**Success Rate:** {summary['success_rate']}% ({results['successful']}/{results['total']})\n\n")
        
        # Impact for owner
        f.write("---\n\n")
        f.write("## What This Means for Stripe Webhooks\n\n")
        
        if classification == "STABLE":
            f.write("✅ **SAFE TO PROCEED**\n\n")
            f.write("Your database connection is stable. You can:\n")
            f.write("1. Rerun the Stripe webhook test\n")
            f.write("2. If that passes, start accepting real payments (small traffic first)\n")
            f.write("3. Monitor webhook success rate in production\n\n")
            f.write("No immediate code changes needed.\n\n")
        elif classification == "MOSTLY_STABLE":
            f.write("⚠️  **SAFE WITH RETRY LOGIC**\n\n")
            f.write("Your database has occasional connectivity issues. Before production:\n")
            f.write("1. Add simple retry logic to webhook handler (1-2 retries)\n")
            f.write("2. Rerun webhook test to verify retry works\n")
            f.write("3. Then safe to accept payments\n\n")
        elif classification == "FLAKY":
            f.write("⚠️  **NOT SAFE WITHOUT RETRY LOGIC**\n\n")
            f.write("Your database connection is unreliable. Before production:\n")
            f.write("1. Add robust retry logic (3 retries with exponential backoff)\n")
            f.write("2. Enable connection pool pre-ping\n")
            f.write("3. Rerun stability test to verify improvements\n")
            f.write("4. Then rerun webhook test\n\n")
        else:
            f.write("❌ **NOT SAFE FOR PRODUCTION**\n\n")
            f.write("Your database connection is too unreliable for paid webhooks.\n")
            f.write("Action required:\n")
            f.write("1. Check Neon database status/health\n")
            f.write("2. Verify DATABASE_URL is correct\n")
            f.write("3. Consider Neon support if persistent\n")
            f.write("4. Do NOT accept real payments until resolved\n\n")
        
        # Detailed results
        f.write("---\n\n")
        f.write("## Test Configuration\n\n")
        f.write(f"- **Total Iterations:** {ITERATIONS}\n")
        f.write(f"- **Delay Between Tests:** {SLEEP_BETWEEN}s\n")
        f.write(f"- **Test Type:** Lightweight SELECT 1 query\n")
        f.write(f"- **Database:** PostgreSQL (Neon via DATABASE_URL)\n\n")
        
        f.write("---\n\n")
        f.write("## Results Summary\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Total Attempts | {results['total']} |\n")
        f.write(f"| Successful | {results['successful']} |\n")
        f.write(f"| Failed | {results['failed']} |\n")
        f.write(f"| Success Rate | {summary['success_rate']}% |\n\n")
        
        if results['errors']:
            f.write("## Error Breakdown\n\n")
            for error_type, info in results['errors'].items():
                f.write(f"### {error_type}\n")
                f.write(f"- **Occurrences:** {info['count']}\n")
                f.write(f"- **Example:**\n")
                f.write(f"  ```\n")
                f.write(f"  {info['example']}\n")
                f.write(f"  ```\n\n")
        
        # Detailed attempt log
        f.write("---\n\n")
        f.write("## Detailed Test Log\n\n")
        f.write("| Iteration | Status | Time (ms) | Error Type |\n")
        f.write("|-----------|--------|-----------|------------|\n")
        
        for attempt in results['attempts']:
            status = "✅ PASS" if attempt['success'] else "❌ FAIL"
            error = attempt['error_type'] or "-"
            f.write(f"| {attempt['iteration']} | {status} | {attempt['elapsed_ms']} | {error} |\n")
        
        f.write("\n---\n\n")
        f.write(f"**Report Generated:** {datetime.utcnow().isoformat()} UTC\n")
    
    print(f"📄 Detailed report saved to: {report_path}")


if __name__ == "__main__":
    try:
        # Run test
        results = run_stability_test()
        
        # Analyze
        classification, summary = analyze_results(results)
        
        # Print summary
        print_summary(results, classification, summary)
        
        # Save report
        save_report(results, classification, summary)
        
        print("=" * 70)
        print("DB stability check complete – open DB-STABILITY-REPORT.md for full details")
        print("=" * 70)
        
        # Exit code based on classification
        if classification == "STABLE":
            sys.exit(0)
        elif classification == "MOSTLY_STABLE":
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)
