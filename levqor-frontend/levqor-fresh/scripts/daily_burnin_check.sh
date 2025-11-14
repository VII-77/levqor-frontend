#!/bin/bash
# Daily Burn-In Monitoring Script (Days 2-7)
# Run at 09:00 UTC every day
# Usage: ./scripts/daily_burnin_check.sh

set -euo pipefail

DAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

echo "============================================================"
echo "LEVQOR GENESIS v8.0 — DAILY BURN-IN CHECK"
echo "============================================================"
echo "Date: $DAY"
echo "Time: $TIMESTAMP"
echo ""

# Section 1: Go/No-Go Dashboard
echo "== SECTION 1: GO/NO-GO DASHBOARD =="
echo ""
python3 scripts/monitoring/notion_go_nogo_dashboard.py 2>&1 || {
  echo "⚠️  Dashboard script failed"
  echo "Continuing with other checks..."
}
echo ""

# Section 2: Platform Metrics
echo "== SECTION 2: PLATFORM METRICS =="
echo ""
METRICS=$(curl -s https://api.levqor.ai/public/metrics 2>&1 || echo '{}')

if echo "$METRICS" | python3 -m json.tool > /dev/null 2>&1; then
  echo "$METRICS" | python3 -m json.tool
  
  # Extract key values
  UPTIME=$(echo "$METRICS" | python3 -c "import json,sys; print(json.load(sys.stdin).get('uptime_rolling_7d', 0))" 2>/dev/null || echo "0")
  JOBS=$(echo "$METRICS" | python3 -c "import json,sys; print(json.load(sys.stdin).get('jobs_today', 0))" 2>/dev/null || echo "0")
  
  echo ""
  echo "Key Metrics:"
  echo "  Uptime (7d rolling): ${UPTIME}%"
  echo "  Jobs Today: $JOBS"
else
  echo "⚠️  Could not fetch metrics"
  echo "$METRICS"
fi
echo ""

# Section 3: Intelligence API Health
echo "== SECTION 3: INTELLIGENCE API HEALTH =="
echo ""
CID="daily-check-$(date +%s)"

for endpoint in status health; do
  echo "--- Testing: /api/intelligence/$endpoint"
  RESPONSE=$(curl -s -H "X-Request-ID: $CID" \
    "https://api.levqor.ai/api/intelligence/$endpoint" 2>&1 || echo '{"error":"failed"}')
  
  if echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f\"✅ OK - CID: {d.get('meta',{}).get('correlation_id','N/A')}, Duration: {d.get('meta',{}).get('duration_ms','N/A')}ms\")" 2>/dev/null; then
    :
  else
    echo "⚠️  Response: $RESPONSE"
  fi
done
echo ""

# Section 4: Log Analysis
echo "== SECTION 4: LOG ANALYSIS (Last 50 entries) =="
echo ""

echo "--- Synthetic Check Results:"
SYNTHETIC=$(grep -hE "synthetic" /tmp/logs/levqor-backend_*.log 2>/dev/null | tail -10 || echo "No synthetic logs")
if [ "$SYNTHETIC" = "No synthetic logs" ]; then
  echo "$SYNTHETIC"
else
  echo "$SYNTHETIC" | tail -5
  COUNT=$(echo "$SYNTHETIC" | wc -l)
  echo "  ($COUNT recent checks)"
fi
echo ""

echo "--- Alert Check Results:"
ALERTS=$(grep -hE "alert" /tmp/logs/levqor-backend_*.log 2>/dev/null | tail -10 || echo "No alert logs")
if [ "$ALERTS" = "No alert logs" ]; then
  echo "$ALERTS"
else
  echo "$ALERTS" | tail -5
  COUNT=$(echo "$ALERTS" | wc -l)
  echo "  ($COUNT recent alerts)"
fi
echo ""

echo "--- Error Scan (last 100 lines):"
ERRORS=$(grep -hE "ERROR|CRITICAL|Exception" /tmp/logs/levqor-backend_*.log 2>/dev/null | tail -100 || echo "")
if [ -z "$ERRORS" ]; then
  echo "✅ No errors found"
else
  ERROR_COUNT=$(echo "$ERRORS" | wc -l)
  echo "⚠️  Found $ERROR_COUNT error entries"
  echo "Recent errors:"
  echo "$ERRORS" | tail -10
fi
echo ""

# Section 5: Cache Freshness
echo "== SECTION 5: CACHE FRESHNESS CHECK =="
echo ""
./scripts/check_cache.sh www.levqor.ai 2>&1 | grep -E "^✅|^❌|^⚠️" || echo "Cache check completed"
echo ""

# Section 6: Daily Summary Report
echo "============================================================"
echo "DAILY SUMMARY REPORT"
echo "============================================================"
echo "Date: $DAY"
echo ""

# Calculate burn-in day
START_DATE="2025-11-11"
DAYS_ELAPSED=$(( ( $(date -d "$DAY" +%s) - $(date -d "$START_DATE" +%s) ) / 86400 + 1 ))
echo "Burn-In Progress: Day $DAYS_ELAPSED/7"
echo ""

# Extract Go/No-Go metrics (from dashboard output above)
echo "Go/No-Go Status:"
echo "  Error Rate: [Check dashboard output above]"
echo "  P1 Incidents: [Check dashboard output above]"
echo "  Daily Cost: [Check dashboard output above]"
echo "  Uptime (7d): ${UPTIME}%"
echo "  Intelligence API Days: $DAYS_ELAPSED/7"
echo ""

echo "Action Items:"
if [ $DAYS_ELAPSED -eq 2 ]; then
  echo "  - Complete Cloudflare configuration"
  echo "  - Run backup + restore test"
  echo "  - Enable 2FA on all accounts"
elif [ $DAYS_ELAPSED -eq 7 ]; then
  echo "  - Prepare for Go/No-Go review (Nov 18, 09:00 UTC)"
  echo "  - Generate final burn-in report"
  echo "  - Schedule Nov 24 decision meeting"
else
  echo "  - Continue monitoring"
  echo "  - Maintain error rate ≤ 0.5%"
  echo "  - Maintain cost ≤ $10/day"
fi
echo ""

echo "Next Check: $(date -d 'tomorrow 09:00' -u '+%Y-%m-%d %H:%M UTC')"
echo ""
echo "== END DAILY CHECK =="
