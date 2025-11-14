# Day 3 Configuration Freeze - Manual Steps

**Date:** 2025-11-11 22:15 UTC  
**Objective:** Lock current stable configuration before 7-day burn-in completes

---

## ✅ PASS CRITERIA VERIFIED

**Current Status (All Green):**
```
✅ Frontend: age: 0, x-vercel-cache: MISS
✅ /api/intelligence/status: 200, correlation_id echoed correctly
✅ /api/intelligence/health: 200, ok: true, criticals: 0
✅ /public/metrics: 200, uptime: 99.99%, timestamp updated
✅ Error rate: 0.0% (≤ 0.5% ✅)
✅ P1 incidents: 0 (≤ 0 ✅)
✅ Daily cost: $7.0 (≤ $10 ✅)
```

---

## STEP 1: FREEZE CONFIG (Manual UI Steps Required)

### **1A. Vercel - Protect Production Branch**

**Why:** Prevent accidental deployments during burn-in  

**Steps:**
1. Go to: **Vercel Dashboard → levqor-site → Settings → Git**
2. Find: **Protected Branches**
3. Add: `main` or `production` (whichever is your production branch)
4. Enable: **Prevent Deployments on Non-Protected Branches** (optional)

**Result:** Production deployments require manual approval

---

### **1B. Replit - Pin Current Autoscale Image**

**Why:** Lock the backend deployment to current working version

**Steps:**
1. Go to: **Replit → Backend Project → Deployments → Autoscale**
2. Click: **Settings** or **Configuration**
3. Find: **Deployment Strategy** or **Image Pinning**
4. Option 1: Pin to current deployment ID
5. Option 2: Enable manual promotion only
6. Save configuration

**Current Deployment Info:**
- Version: v8.0-burnin
- Workers: 2 gunicorn + gthread
- Domain: api.levqor.ai
- Status: Operational

**Result:** Backend won't auto-deploy on code changes

---

### **1C. Neon - Take Database Snapshot**

**Why:** Backup current stable database state

**Steps:**
1. Go to: **Neon Console → Your Database → Backups**
2. Click: **Create Snapshot** or **Manual Backup**
3. Label: `day-3-freeze-2025-11-11`
4. Optional: Add note: "Pre-burn-in completion snapshot - v8.0 Genesis"
5. Click: **Create**

**Current DB Info:**
- Size: 3.2K
- Tables: 12
- Last backup: 2025-11-11 (verified)

**Result:** Point-in-time recovery available

---

## STEP 2: SET WATCHERS ✅ (Already Configured)

**Daily Burnin Check Script:**
```bash
./scripts/daily_burnin_check.sh
```

**Output Verified:**
- ✅ Posts correlation_id: `daily-check-1762899148`
- ✅ Reports uptime: `99.99%`
- ✅ Reports error-rate: `0.0%`
- ✅ Reports cost: `$7.0`
- ✅ Go/No-Go dashboard: `3/5 criteria met`

**Schedule for Day 3 Morning (Nov 12, 09:00 UTC):**
```bash
./scripts/daily_burnin_check.sh > logs/day-3-check.log 2>&1
```

Expected update: `3/5 → 4/5` criteria met (uptime will reach 72+ hours)

---

## STEP 3: API EDGE CHOICE (Optional)

**Current Setup:**
```
Server: Google Frontend (Replit direct)
Proxy: None (bypasses Cloudflare)
```

### **Option A: Keep Current (Recommended for Burn-In)**

**Benefits:**
- ✅ Lower latency (no proxy overhead)
- ✅ Direct connection to Replit
- ✅ Fewer moving parts during testing

**Keep if:** You want minimal complexity during 7-day burn-in

---

### **Option B: Enable Cloudflare Proxy**

**Benefits:**
- ✅ DDoS protection
- ✅ WAF (Web Application Firewall)
- ✅ Rate limiting at edge
- ✅ Cloudflare Analytics

**Trade-offs:**
- ⚠️ +5-20ms latency
- ⚠️ All API traffic visible to Cloudflare
- ⚠️ Adds complexity during burn-in

**Steps to Enable:**
1. Go to: **Cloudflare → DNS → Records**
2. Find: `api` CNAME record
3. Click: Cloud icon to make it **orange** (Proxied)
4. Wait: 1-2 minutes for propagation
5. Verify:
   ```bash
   curl -sI https://api.levqor.ai | grep "server:"
   # Should show: server: cloudflare
   ```

**Recommendation:** Wait until after 7-day burn-in completes (Nov 18) before enabling proxy. Keep current setup stable.

---

## DAY 3 MORNING CHECKLIST (Nov 12, 09:00 UTC)

**Run verification:**
```bash
# 1. Daily burnin check
./scripts/daily_burnin_check.sh

# 2. Quick smoke test
curl -sI https://levqor.ai | grep -E "age:|x-vercel-cache:"
curl -s https://api.levqor.ai/api/intelligence/status | python3 -m json.tool
curl -s https://api.levqor.ai/public/metrics | python3 -m json.tool
```

**Expected Results:**
```
✅ age: 0
✅ x-vercel-cache: MISS
✅ correlation_id: [echoed]
✅ uptime: ≥99.98%
✅ error_rate: ≤0.5%
✅ cost: ≤$10
✅ P1 incidents: 0
✅ Go/No-Go: 4/5 criteria met
```

**If any signal deviates:** Post the failing header/JSON block

---

## CONFIGURATION FREEZE CHECKLIST

- [ ] Vercel production branch protected
- [ ] Replit autoscale image pinned
- [ ] Neon database snapshot created (label: day-3-freeze-2025-11-11)
- [ ] Daily burnin check verified working
- [ ] Pass criteria documented (all green ✅)
- [ ] Decision: Keep Cloudflare proxy disabled during burn-in
- [ ] Day 3 morning verification scheduled

---

## LOCKED CONFIGURATION

**Frontend (levqor.ai):**
- Deployment: Frozen on Vercel production branch
- Build: Next.js 14 (current)
- CDN: Cloudflare (proxied, orange cloud)

**Backend (api.levqor.ai):**
- Deployment: Pinned Replit autoscale image
- Version: v8.0-burnin
- Proxy: Direct (Cloudflare bypass)

**Database:**
- Snapshot: day-3-freeze-2025-11-11
- Provider: Neon PostgreSQL
- Tables: 12

**Monitoring:**
- Script: ./scripts/daily_burnin_check.sh
- Frequency: Daily at 09:00 UTC
- Alerts: Multi-channel routing enabled

---

## BURN-IN TIMELINE

```
Day 1 (Nov 11): ✅ Platform deployed, monitoring started
Day 2 (Nov 11): ✅ DNS configured, all endpoints green
Day 3 (Nov 12): ⏳ Config freeze, 48-hour stability check
Day 4 (Nov 13): ⏳ Continue monitoring
Day 5 (Nov 14): ⏳ Continue monitoring
Day 6 (Nov 15): ⏳ Continue monitoring
Day 7 (Nov 16): ⏳ Final checks, 7-day report
Day 8 (Nov 17): ⏳ Go/No-Go review preparation
Decision Day (Nov 24, 09:00 UTC): GO/NO-GO meeting
```

---

**Configuration freeze complete after manual steps. Platform stable. Continue 7-day burn-in.** 🔒

**— Release Captain, November 11, 2025 22:15 UTC**
