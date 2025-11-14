#!/bin/bash
# Automated Cache Freshness Check
# Ensures HTML is never cached after deployments
# Usage: ./scripts/check_cache.sh [domain]

set -euo pipefail

DOMAIN="${1:-levqor.ai}"
FAIL=0

echo "============================================================"
echo "CACHE FRESHNESS CHECK - $DOMAIN"
echo "============================================================"
echo "Timestamp: $(date -u)"
echo ""

# Check main domain
echo "--- Checking: https://$DOMAIN"
HEADERS=$(curl -sI "https://$DOMAIN" 2>&1 || echo "")

if [ -z "$HEADERS" ]; then
  echo "❌ FAIL: Could not fetch headers"
  exit 1
fi

echo "$HEADERS" | head -20
echo ""

# Test 1: Content-Type is text/html
if echo "$HEADERS" | grep -qi "content-type.*text/html"; then
  echo "✅ PASS: Content-Type is text/html"
else
  echo "❌ FAIL: Content-Type is not text/html"
  FAIL=1
fi

# Test 2: Cache-Control includes no-store
if echo "$HEADERS" | grep -qi "cache-control.*no-store"; then
  echo "✅ PASS: Cache-Control includes no-store"
else
  echo "❌ FAIL: Cache-Control does not include no-store"
  FAIL=1
fi

# Test 3: Age header is 0 or not present
AGE=$(echo "$HEADERS" | grep -i "^age:" | awk '{print $2}' | tr -d '\r' || echo "0")
if [ "$AGE" = "0" ] || [ -z "$AGE" ]; then
  echo "✅ PASS: HTML is fresh (age: $AGE)"
else
  echo "❌ FAIL: HTML cached with age: $AGE seconds"
  FAIL=1
fi

# Test 4: Vercel cache is MISS or not cached
VCACHE=$(echo "$HEADERS" | grep -i "x-vercel-cache" | awk '{print $2}' | tr -d '\r' || echo "NONE")
if [ "$VCACHE" = "MISS" ] || [ "$VCACHE" = "BYPASS" ] || [ "$VCACHE" = "NONE" ]; then
  echo "✅ PASS: Vercel cache status: $VCACHE"
else
  echo "⚠️  WARN: Vercel cache status: $VCACHE (may indicate cached content)"
  # Don't fail on this - could be legitimate prerender
fi

# Test 5: Security headers present
echo ""
echo "--- Security Headers Check"
if echo "$HEADERS" | grep -qi "strict-transport-security"; then
  echo "✅ HSTS header present"
else
  echo "⚠️  WARN: HSTS header missing"
fi

if echo "$HEADERS" | grep -qi "x-frame-options"; then
  echo "✅ X-Frame-Options present"
else
  echo "⚠️  WARN: X-Frame-Options missing"
fi

if echo "$HEADERS" | grep -qi "x-content-type-options"; then
  echo "✅ X-Content-Type-Options present"
else
  echo "⚠️  WARN: X-Content-Type-Options missing"
fi

echo ""
echo "============================================================"
if [ $FAIL -eq 0 ]; then
  echo "✅ ALL CHECKS PASSED"
  echo "HTML is fresh and properly configured"
  exit 0
else
  echo "❌ CHECKS FAILED"
  echo "HTML may be cached or misconfigured"
  exit 1
fi
