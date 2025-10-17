# 💰 EchoPilot Payment System Guide

**Status:** ✅ INSTALLED (Awaiting Configuration)  
**Last Updated:** October 17, 2025

---

## 📋 Overview

The EchoPilot payment system automatically creates **Stripe or PayPal checkout links** for each completed job, sends them in invoice emails, receives webhook notifications to update payment status automatically, and runs nightly reconciliation for missed webhooks.

### Key Features

✅ **Automatic Payment Link Generation** - Every job gets a checkout link (Stripe or PayPal)  
✅ **Webhook Integration** - Payment status updates automatically when paid  
✅ **Nightly Reconciliation** - Catches missed webhooks at 2:10 UTC daily  
✅ **Job Log Integration** - Payment Link and Payment Status tracked in Notion  
✅ **Pricing Formula** - Jobs charged at 3x AI cost (configurable)

---

## 🏗️ What Was Installed

### 1. Core Payment Module (`bot/payments.py`)
- **Stripe Integration**: Checkout sessions with card payments
- **PayPal Integration**: Order creation and capture
- **Unified API**: `create_payment_link(amount, job_id, email)`
- **Webhook Parsers**: Stripe and PayPal webhook verification
- **Configuration Check**: `is_payment_configured()` helper

### 2. Webhook Endpoints (`run.py`)
- `POST /webhook/stripe` - Receives Stripe payment events
- `POST /webhook/paypal` - Receives PayPal payment events
- Auto-updates Notion "Payment Status" on payment completion

### 3. Nightly Reconciliation (`bot/reconcile_payments.py`)
- Runs daily at **2:10 UTC**
- Queries Notion for "Unpaid" jobs
- Attempts PayPal capture for pending orders
- Sends email alert when payments are reconciled

### 4. Processor Integration (`bot/processor.py`)
- Creates payment links after job completion
- Adds `Payment Link` and `Payment Status` to Job Log
- Pricing: **3x AI cost** (e.g., $0.10 AI cost → $0.30 charge)
- Gracefully degrades if payment not configured

### 5. Notion API Updates (`bot/notion_api.py`)
- `update_job_payment_status(job_id, status)` function
- Job log includes `payment_link` and `payment_status` fields
- Auto-creates Payment Link (URL) and Payment Status (Select) properties

---

## ⚙️ Configuration

### Required Notion Fields

Your **EchoPilot Job Log** database needs these properties:

| Property Name | Type | Options |
|--------------|------|---------|
| Payment Link | URL | - |
| Payment Status | Select | Unpaid, Paid, Cancelled |

**To add them:**
1. Open your **Job Log** database in Notion
2. Click "+ New property"
3. Create "Payment Link" (type: URL)
4. Create "Payment Status" (type: Select)
5. Add select options: Unpaid, Paid, Cancelled

### Environment Variables (Stripe - Recommended)

Add these to your Replit Secrets:

```bash
# Stripe (Preferred)
STRIPE_SECRET_KEY=sk_live_xxxxx          # From Stripe dashboard
STRIPE_WEBHOOK_SECRET=whsec_xxxxx        # From webhook configuration

# Payment Settings
PAYMENT_CURRENCY=USD                      # Currency code
PAYMENT_BRAND_NAME=EchoPilot AI          # Brand name in checkout
PAYMENT_SUCCESS_URL=https://Echopilotai.replit.app/pay/success
PAYMENT_CANCEL_URL=https://Echopilotai.replit.app/pay/cancel
```

### Alternative: PayPal Configuration

```bash
# PayPal
PAYPAL_CLIENT_ID=xxxxx                   # From PayPal developer dashboard
PAYPAL_SECRET=xxxxx                      # From PayPal developer dashboard
PAYPAL_LIVE=true                         # Set to 'false' for sandbox testing

# Payment Settings (same as above)
PAYMENT_CURRENCY=USD
PAYMENT_BRAND_NAME=EchoPilot AI
PAYMENT_SUCCESS_URL=https://Echopilotai.replit.app/pay/success
PAYMENT_CANCEL_URL=https://Echopilotai.replit.app/pay/cancel
```

---

## 🎯 Stripe Setup Instructions

### 1. Create Stripe Account
1. Go to https://stripe.com
2. Sign up for a new account
3. Complete verification (required for live payments)

### 2. Get API Keys
1. Go to **Developers** → **API Keys**
2. Copy your **Secret key** (starts with `sk_live_` or `sk_test_`)
3. Add to Replit Secrets as `STRIPE_SECRET_KEY`

### 3. Configure Webhook
1. Go to **Developers** → **Webhooks**
2. Click **Add endpoint**
3. Enter URL: `https://Echopilotai.replit.app/webhook/stripe`
4. Select events to listen for:
   - ✅ `checkout.session.completed`
   - ✅ `payment_intent.succeeded`
   - ✅ `checkout.session.expired`
5. Click **Add endpoint**
6. Copy the **Signing secret** (starts with `whsec_`)
7. Add to Replit Secrets as `STRIPE_WEBHOOK_SECRET`

### 4. Test Mode (Optional)
- Use test keys (`sk_test_...`) for testing
- Use test card: `4242 4242 4242 4242` (any future date, any CVC)
- Switch to live keys when ready for production

---

## 💳 PayPal Setup Instructions

### 1. Create PayPal Developer Account
1. Go to https://developer.paypal.com
2. Sign in with your PayPal account
3. Go to **Dashboard** → **My Apps & Credentials**

### 2. Create App
1. Click **Create App**
2. Enter app name (e.g., "EchoPilot Payments")
3. Select **Merchant** as app type
4. Click **Create App**

### 3. Get API Credentials
1. Copy **Client ID**
2. Copy **Secret**
3. Add to Replit Secrets:
   - `PAYPAL_CLIENT_ID`
   - `PAYPAL_SECRET`

### 4. Configure Webhooks (Optional)
1. In your app settings, scroll to **Webhooks**
2. Click **Add Webhook**
3. Enter URL: `https://Echopilotai.replit.app/webhook/paypal`
4. Select events:
   - ✅ `CHECKOUT.ORDER.APPROVED`
   - ✅ `PAYMENT.CAPTURE.COMPLETED`
5. Click **Save**

**Note:** PayPal webhooks are optional because reconciliation handles missed events.

### 5. Go Live
1. Toggle from **Sandbox** to **Live** in dashboard
2. Set `PAYPAL_LIVE=true` in Replit Secrets
3. Complete PayPal business verification

---

## 🚀 How It Works

### Job Processing Flow

```
1. EchoPilot processes job
2. Job completes (QA ≥ 80%)
3. Processor calculates: charge = AI_cost × 3
4. Payment link created (Stripe or PayPal)
5. Job logged to Notion with:
   - Payment Link: checkout URL
   - Payment Status: "Unpaid"
6. (Future: Email invoice with payment link)
```

### Payment Webhook Flow

```
1. User clicks payment link
2. Completes checkout (Stripe/PayPal)
3. Payment provider sends webhook to EchoPilot
4. Webhook endpoint updates Notion:
   - Payment Status: "Unpaid" → "Paid"
5. Job marked as paid in Job Log
```

### Reconciliation Flow (2:10 UTC Daily)

```
1. Query Notion for "Unpaid" jobs
2. For each job with PayPal link:
   - Attempt to capture payment
   - If successful: mark as "Paid"
3. Send email alert if any jobs updated
4. Log completion
```

---

## 📊 Pricing Configuration

### Current Formula

```python
charge_amount = ai_cost * 3.0
```

**Examples:**
- AI cost $0.05 → Charge $0.15
- AI cost $0.20 → Charge $0.60
- AI cost $1.00 → Charge $3.00

### Customize Pricing

Edit `bot/processor.py`, line 58:

```python
def _create_payment_link(self, job_name: str, cost: float, client_email: str = None):
    # Change multiplier here:
    amount = cost * 3.0  # ← Change this number
```

**Suggested multipliers:**
- 2.0 = 2x markup (competitive)
- 3.0 = 3x markup (moderate, current)
- 5.0 = 5x markup (premium)

---

## 🧪 Testing

### 1. Enable Payment Provider

**For Stripe:**
```bash
# In Replit Secrets
STRIPE_SECRET_KEY=sk_test_xxxxx  # Use test key
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
```

**For PayPal:**
```bash
# In Replit Secrets
PAYPAL_CLIENT_ID=xxxxx
PAYPAL_SECRET=xxxxx
PAYPAL_LIVE=false  # Use sandbox
```

### 2. Process a Test Job

1. Open your **Automation Queue** in Notion
2. Create a test task with Trigger = ☑️
3. Wait for EchoPilot to process it
4. Check **Job Log** for new entry with Payment Link

### 3. Test Payment Flow

**Stripe Test:**
1. Click the Payment Link
2. Use test card: `4242 4242 4242 4242`
3. Any future expiry date, any CVC
4. Complete checkout
5. Check Notion - Payment Status should update to "Paid"

**PayPal Test:**
1. Click the Payment Link
2. Log in with PayPal sandbox account
3. Complete payment
4. Wait for reconciliation (2:10 UTC) or check webhook logs

### 4. Verify Webhook

```bash
# Check workflow logs for webhook activity
grep "Webhook" /tmp/logs/EchoPilot_Bot*.log
```

Expected output:
```
[Stripe Webhook] Updated job [job-name] to status: Paid
```

---

## 📱 Mobile Instructions

**On your Galaxy Fold 6:**

### Add Stripe Keys
1. Tap **Secrets** tab (🔒 icon)
2. Tap **+ New Secret**
3. Name: `STRIPE_SECRET_KEY`
4. Value: `sk_live_xxxxx` (paste from Stripe dashboard)
5. Tap **Add secret**
6. Repeat for `STRIPE_WEBHOOK_SECRET`

### Configure Webhook (Desktop Required)
1. Log into Stripe dashboard on desktop/browser
2. **Developers** → **Webhooks** → **Add endpoint**
3. URL: `https://Echopilotai.replit.app/webhook/stripe`
4. Events: `checkout.session.completed`, `payment_intent.succeeded`
5. Copy signing secret to Replit Secrets

### Test Payment
1. Process a test job in Notion
2. Open **Job Log** database
3. Click the Payment Link in the new job
4. Complete test payment
5. Refresh Notion - Status should be "Paid"

---

## 🔍 Monitoring

### Check Payment Status
```bash
# View recent jobs with payment info
SELECT "Job Name", "Payment Status", "Payment Link"
FROM "EchoPilot Job Log"
ORDER BY "Timestamp" DESC
LIMIT 10
```

### View Webhook Logs
```bash
# In Replit Shell
grep "Webhook" /tmp/logs/EchoPilot_Bot*.log | tail -20
```

### Manual Reconciliation
```bash
# In Replit Shell
python - <<'PY'
from bot.reconcile_payments import reconcile_once
changed = reconcile_once()
print(f"Updated {changed} job(s)")
PY
```

---

## 🛠️ Troubleshooting

### Payment Links Not Generated

**Check:** Is payment provider configured?
```bash
# In Replit Shell
python -c "from bot.payments import is_payment_configured; print('Configured:', is_payment_configured())"
```

**Expected:** `Configured: True`

**If False:**
- Verify `STRIPE_SECRET_KEY` or `PAYPAL_CLIENT_ID` is set in Secrets
- Restart workflow

### Webhook Not Updating Status

**Check:** Webhook signature verification
```bash
# View webhook errors in logs
grep "Webhook.*Error" /tmp/logs/EchoPilot_Bot*.log
```

**Common issues:**
1. **Wrong webhook secret** - Re-copy from Stripe dashboard
2. **Endpoint not reachable** - Check bot is running: `curl https://Echopilotai.replit.app/health`
3. **Wrong endpoint URL** - Should be `https://Echopilotai.replit.app/webhook/stripe`

### Payment Status Stuck on "Unpaid"

**Solution 1:** Wait for reconciliation (2:10 UTC)

**Solution 2:** Manual reconciliation
```bash
python -c "from bot.reconcile_payments import reconcile_once; reconcile_once()"
```

**Solution 3:** Manual update in Notion
1. Open Job Log
2. Find the job
3. Change Payment Status to "Paid"

---

## 📈 Next Steps

### 1. Enable Payment Provider
- [ ] Sign up for Stripe or PayPal
- [ ] Add API keys to Replit Secrets
- [ ] Configure webhook endpoint
- [ ] Test with sandbox/test mode

### 2. Add Notion Properties
- [ ] Open Job Log database
- [ ] Create "Payment Link" (URL) property
- [ ] Create "Payment Status" (Select) property
- [ ] Add options: Unpaid, Paid, Cancelled

### 3. Test End-to-End
- [ ] Process test job
- [ ] Verify payment link created
- [ ] Complete test payment
- [ ] Confirm status updates to "Paid"

### 4. Go Live
- [ ] Switch to live API keys
- [ ] Update webhook to production URL
- [ ] Monitor first few transactions
- [ ] Set up payment notifications

---

## 💡 Tips

- **Start with Stripe test mode** - Easier to debug
- **Use PayPal for international** - Better global coverage
- **Monitor reconciliation** - Check logs at 2:10 UTC
- **Adjust pricing multiplier** - Start at 3x, adjust based on market
- **Keep webhooks active** - Primary payment update mechanism

---

## 🔐 Security Notes

- ✅ Webhook signatures verified for Stripe
- ✅ API keys stored in Replit Secrets (never in code)
- ✅ Payment processing handled by Stripe/PayPal (PCI compliant)
- ✅ No credit card data touches EchoPilot servers
- ⚠️ PayPal webhooks have basic signature verification (use reconciliation as backup)

---

## 📞 Support

**Payment Issues:**
- Stripe: https://support.stripe.com
- PayPal: https://developer.paypal.com/support

**EchoPilot Issues:**
- Check workflow logs
- Test with simplified scenario
- Verify all environment variables set

---

**Your EchoPilot system is now payment-ready!** 💰

Just add your Stripe or PayPal credentials to start charging for AI jobs automatically.
