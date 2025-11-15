#!/bin/bash
set -euo pipefail

echo "========================================="
echo "BACKEND SELF-AUDIT SCRIPT"
echo "========================================="
echo ""
echo "Date: $(date)"
echo "Environment: ${ENVIRONMENT:-development}"
echo ""

# Check if we're in the right directory
if [ ! -f "run.py" ]; then
    echo "❌ ERROR: run.py not found. Run this script from the project root."
    exit 1
fi

echo "✅ Found run.py"
echo ""

# Check Python version
echo "📌 Python version:"
python3 --version || echo "⚠️  Python not found"
echo ""

# Check dependencies
echo "📌 Checking dependencies:"
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
    pip3 list > /dev/null 2>&1 && echo "✅ pip packages installed" || echo "⚠️  pip check failed"
else
    echo "⚠️  requirements.txt not found"
fi
echo ""

# Check environment variables
echo "📌 Checking critical environment variables:"
REQUIRED_VARS=("STRIPE_SECRET_KEY" "STRIPE_WEBHOOK_SECRET" "RESEND_API_KEY")
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var:-}" ]; then
        echo "❌ Missing: $var"
    else
        echo "✅ $var is set"
    fi
done
echo ""

# Check database
echo "📌 Checking database:"
if [ -f "levqor.db" ]; then
    echo "✅ SQLite database found (levqor.db)"
    DB_SIZE=$(du -h levqor.db | cut -f1)
    echo "   Size: $DB_SIZE"
else
    echo "⚠️  SQLite database not found (will be created on first run)"
fi
echo ""

# Check backend structure
echo "📌 Checking backend structure:"
REQUIRED_DIRS=("backend/routes" "backend/models" "backend/services" "backend/utils")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        FILE_COUNT=$(find "$dir" -name "*.py" | wc -l)
        echo "✅ $dir ($FILE_COUNT Python files)"
    else
        echo "❌ Missing: $dir"
    fi
done
echo ""

# Check critical files
echo "📌 Checking critical backend files:"
CRITICAL_FILES=(
    "backend/routes/stripe_checkout_webhook.py"
    "backend/services/onboarding_automation.py"
    "backend/utils/resend_sender.py"
    "backend/utils/telegram_helper.py"
    "backend/models/sales_models.py"
)
for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ Missing: $file"
    fi
done
echo ""

# Test syntax (basic Python check)
echo "📌 Testing Python syntax:"
python3 -m py_compile run.py 2>&1 && echo "✅ run.py syntax valid" || echo "❌ run.py syntax error"
python3 -m py_compile backend/routes/stripe_checkout_webhook.py 2>&1 && echo "✅ stripe_checkout_webhook.py syntax valid" || echo "❌ syntax error"
python3 -m py_compile backend/services/onboarding_automation.py 2>&1 && echo "✅ onboarding_automation.py syntax valid" || echo "❌ syntax error"
echo ""

# Run tests if they exist
echo "📌 Running tests:"
if [ -d "tests" ] && [ -n "$(ls -A tests/*.py 2>/dev/null)" ]; then
    python3 -m pytest tests/ || echo "⚠️  Tests failed"
else
    echo "⚠️  No tests found (tests/ directory empty or missing)"
fi
echo ""

# Check health endpoint (if server is running)
echo "📌 Checking health endpoints:"
if command -v curl > /dev/null 2>&1; then
    echo "Testing local health endpoint..."
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        echo "✅ Backend health endpoint: HTTP $HTTP_CODE"
    else
        echo "⚠️  Backend not running or health endpoint unavailable (HTTP $HTTP_CODE)"
    fi
    
    # Test new checkout webhook health
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/webhooks/stripe/health 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        echo "✅ Stripe checkout webhook health: HTTP $HTTP_CODE"
    else
        echo "⚠️  Stripe checkout webhook endpoint not reachable (HTTP $HTTP_CODE)"
    fi
else
    echo "⚠️  curl not found - skipping health checks"
fi
echo ""

# Summary
echo "========================================="
echo "BACKEND SELF-AUDIT COMPLETED"
echo "========================================="
echo ""
echo "Next steps:"
echo "  1. Review any ❌ or ⚠️  warnings above"
echo "  2. Ensure all required environment variables are set"
echo "  3. Start backend with: gunicorn --bind 0.0.0.0:8000 run:app"
echo "  4. Test Stripe webhook at: /api/webhooks/stripe/checkout-completed"
echo ""
