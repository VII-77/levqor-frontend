# 🚀 Day 2 Manual Tasks - Quick Action Card

**Total Time:** ~35 minutes  
**When:** Complete today (Nov 11, 2025) to stay on schedule

---

## 📋 **OPEN THESE 2 GUIDES:**

1. **2FA Guide:** `2FA-ENABLEMENT-GUIDE.md` (20 min)
2. **Cloudflare Guide:** `CLOUDFLARE-MANUAL-TASKS.md` (15 min)

---

## ⚡ **FASTEST PATH TO COMPLETION**

### **Option A: Sequential** (35 minutes)
```
1. Complete all 6 2FA setups (20 min)
2. Complete all 3 Cloudflare tasks (15 min)
3. Run verification commands
4. Report completion
```

### **Option B: Parallel** (20 minutes)
```
Open all tabs at once, work through simultaneously:
- Vercel 2FA + Cloudflare DNS proxy (5 min)
- GitHub 2FA + Cloudflare rate limit (5 min)  
- Stripe 2FA + Cloudflare cache rules (5 min)
- Neon + Replit + Cloudflare 2FA (5 min)
- Verification (5 min)
```

---

## 🔗 **DIRECT LINKS (Click to Open)**

### **2FA Links:**
1. Vercel: https://vercel.com/account/security
2. Cloudflare: https://dash.cloudflare.com/profile/authentication
3. Stripe: https://dashboard.stripe.com/settings/user
4. GitHub: https://github.com/settings/security
5. Neon: https://console.neon.tech/app/settings/profile
6. Replit: https://replit.com/account#security

### **Cloudflare Links:**
1. DNS: https://dash.cloudflare.com/ → levqor.ai → DNS
2. Rate Limiting: Same → Security → WAF → Rate limiting rules
3. Cache Rules: Same → Caching → Cache Rules

---

## ✅ **COMPLETION CHECKLIST**

### **2FA (6 platforms):**
```
☐ Vercel: 2FA Enabled + Backup codes saved
☐ Cloudflare: 2FA Enabled + Backup codes saved
☐ Stripe: 2FA Enabled + Backup codes saved
☐ GitHub: 2FA Enabled + Backup codes saved
☐ Neon: 2FA Enabled + Backup codes saved
☐ Replit: 2FA Enabled + Backup codes saved
```

### **Cloudflare (3 tasks):**
```
☐ DNS Proxy: Orange cloud enabled for levqor.ai + www
☐ Rate Limit: Rule created (100 req/min per IP on /api/*)
☐ Cache Rules: HTML bypass + /public/* cached
```

---

## 🔍 **VERIFICATION (Copy/Paste)**

After completing all tasks, run:

```bash
# Verify Cloudflare proxy active
curl -sI https://levqor.ai | grep cf-ray

# Verify cache rules working
curl -sI https://levqor.ai | grep cf-cache-status
curl -sI https://api.levqor.ai/public/metrics | grep cf-cache-status
curl -sI https://api.levqor.ai/public/metrics | grep cf-cache-status

# Verify 2FA (log out and back in to each platform)
echo "Test login to all 6 platforms - should require 6-digit code"
```

**Expected output:**
```
cf-ray: 8e3a2f1b4c5d6789-IAD ✅
cf-cache-status: DYNAMIC ✅
cf-cache-status: MISS ✅
cf-cache-status: HIT ✅
```

---

## 📝 **COMPLETION REPORT (Copy/Paste)**

Once verified, report:

```
✅ DAY 2 MANUAL TASKS COMPLETE

2FA Status:
✅ Vercel: 2FA Enabled
✅ Cloudflare: 2FA Enabled
✅ Stripe: 2FA Enabled
✅ GitHub: 2FA Enabled
✅ Neon: 2FA Enabled
✅ Replit: 2FA Enabled

Cloudflare Status:
✅ DNS Proxy: Active (cf-ray header confirmed)
✅ Rate Limiting: 100 req/min per IP on /api/*
✅ Cache Rules: HTML bypass + /public/* cached

Verification:
cf-ray: 8e3a2f1b4c5d6789-IAD ✅
HTML cache: BYPASS ✅
Public API: MISS → HIT ✅

Day 2 Status: 100% Complete
Ready for Day 3: ✅
```

---

## 📊 **WHAT THIS UNLOCKS**

After completion:
- 🔒 **Security:** All platforms protected with 2FA
- 🛡️ **Protection:** Cloudflare DDoS + rate limiting active
- ⚡ **Performance:** Intelligent caching reduces backend load
- ✅ **Day 2:** 60% → 100% complete
- 🚀 **Day 3:** Monitoring calibration unlocked

---

## 🎯 **REMEMBER:**

**2FA Backup Codes:**
- ⚠️ Download and save ALL backup codes
- 📁 Store in password manager or secure location
- ❌ DO NOT skip this step

**Cloudflare Verification:**
- ⏰ Wait 5-10 minutes after DNS proxy enable
- 🔄 May need to clear browser cache
- ✅ cf-ray header confirms proxy is active

---

**Start now. 35 minutes to Day 2 completion. Open both guides and work through systematically.** 🔥

**— Quick Reference, November 11, 2025**
