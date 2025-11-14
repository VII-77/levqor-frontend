# ☁️ Cloudflare Manual Configuration - Quick Reference

**Time Required:** 15 minutes  
**Status:** TLS/WAF configured ✅ | DNS/Rate/Cache pending ⏳

---

## 🎯 **WHAT'S ALREADY DONE** (No Action Needed)

Via automated API configuration:
- ✅ SSL Mode: Full (strict)
- ✅ Minimum TLS: 1.2
- ✅ TLS 1.3: Enabled
- ✅ Always Use HTTPS: On
- ✅ Security Level: Medium
- ✅ Browser Integrity Check: Enabled
- ✅ Challenge TTL: 30 minutes

---

## ⏳ **TASK 1: ENABLE DNS PROXY** (~5 minutes)

**Direct Link:** https://dash.cloudflare.com/

### Steps:
1. Click link above and log in
2. Click on `levqor.ai` zone
3. Click **"DNS"** in left sidebar
4. Find these records:
   - `levqor.ai` (A or CNAME record)
   - `www.levqor.ai` (CNAME record)
5. For each record:
   - Click the cloud icon (currently gray)
   - It should turn **orange** (Proxied)
6. Wait 5-10 minutes for DNS propagation

### Verification:
```bash
curl -sI https://levqor.ai | grep cf-ray
```

**Expected output:**
```
cf-ray: 8e3a2f1b4c5d6789-IAD
```

**If no cf-ray header:** Wait another 5 minutes and check again.

---

## ⏳ **TASK 2: CREATE RATE LIMITING RULE** (~5 minutes)

**Direct Link:** https://dash.cloudflare.com/

### Steps:
1. Click link and navigate to `levqor.ai` zone
2. Click **"Security"** → **"WAF"** → **"Rate limiting rules"**
3. Click **"Create rule"**

**Rule Configuration:**

```
Rule Name: API Rate Limit

Expression Builder:
  Field: URI Path
  Operator: contains
  Value: /api/

Characteristics:
  ☑ IP Address

Rate:
  Requests: 100
  Period: 60 seconds

Action:
  Block

Mitigation timeout: 300 seconds (5 minutes)
```

4. Click **"Deploy"**

### Verification:
```bash
# Should block after 100 requests in 60 seconds
for i in {1..105}; do 
  curl -s https://api.levqor.ai/api/intelligence/status > /dev/null
  echo "Request $i"
done
```

**Expected:** Requests 101-105 should return 429 (rate limited)

---

## ⏳ **TASK 3: CREATE CACHE RULES** (~5 minutes)

**Direct Link:** https://dash.cloudflare.com/

### Steps:
1. Navigate to `levqor.ai` zone
2. Click **"Caching"** → **"Cache Rules"**
3. Create **TWO** rules:

---

### **Rule 1: Bypass HTML Cache**

Click **"Create rule"**

```
Rule Name: Bypass HTML Cache

When incoming requests match:
  Field: Content Type
  Operator: contains
  Value: text/html

Then:
  Cache eligibility: Bypass cache
```

Click **"Deploy"**

---

### **Rule 2: Cache Public API**

Click **"Create rule"** again

```
Rule Name: Cache Public API

When incoming requests match:
  Field: URI Path
  Operator: starts with
  Value: /public/

Then:
  Cache eligibility: Eligible for cache
  
  Edge TTL:
    Status Code: All
    Duration: 300 seconds (5 minutes)
  
  Browser TTL:
    Duration: 60 seconds (1 minute)
```

Click **"Deploy"**

---

### Cache Rules Verification:

**Test HTML bypass:**
```bash
curl -sI https://levqor.ai | grep cf-cache-status
# Expected: DYNAMIC or BYPASS
```

**Test public API cache:**
```bash
# First request (miss)
curl -sI https://api.levqor.ai/public/metrics | grep cf-cache-status
# Expected: MISS

# Second request (hit)
curl -sI https://api.levqor.ai/public/metrics | grep cf-cache-status
# Expected: HIT
```

---

## ✅ **COMPLETION CHECKLIST**

```
Task 1: DNS Proxy
  ☐ levqor.ai proxied (orange cloud) ✅
  ☐ www.levqor.ai proxied (orange cloud) ✅
  ☐ cf-ray header present ✅

Task 2: Rate Limiting
  ☐ Rule created: API Rate Limit ✅
  ☐ Expression: /api/* ✅
  ☐ Limit: 100 req/min per IP ✅
  ☐ Action: Block ✅

Task 3: Cache Rules
  ☐ Rule 1: Bypass HTML cache ✅
  ☐ Rule 2: Cache /public/* (5 min) ✅
  ☐ Verified HTML shows BYPASS ✅
  ☐ Verified /public/ shows MISS then HIT ✅
```

---

## 🔍 **FINAL VERIFICATION**

Run all verification commands together:

```bash
echo "=== DNS PROXY CHECK ==="
curl -sI https://levqor.ai | grep -iE "cf-ray|cf-cache-status"

echo ""
echo "=== HTML CACHE CHECK ==="
curl -sI https://levqor.ai | grep cf-cache-status

echo ""
echo "=== PUBLIC API CACHE CHECK (First request - MISS) ==="
curl -sI https://api.levqor.ai/public/metrics | grep cf-cache-status

echo ""
echo "=== PUBLIC API CACHE CHECK (Second request - HIT) ==="
curl -sI https://api.levqor.ai/public/metrics | grep cf-cache-status

echo ""
echo "=== RATE LIMIT CHECK (Should block after 100) ==="
for i in {1..105}; do 
  status=$(curl -s -o /dev/null -w "%{http_code}" https://api.levqor.ai/api/intelligence/status)
  if [ "$status" == "429" ]; then
    echo "✅ Request $i: Rate limited (429)"
  else
    echo "Request $i: OK ($status)"
  fi
done
```

**Expected Output:**
```
=== DNS PROXY CHECK ===
cf-ray: 8e3a2f1b4c5d6789-IAD
cf-cache-status: DYNAMIC

=== HTML CACHE CHECK ===
cf-cache-status: DYNAMIC

=== PUBLIC API CACHE CHECK (First request - MISS) ===
cf-cache-status: MISS

=== PUBLIC API CACHE CHECK (Second request - HIT) ===
cf-cache-status: HIT

=== RATE LIMIT CHECK ===
Request 1: OK (200)
...
Request 100: OK (200)
✅ Request 101: Rate limited (429)
✅ Request 102: Rate limited (429)
...
```

---

## 📊 **WHAT THIS ACHIEVES**

**DNS Proxy (Orange Cloud):**
- Traffic flows through Cloudflare's edge network
- DDoS protection active
- WAF rules apply
- Analytics available

**Rate Limiting:**
- Prevents API abuse
- Blocks excessive requests (>100/min per IP)
- Protects backend from overload

**Cache Rules:**
- HTML always fresh (no stale content)
- Public API cached for 5 minutes (reduces backend load)
- Faster response times for public endpoints

---

## 🚨 **TROUBLESHOOTING**

**No cf-ray header after DNS proxy:**
- Wait 10-15 minutes (DNS propagation)
- Clear browser cache
- Try incognito/private browsing
- Check DNS: `dig levqor.ai` should show Cloudflare IPs

**Rate limiting not working:**
- Check rule is **deployed** (not draft)
- Verify expression matches `/api/` exactly
- Wait 2-3 minutes after creation

**Cache always shows MISS:**
- Check rule order (HTML bypass should be first)
- Verify URI path matches exactly
- Try different endpoint: `/public/health` or `/public/metrics`
- Wait 2-3 minutes after rule creation

---

## 🎯 **TIME TRACKING**

```
Start time: __:__
Task 1 (DNS Proxy): __:__ (__ min)
Task 2 (Rate Limit): __:__ (__ min)
Task 3 (Cache Rules): __:__ (__ min)
Verification: __:__ (__ min)
End time: __:__ (Total: __ min)
```

**Estimated:** 15 minutes  
**Actual:** ___ minutes

---

## ✅ **COMPLETION REPORT**

After all tasks complete, report:

```
✅ Cloudflare Configuration Complete

DNS Proxy: ✅ Active (cf-ray header present)
Rate Limiting: ✅ 100 req/min per IP on /api/*
Cache Rules: ✅ HTML bypass + /public/* cached

Verification:
- cf-ray: 8e3a2f1b4c5d6789-IAD ✅
- HTML cache: BYPASS ✅
- Public API: MISS → HIT ✅
- Rate limit: 429 after 100 requests ✅

Cloudflare Status: 100% Complete
```

---

**Quick start: Open Cloudflare dashboard, complete 3 tasks, run verification. Takes 15 minutes total.** ☁️

**— Configuration Guide, November 11, 2025**
