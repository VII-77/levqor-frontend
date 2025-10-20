#!/usr/bin/env bash
#
# scripts/run_automations.sh
# Supervisor script for EchoPilot automations with start/stop/status
#

set -euo pipefail
export PYTHONUNBUFFERED=1

PID_FILE="logs/scheduler.pid"
LOG_FILE="logs/scheduler.log"
OUT_FILE="logs/scheduler.out"
RETENTION_LOG="logs/retention.log"

# Ensure log files exist
mkdir -p logs
touch "$LOG_FILE" "$OUT_FILE" "$RETENTION_LOG"

start_scheduler() {
    echo "🚀 Starting EchoPilot Automations..."
    echo ""
    
    # Check if already running
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "⚠️  Scheduler already running (PID: $PID)"
            echo "   Use 'stop' command first to restart"
            return 1
        else
            echo "   Removing stale PID file..."
            rm -f "$PID_FILE"
        fi
    fi
    
    # Run retention cleanup
    echo "🧹 Running retention cleanup..."
    python3 scripts/retention.py || true
    echo ""
    
    # Trigger initial CEO Brief (non-blocking)
    if [ -n "${DASHBOARD_KEY:-}" ]; then
        echo "📊 Triggering initial CEO Brief..."
        curl -s -H "X-Dash-Key: ${DASHBOARD_KEY}" -X POST http://localhost:5000/api/exec/brief >/dev/null 2>&1 || true
        echo "   ✅ Brief triggered (check logs/exec_briefs/)"
        echo ""
    fi
    
    # Start scheduler daemon
    echo "⏰ Starting scheduler daemon..."
    python3 scripts/daemonize.py
    
    # Verify it started
    sleep 2
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "   ✅ Scheduler running (PID: $PID)"
            
            # Write startup marker to log
            echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%S)Z\",\"event\":\"supervisor_start\",\"pid\":$PID}" >> "$LOG_FILE"
            
            echo ""
            echo "✅ Automations started!"
            echo ""
            echo "Commands:"
            echo "  bash scripts/run_automations.sh stop   - Stop scheduler"
            echo "  bash scripts/run_automations.sh status - Check status"
            echo "  tail -f logs/scheduler.log             - Watch activity"
            echo ""
        else
            echo "   ❌ Scheduler failed to start"
            return 1
        fi
    else
        echo "   ❌ PID file not created"
        return 1
    fi
}

stop_scheduler() {
    echo "⏹️  Stopping EchoPilot Automations..."
    echo ""
    
    if [ ! -f "$PID_FILE" ]; then
        echo "   ℹ️  No PID file found - scheduler not running"
        return 0
    fi
    
    PID=$(cat "$PID_FILE")
    
    if ! ps -p "$PID" > /dev/null 2>&1; then
        echo "   ℹ️  Process $PID not running - cleaning up PID file"
        rm -f "$PID_FILE"
        echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%S)Z\",\"event\":\"stopped\",\"pid\":$PID,\"reason\":\"not_running\"}" >> "$LOG_FILE"
        return 0
    fi
    
    echo "   Sending SIGTERM to PID $PID..."
    kill -TERM "$PID" 2>/dev/null || true
    
    # Wait up to 5 seconds for graceful shutdown
    for i in {1..5}; do
        if ! ps -p "$PID" > /dev/null 2>&1; then
            echo "   ✅ Scheduler stopped gracefully"
            rm -f "$PID_FILE"
            echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%S)Z\",\"event\":\"stopped\",\"pid\":$PID,\"reason\":\"sigterm\"}" >> "$LOG_FILE"
            return 0
        fi
        sleep 1
    done
    
    # Force kill if still running
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "   ⚠️  Force killing PID $PID..."
        kill -9 "$PID" 2>/dev/null || true
        sleep 1
    fi
    
    rm -f "$PID_FILE"
    echo "   ✅ Scheduler stopped"
    echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%S)Z\",\"event\":\"stopped\",\"pid\":$PID,\"reason\":\"sigkill\"}" >> "$LOG_FILE"
}

status_scheduler() {
    local running=false
    local pid=null
    local last_activity=""
    
    # Check PID file and process
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            running=true
            pid=$PID
        fi
    fi
    
    # Get last activity from log
    if [ -f "$LOG_FILE" ] && [ -s "$LOG_FILE" ]; then
        last_activity=$(tail -n 1 "$LOG_FILE" | python3 -c "import sys, json; d=json.loads(sys.stdin.read()); print(d.get('ts', ''))" 2>/dev/null || echo "")
    fi
    
    # Output JSON
    cat << EOF
{
  "running": $running,
  "pid": $pid,
  "last_activity": "${last_activity}"
}
EOF
}

# Main command dispatcher
case "${1:-start}" in
    start)
        start_scheduler
        ;;
    stop)
        stop_scheduler
        ;;
    status)
        status_scheduler
        ;;
    restart)
        stop_scheduler
        sleep 2
        start_scheduler
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac
