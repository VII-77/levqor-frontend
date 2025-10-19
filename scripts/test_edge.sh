#!/bin/bash

# EchoPilot Edge Routing Test Script
# Tests endpoints with and without Railway fallback

set -e

echo "======================================"
echo "  EchoPilot Edge Routing Test"
echo "======================================"
echo ""

# Configuration
BASE_URL="${BASE_URL:-https://echopilotai.replit.app}"
EDGE_ENABLE="${EDGE_ENABLE:-false}"
EDGE_BASE_URL="${EDGE_BASE_URL:-}"
SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN:-}"
HEALTH_TOKEN="${HEALTH_TOKEN:-}"
TS=$(date +%s)

echo "Configuration:"
echo "  Base URL:        $BASE_URL"
echo "  Edge Enable:     $EDGE_ENABLE"
echo "  Edge Base URL:   $EDGE_BASE_URL"
echo "  Timestamp:       $TS"
echo ""

# Color output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

test_endpoint() {
    local name=$1
    local url=$2
    local expected_code=${3:-200}
    
    echo -n "Testing $name... "
    
    response_code=$(curl -s -o /dev/null -w "%{http_code}" "$url" || echo "000")
    
    if [ "$response_code" = "$expected_code" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $response_code)"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $response_code, expected $expected_code)"
        return 1
    fi
}

echo "======================================"
echo "  Core Endpoints (Always Work)"
echo "======================================"
echo ""

test_endpoint "/health" "$BASE_URL/health?_t=$TS" 200
test_endpoint "/" "$BASE_URL/?_t=$TS" 200

echo ""
echo "======================================"
echo "  Proxy-Affected Endpoints"
echo "  (404 on Replit, OK on Railway)"
echo "======================================"
echo ""

if [ "$EDGE_ENABLE" = "true" ] && [ -n "$EDGE_BASE_URL" ]; then
    echo -e "${YELLOW}Railway fallback ENABLED${NC}"
    echo "Endpoints will proxy to: $EDGE_BASE_URL"
    echo ""
    EXPECTED=200
else
    echo -e "${YELLOW}Railway fallback DISABLED${NC}"
    echo "Endpoints will return 404 due to Replit proxy"
    echo ""
    EXPECTED=404
fi

test_endpoint "/supervisor" "$BASE_URL/supervisor?token=$SUPERVISOR_TOKEN&_t=$TS" "$EXPECTED" || true
test_endpoint "/forecast" "$BASE_URL/forecast?_t=$TS" "$EXPECTED" || true
test_endpoint "/metrics" "$BASE_URL/metrics?_t=$TS" "$EXPECTED" || true

echo ""
echo "======================================"
echo "  POST Endpoints"
echo "======================================"
echo ""

echo -n "Testing /pulse (POST)... "
response_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/pulse?token=$HEALTH_TOKEN&_t=$TS" || echo "000")

if [ "$EDGE_ENABLE" = "true" ] && [ -n "$EDGE_BASE_URL" ]; then
    EXPECTED=200
else
    EXPECTED=404
fi

if [ "$response_code" = "$EXPECTED" ]; then
    echo -e "${GREEN}✓ PASS${NC} (HTTP $response_code)"
else
    echo -e "${RED}✗ FAIL${NC} (HTTP $response_code, expected $EXPECTED)"
fi

echo ""
echo "======================================"
echo "  Summary"
echo "======================================"
echo ""

if [ "$EDGE_ENABLE" = "true" ] && [ -n "$EDGE_BASE_URL" ]; then
    echo -e "${GREEN}✓ Railway fallback ACTIVE${NC}"
    echo "  All endpoints should work via proxy"
    echo ""
    echo "To verify Railway deployment:"
    echo "  curl -fsS $EDGE_BASE_URL/health"
else
    echo -e "${YELLOW}⚠ Railway fallback DISABLED${NC}"
    echo "  Some endpoints will return 404"
    echo ""
    echo "To enable Railway fallback:"
    echo "  1. Deploy to Railway: https://railway.app"
    echo "  2. Add secrets in Replit:"
    echo "     EDGE_ENABLE=true"
    echo "     EDGE_BASE_URL=https://your-app.railway.app"
    echo "  3. Restart workflow"
    echo "  4. Run this test again"
fi

echo ""
echo "======================================"
echo "  Test Complete"
echo "======================================"
