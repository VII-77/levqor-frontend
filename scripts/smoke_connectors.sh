#!/bin/bash
set -e

BASE_URL="${BASE_URL:-http://localhost:5000}"
TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)
EVIDENCE_FILE="evidence/connectors_smoke_${TIMESTAMP}.json"

mkdir -p evidence

echo "=== Levqor Connectors Smoke Test ==="
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Base URL: $BASE_URL"
echo ""

{
  echo "{"
  echo "  \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
  echo "  \"base_url\": \"$BASE_URL\","
  echo "  \"tests\": {"
  
  echo "    \"health\": $(curl -fsS $BASE_URL/actions/health),"
  
  if [ -n "$RESEND_API_KEY" ]; then
    echo "    \"email\": $(curl -fsS -X POST $BASE_URL/actions/email.send -H 'Content-Type: application/json' -d '{"to":"support@levqor.ai","subject":"smoke","text":"automated test"}' 2>/dev/null || echo '{"status":"failed"}')"
  else
    echo "    \"email\": {\"status\":\"skipped\",\"reason\":\"RESEND_API_KEY not set\"}"
  fi
  
  echo "  }"
  echo "}"
} > "$EVIDENCE_FILE"

echo "✅ Smoke test complete"
echo "Evidence saved to: $EVIDENCE_FILE"
cat "$EVIDENCE_FILE" | python3 -m json.tool 2>/dev/null || cat "$EVIDENCE_FILE"
