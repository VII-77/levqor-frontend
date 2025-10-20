# Phase 27 & 28: EchoPilot Makefile
# Non-destructive automation targets

.PHONY: help self-heal validate27 daily-report optimize validate28 all

help:
        @echo "EchoPilot Makefile (Phase 27 & 28)"
        @echo ""
        @echo "Available targets:"
        @echo "  make self-heal      - Run self-heal service"
        @echo "  make validate27     - Run Phase 27 validation tests"
        @echo "  make daily-report   - Generate daily aggregation report"
        @echo "  make optimize       - Run adaptive optimizer"
        @echo "  make validate28     - Run Phase 28 validation tests"
        @echo "  make all            - Run all tasks"
        @echo ""
        @echo "Usage:"
        @echo "  DASHBOARD_KEY=your_key make self-heal"
        @echo "  DASHBOARD_KEY=your_key make daily-report"

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

all: self-heal daily-report optimize validate28
        @echo "All automation tasks complete!"
