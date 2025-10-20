.PHONY: alerts-now health validate enterprise-report

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
