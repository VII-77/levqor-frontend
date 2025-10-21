#!/bin/bash
#
# EchoPilot Advanced Smoke Test Suite
# Validates advanced features: DB sync, scheduler, governance, SLO tuning
# Requires DASHBOARD_KEY and HEALTH_TOKEN
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
SKIPPED_TESTS=0

# Log file
LOG_FILE="logs/smoke_advanced_$(date +%Y%m%d_%H%M%S).log"
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

skip() {
    echo -e "${YELLOW}⊘${NC} $1" | tee -a "$LOG_FILE"
    ((SKIPPED_TESTS++))
}

test_json_endpoint() {
    local name="$1"
    local url="$2"
    local expected_code="${3:-200}"
    local method="${4:-GET}"
    local data="${5:-}"
    
    ((TOTAL_TESTS++))
    
    local response=$(curl -s -w '\n%{http_code}' \
        -X "$method" \
        -H "X-Dashboard-Key: $DASHBOARD_KEY" \
        -H "Content-Type: application/json" \
        ${data:+-d "$data"} \
        "$BASE_URL$url")
    
    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" == "$expected_code" ]; then
        # Try to parse JSON
        if echo "$body" | python3 -m json.tool > /dev/null 2>&1; then
            success "$name (HTTP $http_code, valid JSON)"
            echo "$body" | python3 -m json.tool >> "$LOG_FILE"
        else
            success "$name (HTTP $http_code, non-JSON response)"
            echo "$body" >> "$LOG_FILE"
        fi
    else
        fail "$name (Expected: $expected_code, Got: $http_code)"
        echo "$body" >> "$LOG_FILE"
    fi
}

# Print header
echo ""
echo "=================================================="
echo "  EchoPilot Advanced Smoke Test Suite"
echo "=================================================="
echo "Base URL: $BASE_URL"
echo "Timestamp: $(date)"
echo "Log File: $LOG_FILE"
echo "=================================================="
echo ""

# Check prerequisites
if [ -z "$DASHBOARD_KEY" ]; then
    echo -e "${RED}ERROR: DASHBOARD_KEY not set${NC}"
    echo "Set DASHBOARD_KEY environment variable to run advanced tests"
    exit 1
fi

if [ -z "$HEALTH_TOKEN" ]; then
    warn "HEALTH_TOKEN not set, some tests may be skipped"
fi

# Test 1: Health Endpoint with DB Check
log "Testing health endpoint with database checks..."
if [ -n "$HEALTH_TOKEN" ]; then
    test_json_endpoint "Health Check (Full)" "/health?token=$HEALTH_TOKEN" 200
else
    test_json_endpoint "Health Check (Basic)" "/health" 200
fi

# Test 2: Metrics Aggregation
log "Testing metrics aggregation..."
test_json_endpoint "System Metrics" "/api/metrics" 200
test_json_endpoint "Pulse Metrics" "/api/pulse" 200

# Test 3: SLO Monitoring
log "Testing SLO monitoring..."
test_json_endpoint "SLO Dashboard" "/api/slo" 200
test_json_endpoint "SLO Violations" "/api/slo/violations" 200

# Test 4: Feature Flags
log "Testing feature flag system..."
test_json_endpoint "Feature Flags List" "/api/flags" 200

# Test 5: Governance System
log "Testing AI governance..."
test_json_endpoint "Governance Report" "/api/governance/report" 200

# Test 6: Forecast Engine
log "Testing forecast engine..."
test_json_endpoint "Load Forecast" "/api/forecast" 200

# Test 7: Warehouse Sync (Dry Run - Read Only)
log "Testing warehouse sync status..."
((TOTAL_TESTS++))
# Just check if the endpoint exists (would return 403 in demo mode)
response=$(curl -s -o /dev/null -w '%{http_code}' \
    -X POST \
    -H "X-Dashboard-Key: $DASHBOARD_KEY" \
    "$BASE_URL/api/warehouse/sync")

if [ "$response" == "200" ] || [ "$response" == "403" ]; then
    success "Warehouse Sync Endpoint (HTTP $response)"
else
    fail "Warehouse Sync Endpoint (Expected: 200/403, Got: $response)"
fi

# Test 8: SLO Tuning (Dry Run)
log "Testing SLO tuning endpoint..."
((TOTAL_TESTS++))
response=$(curl -s -o /dev/null -w '%{http_code}' \
    -X POST \
    -H "X-Dashboard-Key: $DASHBOARD_KEY" \
    "$BASE_URL/api/slo/tune")

if [ "$response" == "200" ] || [ "$response" == "403" ]; then
    success "SLO Tuning Endpoint (HTTP $response)"
else
    fail "SLO Tuning Endpoint (Expected: 200/403, Got: $response)"
fi

# Test 9: Governance Analysis (Dry Run)
log "Testing governance analysis endpoint..."
((TOTAL_TESTS++))
response=$(curl -s -o /dev/null -w '%{http_code}' \
    -X POST \
    -H "X-Dashboard-Key: $DASHBOARD_KEY" \
    "$BASE_URL/api/governance/analyze")

if [ "$response" == "200" ] || [ "$response" == "403" ]; then
    success "Governance Analysis Endpoint (HTTP $response)"
else
    fail "Governance Analysis Endpoint (Expected: 200/403, Got: $response)"
fi

# Test 10: A/B Testing Framework
log "Testing A/B testing framework..."
test_json_endpoint "A/B Test Variants" "/api/ab-tests" 200

# Test 11: Scheduler Health Check
log "Testing scheduler integration..."
((TOTAL_TESTS++))
if pgrep -f "exec_scheduler.py" > /dev/null; then
    success "Scheduler Process Running"
else
    warn "Scheduler Process Not Detected"
fi

# Test 12: Log Files Existence
log "Testing log file generation..."
((TOTAL_TESTS++))
if [ -f "logs/automation_log.ndjson" ]; then
    success "Automation Logs Present"
else
    warn "Automation Logs Not Found (may not have run yet)"
fi

# Test 13: Database Tables (via warehouse sync check)
log "Testing database schema..."
((TOTAL_TESTS++))

# Temporarily disable exit on error to capture exit code
set +e
db_output=$(python3 -c "
import os
try:
    import psycopg2
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s', ('public',))
    count = cur.fetchone()[0]
    print(f'{count} tables found')
    exit(0 if count > 0 else 1)
except ImportError:
    print('psycopg2 not installed, skipping DB schema check')
    exit(2)  # Special exit code for skip
except Exception as e:
    print(f'Error: {e}')
    exit(1)
" 2>&1)
db_check_result=$?
set -e
# Re-enable exit on error

echo "$db_output" | tee -a "$LOG_FILE"

if [ $db_check_result -eq 0 ]; then
    success "Database Schema Valid"
elif [ $db_check_result -eq 2 ]; then
    skip "Database Schema Check (psycopg2 not installed)"
else
    fail "Database Schema Check Failed"
fi

# Test 14: Demo Mode Detection
log "Testing demo mode detection..."
test_json_endpoint "Demo Mode Status" "/api/demo-mode" 200

# Summary
echo ""
echo "=================================================="
echo "  Advanced Test Results Summary"
echo "=================================================="
echo "Total Tests:  $TOTAL_TESTS"
echo -e "${GREEN}Passed:       $PASSED_TESTS${NC}"
echo -e "${RED}Failed:       $FAILED_TESTS${NC}"
echo -e "${YELLOW}Skipped:      $SKIPPED_TESTS${NC}"
if [ $SKIPPED_TESTS -gt 0 ]; then
    echo "Success Rate: $(awk "BEGIN {printf \"%.1f\", ($PASSED_TESTS/($TOTAL_TESTS-$SKIPPED_TESTS))*100}")%"
else
    echo "Success Rate: $(awk "BEGIN {printf \"%.1f\", ($PASSED_TESTS/$TOTAL_TESTS)*100}")%"
fi
echo "=================================================="
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✓ All advanced tests passed!${NC}"
    log "Advanced smoke test completed successfully"
    exit 0
else
    echo -e "${RED}✗ Some advanced tests failed. Check $LOG_FILE for details.${NC}"
    log "Advanced smoke test completed with failures"
    exit 1
fi
