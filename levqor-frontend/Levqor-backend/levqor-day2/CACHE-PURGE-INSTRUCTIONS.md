# 🔧 Cache Purge Instructions

**Issue:** levqor.ai apex domain still serving old cache  
**Status:** www.levqor.ai working ✅ | levqor.ai cached ❌  

---

## ✅ **QUICK FIX: Vercel Dashboard** (30 seconds)

### **Steps:**
1. Open: https://vercel.com/dashboard
2. Click on your **levqor-site** project
3. Go to **"Deployments"** tab
4. Find the **most recent deployment** (top of list)
5. Click the **"..."** menu (3 dots on right)
6. Select **"Invalidate Cache"**

**Result:** Cache will be purged within 30 seconds globally.

---

## 🔄 **ALTERNATIVE: Wait for Natural Expiry**

The cache will clear automatically, typically within **15-30 minutes** of deployment.

Current cache age: **16.7 hours** (very old, from previous deployment)

---

## ✅ **VERIFICATION**

After purging, run:
```bash
curl -I https://levqor.ai | grep -E 'age|cache-control|x-vercel-cache'
```

**Expected:**
```
age: 0
cache-control: private, no-cache, no-store, max-age=0, must-revalidate
x-vercel-cache: MISS
```

---

## 📊 **CURRENT STATUS**

```
Domain            | Age    | Cache    | Status
------------------|--------|----------|--------
www.levqor.ai     | 0      | MISS     | ✅ WORKING
levqor.ai         | 60532  | HIT      | ❌ CACHED
```

---

## 🚀 **NEXT: DEPLOY BACKEND**

While frontend cache clears, proceed with backend deployment:

**In Replit UI:**
1. Click **"Publish"** button
2. Select **"Re-publish to Autoscale"**
3. Wait 60 seconds

**Verify:**
```bash
curl -H "X-Request-ID: test" https://api.levqor.ai/api/intelligence/status | jq .
```

**Expected:** Should see `meta.correlation_id` and `meta.duration_ms`

---

**Dashboard purge is the fastest option. Takes 30 seconds.** 🚀
