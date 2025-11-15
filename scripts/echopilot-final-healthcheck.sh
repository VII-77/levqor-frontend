#!/bin/bash
#
# EchoPilot Final Health Check
# Comprehensive system health verification for Levqor + EchoPilot
#
# Usage: ./scripts/echopilot-final-healthcheck.sh
# Requirements: Backend must be running (gunicorn or python run.py)
#

set -e

REPORT_FILE="ECHOPILOT-FINAL-HEALTH-REPORT.md"
RAW_LOG="integrity_reports/ECHOPILOT-FINAL-HEALTH-RAW.log"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   🧠 ECHOPILOT FINAL HEALTH CHECK                           ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
echo ""

# Initialize counters
PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

# Create/overwrite report file
cat > "$REPORT_FILE" << 'REPORT_HEADER'
# ECHOPILOT FINAL HEALTH REPORT

**Generated:** TIMESTAMP_PLACEHOLDER  
**System:** Levqor + EchoPilot Genesis v8.0

## HEALTH CHECK RESULTS

REPORT_HEADER

sed -i "s/TIMESTAMP_PLACEHOLDER/$(date -u +"%Y-%m-%d %H:%M:%S UTC")/" "$REPORT_FILE"

# Redirect all output to log file as well
exec > >(tee -a "$RAW_LOG") 2>&1

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  LOCAL BACKEND HEALTH CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Try primary endpoint first
echo -n "Testing http://localhost:8000/health ... "
LOCAL_RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:8000/health 2>/dev/null || echo "FAILED\n000")
LOCAL_BODY=$(echo "$LOCAL_RESPONSE" | head -n -1)
LOCAL_CODE=$(echo "$LOCAL_RESPONSE" | tail -n 1)

if [ "$LOCAL_CODE" = "200" ]; then
    echo "✅ PASS (HTTP $LOCAL_CODE)"
    echo "Response: $LOCAL_BODY"
    ((PASS_COUNT++))
    echo -e "\n### ✅ Local Backend Health\n" >> "$REPORT_FILE"
    echo "- **Endpoint:** http://localhost:8000/health" >> "$REPORT_FILE"
    echo "- **Status:** HTTP $LOCAL_CODE (PASS)" >> "$REPORT_FILE"
    echo "- **Response:** \`$LOCAL_BODY\`" >> "$REPORT_FILE"
    echo "- **Reason:** Backend is running and responding correctly on localhost." >> "$REPORT_FILE"
elif [ "$LOCAL_CODE" = "404" ]; then
    echo "⚠️  404 - Trying /internal/health ..."
    LOCAL_RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:8000/internal/health 2>/dev/null || echo "FAILED\n000")
    LOCAL_BODY=$(echo "$LOCAL_RESPONSE" | head -n -1)
    LOCAL_CODE=$(echo "$LOCAL_RESPONSE" | tail -n 1)
    if [ "$LOCAL_CODE" = "200" ]; then
        echo "✅ PASS (HTTP $LOCAL_CODE on /internal/health)"
        ((PASS_COUNT++))
        echo -e "\n### ✅ Local Backend Health\n" >> "$REPORT_FILE"
        echo "- **Endpoint:** http://localhost:8000/internal/health" >> "$REPORT_FILE"
        echo "- **Status:** HTTP $LOCAL_CODE (PASS)" >> "$REPORT_FILE"
        echo "- **Note:** /health returned 404, but /internal/health works." >> "$REPORT_FILE"
    else
        echo "❌ FAIL (HTTP $LOCAL_CODE)"
        ((FAIL_COUNT++))
        echo -e "\n### ❌ Local Backend Health\n" >> "$REPORT_FILE"
        echo "- **Status:** Both /health and /internal/health failed" >> "$REPORT_FILE"
        echo "- **Reason:** Backend may not be running or endpoints not configured." >> "$REPORT_FILE"
    fi
else
    echo "❌ FAIL (HTTP $LOCAL_CODE)"
    ((FAIL_COUNT++))
    echo -e "\n### ❌ Local Backend Health\n" >> "$REPORT_FILE"
    echo "- **Status:** HTTP $LOCAL_CODE (FAIL)" >> "$REPORT_FILE"
    echo "- **Reason:** Backend not responding. Ensure backend is running with \`gunicorn run:app\`" >> "$REPORT_FILE"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  DEPLOYED BACKEND HEALTH CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo -n "Testing https://levqor-backend.replit.app/health ... "
DEPLOYED_RESPONSE=$(curl -s -w "\n%{http_code}" https://levqor-backend.replit.app/health 2>/dev/null || echo "FAILED\n000")
DEPLOYED_BODY=$(echo "$DEPLOYED_RESPONSE" | head -n -1)
DEPLOYED_CODE=$(echo "$DEPLOYED_RESPONSE" | tail -n 1)

if [ "$DEPLOYED_CODE" = "200" ]; then
    echo "✅ PASS (HTTP $DEPLOYED_CODE)"
    echo "Response: $DEPLOYED_BODY"
    ((PASS_COUNT++))
    echo -e "\n### ✅ Deployed Backend Health\n" >> "$REPORT_FILE"
    echo "- **Endpoint:** https://levqor-backend.replit.app/health" >> "$REPORT_FILE"
    echo "- **Status:** HTTP $DEPLOYED_CODE (PASS)" >> "$REPORT_FILE"
    echo "- **Response:** \`$DEPLOYED_BODY\`" >> "$REPORT_FILE"
    echo "- **Reason:** Deployed backend is running and healthy." >> "$REPORT_FILE"
elif [ "$DEPLOYED_CODE" = "404" ]; then
    echo "⚠️  404 - Trying /internal/health ..."
    DEPLOYED_RESPONSE=$(curl -s -w "\n%{http_code}" https://levqor-backend.replit.app/internal/health 2>/dev/null || echo "FAILED\n000")
    DEPLOYED_BODY=$(echo "$DEPLOYED_RESPONSE" | head -n -1)
    DEPLOYED_CODE=$(echo "$DEPLOYED_RESPONSE" | tail -n 1)
    if [ "$DEPLOYED_CODE" = "200" ]; then
        echo "⚠️  WARN (HTTP $DEPLOYED_CODE on /internal/health)"
        ((WARN_COUNT++))
        echo -e "\n### ⚠️ Deployed Backend Health\n" >> "$REPORT_FILE"
        echo "- **Endpoint:** https://levqor-backend.replit.app/internal/health" >> "$REPORT_FILE"
        echo "- **Status:** HTTP $DEPLOYED_CODE (WARN)" >> "$REPORT_FILE"
        echo "- **Note:** /health returned 404, but /internal/health works. Add /health route." >> "$REPORT_FILE"
    else
        echo "❌ FAIL (HTTP $DEPLOYED_CODE)"
        ((FAIL_COUNT++))
        echo -e "\n### ❌ Deployed Backend Health\n" >> "$REPORT_FILE"
        echo "- **Status:** HTTP $DEPLOYED_CODE (FAIL)" >> "$REPORT_FILE"
        echo "- **Reason:** Backend not deployed or routing broken." >> "$REPORT_FILE"
        echo "- **Action:** Open Replit Deployments tab and verify deployment is active." >> "$REPORT_FILE"
    fi
else
    echo "❌ FAIL (HTTP $DEPLOYED_CODE)"
    ((FAIL_COUNT++))
    echo -e "\n### ❌ Deployed Backend Health\n" >> "$REPORT_FILE"
    echo "- **Status:** HTTP $DEPLOYED_CODE (FAIL)" >> "$REPORT_FILE"
    echo "- **Reason:** Deployment may be stopped or misconfigured." >> "$REPORT_FILE"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  PUBLIC API HEALTH CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo -n "Testing https://api.levqor.ai/health ... "
PUBLIC_RESPONSE=$(curl -s -w "\n%{http_code}" https://api.levqor.ai/health 2>/dev/null || echo "FAILED\n000")
PUBLIC_BODY=$(echo "$PUBLIC_RESPONSE" | head -n -1)
PUBLIC_CODE=$(echo "$PUBLIC_RESPONSE" | tail -n 1)

if [ "$PUBLIC_CODE" = "200" ]; then
    echo "✅ PASS (HTTP $PUBLIC_CODE)"
    echo "Response: $PUBLIC_BODY"
    ((PASS_COUNT++))
    echo -e "\n### ✅ Public API Health\n" >> "$REPORT_FILE"
    echo "- **Endpoint:** https://api.levqor.ai/health" >> "$REPORT_FILE"
    echo "- **Status:** HTTP $PUBLIC_CODE (PASS)" >> "$REPORT_FILE"
    echo "- **Response:** \`$PUBLIC_BODY\`" >> "$REPORT_FILE"
    echo "- **Reason:** Public API domain is routing correctly to backend." >> "$REPORT_FILE"
elif [ "$PUBLIC_CODE" = "404" ]; then
    echo "❌ FAIL (HTTP 404)"
    ((FAIL_COUNT++))
    echo -e "\n### ❌ Public API Health\n" >> "$REPORT_FILE"
    echo "- **Endpoint:** https://api.levqor.ai/health" >> "$REPORT_FILE"
    echo "- **Status:** HTTP 404 (FAIL)" >> "$REPORT_FILE"
    echo "- **Reason:** Cloudflare routing or backend deployment broken." >> "$REPORT_FILE"
    echo "- **Action:** First fix deployed backend health, then check Cloudflare CNAME." >> "$REPORT_FILE"
else
    echo "❌ FAIL (HTTP $PUBLIC_CODE)"
    ((FAIL_COUNT++))
    echo -e "\n### ❌ Public API Health\n" >> "$REPORT_FILE"
    echo "- **Status:** HTTP $PUBLIC_CODE (FAIL)" >> "$REPORT_FILE"
    echo "- **Reason:** API domain not reachable or misconfigured." >> "$REPORT_FILE"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣  STRIPE CONNECTIVITY CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -z "$STRIPE_SECRET_KEY" ]; then
    echo "⚠️  WARN - STRIPE_SECRET_KEY not set"
    ((WARN_COUNT++))
    echo -e "\n### ⚠️ Stripe Connectivity\n" >> "$REPORT_FILE"
    echo "- **Status:** WARN" >> "$REPORT_FILE"
    echo "- **Reason:** STRIPE_SECRET_KEY environment variable not set." >> "$REPORT_FILE"
    echo "- **Action:** Set STRIPE_SECRET_KEY in Replit Secrets." >> "$REPORT_FILE"
else
    echo -n "Testing Stripe API connectivity ... "
    STRIPE_RESPONSE=$(curl -s -w "\n%{http_code}" https://api.stripe.com/v1/products?limit=1 \
        -u "$STRIPE_SECRET_KEY:" 2>/dev/null || echo "FAILED\n000")
    STRIPE_CODE=$(echo "$STRIPE_RESPONSE" | tail -n 1)
    
    if [ "$STRIPE_CODE" = "200" ]; then
        echo "✅ PASS (HTTP $STRIPE_CODE)"
        ((PASS_COUNT++))
        echo -e "\n### ✅ Stripe Connectivity\n" >> "$REPORT_FILE"
        echo "- **Status:** PASS" >> "$REPORT_FILE"
        echo "- **Reason:** Stripe API key is valid and API is reachable." >> "$REPORT_FILE"
    else
        echo "❌ FAIL (HTTP $STRIPE_CODE)"
        ((FAIL_COUNT++))
        echo -e "\n### ❌ Stripe Connectivity\n" >> "$REPORT_FILE"
        echo "- **Status:** HTTP $STRIPE_CODE (FAIL)" >> "$REPORT_FILE"
        echo "- **Reason:** Stripe API key invalid or API unreachable." >> "$REPORT_FILE"
        echo "- **Action:** Verify STRIPE_SECRET_KEY in Replit Secrets is correct." >> "$REPORT_FILE"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5️⃣  SCHEDULER SANITY CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo -n "Checking APScheduler configuration ... "
if grep -q "scheduler.add_job\|@scheduler.scheduled_job" monitors/scheduler.py 2>/dev/null; then
    echo "✅ PASS"
    ((PASS_COUNT++))
    echo -e "\n### ✅ Scheduler Configuration\n" >> "$REPORT_FILE"
    echo "- **Status:** PASS" >> "$REPORT_FILE"
    echo "- **Reason:** APScheduler jobs detected in monitors/scheduler.py." >> "$REPORT_FILE"
else
    echo "❌ FAIL"
    ((FAIL_COUNT++))
    echo -e "\n### ❌ Scheduler Configuration\n" >> "$REPORT_FILE"
    echo "- **Status:** FAIL" >> "$REPORT_FILE"
    echo "- **Reason:** No APScheduler jobs found in scheduler.py." >> "$REPORT_FILE"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6️⃣  DATABASE CONNECTIVITY CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo -n "Testing database connectivity ... "
DB_PATH="${DATABASE_PATH:-levqor.db}"

if [ -f "$DB_PATH" ]; then
    if sqlite3 "$DB_PATH" "SELECT 1;" > /dev/null 2>&1; then
        echo "✅ PASS (SQLite)"
        ((PASS_COUNT++))
        echo -e "\n### ✅ Database Connectivity\n" >> "$REPORT_FILE"
        echo "- **Status:** PASS" >> "$REPORT_FILE"
        echo "- **Database:** SQLite ($DB_PATH)" >> "$REPORT_FILE"
        echo "- **Reason:** Database file exists and is readable." >> "$REPORT_FILE"
    else
        echo "❌ FAIL (corrupt database)"
        ((FAIL_COUNT++))
        echo -e "\n### ❌ Database Connectivity\n" >> "$REPORT_FILE"
        echo "- **Status:** FAIL" >> "$REPORT_FILE"
        echo "- **Reason:** Database file exists but cannot be queried." >> "$REPORT_FILE"
    fi
else
    echo "⚠️  WARN (database file not found)"
    ((WARN_COUNT++))
    echo -e "\n### ⚠️ Database Connectivity\n" >> "$REPORT_FILE"
    echo "- **Status:** WARN" >> "$REPORT_FILE"
    echo "- **Reason:** Database file not found at $DB_PATH." >> "$REPORT_FILE"
    echo "- **Note:** Database may be initialized on first backend run." >> "$REPORT_FILE"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "FINAL RESULTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ PASS:  $PASS_COUNT"
echo "⚠️  WARN:  $WARN_COUNT"
echo "❌ FAIL:  $FAIL_COUNT"
echo ""

# Determine overall status
if [ $FAIL_COUNT -eq 0 ] && [ $WARN_COUNT -eq 0 ]; then
    OVERALL="PASS"
    echo "🟢 OVERALL: PASS - All systems healthy"
elif [ $FAIL_COUNT -eq 0 ]; then
    OVERALL="WARNING"
    echo "🟡 OVERALL: WARNING - Some warnings present"
else
    OVERALL="FAIL"
    echo "🔴 OVERALL: FAIL - Critical issues detected"
fi

# Write summary to report
cat >> "$REPORT_FILE" << REPORT_SUMMARY

---

## SUMMARY

**Overall Status:** $OVERALL

**Results:**
- ✅ Pass: $PASS_COUNT
- ⚠️ Warn: $WARN_COUNT
- ❌ Fail: $FAIL_COUNT

**Generated:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")

REPORT_SUMMARY

echo ""
echo "📄 Report saved to: $REPORT_FILE"
echo "📄 Raw log saved to: $RAW_LOG"
echo ""

if [ "$OVERALL" = "FAIL" ]; then
    exit 1
else
    exit 0
fi
