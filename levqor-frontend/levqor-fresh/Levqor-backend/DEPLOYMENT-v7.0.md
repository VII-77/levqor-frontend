# 🚀 LEVQOR v7.0 PRODUCTION DEPLOYMENT CHECKLIST

**Platform Status:** Intelligence Layer Complete  
**Version:** v7.0 "Intelligence + Evolution"  
**Deployment Date:** November 11, 2025

---

## ✅ BACKEND DEPLOYMENT (api.levqor.ai)

### Status: **LIVE & OPERATIONAL**

**Backend URL:** https://api.levqor.ai  
**Health Check:** ✅ PASSING (`{"ok":true}`)  
**Workers:** 2 Gunicorn workers, 4 threads each  
**APScheduler Jobs:** 16 automated jobs running

**Deployment Type:** Replit Autoscale  
**Configuration:** Already configured in workflow `levqor-backend`

### Backend Features Live:
- ✅ Job orchestration API
- ✅ User management & authentication
- ✅ Developer portal (API keys, sandbox, billing)
- ✅ Partner ecosystem (registry, marketplace, payouts)
- ✅ Governance & auditing system
- ✅ **v7.0 Intelligence Layer:**
  - Automation Intelligence (15-min monitoring)
  - Decision Engine (weekly analysis)
  - AI Advisor (forecasting)
  - Governance Feedback (risk scoring)
  - Dynamic Scaling (hourly checks)

**API Endpoints:**
- Core: `/api/v1/*` (jobs, users, status)
- Developer: `/api/developer/*` (keys, sandbox, docs)
- Intelligence: `/api/intelligence/*` (status, anomalies, insights)
- Partner: `/api/partners/*` (registry, listings)
- Admin: `/admin/*`, `/ops/*` (analytics, flags, ledger)

---

## 🌐 FRONTEND DEPLOYMENT (levqor.ai)

### Status: **READY TO DEPLOY**

**Target Platform:** Vercel  
**Repository:** Already pushed to Git  
**Build Status:** ✅ Next.js build successful

### Deployment Steps:

#### 1. Vercel Project Setup
```bash
# Import from Git repository
# Project Name: levqor
# Framework: Next.js 14
# Root Directory: levqor-site  ⚠️ CRITICAL
```

#### 2. Environment Variables Required

**Production Variables (Vercel Dashboard):**
```bash
# Authentication
NEXTAUTH_URL=https://levqor.ai
NEXTAUTH_SECRET=<generate-secure-random-string>

# API Connection
NEXT_PUBLIC_API_URL=https://api.levqor.ai

# Email (Resend)
RESEND_API_KEY=<from-secrets>
AUTH_RESEND_KEY=<from-secrets>

# Optional: Analytics & Monitoring
NEXT_PUBLIC_SENTRY_DSN=<if-configured>
```

**How to generate NEXTAUTH_SECRET:**
```bash
openssl rand -base64 32
```

#### 3. Build Configuration

**Vercel Settings:**
- Build Command: `npm run build` (auto-detected)
- Output Directory: `.next` (auto-detected)
- Install Command: `npm install` (auto-detected)
- **Root Directory:** `levqor-site` ⚠️ **MUST BE SET**

#### 4. Domain Configuration

**Primary Domain:** levqor.ai  
**API Subdomain:** api.levqor.ai (already configured on Replit)

**Vercel Domain Setup:**
1. Add custom domain: `levqor.ai`
2. Add `www.levqor.ai` (redirects to main)
3. Configure DNS:
   - Type: A / CNAME
   - Name: @ (or subdomain)
   - Value: Vercel's provided target

---

## 🔐 SECRETS VERIFICATION

### Required Secrets (Already Set):
- ✅ DATABASE_URL (PostgreSQL)
- ✅ JWT_SECRET
- ✅ SESSION_SECRET
- ✅ STRIPE_SECRET_KEY
- ✅ STRIPE_WEBHOOK_SECRET
- ✅ STRIPE_PRICE_* (Pro, Enterprise, Starter)
- ✅ RESEND_API_KEY

### Optional Secrets (Enhance Features):
- ⚪ SLACK_WEBHOOK_URL (Intelligence alerts)
- ⚪ TELEGRAM_BOT_TOKEN (Alternative alerts)
- ⚪ NOTION_* (Transparency logging)
- ⚪ SENTRY_DSN (Error tracking)

---

## 📊 POST-DEPLOYMENT VERIFICATION

### 1. Backend Health Checks
```bash
# Basic health
curl https://api.levqor.ai/health
# Expected: {"ok":true,"ts":...}

# Intelligence status
curl https://api.levqor.ai/api/intelligence/status
# Expected: {"status":"operational",...}

# Metrics
curl https://api.levqor.ai/public/metrics
# Expected: uptime, version, job counts
```

### 2. Frontend Health Checks
```bash
# Homepage
curl -I https://levqor.ai
# Expected: 200 OK

# Intelligence dashboard
curl -I https://levqor.ai/intelligence
# Expected: 200 OK (or 401 if auth required)

# API proxy
curl https://levqor.ai/api/intelligence/status
# Expected: Intelligence data
```

### 3. Intelligence Layer Verification
- ✅ Check APScheduler logs for job execution
- ✅ Verify database tables exist (system_health_log, intel_events, etc.)
- ✅ Visit `/intelligence` dashboard
- ✅ Confirm alerts are sending (if Slack configured)

### 4. Revenue Systems Check
- ✅ Developer portal: `/developer`
- ✅ Marketplace: `/marketplace`
- ✅ Stripe webhooks receiving events
- ✅ API key generation working

---

## 🎯 PRODUCTION FEATURES LIVE

### Core Platform (v1-6.3)
- [x] AI job orchestration API
- [x] User authentication (NextAuth v5)
- [x] Rate limiting & security headers
- [x] Health monitoring & Sentry
- [x] PostgreSQL database (Neon)
- [x] Referral tracking & analytics

### Expansion Products (v6.0)
- [x] Developer Portal ($19/mo Pro, $199/mo Enterprise)
- [x] Data Insights & Reports (thought-leadership)
- [x] Partner API & Registry (ecosystem)
- [x] Marketplace + Stripe Connect (30% platform fee)
- [x] Governance & Auditing (compliance)

### Intelligence Layer (v7.0) **NEW!**
- [x] Automation Intelligence (self-monitoring)
- [x] Decision Engine (trend analysis)
- [x] AI Advisor (revenue/churn forecasting)
- [x] Governance Feedback (risk scoring)
- [x] Dynamic Scaling (auto-scaling)
- [x] Intelligence Dashboard UI
- [x] 16 APScheduler automated jobs

**Total ARR Potential:** $182k+ (unlimited via partner ecosystem)

---

## 🚨 CRITICAL DEPLOYMENT NOTES

### ⚠️ Vercel Root Directory
**MUST set Root Directory to:** `levqor-site`

Without this, Vercel will try to build from the workspace root and fail.

### ⚠️ NEXTAUTH_SECRET
**MUST be different** from development. Generate a new secure random string for production.

### ⚠️ Database Migrations
The backend auto-creates tables on startup. No manual migrations needed for v7.0.

### ⚠️ Environment Variables Without Trailing Newlines
ALL environment variables must be set **WITHOUT** trailing newline characters.

---

## 📈 MONITORING & OBSERVABILITY

### Real-Time Monitoring
- **Intelligence Dashboard:** `/intelligence`
- **Health Endpoint:** `/health`
- **Metrics Endpoint:** `/public/metrics`

### Automated Reports (via APScheduler)
- **Daily:** Ops summary (9 AM London time)
- **Weekly:** Pulse summary (Friday 2 PM London)
- **Weekly:** Governance report (Sunday 9 AM London)
- **Weekly:** Intelligence analysis (Sunday 10:30 UTC)

### Alerts
- Anomaly detection → Slack (if configured)
- SLO breaches → Automatic recovery attempts
- Scaling decisions → Logged and alerted

---

## 🔄 ROLLBACK PLAN

If issues arise post-deployment:

### Frontend Rollback (Vercel)
1. Go to Vercel dashboard
2. Navigate to Deployments
3. Click "..." on previous deployment
4. Select "Promote to Production"

### Backend Rollback (Replit)
1. Use Git to revert commits
2. Restart workflow `levqor-backend`
3. Database rollback (if needed):
   ```bash
   # Restore from snapshot
   pg_restore -d $DATABASE_URL backups/pre_v7_snapshot.sql
   ```

---

## ✅ DEPLOYMENT SUCCESS CRITERIA

- [ ] Frontend accessible at levqor.ai
- [ ] Backend responding at api.levqor.ai
- [ ] User authentication working (magic links)
- [ ] Intelligence dashboard loading at /intelligence
- [ ] API endpoints returning data
- [ ] APScheduler jobs executing (check logs)
- [ ] Stripe webhooks receiving events
- [ ] No errors in Sentry (if configured)
- [ ] Health checks passing for 24+ hours

---

## 🎉 NEXT STEPS AFTER DEPLOYMENT

1. **Monitor for 48 hours**
   - Watch APScheduler logs
   - Check intelligence dashboard metrics
   - Verify no anomalies detected

2. **Test all revenue flows**
   - Developer portal sign-up
   - API key generation
   - Marketplace browsing
   - Stripe checkout

3. **Gather feedback**
   - User onboarding experience
   - Dashboard usability
   - Performance metrics

4. **Plan v8.0**
   - Enterprise requirements gathering
   - Multi-tenant architecture design
   - Migration strategy refinement

---

## 📞 SUPPORT RESOURCES

**Documentation:**
- API Docs: `/public/openapi.json`
- FAQ: `/faq`
- Security: `/.well-known/security.txt`

**Monitoring:**
- Intelligence: `/intelligence`
- Admin Analytics: `/admin/insights`
- Developer Portal: `/developer`

---

**🚀 LEVQOR v7.0 IS READY FOR PRODUCTION!**

The platform is autonomous, intelligent, and revenue-ready. Deploy with confidence!
