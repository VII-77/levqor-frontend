# EchoPilot Smoke Test Suite

## Overview
Comprehensive smoke test scripts to validate EchoPilot platform health, API endpoints, and critical features.

## Test Scripts

### 1. Basic Smoke Test (`scripts/smoke.sh`)
**Purpose:** Fast validation of core functionality  
**Runtime:** ~30 seconds  
**Prerequisites:** None (optional: `HEALTH_TOKEN`, `DASHBOARD_KEY`)

**Test Coverage:**
- ✓ Health endpoint (`/health`)
- ✓ Public pages (landing, pricing)
- ✓ Dashboard redirect
- ✓ API protection (401 without auth)
- ✓ Feature flags
- ✓ Static assets (CSS, JS)
- ✓ Error handling (404)
- ✓ Workflow builder
- ✓ Boss Mode UI
- ✓ Demo mode status

**Usage:**
```bash
# Basic run
./scripts/smoke.sh

# With auth tokens
HEALTH_TOKEN=xxx DASHBOARD_KEY=yyy ./scripts/smoke.sh

# Against production
BASE_URL=https://echopilotai.replit.app ./scripts/smoke.sh
```

---

### 2. Advanced Smoke Test (`scripts/smoke_advanced.sh`)
**Purpose:** Deep validation of enterprise features  
**Runtime:** ~60 seconds  
**Prerequisites:** `DASHBOARD_KEY` (required), `HEALTH_TOKEN` (optional), `psycopg2` (optional for DB schema checks)

**Test Coverage:**
- ✓ Health endpoint with DB checks
- ✓ Metrics aggregation
- ✓ SLO monitoring & violations
- ✓ Feature flags system
- ✓ AI governance reports
- ✓ Load forecasting
- ✓ Warehouse sync endpoint
- ✓ SLO tuning endpoint
- ✓ Governance analysis endpoint
- ✓ A/B testing framework
- ✓ Scheduler process detection
- ✓ Log file generation
- ✓ Database schema validation
- ✓ Demo mode detection

**Usage:**
```bash
# Basic run (requires DASHBOARD_KEY)
DASHBOARD_KEY=xxx ./scripts/smoke_advanced.sh

# Full run with all tokens
HEALTH_TOKEN=xxx DASHBOARD_KEY=yyy ./scripts/smoke_advanced.sh

# Against production
BASE_URL=https://echopilotai.replit.app DASHBOARD_KEY=yyy ./scripts/smoke_advanced.sh
```

---

## Output Format

### Success Example
```
======================================
  EchoPilot Smoke Test Suite
======================================
Base URL: http://localhost:5000
Timestamp: 2025-10-21 14:30:00
Log File: logs/smoke_test_20251021_143000.log
======================================

✓ Health Check (HTTP 200)
✓ Demo Mode Status (HTTP 200)
✓ Landing Page (HTTP 200)
✓ Pricing Page (HTTP 200)
...

======================================
  Test Results Summary
======================================
Total Tests:  15
Passed:       15
Failed:       0
Success Rate: 100.0%
======================================

✓ All tests passed!
```

### Failure Example
```
✓ Health Check (HTTP 200)
✗ Landing Page (Expected: 200, Got: 500)
⚠ HEALTH_TOKEN not set, skipping authenticated health check

======================================
  Test Results Summary
======================================
Total Tests:  15
Passed:       12
Failed:       3
Success Rate: 80.0%
======================================

✗ Some tests failed. Check logs/smoke_test_20251021_143000.log for details.
```

---

## Exit Codes
- **0:** All tests passed
- **1:** One or more tests failed

---

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Smoke Tests
on: [push, pull_request]

jobs:
  smoke-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Basic Smoke Tests
        run: ./scripts/smoke.sh
        env:
          BASE_URL: ${{ secrets.STAGING_URL }}
          
      - name: Run Advanced Smoke Tests
        run: ./scripts/smoke_advanced.sh
        env:
          BASE_URL: ${{ secrets.STAGING_URL }}
          DASHBOARD_KEY: ${{ secrets.DASHBOARD_KEY }}
          HEALTH_TOKEN: ${{ secrets.HEALTH_TOKEN }}
```

### Pre-Deployment Validation
```bash
#!/bin/bash
# deploy.sh

# Run smoke tests before deploying
if ./scripts/smoke_advanced.sh; then
    echo "✓ Smoke tests passed, proceeding with deployment"
    # Deploy commands here
else
    echo "✗ Smoke tests failed, aborting deployment"
    exit 1
fi
```

---

## Log Files
All smoke test runs create detailed logs in `logs/`:

- `logs/smoke_test_YYYYMMDD_HHMMSS.log` - Basic smoke test logs
- `logs/smoke_advanced_YYYYMMDD_HHMMSS.log` - Advanced smoke test logs

**Log Contents:**
- Timestamp for each test
- HTTP response codes
- Response bodies (JSON formatted when applicable)
- Error messages
- Test summary

**Example:**
```
[2025-10-21 14:30:01] Testing basic health endpoints...
✓ Health Check (HTTP 200)
{
  "status": "healthy",
  "uptime": 12345,
  "database": "connected"
}
```

---

## Troubleshooting

### Problem: All tests fail with connection errors
**Solution:** Check that the server is running on the expected BASE_URL
```bash
curl http://localhost:5000/health
```

### Problem: 401 errors on all authenticated endpoints
**Solution:** Set valid DASHBOARD_KEY
```bash
export DASHBOARD_KEY=$(cat .env | grep DASHBOARD_KEY | cut -d'=' -f2)
```

### Problem: Database schema validation fails
**Solution 1:** Install psycopg2 for database validation
```bash
pip install psycopg2-binary
```

**Solution 2:** The test will gracefully skip if psycopg2 is not installed

**Solution 3:** If psycopg2 is installed but failing, run database migrations
```bash
npm run db:push
```

### Problem: Scheduler process not detected
**Solution:** Ensure Scheduler workflow is running
```bash
pgrep -f exec_scheduler.py
```

---

## Best Practices

1. **Run before deployment:** Always run smoke tests before pushing to production
2. **Monitor logs:** Review log files for warnings even when tests pass
3. **Use in CI/CD:** Integrate smoke tests into your deployment pipeline
4. **Test locally:** Run smoke tests locally before committing changes
5. **Update tests:** Add new tests when adding new features
6. **Check demo mode:** Test with `DEMO_MODE=true` to verify read-only protection

---

## Extending the Tests

### Adding a New Test to Basic Smoke Test
```bash
# In scripts/smoke.sh, add:
test_endpoint "My New Feature" "/api/my-feature" 200
```

### Adding a New Test to Advanced Smoke Test
```bash
# In scripts/smoke_advanced.sh, add:
test_json_endpoint "My Advanced Feature" "/api/advanced-feature" 200
```

### Testing POST Endpoints
```bash
test_json_endpoint "Create Resource" "/api/resources" 201 "POST" '{"name":"test"}'
```

---

## Comparison: Basic vs Advanced

| Feature | Basic | Advanced |
|---------|-------|----------|
| Public pages | ✓ | ✓ |
| Health check | ✓ | ✓ (with DB) |
| API protection | ✓ | ✓ |
| Metrics | - | ✓ |
| SLO monitoring | - | ✓ |
| Governance | - | ✓ |
| Forecasting | - | ✓ |
| DB validation | - | ✓ |
| Scheduler check | - | ✓ |
| Prerequisites | None | DASHBOARD_KEY |
| Runtime | ~30s | ~60s |

**Recommendation:** Run basic smoke tests for quick validation, advanced smoke tests for comprehensive pre-deployment checks.
