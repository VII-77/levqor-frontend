# Phase 27: EchoPilot Makefile
# Non-destructive automation targets

.PHONY: help self-heal validate27 all

help:
	@echo "EchoPilot Phase 27 Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make self-heal    - Run self-heal service"
	@echo "  make validate27   - Run Phase 27 validation tests"
	@echo "  make all          - Run both self-heal and validation"
	@echo ""
	@echo "Usage:"
	@echo "  DASHBOARD_KEY=your_key make self-heal"
	@echo "  DASHBOARD_KEY=your_key make validate27"

self-heal:
	@echo "Running self-heal service..."
	@bash scripts/self_heal.sh http://localhost:5000

validate27:
	@echo "Running Phase 27 validation..."
	@bash scripts/phase27_validate.sh http://localhost:5000

all: self-heal validate27
	@echo "All Phase 27 tasks complete!"
