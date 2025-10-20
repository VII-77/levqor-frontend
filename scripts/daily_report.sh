#!/bin/bash
# Phase 28: Daily Report Aggregator
# Combines finance, self-heal, metrics into one report
# Sends Telegram summary if configured
# Always exits 0 for cron compatibility

set +e  # Don't exit on error

TIMESTAMP=$(date +%Y%m%d)
OUTPUT_FILE="logs/daily_report_${TIMESTAMP}.json"
mkdir -p logs

echo "📊 Running daily report aggregation..."

# Fetch finance metrics
FINANCE=$(curl -s -H "X-Dash-Key: ${DASHBOARD_KEY}" http://localhost:5000/api/finance-metrics 2>/dev/null || echo '{"ok":false}')

# Fetch self-heal status
SELFHEAL=$(curl -s -X POST -H "X-Dash-Key: ${DASHBOARD_KEY}" http://localhost:5000/api/self-heal 2>/dev/null || echo '{"ok":false}')

# Fetch metrics summary
METRICS=$(curl -s -H "X-Dash-Key: ${DASHBOARD_KEY}" http://localhost:5000/api/metrics-summary 2>/dev/null || echo '{"ok":false}')

# Combine into JSON
cat > "$OUTPUT_FILE" << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "finance_metrics": $FINANCE,
  "self_heal": $SELFHEAL,
  "metrics_summary": $METRICS
}
EOF

echo "✅ Report saved to $OUTPUT_FILE"

# Send Telegram summary if configured
if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
    # Parse data
    JOBS=$(echo "$FINANCE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('data',{}).get('jobs_7d',0))" 2>/dev/null || echo "N/A")
    QA=$(echo "$METRICS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(round(d.get('data',{}).get('avg_qa_7d',0),1))" 2>/dev/null || echo "N/A")
    ROI=$(echo "$FINANCE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(round(d.get('data',{}).get('roi_30d',0),1))" 2>/dev/null || echo "N/A")
    RETRIES=$(echo "$SELFHEAL" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('retried_count',0))" 2>/dev/null || echo "0")
    
    MESSAGE="📊 EchoPilot Daily Report – Jobs: ${JOBS} | QA ${QA}% | ROI ${ROI}% | Retries ${RETRIES}"
    
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -H "Content-Type: application/json" \
        -d "{\"chat_id\":\"${TELEGRAM_CHAT_ID}\",\"text\":\"${MESSAGE}\"}" > /dev/null 2>&1
    
    echo "📱 Telegram summary sent"
else
    echo "⚠️  Telegram not configured (skipping notification)"
fi

echo "✅ Daily report complete"
exit 0
