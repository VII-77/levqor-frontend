#!/bin/bash
echo "=== Testing Actually Deployed Endpoints ==="
curl -s https://api.levqor.ai/ops/uptime | python3 -m json.tool
echo ""
echo "=== Queue Health ==="
curl -s https://api.levqor.ai/ops/queue_health | python3 -m json.tool
echo ""
echo "=== Billing Health ==="
curl -s https://api.levqor.ai/billing/health | python3 -m json.tool
