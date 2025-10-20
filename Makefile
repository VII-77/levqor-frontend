# Phase 27, 28 & 29: EchoPilot Makefile
# Non-destructive automation targets

.PHONY: help self-heal validate27 daily-report optimize validate28 all
.PHONY: start-automations stop-automations run-brief run-selfheal retention status-automations

help:
	@echo "EchoPilot Makefile (Phase 27, 28 & 29)"
	@echo ""
	@echo "Manual Tasks:"
	@echo "  make self-heal      - Run self-heal service"
	@echo "  make validate27     - Run Phase 27 validation tests"
	@echo "  make daily-report   - Generate daily aggregation report"
	@echo "  make optimize       - Run adaptive optimizer"
	@echo "  make validate28     - Run Phase 28 validation tests"
	@echo "  make run-brief      - Generate CEO Brief (Phase 29)"
	@echo "  make run-selfheal   - Run self-heal via API"
	@echo "  make retention      - Run retention cleanup"
	@echo ""
	@echo "Automation Control:"
	@echo "  make start-automations  - Start background scheduler"
	@echo "  make stop-automations   - Stop background scheduler"
	@echo "  make status-automations - Check scheduler status"
	@echo ""
	@echo "Usage:"
	@echo "  DASHBOARD_KEY=your_key make start-automations"
	@echo "  DASHBOARD_KEY=your_key make run-brief"

self-heal:
	@echo "Running self-heal service..."
	@bash scripts/self_heal.sh http://localhost:5000

validate27:
	@echo "Running Phase 27 validation..."
	@bash scripts/phase27_validate.sh http://localhost:5000

daily-report:
	@echo "Running daily report aggregator..."
	@bash scripts/daily_report.sh

optimize:
	@echo "Running adaptive optimizer..."
	@curl -s -H "X-Dash-Key: $(DASHBOARD_KEY)" -X POST http://localhost:5000/api/optimizer/run | python3 -m json.tool

validate28:
	@echo "Running Phase 28 validation..."
	@bash scripts/phase28_validate.sh

run-brief:
	@curl -s -H "X-Dash-Key: $(DASHBOARD_KEY)" -X POST http://localhost:5000/api/exec/brief | python3 -m json.tool

run-selfheal:
	@curl -s -H "X-Dash-Key: $(DASHBOARD_KEY)" -X POST http://localhost:5000/api/self-heal | python3 -m json.tool

retention:
	@python3 scripts/retention.py

start-automations:
	@bash scripts/run_automations.sh

stop-automations:
	@pkill -f exec_scheduler.py || true
	@echo "✅ Scheduler stopped"

status-automations:
	@curl -s -H "X-Dash-Key: $(DASHBOARD_KEY)" http://localhost:5000/api/automations/status | python3 -m json.tool

all: self-heal daily-report optimize validate28
	@echo "All automation tasks complete!"
