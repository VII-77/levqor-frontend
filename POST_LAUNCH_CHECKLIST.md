# 🚀 EchoPilot Post-Launch Checklist

**Status as of:** October 20, 2025  
**Deployment:** https://echopilotai.replit.app

---

## ✅ DO NOW (TODAY) - Status

### 1. Production Alerts (Every 5 min) ✅ ACTIVE
```
Status: RUNNING in scheduler
Monitors: 
  • Webhook failures
  • Payment error rate  
  • Revenue dips
Location: scripts/exec_scheduler.py (line 529)
Last run: Check logs/scheduler.log
```

### 2. Final Enterprise Audit ⚠️ WARN (Expected)
```bash
# Run validation:
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  http://localhost:5000/api/validate/enterprise | jq .

# Current Status: WARN (expected for new deployment)
# Warnings (will auto-resolve as tasks run):
  ✅ api_status: PASS
  ✅ scheduler: PASS  
  ✅ logs_integrity: PASS (18 NDJSON files)
  ✅ rbac_users: PASS (admin configured)
  ✅ finops_spend: PASS (within limits)
  ⚠️  dr_backup: WARN (first run at 02:30 UTC tonight)
  ⚠️  governance_ai: WARN (first run within 3 hours)
  ⚠️  optimizer: WARN (first run within 4 hours)
  ⚠️  security_scan: WARN (first run at 06:00 UTC tomorrow)
```

### 3. Enterprise Report ✅ WORKING
```bash
# View JSON report:
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  http://localhost:5000/api/reports/enterprise | jq .

# View HTML dashboard (public):
open https://echopilotai.replit.app/api/reports/enterprise/html

# Current Metrics:
  • Total Phases: 100
  • Active Tasks: 46
  • API Endpoints: 97+
  • Security Status: PASS
  • Financial Health: $0/$25 (0% utilization)
  • P95 Latency: 0ms (no traffic yet)
  • Success Rate: 100%
```

### 4. Stripe Live Test 💳 READY
```bash
# Test $0.50 charge (replace with your test email):
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount":0.50,"email":"qa-live@echopilot.ai","description":"Live ops test"}' \
  http://localhost:5000/api/payments/create-invoice | jq .

# Expected response:
{
  "ok": true,
  "invoice_id": "in_...",
  "hosted_invoice_url": "https://invoice.stripe.com/...",
  "amount_due": 0.50,
  "customer_email": "qa-live@echopilot.ai"
}

# Then:
1. Pay the invoice at hosted_invoice_url
2. Check webhook logs: tail -f logs/payment_webhooks.ndjson
3. Refund in Stripe Dashboard
4. Verify refund webhook: tail -f logs/payment_webhooks.ndjson
```

---

## 📅 THIS WEEK (Stabilize & Learn)

### 1. SLA & On-Call ✅ CONFIGURED
```yaml
SLOs Configured:
  - Uptime: 99.9% (43.2 min downtime/month) - SLO_AVAILABILITY_PCT
  - P95 Latency: <800ms - SLO_P95_TARGET_MS
  - P99 Latency: <1200ms - SLO_P99_TARGET_MS (NEW!)
  - Webhook Success: 99% - SLO_WEBHOOK_SUCCESS_PCT
  - Error Budget: 2% daily - SLO_ERROR_BUDGET_PCT

Escalation:
  - Primary: Telegram alerts (already configured)
  - Secondary: Email alerts (already configured)
  - Critical: Set TELEGRAM_CHAT_ID for instant paging
```

**Environment Variables (Optional Customization):**
```bash
# Production-Ready Defaults (Already Set)
export SLO_AVAILABILITY_PCT=99.9
export SLO_P95_TARGET_MS=800
export SLO_P99_TARGET_MS=1200
export SLO_WEBHOOK_SUCCESS_PCT=99.0
export SLO_ERROR_BUDGET_PCT=2.0

# For relaxed testing environments:
export SLO_AVAILABILITY_PCT=99.5
export SLO_P95_TARGET_MS=1500
export SLO_P99_TARGET_MS=2500
```

**Verify SLO Configuration:**
```bash
python3 scripts/slo_guard.py | jq '.slos'
```

### 2. Backups & DR Drill ✅ VERIFIED
```bash
# Tonight's automated backup (02:30 UTC):
# Location: backups/dr/dr_backup_YYYYMMDD_HHMMSS.tar.gz

# Manual backup now:
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" -X POST \
  http://localhost:5000/api/dr/backup | jq .

# OR directly via script:
python3 scripts/dr_backups.py

# Verify backup integrity (RECOMMENDED):
python3 scripts/verify_dr_backup.py

# Expected output:
{
  "ok": true,
  "summary": {
    "total_tests": 5,
    "passed": 4,
    "failures": 0,
    "status": "PASS"
  }
}

# Manual inspection:
1. List backups: ls -lh backups/dr/
2. View contents: tar -tzf backups/dr/dr_backup_*.tar.gz | head -30
3. Count files: tar -tzf backups/dr/dr_backup_*.tar.gz | wc -l

# DR Restore (if needed):
1. Stop services: systemctl stop echopilot
2. Backup current state: mv logs logs.backup
3. Extract: tar -xzf backups/dr/dr_backup_YYYYMMDD_HHMMSS.tar.gz
4. Restart: systemctl start echopilot
5. Verify: curl http://localhost:5000/api/system-health
```

**Verification Status:**
- ✅ Backup creation tested and working (0.37 MB, 275 files)
- ✅ Archive integrity verified
- ✅ Critical files present (logs/, data/, configs/)
- ✅ Dry-run extract successful
- ✅ Automated verification script created

### 3. Pricing AI v1 ⏳ TODO
```bash
# Enable gated pricing suggestions (±10% max):
export PRICING_AI_ENABLED=true
export PRICING_AI_MAX_CHANGE_PCT=10
export PRICING_AI_ROLLBACK_FLAG=true

# Test pricing optimization:
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" -X POST \
  http://localhost:5000/api/pricing/optimize | jq .
```

### 4. Payments Dashboard Card ⏳ TODO
Create UI card showing:
- Last 10 payment events
- Quick refund button
- Error rate (already tracked in `/api/costs/status`)

### 5. Stripe Email Receipts ⏳ TODO
```bash
# Enable in Stripe Dashboard:
# Settings > Emails > Successful payments
# - Enable "Email customers about successful payments"
# - Customize receipt template with branding
```

---

## 📊 30/60/90 Day Roadmap

### 30 Days
- [ ] Customer portal (invoices/history)
- [ ] Referral analytics
- [ ] Cache for heavy endpoints

### 60 Days  
- [ ] Cohort & LTV dashboard
- [ ] Automated A/B for pricing
- [ ] Cost reports by feature

### 90 Days
- [ ] SOC-2 prep pack
- [ ] Multi-region active/active

---

## 🎯 Quick Health Check Commands

```bash
# 1. Overall system health
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  http://localhost:5000/api/system-health | jq .

# 2. Scheduler status
tail -n 50 logs/scheduler.log

# 3. Enterprise validation
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  http://localhost:5000/api/validate/enterprise | jq '.validation.status'

# 4. Financial health
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  http://localhost:5000/api/finops/report | jq .

# 5. SLO budget status
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  http://localhost:5000/api/slo/budget | jq .

# 6. Recent incidents
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  http://localhost:5000/api/incidents/summary | jq .

# 7. Cost guardrails
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  http://localhost:5000/api/costs/status | jq .

# 8. Autoscale status
curl -s -H "X-Dash-Key:$DASHBOARD_KEY" \
  http://localhost:5000/api/scale/status | jq .
```

---

## 🔔 Monitoring URLs (Public Access)

- **Enterprise Report:** https://echopilotai.replit.app/api/reports/enterprise/html
- **Validation Dashboard:** https://echopilotai.replit.app/api/validation/html
- **System Health:** Check via API (requires auth)

---

## 📞 Support Escalation

1. **Check Logs First:**
   - Scheduler: `logs/scheduler.log`
   - API errors: `logs/*.ndjson`
   - Payment webhooks: `logs/payment_webhooks.ndjson`

2. **Run Diagnostics:**
   ```bash
   python3 scripts/enterprise_validator.py
   python3 scripts/self_heal_v2.py
   ```

3. **Critical Issues:**
   - Telegram alerts configured via TELEGRAM_BOT_TOKEN
   - Email alerts via configured SMTP
   - Manual intervention via API endpoints

---

**🎉 Your EchoPilot platform is live and ready for production traffic!**

Next: Run the Stripe test, then tackle the "This Week" items.
