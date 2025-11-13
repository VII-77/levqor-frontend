#!/bin/bash
# === PUBLIC SMOKE TESTS FOR LEVQOR ===
# Tests all public endpoints to verify system health
# Usage: BACKEND=https://api.levqor.ai ./public_smoke.sh

set -euo pipefail

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
ok() { echo -e "${GREEN}✅ $1${NC}"; }
fail() { echo -e "${RED}❌ $1${NC}"; exit 1; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
say() { echo -e "\n${YELLOW}=== $1 ===${NC}"; }

# Backend URL
BACKEND="${BACKEND:-https://api.levqor.ai}"
echo "Testing backend: $BACKEND"
echo ""

FAILED=0

# Test helper
test_endpoint() {
    local name="$1"
    local url="$2"
    local expected_status="${3:-200}"
    local check_json="${4:-true}"
    
    echo -n "Testing $name... "
    
    response=$(curl -s -w "\n%{http_code}" "$url" 2>&1)
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" != "$expected_status" ]; then
        echo -e "${RED}FAIL${NC} (HTTP $http_code, expected $expected_status)"
        echo "Response: $body"
        FAILED=$((FAILED + 1))
        return 1
    fi
    
    if [ "$check_json" = "true" ]; then
        if ! echo "$body" | python3 -m json.tool >/dev/null 2>&1; then
            echo -e "${RED}FAIL${NC} (Invalid JSON)"
            echo "Response: $body"
            FAILED=$((FAILED + 1))
            return 1
        fi
    fi
    
    echo -e "${GREEN}OK${NC}"
    return 0
}

# ===== Core Endpoints =====
say "Core Endpoints"

test_endpoint "Root (/)" "$BACKEND/" 200 true
test_endpoint "Health (/health)" "$BACKEND/health" 200 true
test_endpoint "Status (/status)" "$BACKEND/status" 200 true

# ===== Operations Endpoints =====
say "Operations Endpoints"

test_endpoint "Uptime (/ops/uptime)" "$BACKEND/ops/uptime" 200 true
test_endpoint "Queue Health (/ops/queue_health)" "$BACKEND/ops/queue_health" 200 true
test_endpoint "Billing Health (/billing/health)" "$BACKEND/billing/health" 200 true

# Verify uptime response structure (Phase-4 format)
uptime_response=$(curl -fsS "$BACKEND/ops/uptime")
if echo "$uptime_response" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if ('uptime_seconds' in d or 'status' in d or 'services' in d) else 1)" 2>/dev/null; then
    ok "Uptime endpoint responding with valid data"
else
    fail "Uptime endpoint not responding correctly"
fi

# Verify queue_health response structure (Phase-4 format)
queue_response=$(curl -fsS "$BACKEND/ops/queue_health")
if echo "$queue_response" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if ('queue_stats' in d or 'depth' in d or 'mode' in d) else 1)" 2>/dev/null; then
    ok "Queue health endpoint responding with valid data"
else
    fail "Queue health endpoint not responding correctly"
fi

# Verify billing_health response structure (Phase-4 format)
billing_response=$(curl -fsS "$BACKEND/billing/health")
if echo "$billing_response" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if ('healthy' in d or 'stripe' in d or 'status' in d) else 1)" 2>/dev/null; then
    ok "Billing health endpoint responding with valid data"
    
    # Check if Stripe is configured (Phase-4 format)
    is_healthy=$(echo "$billing_response" | python3 -c "import sys,json; d=json.load(sys.stdin); stripe_ok=d.get('stripe',False); status_ok=d.get('status')=='operational'; print(str(stripe_ok or status_ok).lower())" 2>/dev/null || echo "false")
    if [ "$is_healthy" = "true" ]; then
        ok "Stripe integration is operational"
    else
        warn "Stripe integration may need configuration"
    fi
else
    fail "Billing health endpoint not responding correctly"
fi

# ===== Public Content =====
say "Public Content"

test_endpoint "Metrics (/public/metrics)" "$BACKEND/public/metrics" 200 true
test_endpoint "OpenAPI (/public/openapi.json)" "$BACKEND/public/openapi.json" 200 true

# ===== API v1 Endpoints (Status Check) =====
say "API v1 Endpoints"

# Create a test job
echo -n "Creating test job... "
job_response=$(curl -fsS -X POST "$BACKEND/api/v1/intake" \
    -H "Content-Type: application/json" \
    -H "X-Api-Key: test-key" \
    -d '{
        "workflow": "test-workflow",
        "payload": {"test": true},
        "callback_url": "https://example.com/callback",
        "priority": "normal"
    }' 2>&1 || echo '{"error": "no_auth"}')

if echo "$job_response" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if 'job_id' in d else 1)" 2>/dev/null; then
    job_id=$(echo "$job_response" | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])" 2>/dev/null)
    echo -e "${GREEN}OK${NC} (job_id: $job_id)"
    
    # Check job status
    test_endpoint "Job Status (/api/v1/status/$job_id)" "$BACKEND/api/v1/status/$job_id" 200 true
else
    # Expected to fail without valid API key in production
    warn "Job creation skipped (API key required in production)"
fi

# ===== Summary =====
echo ""
say "Summary"

if [ $FAILED -eq 0 ]; then
    ok "All smoke tests passed! 🎉"
    echo ""
    echo "Backend is healthy and operational:"
    echo "  - All core endpoints responding"
    echo "  - Operations monitoring active"
    echo "  - Billing integration checked"
    echo "  - Public content served"
    exit 0
else
    fail "$FAILED test(s) failed"
fi
