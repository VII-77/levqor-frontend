#!/usr/bin/env bash
#
# scripts/run_automations.sh
# Supervisor launcher for Phase 27-29 automations
#

set -euo pipefail
export PYTHONUNBUFFERED=1

echo "🚀 Starting EchoPilot Automations..."
echo ""

# 1) One-off cleanup
echo "🧹 Running retention cleanup..."
python3 scripts/retention.py || true
echo ""

# 2) Kick today's brief immediately (non-blocking)
echo "📊 Triggering initial CEO Brief..."
curl -s -H "X-Dash-Key: ${DASHBOARD_KEY}" -X POST http://localhost:5000/api/exec/brief >/dev/null 2>&1 || true
echo "   ✅ Brief triggered (check logs/exec_briefs/)"
echo ""

# 3) Start scheduler in background
echo "⏰ Starting scheduler daemon..."
nohup python3 scripts/exec_scheduler.py >> logs/scheduler.out 2>&1 &
SCHEDULER_PID=$!

echo "   ✅ Scheduler started (PID: $SCHEDULER_PID)"
echo "   📝 Logs: logs/scheduler.log"
echo "   📤 Output: logs/scheduler.out"
echo ""

# Save PID for later reference
echo $SCHEDULER_PID > logs/scheduler.pid

echo "✅ Automations running!"
echo ""
echo "Commands:"
echo "  make stop-automations  - Stop scheduler"
echo "  tail -f logs/scheduler.log  - Watch scheduler activity"
echo "  curl -H 'X-Dash-Key: \$DASHBOARD_KEY' http://localhost:5000/api/automations/status | python3 -m json.tool"
echo ""
