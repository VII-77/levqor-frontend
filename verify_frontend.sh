#!/bin/bash
set -euo pipefail

echo "🔍 LEVQOR FRONTEND VERIFICATION SCRIPT"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

FAILURES=0

# Test 1: Check if cookies.ts is tracked in git
echo -n "📋 Test 1: src/lib/cookies.ts tracked in git... "
if git ls-files --error-unmatch levqor-site/src/lib/cookies.ts >/dev/null 2>&1; then
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "   File not tracked. Run: git add levqor-site/src/lib/cookies.ts"
    FAILURES=$((FAILURES + 1))
fi

# Test 2: Check if .gitignore still blocks lib/
echo -n "📋 Test 2: .gitignore does not block lib/... "
if grep -q "^lib/$" .gitignore 2>/dev/null; then
    echo -e "${RED}❌ FAIL${NC}"
    echo "   .gitignore still contains 'lib/' rule"
    FAILURES=$((FAILURES + 1))
else
    echo -e "${GREEN}✅ PASS${NC}"
fi

# Test 3: Local build check
echo -n "📋 Test 3: Frontend builds locally... "
cd levqor-site
if npm run build >/dev/null 2>&1; then
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "   Run 'cd levqor-site && npm run build' to see errors"
    FAILURES=$((FAILURES + 1))
fi
cd ..

# Test 4: Live site HTTP 200
echo -n "📋 Test 4: https://www.levqor.ai returns HTTP 200... "
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://www.levqor.ai)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ PASS (HTTP $HTTP_CODE)${NC}"
else
    echo -e "${RED}❌ FAIL (HTTP $HTTP_CODE)${NC}"
    FAILURES=$((FAILURES + 1))
fi

# Test 5: Live site contains correct title
echo -n "📋 Test 5: Live site contains expected title... "
if curl -s https://www.levqor.ai | grep -q "Automate work. Ship faster."; then
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "   Title not found in HTML"
    FAILURES=$((FAILURES + 1))
fi

# Test 6: CSS stylesheets present
echo -n "📋 Test 6: Live site has CSS stylesheets... "
if curl -s https://www.levqor.ai | grep -q '<link rel="stylesheet"'; then
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "   No stylesheet links found"
    FAILURES=$((FAILURES + 1))
fi

# Test 7: Check one CSS file loads
echo -n "📋 Test 7: CSS file returns HTTP 200... "
CSS_URL=$(curl -s https://www.levqor.ai | grep -o '/_next/static/css/[^"]*\.css' | head -n1)
if [ -n "$CSS_URL" ]; then
    CSS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://www.levqor.ai$CSS_URL")
    if [ "$CSS_CODE" = "200" ]; then
        echo -e "${GREEN}✅ PASS (HTTP $CSS_CODE)${NC}"
    else
        echo -e "${RED}❌ FAIL (HTTP $CSS_CODE)${NC}"
        FAILURES=$((FAILURES + 1))
    fi
else
    echo -e "${YELLOW}⚠️  SKIP (no CSS URL found)${NC}"
fi

# Final summary
echo ""
echo "========================================"
if [ $FAILURES -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED${NC}"
    echo "Frontend is healthy and deployed correctly."
    exit 0
else
    echo -e "${RED}❌ $FAILURES TEST(S) FAILED${NC}"
    echo "Review failures above and fix before deploying."
    exit 1
fi
