"""
Boss Mode Phase 13: Testing Suite Foundation
Basic health and integration tests for EchoPilot
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_health_endpoint():
    """Test /health endpoint returns 200"""
    try:
        from run import app
        with app.test_client() as client:
            response = client.get('/health')
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.get_json()
            assert data is not None, "Response JSON is None"
            assert "status" in data, "Response missing 'status' field"
            print("✅ PASS: /health endpoint")
            return True
    except Exception as e:
        print(f"❌ FAIL: /health endpoint - {e}")
        return False

def test_landing_page():
    """Test / endpoint returns HTML"""
    try:
        from run import app
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            assert b'<!DOCTYPE html>' in response.data, "Response is not HTML"
            print("✅ PASS: Landing page")
            return True
    except Exception as e:
        print(f"❌ FAIL: Landing page - {e}")
        return False

def test_about_page():
    """Test /about endpoint returns HTML"""
    try:
        from run import app
        with app.test_client() as client:
            response = client.get('/about')
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            assert b'<!DOCTYPE html>' in response.data, "Response is not HTML"
            print("✅ PASS: About page")
            return True
    except Exception as e:
        print(f"❌ FAIL: About page - {e}")
        return False

def test_dashboard():
    """Test /dashboard/v2 endpoint returns HTML"""
    try:
        from run import app
        with app.test_client() as client:
            response = client.get('/dashboard/v2')
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            assert b'command-palette' in response.data, "Dashboard missing command palette"
            print("✅ PASS: Dashboard V2")
            return True
    except Exception as e:
        print(f"❌ FAIL: Dashboard V2 - {e}")
        return False

def test_payments_page():
    """Test /payments endpoint returns HTML"""
    try:
        from run import app
        with app.test_client() as client:
            response = client.get('/payments')
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            assert b'Payments Center' in response.data, "Payments page missing title"
            print("✅ PASS: Payments page")
            return True
    except Exception as e:
        print(f"❌ FAIL: Payments page - {e}")
        return False

def test_feature_flags():
    """Test /api/feature-flags endpoint"""
    try:
        from run import app
        with app.test_client() as client:
            response = client.get('/api/feature-flags')
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.get_json()
            assert "ok" in data, "Response missing 'ok' field"
            print("✅ PASS: Feature flags API")
            return True
    except Exception as e:
        print(f"❌ FAIL: Feature flags API - {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("=" * 60)
    print("🧪 Boss Mode Phase 13: Test Suite")
    print("=" * 60)
    
    tests = [
        test_health_endpoint,
        test_landing_page,
        test_about_page,
        test_dashboard,
        test_payments_page,
        test_feature_flags
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed ({int(passed/total*100)}%)")
    print("=" * 60)
    
    return all(results)

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
