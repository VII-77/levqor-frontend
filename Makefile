.PHONY: alerts-now health validate enterprise-report ops-check uptime slo backup-verify dr-drill

alerts-now:
        @echo "Running production alerts..."
        @python3 scripts/production_alerts.py | jq .

health:
        @echo "System health check..."
        @curl -s -H "X-Dash-Key:${DASHBOARD_KEY}" http://localhost:5000/api/system-health 2>/dev/null | jq . || echo "Server not ready"

validate:
        @echo "Enterprise validation..."
        @curl -s -H "X-Dash-Key:${DASHBOARD_KEY}" http://localhost:5000/api/validate/enterprise 2>/dev/null | jq . || echo "Server not ready"

enterprise-report:
        @echo "Enterprise report..."
        @curl -s -H "X-Dash-Key:${DASHBOARD_KEY}" http://localhost:5000/api/reports/enterprise 2>/dev/null | jq . || echo "Server not ready"

# ==================== STABILIZATION SPRINT: RELIABILITY ====================

ops-check:
        @echo "Running comprehensive ops check..."
        @BASE_URL=http://localhost:5000 DASHBOARD_KEY=${DASHBOARD_KEY} python3 scripts/ops_check.py

uptime:
        @echo "Testing uptime monitor..."
        @curl -s -H "X-Dash-Key:${DASHBOARD_KEY}" -X POST http://localhost:5000/api/ops/uptime/test 2>/dev/null | jq . || echo "Server not ready"

slo:
        @echo "Checking SLO status..."
        @curl -s -H "X-Dash-Key:${DASHBOARD_KEY}" http://localhost:5000/api/ops/slo/status 2>/dev/null | jq . || echo "Server not ready"

backup-verify:
        @echo "Running backup verification..."
        @python3 scripts/backup_verify.py && tail -1 logs/backup_verify.ndjson | jq .

dr-drill:
        @echo "Running DR drill..."
        @python3 scripts/dr_drill.py && tail -1 logs/dr_report_*.json 2>/dev/null || echo "No DR reports yet"
