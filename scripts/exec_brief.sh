#!/usr/bin/env bash
#
# scripts/exec_brief.sh
# Runs the AI Executive Mode workflow: ingest → brief → email
#
# Usage:
#   DASHBOARD_KEY=your_key bash scripts/exec_brief.sh [BASE_URL]
#
# Cron example (daily at 8 AM UTC):
#   0 8 * * * cd /path/to/echopilot && DASHBOARD_KEY=$DASHBOARD_KEY bash scripts/exec_brief.sh http://localhost:5000

set -euo pipefail

BASE_URL="${1:-http://localhost:5000}"
HDR="X-Dash-Key: ${DASHBOARD_KEY}"

echo "🧠 AI Executive Mode: Generating CEO Brief..."
echo ""

# 1) Ingest signals
echo "📥 Step 1/3: Ingesting signals..."
INGEST_RESULT=$(curl -s -H "$HDR" -X POST "$BASE_URL/api/exec/ingest")
INGEST_OK=$(echo "$INGEST_RESULT" | jq -r '.ok // false')

if [ "$INGEST_OK" != "true" ]; then
    echo "❌ Ingest failed: $(echo "$INGEST_RESULT" | jq -r '.error // "Unknown error"')"
    exit 1
fi

INGEST_PATH=$(echo "$INGEST_RESULT" | jq -r '.saved_to')
echo "   ✅ Saved to: $INGEST_PATH"
echo ""

# 2) Generate brief (runs analyze internally)
echo "📊 Step 2/3: Generating brief..."
BRIEF_RESULT=$(curl -s -H "$HDR" -X POST "$BASE_URL/api/exec/brief")
BRIEF_OK=$(echo "$BRIEF_RESULT" | jq -r '.ok // false')

if [ "$BRIEF_OK" != "true" ]; then
    echo "❌ Brief failed: $(echo "$BRIEF_RESULT" | jq -r '.error // "Unknown error"')"
    exit 1
fi

JSON_PATH=$(echo "$BRIEF_RESULT" | jq -r '.json_path')
HTML_PATH=$(echo "$BRIEF_RESULT" | jq -r '.html_path')
HEADLINE=$(echo "$BRIEF_RESULT" | jq -r '.data.headline')

echo "   ✅ JSON: $JSON_PATH"
echo "   ✅ HTML: $HTML_PATH"
echo "   📰 Headline: $HEADLINE"
echo ""

# 3) Email brief
echo "📧 Step 3/3: Sending brief..."
EMAIL_RESULT=$(curl -s -H "$HDR" -X POST "$BASE_URL/api/exec/email")
EMAIL_OK=$(echo "$EMAIL_RESULT" | jq -r '.ok // false')

if [ "$EMAIL_OK" != "true" ]; then
    echo "⚠️  Email failed: $(echo "$EMAIL_RESULT" | jq -r '.error // "Unknown error"')"
    echo "   (Brief was still generated successfully)"
else
    EMAIL_SENT=$(echo "$EMAIL_RESULT" | jq -r '.sent // false')
    if [ "$EMAIL_SENT" = "true" ]; then
        EMAIL_TO=$(echo "$EMAIL_RESULT" | jq -r '.to')
        echo "   ✅ Sent to: $EMAIL_TO"
    else
        EMAIL_LOG=$(echo "$EMAIL_RESULT" | jq -r '.logged_to')
        echo "   📝 Logged to: $EMAIL_LOG (SMTP not configured)"
    fi
fi

echo ""
echo "✅ CEO Brief workflow complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$HEADLINE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exit 0
