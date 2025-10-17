# 🚀 Super Easy Stripe Setup (2 Minutes!)

## The Easiest Way - Test Mode (No Verification Needed!)

You can start accepting test payments in **under 2 minutes** with just ONE API key!

---

## 📱 Quick Steps (On Your Galaxy Fold 6)

### Step 1: Get Your Stripe Test Key (1 minute)

1. **Go to:** https://dashboard.stripe.com/register
   - Sign up with email (no verification needed for test mode!)
   - Or login if you have an account

2. **Copy your test key:**
   - Dashboard automatically shows your API keys
   - Look for "Secret key" starting with `sk_test_`
   - Tap to reveal and copy it

### Step 2: Add to Replit (30 seconds)

1. **Open Replit app**
2. **Tap ⋮ (three dots)** → **Secrets**
3. **Add one secret:**
   ```
   Secret Name: STRIPE_SECRET_KEY
   Value: sk_test_... (paste your key)
   ```

### Step 3: Done! ✅

**That's it!** Your payment system is now active.

The bot will auto-restart and start creating Stripe checkout links for every job!

---

## ✨ What You Get With Just This One Key

✅ **Payment links auto-created** (3x AI cost pricing)  
✅ **Stripe-hosted checkout pages** (secure, PCI compliant)  
✅ **Test card payments** (use 4242 4242 4242 4242)  
✅ **Automatic logging** to Notion Job Log  

**Without webhook secret:** Payments work, but you'll rely on nightly reconciliation (2:10 UTC) to update payment status.

---

## 🔄 Optional: Add Webhooks Later (For Real-Time Updates)

When you're ready for instant payment confirmations:

1. **Go to:** https://dashboard.stripe.com/webhooks
2. **Click:** "Add endpoint"
3. **Webhook URL:** `https://Echopilotai.replit.app/webhook/stripe`
4. **Select events:** 
   - `checkout.session.completed`
   - `checkout.session.expired`
5. **Copy signing secret** (starts with `whsec_`)
6. **Add to Replit Secrets:**
   ```
   Secret Name: STRIPE_WEBHOOK_SECRET
   Value: whsec_... (paste)
   ```

**With webhooks:** Payment status updates instantly when customers pay!

---

## 🧪 Testing Your Payments

### Test Card Numbers (Use These!)

| Card Number | Result |
|-------------|--------|
| 4242 4242 4242 4242 | ✅ Success |
| 4000 0000 0000 9995 | ❌ Declined |
| 4000 0025 0000 3155 | 🔐 Requires 3D Secure |

**Any future date for expiry, any CVC, any ZIP**

### How to Test:

1. **Trigger a job** in Notion (set Status = "Triggered")
2. **Job completes** → Payment link created
3. **Check Notion Job Log** → Payment Link field has Stripe URL
4. **Click payment link** → Stripe checkout page opens
5. **Use test card:** 4242 4242 4242 4242
6. **Complete payment** → Status updates (instantly with webhooks, or at 2:10 UTC without)

---

## 💡 Why This Is The Easiest Way

**Traditional Stripe Integration:**
- ❌ Build checkout UI
- ❌ Handle card validation
- ❌ Manage PCI compliance
- ❌ Write success/failure handlers
- ❌ 100+ lines of code

**Your Setup:**
- ✅ Add 1 secret key
- ✅ Stripe hosts everything
- ✅ Auto-generates payment links
- ✅ Already built and tested!

---

## 🎯 Current Status Check

Run this to see if Stripe is active:
```bash
python autoconfig.py
```

Should show:
```
✅ Active: Payment System (Stripe)
```

Test all systems:
```bash
python test_integration.py
```

Should show:
```
✅ PASS: Payment System (Stripe configured)
```

---

## 🚀 Go Live When Ready

When you're ready for real payments:

1. **Complete Stripe verification** (business info, bank account)
2. **Switch to live mode** in Stripe Dashboard (toggle in top right)
3. **Replace test key** with live key (starts with `sk_live_`)
4. **Update webhook** (if using) to listen to live events

That's it! Same code, real money. 💰

---

## 📞 Need Help?

**Stripe gives you free test mode forever!**
- No credit card needed for testing
- Unlimited test payments
- Full feature access

**Questions?**
- Telegram: Send `/status` to @Echopilotai_bot
- Check logs: `cat /tmp/logs/EchoPilot_Bot_*.log | grep -i payment`

---

## 🎉 Summary

**Minimum to activate payments:**
- [ ] 1 secret: `STRIPE_SECRET_KEY` (from stripe.com/dashboard)
- [ ] That's it!

**Optional for real-time updates:**
- [ ] Add webhook endpoint
- [ ] Add `STRIPE_WEBHOOK_SECRET`

**Your payment system has:**
- ✅ Auto checkout link creation
- ✅ Stripe-hosted secure payments
- ✅ Test mode (no verification)
- ✅ Notion integration
- ✅ Nightly reconciliation
- ✅ All features built-in!

**Next:** Add `STRIPE_SECRET_KEY` to Replit Secrets and you're done! 🚀
