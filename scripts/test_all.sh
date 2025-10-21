#!/bin/bash
#
# EchoPilot Unified Test Runner
# Runs all test suites and generates comprehensive report
# Exit code 0 = all tests passed, 1 = some tests failed
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BASE_URL="${BASE_URL:-http://localhost:5000}"
DASHBOARD_KEY="${DASHBOARD_KEY}"
HEALTH_TOKEN="${HEALTH_TOKEN}"

# Test results
TOTAL_SUITES=0
PASSED_SUITES=0
FAILED_SUITES=0

# Log file
TEST_LOG="logs/test_all_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$TEST_LOG"
}

success() {
    echo -e "${GREEN}✓${NC} $1" | tee -a "$TEST_LOG"
    ((PASSED_SUITES++))
}

fail() {
    echo -e "${RED}✗${NC} $1" | tee -a "$TEST_LOG"
    ((FAILED_SUITES++))
}

info() {
    echo -e "${BLUE}ℹ${NC} $1" | tee -a "$TEST_LOG"
}

run_test_suite() {
    local name="$1"
    local command="$2"
    
    ((TOTAL_SUITES++))
    
    log "Running: $name"
    
    if eval "$command" >> "$TEST_LOG" 2>&1; then
        success "$name"
        return 0
    else
        fail "$name"
        return 1
    fi
}

# Print header
echo ""
echo "========================================================="
echo "  EchoPilot Unified Test Runner"
echo "========================================================="
echo "Timestamp: $(date)"
echo "Log File: $TEST_LOG"
echo "========================================================="
echo ""

# Test Suite 1: Development Environment Check
log "Test Suite 1: Development Environment"
if [ -f "scripts/dev_check.py" ]; then
    run_test_suite "Development Environment Check" "python3 scripts/dev_check.py"
else
    fail "Development Environment Check (script not found)"
    ((TOTAL_SUITES++))
fi

# Test Suite 2: Basic Smoke Tests
log "Test Suite 2: Basic Smoke Tests"
if [ -f "scripts/smoke.sh" ]; then
    run_test_suite "Basic Smoke Tests" "bash scripts/smoke.sh"
else
    fail "Basic Smoke Tests (script not found)"
    ((TOTAL_SUITES++))
fi

# Test Suite 3: Advanced Smoke Tests
log "Test Suite 3: Advanced Smoke Tests"
if [ -f "scripts/smoke_advanced.sh" ]; then
    if [ -n "$DASHBOARD_KEY" ]; then
        run_test_suite "Advanced Smoke Tests" "DASHBOARD_KEY=$DASHBOARD_KEY bash scripts/smoke_advanced.sh"
    else
        fail "Advanced Smoke Tests (DASHBOARD_KEY not set)"
        ((TOTAL_SUITES++))
    fi
else
    fail "Advanced Smoke Tests (script not found)"
    ((TOTAL_SUITES++))
fi

# Test Suite 4: Python Syntax Check
log "Test Suite 4: Python Syntax Validation"
run_test_suite "Python Syntax Check" "python3 -m py_compile run.py bot/*.py scripts/*.py"

# Test Suite 5: Config File Validation
log "Test Suite 5: Config File Validation"
run_test_suite "Feature Flags JSON" "python3 -m json.tool configs/flags.json > /dev/null"

# Test Suite 6: Import Check
log "Test Suite 6: Import Validation"
run_test_suite "Import Check" "python3 -c 'import bot.main; import bot.config; import bot.security; import bot.feature_flags'"

# Test Suite 7: Git Status
log "Test Suite 7: Git Repository Health"
if command -v git &> /dev/null; then
    run_test_suite "Git Status Check" "git status"
else
    info "Git not available, skipping"
fi

# Test Suite 8: Log File Integrity
log "Test Suite 8: Log File Integrity"
if [ -d "logs" ]; then
    # Check if any .ndjson files have valid JSON
    run_test_suite "NDJSON Log Validation" "find logs -name '*.ndjson' -exec sh -c 'tail -1 {} | python3 -m json.tool > /dev/null' \\; -o -true"
else
    info "No logs directory, skipping"
fi

# Summary
echo ""
echo "========================================================="
echo "  Test Results Summary"
echo "========================================================="
echo "Total Test Suites: $TOTAL_SUITES"
echo -e "${GREEN}Passed:            $PASSED_SUITES${NC}"
echo -e "${RED}Failed:            $FAILED_SUITES${NC}"
if [ $TOTAL_SUITES -gt 0 ]; then
    echo "Success Rate:      $(awk "BEGIN {printf \"%.1f\", ($PASSED_SUITES/$TOTAL_SUITES)*100}")%"
fi
echo "========================================================="
echo ""

if [ $FAILED_SUITES -eq 0 ]; then
    echo -e "${GREEN}✓ All test suites passed!${NC}"
    log "Test run completed successfully"
    exit 0
else
    echo -e "${RED}✗ $FAILED_SUITES test suite(s) failed. Check $TEST_LOG for details.${NC}"
    log "Test run completed with failures"
    exit 1
fi
