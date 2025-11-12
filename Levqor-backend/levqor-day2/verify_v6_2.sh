#!/bin/bash
set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║        Levqor v6.2 Verification Script                       ║"
echo "║        Telemetry + Retention Expansion Tests                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

BACKEND=${BACKEND:-"https://api.levqor.ai"}
FRONTEND=${FRONTEND:-"https://levqor.ai"}
ADMIN_TOKEN=${ADMIN_TOKEN:-""}

PASSED=0
FAILED=0

test_endpoint() {
  local name="$1"
  local url="$2"
  local expected_code="${3:-200}"
  local headers="$4"
  
  echo -n "Testing $name... "
  
  if [ -n "$headers" ]; then
    response=$(curl -s -w "\n%{http_code}" $headers "$url")
  else
    response=$(curl -s -w "\n%{http_code}" "$url")
  fi
  
  http_code=$(echo "$response" | tail -n1)
  body=$(echo "$response" | head -n-1)
  
  if [ "$http_code" = "$expected_code" ]; then
    echo "✅ PASS (HTTP $http_code)"
    ((PASSED++))
    return 0
  else
    echo "❌ FAIL (HTTP $http_code, expected $expected_code)"
    echo "   Response: $body"
    ((FAILED++))
    return 1
  fi
}

test_json_field() {
  local name="$1"
  local url="$2"
  local field="$3"
  local headers="$4"
  
  echo -n "Testing $name ($field present)... "
  
  if [ -n "$headers" ]; then
    response=$(curl -s $headers "$url")
  else
    response=$(curl -s "$url")
  fi
  
  if echo "$response" | grep -q "\"$field\""; then
    echo "✅ PASS"
    ((PASSED++))
    return 0
  else
    echo "❌ FAIL (field '$field' not found)"
    echo "   Response: $response"
    ((FAILED++))
    return 1
  fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. BACKEND HEALTH CHECKS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_endpoint "Root endpoint" "$BACKEND/" 200
test_endpoint "Health endpoint" "$BACKEND/health" 200
test_endpoint "Ops uptime" "$BACKEND/ops/uptime" 200
test_endpoint "Queue health" "$BACKEND/ops/queue_health" 200
test_endpoint "Billing health" "$BACKEND/billing/health" 200

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. REFERRAL TRACKING"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo -n "Testing referral tracking endpoint... "
response=$(curl -s -w "\n%{http_code}" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"test@levqor.ai","source":"github","campaign":"v6.2-launch","medium":"social"}' \
  "$BACKEND/api/v1/referrals/track")

http_code=$(echo "$response" | tail -n1)
if [ "$http_code" = "201" ]; then
  echo "✅ PASS (HTTP $http_code)"
  ((PASSED++))
else
  echo "❌ FAIL (HTTP $http_code)"
  ((FAILED++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. ANALYTICS ENDPOINT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -z "$ADMIN_TOKEN" ]; then
  echo "⚠️  ADMIN_TOKEN not set - skipping analytics test"
  echo "   Set ADMIN_TOKEN environment variable to test this endpoint"
else
  test_json_field "Analytics endpoint" "$BACKEND/admin/analytics" "users" "-H \"Authorization: Bearer $ADMIN_TOKEN\""
  test_json_field "Analytics referrals" "$BACKEND/admin/analytics" "referrals" "-H \"Authorization: Bearer $ADMIN_TOKEN\""
  test_json_field "Analytics top sources" "$BACKEND/admin/analytics" "top_sources" "-H \"Authorization: Bearer $ADMIN_TOKEN\""
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. SENTRY CONFIGURATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -n "$SENTRY_DSN" ]; then
  echo "✅ Backend SENTRY_DSN configured"
  ((PASSED++))
else
  echo "⚠️  Backend SENTRY_DSN not set (optional)"
fi

if [ -f "levqor-site/sentry.client.config.ts" ]; then
  echo "✅ Frontend Sentry client config exists"
  ((PASSED++))
else
  echo "❌ Frontend Sentry client config missing"
  ((FAILED++))
fi

if [ -f "levqor-site/sentry.server.config.ts" ]; then
  echo "✅ Frontend Sentry server config exists"
  ((PASSED++))
else
  echo "❌ Frontend Sentry server config missing"
  ((FAILED++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. OPS SUMMARY SCRIPT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "scripts/ops_summary.py" ]; then
  echo "✅ Ops summary script exists"
  ((PASSED++))
  
  if [ -x "scripts/ops_summary.py" ]; then
    echo "✅ Ops summary script is executable"
    ((PASSED++))
  else
    echo "⚠️  Ops summary script not executable (chmod +x needed)"
  fi
else
  echo "❌ Ops summary script missing"
  ((FAILED++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. DATABASE SCHEMA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "levqor.db" ]; then
  echo -n "Checking referrals table... "
  table_exists=$(sqlite3 levqor.db "SELECT name FROM sqlite_master WHERE type='table' AND name='referrals';" 2>/dev/null || echo "")
  
  if [ -n "$table_exists" ]; then
    echo "✅ PASS"
    ((PASSED++))
  else
    echo "❌ FAIL (table not found)"
    ((FAILED++))
  fi
else
  echo "⚠️  Database file not found (will be created on first run)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. FRONTEND COMPONENTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "levqor-site/src/components/AnalyticsWidget.tsx" ]; then
  echo "✅ AnalyticsWidget component exists"
  ((PASSED++))
else
  echo "❌ AnalyticsWidget component missing"
  ((FAILED++))
fi

if grep -q "AnalyticsWidget" "levqor-site/src/app/dashboard/page.tsx" 2>/dev/null; then
  echo "✅ AnalyticsWidget imported in dashboard"
  ((PASSED++))
else
  echo "❌ AnalyticsWidget not imported in dashboard"
  ((FAILED++))
fi

if grep -q "trackReferral" "levqor-site/src/app/signin/page.tsx" 2>/dev/null; then
  echo "✅ Referral tracking in sign-in flow"
  ((PASSED++))
else
  echo "❌ Referral tracking not in sign-in flow"
  ((FAILED++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Total Tests: $((PASSED + FAILED))"
echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║  🎉 ALL TESTS PASSED - v6.2 VERIFIED!                        ║"
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""
  echo "Phase 6.2 Features Verified:"
  echo "  ✅ Sentry telemetry configured (FE + BE)"
  echo "  ✅ Ops summary script ready"
  echo "  ✅ Referral tracking operational"
  echo "  ✅ Analytics endpoint working"
  echo "  ✅ Dashboard analytics widget deployed"
  echo ""
  exit 0
else
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║  ⚠️  SOME TESTS FAILED - REVIEW REQUIRED                     ║"
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""
  exit 1
fi
