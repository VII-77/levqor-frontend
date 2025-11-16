# Levqor Pricing Sync Notes

**Date:** November 16, 2025  
**Status:** Frontend Updated, Stripe Manual Update Required  
**Action Required:** Update STARTER price in Stripe Dashboard from £19 to £29

---

## Executive Summary

Frontend pricing has been updated to align with the launch pricing strategy:
- **STARTER:** £29/month (£290/year)
- **PRO:** £49/month (£490/year) ✅ Already correct in Stripe
- **GROWTH:** £79/month (£790/year) ✅ Already correct in Stripe
- **BUSINESS:** £149/month (£1,490/year)

**Critical Issue:** Stripe STARTER monthly price is currently £19, needs manual update to £29 (2900 pence).

---

## Current System State

### ✅ Frontend Pricing (UPDATED)

All frontend pricing displays have been updated in:

1. **`levqor-site/src/config/pricing.ts`** ✅
   - Starter: £29/month (£290/year)
   - Growth: £79/month (£790/year)
   - Pro: £49/month (£490/year)
   - Business: £149/month (£1,490/year)

2. **`levqor-site/src/app/faq/page.tsx`** ✅
   - Updated subscription range from "£29-£299/month" to "£29-£149/month"

3. **`levqor-site/src/app/how-it-works/page.tsx`** ✅
   - Updated DFY Professional from £299 to £249 (correct DFY price)

4. **`levqor-site/src/app/pricing/page.tsx`** ✅
   - Uses pricing.ts config (automatically updated)

### ⚠️ Stripe Actual Prices (MANUAL UPDATE NEEDED)

**Live Stripe Prices as of November 16, 2025:**

| Plan | Current Stripe | Target | Status |
|------|----------------|--------|--------|
| STARTER (monthly) | £19.00 (1900 pence) | £29.00 (2900 pence) | ⚠️ **NEEDS UPDATE** |
| PRO (monthly) | £49.00 (4900 pence) | £49.00 (4900 pence) | ✅ Correct |
| GROWTH (monthly) | £79.00 (7900 pence) | £79.00 (7900 pence) | ✅ Correct |

**Note:** STARTER yearly, PRO yearly, GROWTH yearly, BUSINESS monthly, and BUSINESS yearly prices not verified yet.

### ✅ Checkout API Wiring (VERIFIED)

The checkout API (`levqor-site/src/app/api/checkout/route.ts`) is correctly configured:

```typescript
const subMap: Record<string, string | undefined> = {
  "starter:monthly": env.STARTER_M,      // → STRIPE_PRICE_STARTER
  "starter:yearly": env.STARTER_Y,       // → STRIPE_PRICE_STARTER_YEAR
  "growth:monthly": env.GROWTH_M,        // → STRIPE_PRICE_GROWTH
  "growth:yearly": env.GROWTH_Y,         // → STRIPE_PRICE_GROWTH_YEAR
  "pro:monthly": env.PRO_M,              // → STRIPE_PRICE_PRO
  "pro:yearly": env.PRO_Y,               // → STRIPE_PRICE_PRO_YEAR
  "business:monthly": env.BIZ_M,         // → STRIPE_PRICE_BUSINESS
  "business:yearly": env.BIZ_Y,          // → STRIPE_PRICE_BUSINESS_YEAR
};
```

**Result:** When users click "Get Pro" for £49/month, they get the correct Stripe price ID and are charged £49. ✅

---

## Required Manual Actions

### 1. Update Stripe STARTER Monthly Price

**In Stripe Dashboard:**

1. Navigate to: **Products → Levqor Starter Subscription**
2. Find the **monthly recurring price** (currently £19.00)
3. Options:
   - **Option A (Recommended):** Create a NEW price at £29.00 (2900 pence) and update the `STRIPE_PRICE_STARTER` environment variable
   - **Option B:** Archive the old £19 price and create a new £29 price (prevents existing customers from being affected)

**Environment Variable Update:**
```bash
STRIPE_PRICE_STARTER=price_XXXXXXXXXXXXXXXXXX  # New price ID at £29
```

**Replit Deployment:** After updating the env var in Replit Secrets, redeploy both backend and frontend.

### 2. Verify All Yearly Prices

**Check in Stripe Dashboard:**

- STARTER yearly: Should be £290 (29000 pence)
- PRO yearly: Should be £490 (49000 pence)
- GROWTH yearly: Should be £790 (79000 pence)
- BUSINESS monthly: Should be £149 (14900 pence)
- BUSINESS yearly: Should be £1490 (149000 pence)

**Update environment variables if needed:**
```bash
STRIPE_PRICE_STARTER_YEAR=price_XXXXXXXXXXXXXXXXXX
STRIPE_PRICE_PRO_YEAR=price_XXXXXXXXXXXXXXXXXX
STRIPE_PRICE_GROWTH_YEAR=price_XXXXXXXXXXXXXXXXXX
STRIPE_PRICE_BUSINESS=price_XXXXXXXXXXXXXXXXXX
STRIPE_PRICE_BUSINESS_YEAR=price_XXXXXXXXXXXXXXXXXX
```

---

## Why This Matters

### User Experience Impact

**Current Behavior:**
1. User visits www.levqor.ai/pricing
2. Sees "STARTER £29/month" ✅
3. Clicks "Get Starter"
4. Stripe checkout shows £19/month ⚠️ **MISMATCH**
5. User confusion / trust issues

**After Manual Update:**
1. User visits www.levqor.ai/pricing
2. Sees "STARTER £29/month" ✅
3. Clicks "Get Starter"
4. Stripe checkout shows £29/month ✅ **ALIGNED**
5. Smooth, professional experience

### Business Impact

- **Revenue Loss:** Every STARTER subscriber is paying £10/month less than intended (£120/year per subscriber)
- **Pricing Strategy:** STARTER at £19 undercuts the intended pricing tier structure
- **Trust & Credibility:** Mismatched pricing damages brand trust

---

## Verification Checklist

After manual Stripe updates, verify:

- [ ] Visit www.levqor.ai/pricing in incognito mode
- [ ] Click "Get Starter" (monthly)
- [ ] Confirm Stripe checkout shows £29.00
- [ ] Complete test purchase with test card
- [ ] Verify webhook creates subscription at £29/month
- [ ] Check `/api/stripe/check` endpoint shows £29 (2900 pence)
- [ ] Repeat for yearly plans

**Test Card:** `4242 4242 4242 4242` (any future date, any CVC)

---

## Technical Notes

### Pricing Architecture

**Frontend Display → Checkout API → Stripe Price IDs → Actual Charge**

1. **Frontend Display:** `pricing.ts` config (visual only, no payment impact)
2. **Checkout API:** Maps plan names to env var names
3. **Environment Variables:** Contain actual Stripe price IDs
4. **Stripe Prices:** Actual amounts charged to customers

**Example Flow:**
```
User clicks "Get Pro £49/month"
  ↓
Frontend sends {mode: "subscription", plan: "pro", term: "monthly"}
  ↓
Checkout API reads env.PRO_M (STRIPE_PRICE_PRO)
  ↓
Creates Stripe session with price_XXXXXXXX (£49 price)
  ↓
User pays £49.00 in Stripe
```

### Rate Limiting

Checkout API has built-in rate limiting:
- **Max:** 3 checkout attempts per user per 60 seconds
- **Purpose:** Prevents checkout spam and financial abuse
- **Impact:** None on normal usage

---

## Deployment Status

**Latest Git Commit:** 30aaded (deployed 2025-11-16 03:02:44 UTC)

**Frontend Changes (November 16, 2025):**
- ✅ pricing.ts updated (Pro £149→£49, Business £299→£149)
- ✅ FAQ page updated (subscription range £29-£149)
- ✅ How-it-works page updated (DFY Professional £299→£249)

**Backend:** No changes required (checkout API is env-var driven)

**Next Deployment:** Required after Stripe env var updates

---

## Contact & Support

**Owner Action Required:** Update Stripe prices manually in dashboard  
**Questions:** Check Launch Guard Status and Pre-Launch Snapshot docs  
**Emergency:** Contact support@levqor.ai or check owner handbook

---

## Appendix: Quick Reference

### Current Pricing Structure

**DFY (One-Time):**
- Starter: £99 (1 workflow, 48hr delivery, 7 days support)
- Professional: £249 (3 workflows, 3-4 days delivery, 14 days support)
- Enterprise: £599 (7 workflows, 7 days delivery, 30 days support)

**Subscriptions (Recurring):**
- Starter: £29/month or £290/year (1 workflow/month)
- Growth: £79/month or £790/year (3 workflows/month)
- Pro: £49/month or £490/year (5 workflows/month)
- Business: £149/month or £1,490/year (unlimited workflows)

**Add-ons:**
- Priority Support: TBD
- SLA 99.9%: TBD
- White Label: TBD

---

**End of Document**
