# Vercel Cleanup Guide for Levqor

## 🎯 Current Status
Based on code analysis, here's what's **actually needed** vs what can be removed.

---

## ✅ KEEP THESE - Production Environment Variables

### Authentication (4 required)
```
NEXTAUTH_SECRET          ← Essential for NextAuth
NEXTAUTH_URL             ← Essential for NextAuth (https://www.levqor.ai)
RESEND_API_KEY           ← Essential for email (magic links, marketing)
AUTH_FROM_EMAIL          ← Email sender address
```

### Backend Integration (2 required)
```
NEXT_PUBLIC_API_URL      ← Backend API endpoint (Production)
INTERNAL_API_SECRET      ← For webhook → backend auth
```

### Stripe - Core (3 required)
```
STRIPE_SECRET_KEY        ← Essential for all Stripe operations
STRIPE_WEBHOOK_SECRET    ← Essential for webhook verification (Production)
SITE_URL                 ← Used in checkout redirects (https://levqor.ai)
```

### Stripe - Subscription Price IDs (6 required)
```
STRIPE_PRICE_STARTER          ← Monthly subscription
STRIPE_PRICE_STARTER_YEAR     ← Annual subscription
STRIPE_PRICE_PRO              ← Monthly subscription
STRIPE_PRICE_PRO_YEAR         ← Annual subscription
STRIPE_PRICE_BUSINESS         ← Monthly subscription
STRIPE_PRICE_BUSINESS_YEAR    ← Annual subscription
```

### Stripe - Add-on Price IDs (3 optional but recommended)
```
STRIPE_PRICE_ADDON_PRIORITY_SUPPORT  ← Add-on
STRIPE_PRICE_ADDON_SLA_99_9          ← Add-on
STRIPE_PRICE_ADDON_WHITE_LABEL       ← Add-on
```

**Total Essential Production Variables: 18**

---

## 🔵 PREVIEW ENVIRONMENT ONLY

These are ONLY in Preview environment (not Production):

```
STRIPE_PRICE_DFY_STARTER           ← Preview only
STRIPE_PRICE_DFY_PROFESSIONAL      ← Preview only
STRIPE_PRICE_DFY_ENTERPRISE        ← Preview only
STRIPE_PRICE_GROWTH                ← Preview only
STRIPE_PRICE_GROWTH_YEAR           ← Preview only
STRIPE_WEBHOOK_SECRET (Preview)    ← Different webhook secret for testing
NEXTAUTH_SECRET (Preview)          ← Can use different secret for testing
```

**Action:** Keep these in Preview environment for testing, but they're not needed in Production.

---

## ❌ SAFE TO REMOVE (Not Used in Code)

These environment variables are NOT referenced anywhere in the codebase:

### OAuth Variables (Not Implemented)
```
GOOGLE_CLIENT_ID          ← Code has fallback to ""
GOOGLE_CLIENT_SECRET      ← Code has fallback to ""
MICROSOFT_CLIENT_ID       ← Code has fallback to ""
MICROSOFT_CLIENT_SECRET   ← Code has fallback to ""
```

**Why:** OAuth login is not fully implemented. Code defaults to empty strings.

### Other Variables
```
FREE_TRIAL_DAYS           ← Only visible in Production, not used in frontend
JWT_SECRET                ← Duplicate of NEXTAUTH_SECRET
```

---

## 🧹 CLEANUP ACTIONS

### 1. Remove Failed Deployments
**Go to:** https://vercel.com/vii-77s-projects/levqor-site/deployments
- Failed deployments auto-delete after 30 days
- No manual action needed unless you want to clear them now

### 2. Remove Unused Environment Variables

**Production Environment:**
Keep only the 18 essential variables listed above.

**To remove OAuth variables (if not using):**
1. Go to: https://vercel.com/vii-77s-projects/levqor-site/settings/environment-variables
2. Delete:
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`
   - `MICROSOFT_CLIENT_ID`
   - `MICROSOFT_CLIENT_SECRET`
   - `JWT_SECRET` (duplicate of NEXTAUTH_SECRET)

### 3. Verify Essential Variables

**Double-check these are set in Production:**
```bash
✓ NEXTAUTH_SECRET
✓ NEXTAUTH_URL (https://www.levqor.ai)
✓ NEXT_PUBLIC_API_URL (your backend URL)
✓ STRIPE_SECRET_KEY
✓ STRIPE_WEBHOOK_SECRET (Production)
✓ RESEND_API_KEY
✓ AUTH_FROM_EMAIL
✓ SITE_URL (https://levqor.ai)
✓ All 9 STRIPE_PRICE_* variables
```

### 4. Optimize Build Settings

**Current settings (KEEP AS IS):**
```
Framework: Next.js
Build Command: npm run build
Output Directory: .next
Root Directory: levqor-site
Node.js Version: 22.x
```

**Build optimization settings:**
- On-Demand Concurrent Builds: Disabled (keep disabled unless needed)
- Build Machine: Standard performance (sufficient)
- Skip deployments when no changes: Disabled (keep disabled for now)

### 5. Enable Auto-Deploy (IMPORTANT)

**Go to:** https://vercel.com/vii-77s-projects/levqor-site/settings/git

**Verify:**
- ✅ Git Integration: Connected to `VII-77/levqor-frontend`
- ✅ Production Branch: `main`
- ✅ Auto-deploy: ENABLED

**If auto-deploy is disabled, enable it** so future git pushes automatically trigger deployments.

---

## 📊 BEFORE vs AFTER

### Before Cleanup:
- **Environment Variables:** ~25+ variables (many unused)
- **Failed Deployments:** 10+ failed builds
- **Auto-deploy:** Possibly disabled

### After Cleanup:
- **Environment Variables:** 18 essential (Production) + 7 preview-only
- **Failed Deployments:** Auto-removed after 30 days
- **Auto-deploy:** Enabled for seamless updates

---

## 🚀 NEXT STEPS

1. **Manual redeploy** (one-time action):
   - Go to: https://vercel.com/vii-77s-projects/levqor-site/deployments
   - Click "Redeploy" on the latest deployment
   - This will pick up the `cookies.ts` file from GitHub

2. **After successful deployment:**
   - Remove unused OAuth environment variables
   - Enable auto-deploy if disabled

3. **Going forward:**
   - Git push → Auto-deploy (no manual action needed)
   - Monitor deployments for any issues
   - Only add new env vars when actually needed in code

---

## 💡 TIPS

- **Don't delete Stripe price IDs** even if some tiers aren't visible - they're needed for checkout
- **Keep Preview environment separate** - use it for testing new features
- **Auto-deploy saves time** - enable it to avoid manual redeployments
- **Failed deployments are normal** - they auto-clean after 30 days

---

## ✅ VERIFICATION CHECKLIST

After cleanup, verify:
- [ ] Production has 18 essential environment variables
- [ ] Auto-deploy is enabled
- [ ] Latest deployment succeeded
- [ ] New pages work: `/my-data`, `/dfy-contract`, `/cookie-settings`
- [ ] Checkout flow works with Stripe
- [ ] Email sending works (magic links)
- [ ] Backend API calls work
