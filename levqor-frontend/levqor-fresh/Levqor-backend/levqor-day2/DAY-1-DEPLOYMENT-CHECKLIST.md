# ✅ Day 1 Deployment Checklist

**Status:** READY FOR DEPLOYMENT  
**Risk Level:** 🟢 LOW  
**Estimated Time:** 15 minutes  

---

## 🎯 **QUICK START**

### **1. Deploy Frontend (5 min)**
```bash
cd levqor-site
git add src/app/layout.tsx
git commit -m "fix: force dynamic rendering to prevent HTML caching"
git push origin main

# Wait 2-3 minutes for Vercel deployment
# Verify
curl -I https://levqor.ai | grep -E 'age|cache-control|x-vercel-cache'
```

**Expected:** `age: 0`, `cache-control: no-store`, `x-vercel-cache: MISS`

---

### **2. Deploy Backend (5 min)**
**In Replit UI:**
1. Click "Publish" button
2. Select "Re-publish to Autoscale"
3. Wait for deployment (60 seconds)

**Verify:**
```bash
curl -s -H "X-Request-ID: test-$(date +%s)" \
  https://api.levqor.ai/api/intelligence/status | jq .
```

**Expected:**
```json
{
  "ok": true,
  "meta": {
    "correlation_id": "test-1762879xxx",
    "duration_ms": 45,
    "timestamp": "2025-11-11T17:00:00.000Z"
  }
}
```

---

### **3. Run Daily Burn-In Checks (5 min)**
```bash
# Go/No-Go Dashboard
python3 scripts/monitoring/notion_go_nogo_dashboard.py

# Platform Metrics
curl https://api.levqor.ai/public/metrics | jq .

# Recent Logs
grep "synthetic\|alert\|ERROR" /tmp/logs/levqor-backend_*.log | tail -50
```

---

## 📊 **SUCCESS CRITERIA**

### **Frontend:**
- ✅ HTML age: 0 seconds
- ✅ No HIT cache entries
- ✅ Fresh content on every page load

### **Backend:**
- ✅ All 5 intelligence endpoints return structured JSON
- ✅ Correlation IDs present in responses
- ✅ Performance timing (duration_ms) tracked
- ✅ No increase in error rate

### **Burn-In Metrics:**
- ✅ Error rate: ≤ 0.5%
- ✅ P1 incidents: 0
- ✅ Daily cost: ≤ $10
- ✅ Uptime: 99.98%+

---

## 🚨 **ROLLBACK PLAN**

### **Frontend Rollback:**
```bash
cd levqor-site
git revert HEAD
git push origin main
```

### **Backend Rollback:**
- Replit UI → Deployments → Previous deployment → Activate

---

## 📅 **DAILY ROUTINE (Days 2-7)**

**Every morning at 09:00 UTC:**
1. Run Go/No-Go dashboard
2. Check platform metrics
3. Review synthetic check results
4. Grep logs for errors
5. Update daily log entry

**Track Progress:**
- Day 1: 1/7 days complete
- Day 2: 2/7 days complete
- ...
- Day 7: Go/No-Go review complete
- Day 8 (Nov 24): Final decision meeting

---

## 📝 **DEPLOYMENT LOG**

```
[TIMESTAMP] Frontend deployed to Vercel
  Commit: [SHA]
  Deployment ID: [VERCEL_ID]
  Verification: [PASS/FAIL]

[TIMESTAMP] Backend deployed to Autoscale
  Deployment ID: [REPLIT_ID]
  Verification: [PASS/FAIL]
  Sample response: [JSON]
```

---

**All fixes staged and tested. Ready for deployment.** 🚀
