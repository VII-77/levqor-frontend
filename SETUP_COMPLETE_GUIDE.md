# 🚀 Complete Payment & Client System Setup

This guide will walk you through activating both systems on your Galaxy Fold 6.

---

## 📱 **Step 1: Choose Payment Provider**

You need to pick ONE payment provider (Stripe is recommended):

### Option A: Stripe (Recommended) ✅

**Why Stripe?**
- Better developer experience
- More reliable webhooks
- Customer email support built-in
- Easier testing

**What you need:**
1. Stripe account (free to create at stripe.com)
2. API keys from Stripe Dashboard → Developers → API Keys
3. Webhook secret from Stripe Dashboard → Developers → Webhooks

### Option B: PayPal

**What you need:**
1. PayPal Business account
2. Client ID and Secret from developer.paypal.com
3. Choose test/live mode

---

## 📱 **Step 2: Add Payment Credentials to Replit**

### On Your Galaxy Fold 6:

1. **Open Replit App**
2. **Tap the 3 dots (⋮)** in top right
3. **Select "Secrets"**
4. **Add these secrets:**

#### For Stripe:
```
Secret Name: STRIPE_SECRET_KEY
Value: sk_test_... (your Stripe secret key)

Secret Name: STRIPE_WEBHOOK_SECRET  
Value: whsec_... (your webhook signing secret)
```

#### OR For PayPal:
```
Secret Name: PAYPAL_CLIENT_ID
Value: (your PayPal client ID)

Secret Name: PAYPAL_SECRET
Value: (your PayPal secret)

Secret Name: PAYPAL_LIVE
Value: false (use 'true' for production)
```

---

## 📊 **Step 3: Create Notion Clients Database**

### In Notion (on your phone or computer):

1. **Go to your Notion workspace**
2. **Create a new database** (click + → Table)
3. **Name it:** `EchoPilot Clients`
4. **Add these properties:**

| Property Name | Type | Required | Notes |
|--------------|------|----------|-------|
| Client Name | Title | ✅ Yes | Auto-created |
| Email | Email | ✅ Yes | For invoices |
| Rate USD/min | Number | ✅ Yes | Billing rate (e.g., 5.0) |
| Active | Checkbox | ✅ Yes | Enable/disable client |

5. **Add a test client:**
   - Client Name: "Test Client"
   - Email: your-email@example.com
   - Rate USD/min: 5.0
   - Active: ✅ checked

6. **Copy the database ID:**
   - Open database as a full page
   - Copy the URL: `notion.so/xxxxx?v=yyy`
   - The database ID is the `xxxxx` part (32 characters)

---

## 📱 **Step 4: Add Notion Client DB to Replit Secrets**

### On Your Galaxy Fold 6:

1. **Open Replit App**
2. **Tap the 3 dots (⋮)** → **Secrets**
3. **Add:**

```
Secret Name: NOTION_CLIENT_DB_ID
Value: (paste the 32-character database ID)

Secret Name: DEFAULT_RATE_USD_PER_MIN
Value: 5.0
```

---

## 📊 **Step 5: Extend Job Log Database**

### In Notion:

1. **Open your Job Log database** (the one with JOB_LOG_DB_ID)
2. **Add these properties:**

| Property Name | Type | Format/Settings |
|--------------|------|-----------------|
| Client | Relation | → Link to "EchoPilot Clients" database |
| Client Email | Email | - |
| Client Rate USD/min | Number | Number format |
| Gross USD | Number | Number format, 2 decimals |
| Profit USD | Number | Number format, 2 decimals |
| Margin % | Number | Number format, 1 decimal |

3. **Add Payment fields if not present:**

| Property Name | Type | Format/Settings |
|--------------|------|-----------------|
| Payment Link | URL | - |
| Payment Status | Select | Options: Pending, Paid, Failed, Cancelled |

---

## 🔗 **Step 6: Configure Webhook URLs**

### For Stripe:

1. **Go to:** Stripe Dashboard → Developers → Webhooks
2. **Click "Add endpoint"**
3. **Endpoint URL:** `https://Echopilotai.replit.app/webhook/stripe`
4. **Select events:**
   - `checkout.session.completed`
   - `checkout.session.expired`
5. **Copy webhook signing secret** → Add to Replit Secrets as `STRIPE_WEBHOOK_SECRET`

### For PayPal:

1. **Go to:** developer.paypal.com → My Apps
2. **Select your app** → Webhooks
3. **Add webhook:** `https://Echopilotai.replit.app/webhook/paypal`
4. **Subscribe to events:**
   - `CHECKOUT.ORDER.APPROVED`
   - `CHECKOUT.ORDER.COMPLETED`

---

## ✅ **Step 7: Test the System**

### On Your Galaxy Fold 6:

1. **Open Replit Shell** (swipe from left)
2. **Run test:**
```bash
python test_integration.py
```

3. **Check configuration:**
```bash
python autoconfig.py
```

4. **Expected output:**
```
✅ Active: Payment System
✅ Active: Client Management
```

---

## 🎯 **What Happens Next**

Once configured, for every completed job:

1. ✅ **Calculate AI cost** (tokens × pricing)
2. ✅ **Create payment link** (3x AI cost)
3. ✅ **Look up client rate** (or use $5/min default)
4. ✅ **Calculate revenue:**
   - Gross USD = Duration (min) × Client Rate
   - Profit USD = Gross - AI Cost
   - Margin % = (Profit / Gross) × 100
5. ✅ **Generate PDF invoice** with:
   - Job details
   - Financial breakdown
   - Payment link embedded
6. ✅ **Email invoice** to client automatically
7. ✅ **Log everything** to Notion Job Log
8. ✅ **Track payment** via webhooks
9. ✅ **Reconcile nightly** (2:10 UTC) for missed webhooks

---

## 📧 **Invoice Email Format**

Clients receive:
```
Subject: Invoice for [Job Name]

Hello [Client Name],

Your job has been completed successfully!

Job: [Job Name]
Duration: X.XX minutes
Rate: $X.XX/min
Total: $XX.XX

Please find the attached invoice (PDF).

Pay now: [Payment Link]

Best regards,
EchoPilot
```

---

## 🔍 **Verification Checklist**

Before you're done, check:

- [ ] Payment credentials added to Secrets
- [ ] Notion Clients database created with 4 fields
- [ ] Test client added to database
- [ ] NOTION_CLIENT_DB_ID added to Secrets
- [ ] Job Log extended with 6 new fields (Client, Client Email, rates, revenue)
- [ ] Payment fields added (Payment Link, Payment Status)
- [ ] Webhook URL configured in Stripe/PayPal
- [ ] `python test_integration.py` shows all green ✅
- [ ] `python autoconfig.py` shows both systems active

---

## 📱 **Quick Mobile Commands**

From Replit Shell on your Galaxy Fold:

```bash
# Test everything
python test_integration.py

# Check status
python autoconfig.py

# View logs
cat /tmp/logs/EchoPilot_Bot_*.log | tail -50

# Restart bot (after adding secrets)
# No command needed - auto-restarts on secret changes
```

---

## 🆘 **Troubleshooting**

### Payment system not activating?
- Verify secrets are exactly named (case-sensitive)
- Check Stripe/PayPal credentials are correct
- Restart happens automatically when secrets added

### Client system not working?
- Verify database ID is 32 characters (no dashes, no extra characters)
- Check Client database has all 4 required fields
- Verify Job Log has all 6 revenue fields

### Invoices not sending?
- Check client has valid email in Clients database
- Gmail OAuth is already configured ✅
- Check logs: `cat /tmp/logs/EchoPilot_Bot_*.log | grep -i invoice`

---

## 🎉 **You're Done!**

Once all steps are complete:
- Payment links auto-create for every job
- Revenue auto-calculates based on client rates
- Invoices auto-generate as PDF
- Emails auto-send to clients
- Webhooks auto-update payment status
- Nightly reconciliation catches anything missed

**Full monetization activated!** 💰

---

## 📞 **Need Help?**

Telegram commands for monitoring:
- `/status` - Check bot status
- `/health` - System health
- `/report` - Email supervisor report

Check status anytime:
- https://Echopilotai.replit.app/health
- https://Echopilotai.replit.app/ops-report
