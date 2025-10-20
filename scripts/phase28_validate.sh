#!/bin/bash
# Phase 28: Validation Suite
# Tests all Phase 28 endpoints and generates report
# Always exits 0 for cron compatibility

set +e  # Don't exit on error

TIMESTAMP=$(date +%Y%m%d_%H%M)
OUTPUT_FILE="logs/phase28_report_${TIMESTAMP}.json"
mkdir -p logs

echo "════════════════════════════════════════════"
echo "   PHASE 28 VALIDATION SUITE"
echo "════════════════════════════════════════════"
echo ""

# Check if DASHBOARD_KEY is set
if [ -z "$DASHBOARD_KEY" ]; then
    echo "❌ ERROR: DASHBOARD_KEY not set"
    echo '{"ok":false,"error":"DASHBOARD_KEY not set"}' > "$OUTPUT_FILE"
    exit 0
fi

echo "🔍 Testing Phase 28 endpoints..."
echo ""

# Test 1: Alerts Trigger
echo "1️⃣  Testing /api/alerts/trigger..."
ALERTS=$(curl -s -X POST -H "X-Dash-Key: ${DASHBOARD_KEY}" http://localhost:5000/api/alerts/trigger 2>&1)
ALERTS_STATUS=$?

if [ $ALERTS_STATUS -eq 0 ]; then
    ALERTS_OK=$(echo "$ALERTS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('ok',False))" 2>/dev/null || echo "false")
    if [ "$ALERTS_OK" = "True" ]; then
        echo "   ✅ PASS"
    else
        echo "   ⚠️  FAIL (returned ok:false)"
    fi
else
    echo "   ❌ ERROR (curl failed)"
    ALERTS='{"ok":false,"error":"curl failed"}'
fi
echo ""

# Test 2: Finance Metrics
echo "2️⃣  Testing /api/finance-metrics..."
FINANCE=$(curl -s -H "X-Dash-Key: ${DASHBOARD_KEY}" http://localhost:5000/api/finance-metrics 2>&1)
FINANCE_STATUS=$?

if [ $FINANCE_STATUS -eq 0 ]; then
    # Finance can return ok:false if no data - that's acceptable
    echo "   ✅ PASS (responded)"
else
    echo "   ❌ ERROR (curl failed)"
    FINANCE='{"ok":false,"error":"curl failed"}'
fi
echo ""

# Test 3: Optimizer
echo "3️⃣  Testing /api/optimizer/run..."
OPTIMIZER=$(curl -s -X POST -H "X-Dash-Key: ${DASHBOARD_KEY}" http://localhost:5000/api/optimizer/run 2>&1)
OPTIMIZER_STATUS=$?

if [ $OPTIMIZER_STATUS -eq 0 ]; then
    OPTIMIZER_OK=$(echo "$OPTIMIZER" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('ok',False))" 2>/dev/null || echo "false")
    if [ "$OPTIMIZER_OK" = "True" ]; then
        echo "   ✅ PASS"
    else
        echo "   ⚠️  FAIL (returned ok:false - may need job data)"
    fi
else
    echo "   ❌ ERROR (curl failed)"
    OPTIMIZER='{"ok":false,"error":"curl failed"}'
fi
echo ""

# Generate combined report
echo "📊 Generating report..."
cat > "$OUTPUT_FILE" << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "phase": 28,
  "tests": {
    "alerts_trigger": $ALERTS,
    "finance_metrics": $FINANCE,
    "optimizer_run": $OPTIMIZER
  },
  "summary": {
    "alerts_pass": $([ "$ALERTS_OK" = "True" ] && echo "true" || echo "false"),
    "finance_pass": $([ $FINANCE_STATUS -eq 0 ] && echo "true" || echo "false"),
    "optimizer_pass": $([ "$OPTIMIZER_OK" = "True" ] && echo "true" || echo "false")
  }
}
EOF

echo ""
echo "════════════════════════════════════════════"
echo "✅ Validation complete"
echo "📁 Report saved to: $OUTPUT_FILE"
echo "════════════════════════════════════════════"

exit 0
