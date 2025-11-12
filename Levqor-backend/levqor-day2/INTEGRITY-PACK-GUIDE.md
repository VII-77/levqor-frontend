# Levqor Integrity + Finalizer Pack

**Status:** ✅ **READY FOR SALE**  
**Version:** 1.0.0  
**Date:** November 11, 2025

---

## 🎯 Overview

The **Integrity + Finalizer Pack** is an enterprise-grade verification system that provides:

- **E2E Integrity Tests**: Comprehensive health checks across backend, database, APIs, and workflows
- **Finalizer Validation**: Schema integrity, environment secrets, webhook endpoints, deployment readiness
- **PDF Evidence Reports**: Professional PDF documentation with test results and recommendations
- **Automated Verification**: Run manually or schedule regular integrity checks

**Perfect for:** Enterprise customers, agencies, compliance requirements, pre-deployment validation

---

## 💰 Pricing

| Plan | Price | Description |
|------|-------|-------------|
| **One-Time** | $49 | Single integrity pack run + PDF evidence |
| **Monthly** | $19/month | Unlimited runs, automated weekly checks |

---

## ✅ What Gets Tested

### Integrity Tests (10 Checks)

1. **Backend Health**
   - Main health endpoint
   - Public metrics API
   - Ops uptime endpoint
   - Queue health status
   - Billing health check

2. **Database Connectivity**
   - Read/write operations
   - Schema validation
   - Table existence
   - Row count verification

3. **External API Integrations**
   - Stripe API connectivity
   - Payment processing readiness

4. **Workflow Execution**
   - APScheduler status
   - Job count verification
   - Background task health

5. **Security Headers**
   - HSTS configuration
   - Content type protection
   - Clickjacking protection

### Finalizer Validation (12 Checks)

1. **Environment Secrets**
   - JWT_SECRET configuration
   - SESSION_SECRET validation
   - STRIPE_SECRET_KEY verification
   - STRIPE_WEBHOOK_SECRET check
   - RESEND_API_KEY confirmation
   - Optional: SENTRY_DSN, SLACK_WEBHOOK_URL, TELEGRAM_BOT_TOKEN

2. **Database Schema**
   - Required tables present
   - Schema integrity
   - Row count sanity checks

3. **Webhook Endpoints**
   - Stripe webhook secret format
   - Endpoint accessibility
   - Response validation

4. **Deployment Config**
   - Frontend (levqor.ai) accessibility
   - Backend API (api.levqor.ai) accessibility
   - SSL certificate validation

---

## 📊 Generated Reports

Each integrity pack run generates **3 files**:

1. **`integrity_report_[timestamp].json`**
   - Complete test results in JSON format
   - Timestamps, latency metrics, error details
   - Success rates and statistics

2. **`finalizer_report_[timestamp].json`**
   - Validation results in JSON format
   - Deployment readiness status
   - Configuration audit trail

3. **`integrity_evidence_[timestamp].pdf`**
   - Professional PDF report
   - Executive summary
   - Detailed test results
   - Recommendations
   - Compliance-ready documentation

---

## 🚀 How to Use

### Manual Run (Command Line)

```bash
# Run complete integrity pack
python3 modules/integrity_pack/run_integrity_pack.py

# Reports saved to: integrity_reports/
```

### API Endpoint (Coming Soon)

```bash
POST /api/v1/integrity/run
Authorization: Bearer <api_key>

# Response:
{
  "overall_passed": true,
  "evidence_pdf_url": "https://...",
  "summary": {
    "integrity": {
      "total": 10,
      "passed": 8,
      "failed": 0,
      "success_rate": 80.0
    },
    "finalizer": {
      "total": 12,
      "passed": 11,
      "failed": 0,
      "deployment_ready": true
    }
  }
}
```

---

## 📈 Sample Results

### ✅ Successful Run

```
======================================================================
📊 INTEGRITY PACK COMPLETE
======================================================================
Overall Status: ✅ PASSED

Integrity Tests: 8/10 passed
Finalizer Checks: 11/12 passed
Deployment Ready: YES

📁 Generated Files:
  • Integrity JSON: integrity_reports/integrity_report_1762866750.json
  • Finalizer JSON: integrity_reports/finalizer_report_1762866750.json
  • Evidence PDF:   integrity_reports/integrity_evidence_1762866750.pdf
======================================================================
```

### Test Breakdown

**Backend Health:**
- ✅ Main Health: OK (145ms)
- ✅ Public Metrics: OK (76ms)
- ✅ Ops Uptime: OK (91ms)
- ✅ Queue Health: OK (109ms)
- ✅ Billing Health: OK (126ms)

**Database:**
- ✅ Read Operations: 245 users
- ✅ Schema Validation: All tables present

**External APIs:**
- ✅ Stripe API: Connected

**Workflows:**
- ✅ APScheduler: 11 jobs running

**Security:**
- ✅ HSTS: Present
- ⚠️ Content Type Protection: Missing (CDN filtered)
- ⚠️ Clickjacking Protection: Missing (CDN filtered)

---

## 🔧 Setup Instructions

### 1. Install Package

Already installed! The Integrity Pack is ready to use.

### 2. Create Stripe Product (For Sales)

```bash
python3 scripts/create_integrity_pack_stripe_product.py
```

This creates:
- **Product**: Integrity + Finalizer Pack
- **One-time Price**: $49.00
- **Monthly Price**: $19/month

### 3. Add Price IDs to Secrets

After running the Stripe script, add these to Replit Secrets:
```
STRIPE_PRICE_INTEGRITY_ONETIME = price_xxx...
STRIPE_PRICE_INTEGRITY_MONTHLY = price_yyy...
```

### 4. Test the System

```bash
# Run manual integrity check
python3 modules/integrity_pack/run_integrity_pack.py

# Check generated reports
ls -la integrity_reports/
```

---

## 📝 Use Cases

### 1. Pre-Deployment Validation
Run before each deployment to ensure system readiness:
```bash
python3 modules/integrity_pack/run_integrity_pack.py
# Exit code 0 = ready to deploy
# Exit code 1 = issues found
```

### 2. Compliance Documentation
Generate PDF evidence reports for:
- SOC 2 compliance audits
- Enterprise customer requirements
- Internal security reviews
- Quarterly system audits

### 3. Troubleshooting
When issues arise, run integrity pack to identify:
- Failed health checks
- Missing configurations
- Database problems
- API connectivity issues

### 4. Scheduled Monitoring
Add to cron or APScheduler for automated checks:
```python
# Weekly integrity verification
scheduler.add_job(
    run_integrity_pack,
    CronTrigger(day_of_week='sun', hour=23, minute=0),
    id='weekly_integrity_check'
)
```

---

## 💡 Integration Options

### Notion Integration

Store integrity results in Notion database:
```python
# Coming soon: Auto-log to Notion
from server.notion_helper import NotionHelper

notion = NotionHelper()
notion.create_page(
    database_id=os.getenv("NOTION_INTEGRITY_DB_ID"),
    properties={
        "Name": notion_title(f"Integrity Report {timestamp}"),
        "Status": notion_select("Passed" if overall_passed else "Failed"),
        "Tests Passed": notion_number(passed_count),
        "PDF Link": notion_url(pdf_url),
    }
)
```

### Email Alerts

Send PDF reports via email:
```python
# Coming soon: Email delivery
import resend

resend.api_key = os.getenv("RESEND_API_KEY")

resend.Emails.send({
    "from": "Levqor <integrity@levqor.ai>",
    "to": ["admin@yourcompany.com"],
    "subject": "Integrity Pack Report - Nov 11, 2025",
    "attachments": [{
        "filename": "integrity_evidence.pdf",
        "content": pdf_base64
    }]
})
```

### Google Drive Upload

Automatically upload evidence to Google Drive:
```python
# Coming soon: Google Drive integration
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Upload PDF to Google Drive
# Share link with customer
# Store link in database
```

---

## 🎨 Customization

### Custom Test Categories

Add your own integrity tests:
```python
# modules/integrity_pack/custom_tests.py

class CustomIntegrityTester(IntegrityTester):
    def test_custom_api(self):
        """Test your custom API endpoints"""
        response = requests.get("https://api.yourservice.com/status")
        self.results.append({
            "test": "Custom API: Status Endpoint",
            "category": "custom",
            "status": "passed" if response.status_code == 200 else "failed",
            "timestamp": datetime.utcnow().isoformat(),
        })
```

### Custom PDF Branding

Modify PDF template for white-label:
```python
# modules/integrity_pack/evidence_export.py

# Change company name, logo, colors
title = Paragraph("YOUR COMPANY Integrity Report", self.styles['CustomTitle'])
```

---

## 🐛 Troubleshooting

### "Database not found"
- Check DATABASE_URL environment variable
- Verify database file exists (levqor.db)
- Ensure database has correct schema

### "Stripe API failed"
- Verify STRIPE_SECRET_KEY is configured
- Check Stripe account is active
- Ensure API key starts with `sk_`

### "PDF generation failed"
- Verify reportlab is installed
- Check write permissions in output directory
- Ensure disk space is available

### "Some tests failed"
- Review JSON reports for specific errors
- Check logs: `/tmp/logs/levqor-backend_*.log`
- Verify all required services are running

---

## 📚 API Reference

### IntegrityTester

```python
from modules.integrity_pack import IntegrityTester

tester = IntegrityTester()
results = tester.run_all_tests()

# Results structure:
{
    "test_run_id": "integrity_1762866750",
    "timestamp": "2025-11-11T13:12:28.415867",
    "duration_seconds": 1.99,
    "summary": {
        "total": 10,
        "passed": 8,
        "failed": 0,
        "warnings": 2,
        "success_rate": 80.0
    },
    "results": [...]
}
```

### Finalizer

```python
from modules.integrity_pack import Finalizer

finalizer = Finalizer()
report = finalizer.validate_all()

# Report structure:
{
    "validation_id": "finalizer_1762866750",
    "timestamp": "2025-11-11T13:12:30.123456",
    "summary": {
        "total": 12,
        "passed": 11,
        "failed": 0,
        "deployment_ready": true
    },
    "validations": [...]
}
```

### EvidenceExporter

```python
from modules.integrity_pack import generate_evidence_report

pdf_path = generate_evidence_report(
    integrity_results,
    finalizer_results,
    output_dir="reports"
)
# Returns: "reports/integrity_evidence_1762866750.pdf"
```

---

## 🚀 Next Steps

1. **Enable Sales**: Create Stripe product and prices
2. **Add API Endpoint**: Expose integrity pack via REST API
3. **Notion Integration**: Auto-log results to Notion database
4. **Email Delivery**: Send PDF reports to customers
5. **Google Drive**: Upload and share evidence reports
6. **Scheduled Runs**: Add weekly automated checks
7. **White-Label**: Customize PDF branding for agencies

---

## 📞 Support

For issues or questions:
- Check logs: `/tmp/logs/`
- Review JSON reports for detailed error messages
- Run individual tests manually for debugging
- Contact: support@levqor.ai

---

**Version:** 1.0.0  
**Last Updated:** November 11, 2025  
**License:** Proprietary (Levqor Enterprise Add-On)
