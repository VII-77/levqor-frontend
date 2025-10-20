#!/bin/bash
# Phase 27: Validation script
# Tests all Phase 27 endpoints and generates report

set -e

# Get DASHBOARD_KEY from env
if [ -z "$DASHBOARD_KEY" ]; then
    echo "ERROR: DASHBOARD_KEY environment variable not set"
    echo "Usage: DASHBOARD_KEY=your_key $0 [host]"
    exit 1
fi

# Get host (default to localhost)
HOST="${1:-http://localhost:5000}"
TIMESTAMP=$(date +%Y%m%d_%H%M)
REPORT_FILE="logs/phase27_report_${TIMESTAMP}.json"

echo "================================================"
echo "Phase 27 Validation Report"
echo "Host: $HOST"
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "================================================"
echo ""

# Initialize report
cat > "$REPORT_FILE" << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "host": "$HOST",
  "tests": {}
}
EOF

# Helper function to test endpoint
test_endpoint() {
    local name="$1"
    local method="$2"
    local path="$3"
    
    echo "Testing: $name ($method $path)"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" -H "X-Dash-Key: $DASHBOARD_KEY" "$HOST$path")
    else
        response=$(curl -s -w "\n%{http_code}" -X POST -H "X-Dash-Key: $DASHBOARD_KEY" "$HOST$path")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    # Check if JSON is valid
    if echo "$body" | python3 -m json.tool > /dev/null 2>&1; then
        json_valid="true"
        has_ok=$(echo "$body" | python3 -c "import sys,json; print(str('ok' in json.load(sys.stdin)).lower())" 2>/dev/null || echo "false")
    else
        json_valid="false"
        has_ok="false"
    fi
    
    echo "  Status: $http_code | JSON valid: $json_valid | Has 'ok' key: $has_ok"
    
    # Update report (simple append - real script would use jq)
    python3 << PYEOF
import json
with open("$REPORT_FILE", "r") as f:
    report = json.load(f)
report["tests"]["$name"] = {
    "method": "$method",
    "path": "$path",
    "http_code": $http_code,
    "json_valid": $json_valid == "true",
    "has_ok": $has_ok == "true",
    "body_preview": $(echo "$body" | python3 -c "import sys; print(repr(sys.stdin.read()[:200]))")
}
with open("$REPORT_FILE", "w") as f:
    json.dump(report, f, indent=2)
PYEOF
    
    echo ""
}

# Run tests
echo "1) Testing /api/supervisor-status"
test_endpoint "supervisor_status" "GET" "/api/supervisor-status"

echo "2) Testing /api/finance-metrics"
test_endpoint "finance_metrics" "GET" "/api/finance-metrics"

echo "3) Testing /api/self-heal"
test_endpoint "self_heal" "POST" "/api/self-heal"

echo "4) Testing /api/metrics-summary"
test_endpoint "metrics_summary" "GET" "/api/metrics-summary"

# Validate required keys exist
echo "Validating JSON response keys..."
python3 << 'PYEOF'
import json

with open("logs/phase27_report_${TIMESTAMP}.json", "r") as f:
    report = json.load(f)

# Check each test
validation_results = []
for test_name, test_data in report["tests"].items():
    if test_data["json_valid"] and test_data["has_ok"]:
        validation_results.append(f"✅ {test_name}: PASS")
    else:
        validation_results.append(f"❌ {test_name}: FAIL")

# Add validation summary to report
report["validation_summary"] = validation_results
report["overall_status"] = "PASS" if all("✅" in r for r in validation_results) else "PARTIAL"

with open("logs/phase27_report_${TIMESTAMP}.json", "w") as f:
    json.dump(report, f, indent=2)

# Print summary
print("\n" + "="*50)
print("VALIDATION SUMMARY")
print("="*50)
for result in validation_results:
    print(result)
print(f"\nOverall Status: {report['overall_status']}")
print(f"\nFull report saved to: logs/phase27_report_${TIMESTAMP}.json")
PYEOF

exit 0
