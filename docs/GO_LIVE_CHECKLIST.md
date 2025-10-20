# 🚀 EchoPilot Go-Live Checklist

## ✅ Completed (LIVE Mode Active)

### Core System
- [x] Stripe LIVE mode activated
- [x] LIVE API key verified working
- [x] Webhook configured + secret rotated
- [x] Production URL: https://echopilotai.replit.app
- [x] All 10 enterprise features validated
- [x] Scheduler autonomous (PID confirmed)

### Payment Security  
- [x] Minimum: $0.50 USD
- [x] HMAC signed download URLs
- [x] Webhook signature verification

---

## 📋 Stripe Settings (Do These Now)

### 1. Fraud Protection
Stripe → Radar → Rules:
- Enable velocity checks (max 5/card/hour)
- Require CVC verification
- Optional: Block prepaid cards

### 2. Email Receipts
Stripe → Settings → Emails:
- **Enable automatic receipts** ← Do this!
- Customize with EchoPilot branding

### 3. Webhook Monitoring
Stripe → Webhooks → Your endpoint:
- Verify 200 OK responses
- Set 3 retries with backoff
- Rotate secret monthly

---

## 🧪 Payment Ops Testing

### Test $0.50 charge → full refund
1. Create invoice via dashboard
2. Complete payment (test card: 4242...)
3. Stripe Dashboard → Find payment → Refund
4. Verify webhook logged event

### Test partial refund ($0.10)
Same flow, partial amount

---

## 🚨 Production Alerts (NEW!)

**Created:** `scripts/production_alerts.py`

**Monitors:**
- Webhook failures (>3 in 5min) → Telegram alert
- Payment errors (>5%/hour) → Telegram alert  
- Revenue dip (>30% day-over-day) → Telegram warning

**Test now:**
```bash
python3 scripts/production_alerts.py
```

**Add to scheduler** (optional):
```python
# In exec_scheduler.py, add:
schedule.every(5).minutes.do(run_production_alerts)
```

---

## 📊 Daily Ops Checklist

**Morning (08:00-09:00 UTC):**
- CEO Brief delivered ✅ (auto)
- Daily Report sent ✅ (auto)
- Check Telegram for alerts

**Anytime:**
- `logs/scheduler.log` → last tick <60s
- Stripe dashboard → no failed payments

---

## 🔄 Rollback (Emergency)

**Mobile Steps:**
1. Secrets → STRIPE_MODE → change `live` to `test`
2. Workflows → Restart "EchoPilot Bot"
3. Verify: Payment mode shows "test"

**Safe:** All data intact, only payments switch to test mode

---

*LIVE Mode Active Since: Oct 20, 2025*
