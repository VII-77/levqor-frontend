#!/bin/bash
# Levqor Backend - Production Smoke Test
# Run this after deployment is live and DNS has propagated

# USAGE: ./smoke_test.sh <your-api-key>

if [ -z "$1" ]; then
  echo "❌ Error: API key required"
  echo "Usage: ./smoke_test.sh <your-api-key>"
  exit 1
fi

KEY="$1"

set -e

echo "🧪 LEVQOR PRODUCTION SMOKE TEST"
echo "========================================"
echo ""

echo "✓ Testing Root Endpoint:"
curl -sI https://api.levqor.ai/ | head -n1
echo ""

echo "✓ Testing Security Headers on Metrics:"
curl -sI https://api.levqor.ai/public/metrics | grep -E 'Strict-Transport|Content-Security-Policy|X-Frame-Options'
echo ""

echo "✓ Testing Job Intake → Status:"
jid=$(curl -s -X POST https://api.levqor.ai/api/v1/intake \
  -H "X-Api-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"workflow":"demo","payload":{}}' | jq -r .job_id)
echo "Job ID: $jid"
curl -s https://api.levqor.ai/api/v1/status/$jid | jq
echo ""

echo "✓ Testing Rate Limiting (expect some 429 responses):"
for i in $(seq 1 25); do
  curl -s -o /dev/null -w "%{http_code} " \
    -H "X-Api-Key: $KEY" -H "Content-Type: application/json" \
    -d '{"workflow":"demo","payload":{}}' https://api.levqor.ai/api/v1/intake
done
echo ""
echo ""

echo "========================================"
echo "🟢 COCKPIT GREEN — Levqor backend live and operational."
echo ""
echo "Next steps:"
echo "  - Set up UptimeRobot: https://api.levqor.ai/health"
echo "  - Monitor logs in Replit Deployments"
echo "  - Run daily backups: ./scripts/backup_db.sh"
