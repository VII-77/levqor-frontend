#!/bin/bash
#
# EchoPilot Smoke Test Suite
# Validates all critical endpoints and system health
# Exit code 0 = success, 1 = failure
#

set -eo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BASE_URL="${BASE_URL:-http://localhost:5000}"
HEALTH_TOKEN="${HEALTH_TOKEN}"
DASHBOARD_KEY="${DASHBOARD_KEY}"
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Log file
LOG_FILE="logs/smoke_test_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

# Helper functions
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✓${NC} $1" | tee -a "$LOG_FILE"
    ((PASSED_TESTS++))
}

fail() {
    echo -e "${RED}✗${NC} $1" | tee -a "$LOG_FILE"
    ((FAILED_TESTS++))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1" | tee -a "$LOG_FILE"
}

test_endpoint() {
    local name="$1"
    local url="$2"
    local expected_code="${3:-200}"
    local method="${4:-GET}"
    local data="${5:-}"
    local headers="${6:-}"
    
    ((TOTAL_TESTS++))
    
    local cmd="curl -s -w '\n%{http_code}' -X $method '$BASE_URL$url'"
    
    if [ -n "$headers" ]; then
        cmd="$cmd -H '$headers'"
    fi
    
    if [ -n "$data" ]; then
        cmd="$cmd -d '$data' -H 'Content-Type: application/json'"
    fi
    
    local response=$(eval $cmd)
    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" == "$expected_code" ]; then
        success "$name (HTTP $http_code)"
        echo "$body" >> "$LOG_FILE"
    else
        fail "$name (Expected: $expected_code, Got: $http_code)"
        echo "$body" >> "$LOG_FILE"
    fi
}

# Print header
echo ""
echo "======================================"
echo "  EchoPilot Smoke Test Suite"
echo "======================================"
echo "Base URL: $BASE_URL"
echo "Timestamp: $(date)"
echo "Log File: $LOG_FILE"
echo "======================================"
echo ""

# Test 1: Basic Health Check
log "Testing basic health endpoints..."
test_endpoint "Health Check" "/health" 200

# Test 2: Demo Mode Status
log "Testing demo mode status..."
test_endpoint "Demo Mode Status" "/api/demo-mode" 200

# Test 3: Landing Page
log "Testing public pages..."
test_endpoint "Landing Page" "/" 200
test_endpoint "Pricing Page" "/pricing" 200

# Test 4: Dashboard (should redirect without auth)
log "Testing dashboard access..."
test_endpoint "Dashboard Redirect" "/dashboard" 302

# Test 5: Protected API Endpoints (should fail without auth)
log "Testing API protection..."
test_endpoint "Metrics API (No Auth)" "/api/metrics" 401
test_endpoint "SLO API (No Auth)" "/api/slo" 401
test_endpoint "Governance API (No Auth)" "/api/governance/report" 401

# Test 6: Feature Flags API
log "Testing feature flags..."
test_endpoint "Feature Flags List" "/api/flags" 200

# Test 7: Database Connectivity (via health endpoint)
if [ -n "$HEALTH_TOKEN" ]; then
    log "Testing database connectivity with health token..."
    test_endpoint "Health Check with Token" "/health?token=$HEALTH_TOKEN" 200
else
    warn "HEALTH_TOKEN not set, skipping authenticated health check"
fi

# Test 8: Dashboard APIs (with auth)
if [ -n "$DASHBOARD_KEY" ]; then
    log "Testing dashboard APIs with auth..."
    test_endpoint "Metrics API (Authed)" "/api/metrics" 200 "GET" "" "X-Dashboard-Key: $DASHBOARD_KEY"
    test_endpoint "SLO API (Authed)" "/api/slo" 200 "GET" "" "X-Dashboard-Key: $DASHBOARD_KEY"
    test_endpoint "Governance Report (Authed)" "/api/governance/report" 200 "GET" "" "X-Dashboard-Key: $DASHBOARD_KEY"
    test_endpoint "Feature Flags List (Authed)" "/api/flags" 200 "GET" "" "X-Dashboard-Key: $DASHBOARD_KEY"
else
    warn "DASHBOARD_KEY not set, skipping authenticated API tests"
fi

# Test 9: Static Assets
log "Testing static assets..."
test_endpoint "Brand CSS" "/static/brand.css" 200
test_endpoint "Feature Flags JS" "/static/feature-flags.js" 200

# Test 10: API 404 Handling
log "Testing error handling..."
test_endpoint "404 Handler" "/api/nonexistent" 404

# Test 11: Workflow Builder (if enabled)
log "Testing workflow builder..."
test_endpoint "Workflow Builder" "/workflow-builder" 200

# Test 12: Boss Mode UI
log "Testing Boss Mode UI..."
test_endpoint "Boss Mode Dashboard" "/boss" 200

# Summary
echo ""
echo "======================================"
echo "  Test Results Summary"
echo "======================================"
echo "Total Tests:  $TOTAL_TESTS"
echo -e "${GREEN}Passed:       $PASSED_TESTS${NC}"
echo -e "${RED}Failed:       $FAILED_TESTS${NC}"
echo "Success Rate: $(awk "BEGIN {printf \"%.1f\", ($PASSED_TESTS/$TOTAL_TESTS)*100}")%"
echo "======================================"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    log "Smoke test completed successfully"
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Check $LOG_FILE for details.${NC}"
    log "Smoke test completed with failures"
    exit 1
fi
