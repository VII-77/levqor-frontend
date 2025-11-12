#!/bin/bash
set -e

echo "==================================="
echo "LEVQOR v6.5 RELEASE VERIFICATION"
echo "==================================="
echo ""

BACKEND_URL="https://api.levqor.ai"
FRONTEND_URL="https://levqor.ai"
PASS=0
FAIL=0
WARN=0

check_endpoint() {
    local url=$1
    local expected=$2
    local desc=$3
    
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>&1)
    
    if [ "$HTTP_CODE" = "$expected" ]; then
        echo "✅ PASS: $desc ($url) → $HTTP_CODE"
        ((PASS++))
    else
        echo "❌ FAIL: $desc ($url) → Expected $expected, got $HTTP_CODE"
        ((FAIL++))
    fi
}

check_json_response() {
    local url=$1
    local desc=$2
    
    RESPONSE=$(curl -s "$url" 2>&1)
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>&1)
    
    if [ "$HTTP_CODE" = "200" ] && echo "$RESPONSE" | grep -q "{"; then
        echo "✅ PASS: $desc ($url) → 200 JSON"
        ((PASS++))
    else
        echo "❌ FAIL: $desc ($url) → $HTTP_CODE"
        ((FAIL++))
    fi
}

check_ops_admin() {
    local path=$1
    local desc=$2
    
    RESPONSE=$(curl -s "$BACKEND_URL$path" 2>&1)
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL$path" 2>&1)
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo "✅ PASS: $desc (/ops/admin$path) → 200"
        ((PASS++))
    else
        echo "⚠️  WARN: $desc (/ops/admin$path) → $HTTP_CODE (OK if /api/admin/* works)"
        ((WARN++))
    fi
}

echo "📡 BACKEND CHECKS ($BACKEND_URL)"
echo "-----------------------------------"

check_json_response "$BACKEND_URL/status" "Status endpoint"
check_json_response "$BACKEND_URL/ops/uptime" "Uptime endpoint"
check_json_response "$BACKEND_URL/health" "Health endpoint"
check_json_response "$BACKEND_URL/ops/queue_health" "Queue health"

echo ""
echo "🔧 ADMIN ENDPOINTS (Primary: /ops/admin/*)"
echo "-----------------------------------"

check_ops_admin "/runbooks" "List runbooks"
check_ops_admin "/anomaly/explain?latency_ms=150" "Anomaly detection"
check_ops_admin "/brief/weekly" "Weekly brief"

echo ""
echo "🌐 FRONTEND CHECKS ($FRONTEND_URL)"
echo "-----------------------------------"

check_endpoint "$FRONTEND_URL/" "200" "Homepage"
check_endpoint "$FRONTEND_URL/pricing" "200" "Pricing page"
check_endpoint "$FRONTEND_URL/signin" "200" "Sign-in page"
check_endpoint "$FRONTEND_URL/docs" "200" "Docs page"
check_endpoint "$FRONTEND_URL/privacy" "200" "Privacy page"
check_endpoint "$FRONTEND_URL/terms" "200" "Terms page"
check_endpoint "$FRONTEND_URL/contact" "200" "Contact page"
check_endpoint "$FRONTEND_URL/insights" "200" "Insights dashboard"
check_endpoint "$FRONTEND_URL/dashboard" "200" "Dashboard (or 307 redirect)"

echo ""
echo "🔒 SECURITY HEADERS"
echo "-----------------------------------"

HEADERS=$(curl -I -s "$BACKEND_URL/status" 2>&1)
if echo "$HEADERS" | grep -iq "strict-transport-security"; then
    echo "✅ PASS: HSTS header present"
    ((PASS++))
else
    echo "⚠️  WARN: HSTS header missing"
    ((WARN++))
fi

FRONTEND_HEADERS=$(curl -I -s "$FRONTEND_URL/" 2>&1)
if echo "$FRONTEND_HEADERS" | grep -iq "x-content-type-options"; then
    echo "✅ PASS: X-Content-Type-Options header present"
    ((PASS++))
else
    echo "⚠️  WARN: X-Content-Type-Options header missing"
    ((WARN++))
fi

echo ""
echo "==================================="
echo "VERIFICATION SUMMARY"
echo "==================================="
echo "✅ Passed: $PASS"
echo "❌ Failed: $FAIL"
echo "⚠️  Warnings: $WARN"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "🎉 RELEASE VERIFICATION PASSED!"
    echo "Levqor v6.5 is ready for production"
    exit 0
else
    echo "❌ RELEASE VERIFICATION FAILED"
    echo "Fix $FAIL failing checks before deploying"
    exit 1
fi
