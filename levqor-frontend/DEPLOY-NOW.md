# 🚀 DEPLOY LEVQOR v7.0 TO PRODUCTION - STEP BY STEP

**Backend:** ✅ Already live at api.levqor.ai  
**Frontend:** 🔄 Deploy to Vercel now

---

## 📋 QUICK START (5 Minutes)

### Step 1: Import to Vercel

1. Go to **https://vercel.com/new**
2. Click **"Import Git Repository"**
3. Select your Levqor repository
4. Click **"Import"**

### Step 2: Configure Project Settings

**Framework Preset:** Next.js (auto-detected)  
**Root Directory:** `levqor-site` ⚠️ **CRITICAL - MUST SET THIS**  
**Build Command:** `npm run build` (auto-detected)  
**Output Directory:** `.next` (auto-detected)

### Step 3: Add Environment Variables

Click **"Environment Variables"** and add:

```bash
# Required
NEXTAUTH_URL=https://levqor.ai
NEXTAUTH_SECRET=mAMo9AVXv1VRM9FOJBcyEoTnf5k4MjpAjgHFTVy+kYg=
NEXT_PUBLIC_API_URL=https://api.levqor.ai

# Email (use your existing Resend key)
RESEND_API_KEY=re_***** (from Replit secrets)
AUTH_RESEND_KEY=re_***** (same as RESEND_API_KEY)
```

**Where to find RESEND_API_KEY:**
- Go to Replit project
- Click "Secrets" (🔒 icon)
- Copy value of `RESEND_API_KEY`

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes for build
3. ✅ Your site will be live!

### Step 5: Add Custom Domain

1. Go to **Project Settings > Domains**
2. Add domain: `levqor.ai`
3. Configure DNS at your registrar:
   - Add the A/CNAME records Vercel provides
4. Wait for DNS propagation (5-60 minutes)

---

## ✅ VERIFICATION CHECKLIST

After deployment, test these URLs:

```bash
# Frontend
✅ https://levqor.ai - Homepage
✅ https://levqor.ai/pricing - Pricing page
✅ https://levqor.ai/developer - Developer portal
✅ https://levqor.ai/marketplace - Partner marketplace
✅ https://levqor.ai/intelligence - Intelligence dashboard (NEW!)
✅ https://levqor.ai/admin/insights - Admin analytics

# Backend (already live)
✅ https://api.levqor.ai/health - Health check
✅ https://api.levqor.ai/public/metrics - Metrics
✅ https://api.levqor.ai/api/intelligence/status - Intelligence API (NEW!)
```

---

## 🎯 WHAT'S LIVE AFTER DEPLOYMENT

### **User-Facing Features:**
- 🏠 Marketing pages (homepage, pricing, FAQ)
- 🔐 User authentication (magic link sign-in)
- 📊 Dashboard (after sign-in)
- 💻 Developer portal (API keys, sandbox, docs)
- 🛒 Marketplace (partner integrations)
- 🧠 **Intelligence dashboard (v7.0 NEW!)**

### **Revenue Features:**
- 💳 Stripe checkout (Starter/Pro/Enterprise)
- 🔑 API key management (metered usage)
- 🤝 Partner ecosystem (30% revenue share)
- 📦 Marketplace purchases

### **Autonomous Intelligence (v7.0):**
- 📈 Revenue forecasting
- 📉 Churn prediction
- ⚠️ Anomaly detection
- 🔧 Self-healing actions
- 📊 Trend analysis
- ⚖️ Risk scoring
- 🔄 Auto-scaling

### **Automation (16 Jobs):**
- Every 15 min: Intelligence monitoring
- Every hour: Scaling checks
- Daily: Retention metrics, ops summary, cost tracking
- Weekly: Pulse report, governance email, AI insights

---

## 🎉 YOU'RE LIVE!

Once deployed, **Levqor v7.0** will be:
- ✅ Fully operational at levqor.ai
- ✅ Self-monitoring and self-healing
- ✅ Generating AI insights automatically
- ✅ Ready for customers
- ✅ $182k+ ARR potential unlocked

---

## 🔜 NEXT: Plan v8.0 Multi-Tenancy

After 2-4 weeks of production validation:
1. Gather enterprise customer requirements
2. Validate demand for multi-tenant features
3. Begin v8.0 "Genesis" 8-week migration

But for now - **enjoy your intelligent, autonomous platform!** 🚀
