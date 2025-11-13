# 🚀 Pricing v2.1 Deployment Guide

## ✅ What's Been Implemented

### **Complete Two-Tier Pricing System**

**Features:**
- ✨ Monthly/Yearly toggle with visual state
- 💰 **Starter Plan**: £19/mo or £190/yr (2 months free)
- 🔥 **Pro Plan**: £49/mo or £490/yr (2 months free) - "Most Popular" badge
- 📊 Comparison blurb showing exact savings
- 🏷️ Promo code support at checkout
- 🌍 Automatic VAT calculation
- ❓ Built-in FAQ section

**Technical:**
- Stripe Checkout API with session management
- Success redirect to `/thanks`
- Cancel returns to `/pricing`
- Automatic tax calculation
- Promotion code support

---

## 🔧 Required Configuration (One-Time Setup)

### Step 1: Create Stripe Products & Prices

You need to create **4 price IDs** in Stripe:

#### In Stripe Dashboard: https://dashboard.stripe.com/products

**1. Levqor Starter - Monthly**
   - Product Name: `Levqor Starter`
   - Description: `1 project, email support, basic insights`
   - Pricing: **Recurring**
   - Amount: `£19 GBP`
   - Billing Period: `Monthly`
   - Save → Copy **Price ID** → Add as `STRIPE_PRICE_STARTER`

**2. Levqor Starter - Yearly**
   - Same product as above, add new price
   - Amount: `£190 GBP` (2 months free: 19×10 instead of 19×12)
   - Billing Period: `Yearly`
   - Save → Copy **Price ID** → Add as `STRIPE_PRICE_STARTER_YEAR`

**3. Levqor Pro - Monthly**
   - Product Name: `Levqor Pro`
   - Description: `Unlimited projects, priority support, advanced insights + runbooks`
   - Pricing: **Recurring**
   - Amount: `£49 GBP`
   - Billing Period: `Monthly`
   - Save → Copy **Price ID** → Add as `STRIPE_PRICE_PRO`

**4. Levqor Pro - Yearly**
   - Same product as above, add new price
   - Amount: `£490 GBP` (2 months free: 49×10 instead of 49×12)
   - Billing Period: `Yearly`
   - Save → Copy **Price ID** → Add as `STRIPE_PRICE_PRO_YEAR`

---

### Step 2: Add Secrets to Replit

In **Tools → Secrets**, add these **6 environment variables**:

```bash
# Already configured ✓
STRIPE_SECRET_KEY=sk_...          # Already exists
STRIPE_WEBHOOK_SECRET=whsec_...   # Already exists

# New - Add these 4 price IDs:
STRIPE_PRICE_STARTER=price_xxxxx         # Monthly £19
STRIPE_PRICE_PRO=price_xxxxx             # Monthly £49
STRIPE_PRICE_STARTER_YEAR=price_xxxxx    # Yearly £190
STRIPE_PRICE_PRO_YEAR=price_xxxxx        # Yearly £490

# Site URL
SITE_URL=https://levqor.ai
```

---

### Step 3: Add Same Secrets to Vercel

**After deployment**, add these to Vercel:

1. Go to: https://vercel.com/your-project/settings/environment-variables
2. Add all 6 secrets:
   - `STRIPE_SECRET_KEY`
   - `STRIPE_PRICE_STARTER`
   - `STRIPE_PRICE_PRO`
   - `STRIPE_PRICE_STARTER_YEAR`
   - `STRIPE_PRICE_PRO_YEAR`
   - `SITE_URL`
3. Apply to: **Production**, **Preview**, **Development**
4. Redeploy after adding secrets

---

## 📦 Deploy to Vercel

Once all secrets are added:

```bash
# Clean any git locks
rm -f .git/index.lock || true

# Stage all pricing changes
git add levqor-site/.env.example \
        levqor-site/src/app/pricing/page.tsx \
        levqor-site/src/app/api/checkout/route.ts \
        levqor-site/package.json \
        levqor-site/package-lock.json

# Commit with descriptive message
git commit -m "Pricing v2.1: monthly+yearly toggle, comparison blurb, VAT notes, FAQ"

# Push to deploy (Vercel auto-deploys from main branch)
git push origin main
```

**Wait 2-3 minutes** for Vercel to build and deploy.

---

## ✅ Testing Checklist

After deployment (≈3 minutes):

### 1. **Visit Pricing Page**
```bash
curl -I https://levqor.ai/pricing | grep "HTTP"
# Expected: HTTP/2 200
```

### 2. **Test Monthly Plan**
- Visit: https://levqor.ai/pricing
- Ensure "Monthly" is selected (default)
- Click "Buy now" on Starter (should show £19)
- Should redirect to Stripe Checkout
- URL should contain: `plan=starter&term=monthly`

### 3. **Test Yearly Plan**
- Toggle to "Yearly"
- Verify prices change: Starter £190, Pro £490
- Verify green "2 months free" message appears
- Click "Buy now" on Pro (should show £490)
- URL should contain: `plan=pro&term=yearly`

### 4. **Test Stripe Checkout**
Use Stripe test card if in test mode:
- Card: `4242 4242 4242 4242`
- Expiry: Any future date
- CVC: Any 3 digits
- Complete checkout
- Should redirect to: `https://levqor.ai/thanks`

### 5. **Verify Promo Codes**
- At Stripe Checkout, look for "Add promotion code" link
- Enter any valid promo code from your Stripe dashboard
- Verify discount applies

---

## 📊 Pricing Structure Summary

| Plan | Monthly | Yearly | Savings |
|------|---------|--------|---------|
| **Starter** | £19/mo | £190/yr | £38/yr (2 months free) |
| **Pro** | £49/mo | £490/yr | £98/yr (2 months free) |

**Monthly Total per Year:**
- Starter: £228/yr (19×12)
- Pro: £588/yr (49×12)

**Yearly Savings:**
- Starter: £38/yr saved (17% discount)
- Pro: £98/yr saved (17% discount)

---

## 🎨 UX Features

✅ **Monthly/Yearly Toggle** - Clear visual state with black background
✅ **Comparison Blurb** - Shows exact savings calculation
✅ **Most Popular Badge** - Pro plan highlighted
✅ **VAT Notice** - Transparent about tax calculations
✅ **Promo Code Hint** - Guides users to enter codes at checkout
✅ **FAQ Section** - Answers common questions (plan switching, refunds)
✅ **Responsive Design** - Works on mobile and desktop

---

## 🔍 Troubleshooting

**Error: "Unknown plan/term"**
→ Check that all 4 price IDs are set in Vercel environment variables

**Checkout doesn't redirect**
→ Verify `SITE_URL` is set correctly (no trailing slash)

**Prices don't toggle**
→ Clear browser cache or hard refresh (Cmd+Shift+R / Ctrl+Shift+R)

**VAT not calculating**
→ Ensure `automatic_tax: { enabled: true }` in checkout route (already configured)

**Promo codes not working**
→ Verify `allow_promotion_codes: true` in checkout route (already configured)

---

## 📁 Files Changed

```
levqor-site/
├── .env.example                       # Added Stripe price IDs
├── src/app/
│   ├── api/checkout/route.ts (1.4KB)  # Monthly/yearly support
│   └── pricing/page.tsx (4.1KB)       # Full v2.1 with toggle, blurb, FAQ
└── package.json                        # stripe@19.3.0

Backend:
✅ api.levqor.ai/billing/health → healthy: true
✅ api.levqor.ai/status → pass
```

---

## 🚀 Go Live

1. ✅ Create 4 Stripe prices (see Step 1)
2. ✅ Add 6 secrets to Replit (see Step 2)
3. ✅ Run git commands above
4. ✅ Add 6 secrets to Vercel (see Step 3)
5. ✅ Test with checklist above
6. ✅ Monitor Vercel deployment logs

**Your pricing page will be live at:** https://levqor.ai/pricing 🎉
