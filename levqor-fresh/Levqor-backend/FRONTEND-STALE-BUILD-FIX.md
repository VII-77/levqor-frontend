# Frontend Serving Stale Build - IMMEDIATE FIX

**Issue:** Vercel Root Directory is set to wrong path: `~/workspace/levqor-site/levqor-site`  
**Should be:** `levqor-site`

---

## OPTION 1: Fix Vercel Settings (2 minutes - RECOMMENDED)

**Step 1: Update Root Directory**
1. Go to: https://vercel.com/vii-77s-projects/levqor-site/settings
2. Find: **Root Directory** setting
3. Current value: `~/workspace/levqor-site/levqor-site` ❌
4. Change to: `levqor-site` ✅
5. Click: **Save**

**Step 2: Trigger Redeploy**
1. Go to: https://vercel.com/vii-77s-projects/levqor-site/deployments
2. Find: Latest deployment (top of list)
3. Click: **⋯ (three dots)** → **Redeploy**
4. Select: **Use existing Build Cache** ❌ (uncheck this!)
5. Click: **Redeploy**

**Result:** Fresh build in ~2 minutes

---

## OPTION 2: Force Instant Redeploy (30 seconds)

If you just want to force a fresh deploy without fixing the path:

1. Go to: https://vercel.com/vii-77s-projects/levqor-site/deployments
2. Click: **⋯ (three dots)** next to latest deployment
3. Click: **Redeploy**
4. **IMPORTANT:** Uncheck "Use existing Build Cache"
5. Click: **Redeploy**

---

## VERIFICATION (After Redeploy)

```bash
# Wait 2 minutes, then test:
curl -sI https://levqor.ai | grep -E "x-vercel-cache|age:"
```

**Expected:**
```
age: 0
x-vercel-cache: MISS
```

**Current HTML test:**
```bash
curl -s https://levqor.ai | grep "<title>"
```

Should show fresh Next.js content.

---

## WHY THIS HAPPENED

Vercel's Root Directory setting points to:
```
~/workspace/levqor-site/levqor-site  (WRONG - double path)
```

Should be:
```
levqor-site  (CORRECT)
```

This causes Vercel to look in the wrong directory for builds.

---

## FASTEST FIX RIGHT NOW

1. **Vercel Dashboard** → https://vercel.com/vii-77s-projects/levqor-site/deployments
2. **Click the ⋯ menu** on the latest deployment
3. **Redeploy** with **"Use existing Build Cache" UNCHECKED**
4. **Wait 90 seconds**
5. **Test:** `curl -s https://levqor.ai | head -30`

---

**After fixing, all future deploys will serve fresh builds.**
