#!/bin/bash

set -e

BASE_URL="${1:-http://localhost:5000}"
DATE=$(date +%F)
LOG_FILE="logs/daily_health_${DATE}.json"
DASH_KEY="${DASHBOARD_KEY}"

echo "========================================"
echo "EchoPilot Daily Health Check - ${DATE}"
echo "========================================"
echo ""

mkdir -p logs

{
  echo "{"
  echo "  \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
  echo "  \"checks\": {"

  echo -n "    \"health\": "
  HEALTH=$(curl -s "${BASE_URL}/health" || echo '{"error":"timeout"}')
  echo "${HEALTH},"
  echo ""

  sleep 2

  echo -n "    \"supervisor\": "
  SUPERVISOR=$(curl -s -H "X-Dash-Key: ${DASH_KEY}" "${BASE_URL}/api/supervisor-status" || echo '{"error":"timeout"}')
  echo "${SUPERVISOR},"
  echo ""

  sleep 30

  echo -n "    \"pulse\": "
  PULSE=$(curl -s -X POST \
    -H "X-Dash-Key: ${DASH_KEY}" \
    -H "Content-Type: application/json" \
    -H "Referer: ${BASE_URL}/" \
    "${BASE_URL}/api/pulse" || echo '{"error":"timeout"}')
  echo "${PULSE},"
  echo ""

  sleep 30

  echo -n "    \"job_log\": "
  JOB_LOG=$(curl -s -H "X-Dash-Key: ${DASH_KEY}" "${BASE_URL}/api/job-log-latest" || echo '{"error":"timeout"}')
  echo "${JOB_LOG}"
  echo ""

  echo "  }"
  echo "}"
} | tee "${LOG_FILE}"

echo ""
echo "========================================"
echo "Summary:"
echo "========================================"

HEALTH_OK=$(echo "${HEALTH}" | grep -o '"ok"[[:space:]]*:[[:space:]]*true' || echo "")
SUPERVISOR_OK=$(echo "${SUPERVISOR}" | grep -o '"ok"[[:space:]]*:[[:space:]]*true' || echo "")
PULSE_OK=$(echo "${PULSE}" | grep -o '"ok"[[:space:]]*:[[:space:]]*true' || echo "")
JOB_LOG_OK=$(echo "${JOB_LOG}" | grep -o '"ok"[[:space:]]*:[[:space:]]*true' || echo "")

QA_SCORE=$(echo "${JOB_LOG}" | grep -o '"qa_score"[[:space:]]*:[[:space:]]*[0-9]*' | grep -o '[0-9]*' || echo "N/A")

if [[ -n "${HEALTH_OK}" && -n "${SUPERVISOR_OK}" && -n "${PULSE_OK}" && -n "${JOB_LOG_OK}" ]]; then
  echo "✅ [${DATE}] Health OK | QA: ${QA_SCORE}% | Jobs OK | Pulse: created"
  echo ""
  echo "Log saved to: ${LOG_FILE}"
  exit 0
else
  echo "❌ [${DATE}] Health check FAILED"
  echo ""
  echo "Details:"
  [[ -z "${HEALTH_OK}" ]] && echo "  - Health endpoint failed"
  [[ -z "${SUPERVISOR_OK}" ]] && echo "  - Supervisor endpoint failed"
  [[ -z "${PULSE_OK}" ]] && echo "  - Pulse endpoint failed"
  [[ -z "${JOB_LOG_OK}" ]] && echo "  - Job log endpoint failed"
  echo ""
  echo "Log saved to: ${LOG_FILE}"
  exit 1
fi
