# ✅ Stripe Checkout - FIXED & READY TO DEPLOY

**Status:** Code fixed, awaiting manual deployment  
**Date:** November 9, 2025

---

## 🎯 What Was Fixed

### **Before:**
- ❌ Complex logic with dynamic string interpolation
- ❌ POST endpoint returning 405 or "Price ID not found" errors
- ❌ Fragile environment variable checking
- ❌ Build failures on Vercel

### **After:**
- ✅ Clean, simple code with static env references only
- ✅ Dual environment variable scheme support
- ✅ POST handler: `{"plan":"starter","term":"monthly"}`
- ✅ GET handler: `?plan=starter&term=monthly`
- ✅ No LSP errors, builds successfully

---

## 📋 Environment Variable Support

The new code supports **both naming schemes**:

### Scheme 1: Four Variables (Full Support)
```
STRIPE_PRICE_STARTER         → Starter Monthly
STRIPE_PRICE_STARTER_YEAR    → Starter Yearly
STRIPE_PRICE_PRO             → Pro Monthly
STRIPE_PRICE_PRO_YEAR        → Pro Yearly
```

### Scheme 2: Two/Four Variables (Flexible)
```
STRIPE_PRICE_ID_STARTER      → Starter Monthly
STRIPE_PRICE_ID_PRO          → Pro Monthly
STRIPE_PRICE_ID_STARTER_YEAR → Starter Yearly (optional)
STRIPE_PRICE_ID_PRO_YEAR     → Pro Yearly (optional)
```

The code will use whichever scheme is configured in your Vercel environment.

---

## 🚀 Deploy Now (One Command)

Run this in your **Shell terminal**:

```bash
./fix-and-deploy.sh
```

This script will:
1. ✅ Commit the checkout fix
2. ✅ Push to GitHub
3. ✅ Wait 3 minutes for Vercel auto-deploy
4. ✅ Test all 4 checkout combinations
5. ✅ Verify GET endpoint (backward compatibility)
6. ✅ Show which environment variables are configured

**Total time:** ~4 minutes

---

## 🧪 Expected Test Results

After deployment, you should see:

```
Test 1: Starter Monthly (POST)
✅ URL: https://checkout.stripe.com/c/pay/cs_test_...

Test 2: Pro Monthly (POST)
✅ URL: https://checkout.stripe.com/c/pay/cs_test_...

Test 3: Starter Yearly (POST)
✅ URL: https://checkout.stripe.com/c/pay/cs_test_...

Test 4: Pro Yearly (POST)
✅ URL: https://checkout.stripe.com/c/pay/cs_test_...

Test 5: GET endpoint
HTTP/2 200
```

---

## 📦 What Changed

**File:** `levqor-site/src/app/api/checkout/route.ts`

**Key Improvements:**
1. Single `getPriceId()` function with lookup table
2. Static environment variable assignments (no dynamic interpolation)
3. Clear error messages that don't leak secret values
4. Unified `createSession()` function for both POST and GET
5. Simplified stripe session creation (removed unnecessary options)

---

## 🔍 Manual Deployment (Alternative)

If the script doesn't work, deploy manually via Vercel:

1. Go to: https://vercel.com/vii-77s-projects/levqor-site
2. Click "Deployments" → "Deploy" (top right)
3. Select "main" branch
4. Click "Deploy"
5. Wait 2-3 minutes
6. Test:
   ```bash
   curl -X POST https://levqor.ai/api/checkout \
     -H 'content-type: application/json' \
     --data '{"plan":"starter","term":"monthly"}'
   ```

---

## ✅ Final Checklist

- [x] Code fixed with dual env scheme support
- [x] LSP errors resolved
- [x] Local build successful
- [x] Deployment script created
- [ ] **Run `./fix-and-deploy.sh` in Shell**
- [ ] Verify all 4 checkout URLs work
- [ ] Confirm GET endpoint backward compatibility

---

**Ready to deploy!** Run the script and your Stripe checkout will be fully operational. 🚀
