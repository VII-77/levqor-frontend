# 🚀 EchoPilot Go-Live Cutover Guide

## Current Status

✅ **All 8 phases validated and tested**  
✅ **Smoke tests passed (local)**  
✅ **Webhook endpoint added**  
✅ **RUNBOOK.md updated**  
⚠️  **Stripe in TEST mode** (ready to switch)

---

## GO-LIVE STEPS (Manual Actions Required)

### Step 1: Switch Stripe to LIVE Mode

**In Replit Secrets (mobile-friendly):**

1. Open Replit → Your project → Tools (⚙️) → Secrets
2. Add/Update these secrets:
   ```
   STRIPE_MODE = live
   STRIPE_SECRET_LIVE = sk_live_xxxxx (your live secret key)
   STRIPE_WEBHOOK_SECRET = whsec_xxxxx (your live webhook secret)
   ```
3. Keep existing `STRIPE_SECRET_KEY` (for rollback)

### Step 2: Configure Stripe Webhook

**In Stripe Dashboard:**

1. Go to: Developers → Webhooks → Add endpoint
2. Endpoint URL: `https://echopilotai.replit.app/api/payments/webhook`
3. Events to listen: `checkout.session.completed`, `payment_intent.succeeded`
4. Copy Signing secret → Add as `STRIPE_WEBHOOK_SECRET` in Replit

### Step 3: Restart Server

In Replit:
- Tools → Workflows → "EchoPilot Bot" → Stop → Start
- Wait 15 seconds for restart

### Step 4: Send Stripe Test Event

In Stripe Dashboard:
- Webhooks → Your endpoint → Send test webhook
- Choose: `checkout.session.completed`
- Check: `logs/stripe_webhook.log` (should have new entry)

### Step 5: Verify Scheduler

Dashboard → Automations Scheduler → Status should show:
- ✅ Running
- Recent ticks visible
- Next runs calculated

---

## POST-CUTOVER SMOKE TESTS

### Test 1: Create Live Invoice

```bash
curl -H "X-Dash-Key: $DASHBOARD_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount":1.00,"email":"live-test@example.com"}' \
  https://echopilotai.replit.app/api/payments/create-invoice
```

**Expected:** `"mode": "live"` in response, checkout URL contains `checkout.stripe.com`

### Test 2: Dashboard Health

1. Open: https://echopilotai.replit.app/dashboard
2. Check "🚀 Enterprise Expansion Tools" card exists
3. Click "💹 Optimize Pricing" → Should get pricing recommendation
4. Click "🎯 New Referral" → Should generate EP-XXXXXX code

### Test 3: Scheduler Verification

```bash
tail -20 logs/scheduler.log | jq -r '.event'
```

**Expected:** See `tick`, `replica_sync`, `ai_ops_brain` events

---

## ROLLBACK PROCEDURE (30 seconds)

### If Issues Occur:

1. **Replit Secrets:**
   - Change `STRIPE_MODE = test`
   - Keep `STRIPE_SECRET_LIVE` (for later)

2. **Restart:**
   - Workflows → "EchoPilot Bot" → Restart

3. **Verify:**
   ```bash
   curl -H "X-Dash-Key: $DASHBOARD_KEY" \
     -d '{"amount":1.00}' \
     https://echopilotai.replit.app/api/payments/create-invoice
   ```
   Should return `"mode": "test"`

---

## VERIFICATION CHECKLIST

After go-live, verify:

- [ ] Invoice creation returns `"mode": "live"`
- [ ] Stripe webhook test event logged to `logs/stripe_webhook.log`
- [ ] Dashboard "Enterprise Expansion Tools" functional
- [ ] Scheduler running (check `/dashboard`)
- [ ] No errors in workflow logs

---

## MONITORING

### Daily Checks

1. **Dashboard:** https://echopilotai.replit.app/dashboard
   - Health indicators all green
   - Scheduler status: Running
   - Cost metrics within budget

2. **Logs:**
   ```bash
   tail logs/scheduler.log     # Scheduler events
   tail logs/stripe_webhook.log # Payment webhooks
   tail logs/ops_brain_*.json   # AI recommendations
   ```

3. **Scheduler Tasks:**
   - Pricing AI: Daily 03:00 UTC
   - Audit Pack: Monday 00:30 UTC
   - Replica Sync: Every 2 hours
   - AI Ops Brain: Every 12 hours

### Weekly Reviews

- Check AI Ops Brain recommendations (`logs/ops_brain_*.json`)
- Review audit reports (`backups/audit/`)
- Analyze referral code usage (`logs/referrals.log`)
- Validate pricing AI suggestions

---

## SUPPORT & DOCUMENTATION

- **RUNBOOK:** `RUNBOOK.md` (278 lines, complete ops guide)
- **Release Report:** `logs/RELEASE_CAPTAIN_REPORT.txt`
- **Gate Files:** `logs/phase33_ok.txt` through `logs/phase40_ok.txt`
- **Completion Summary:** `logs/PHASE33-40_ENTERPRISE_EXPANSION_COMPLETE.txt`

---

## CONTACTS & ESCALATION

**For Issues:**
1. Check logs first (`logs/`)
2. Review RUNBOOK.md troubleshooting section
3. Test rollback procedure
4. Contact Replit support if infrastructure issues

**Production-Ready Features:**
- ✅ Real payments (Stripe test/live toggle)
- ✅ Customer signed URLs (24h expiry)
- ✅ GDPR compliance exports
- ✅ Adaptive AI pricing
- ✅ Referral tracking (EP-XXXXXX codes)
- ✅ SOC-lite audit trails
- ✅ Multi-region backups
- ✅ AI ops intelligence (GPT-4o-mini)

---

**Status:** READY FOR GO-LIVE  
**Mode:** TEST (switch to LIVE when ready)  
**Deployment:** https://echopilotai.replit.app
