#!/bin/bash
# Phase 27: Self-heal script
# Calls /api/self-heal endpoint with dashboard key

set -e

# Get DASHBOARD_KEY from env or fail gracefully
if [ -z "$DASHBOARD_KEY" ]; then
    echo "ERROR: DASHBOARD_KEY environment variable not set"
    exit 0  # Never crash cron
fi

# Get host (default to localhost)
HOST="${1:-http://localhost:5000}"

# Output file
TIMESTAMP=$(date +%F_%H%M)
OUTPUT_FILE="logs/self_heal_run_${TIMESTAMP}.json"

# Make request
echo "Running self-heal at $HOST..."
curl -s -X POST \
    -H "X-Dash-Key: $DASHBOARD_KEY" \
    "$HOST/api/self-heal" \
    | tee "$OUTPUT_FILE" \
    | python3 -m json.tool || true

echo ""
echo "Results saved to: $OUTPUT_FILE"

exit 0
