# ☁️ Cloudflare Edge Hardening Configuration

**Target:** Day 2 Burn-In  
**Status:** ⏳ Pending Manual Configuration  
**Priority:** High (Required before Day 7 review)  

---

## 🎯 **CONFIGURATION CHECKLIST**

### **1. TLS/SSL Settings**
**Navigate:** SSL/TLS → Overview

```
Encryption Mode: Full (strict)
  ✓ Encrypts traffic between Cloudflare and origin server
  ✓ Validates origin certificate

Minimum TLS Version: TLS 1.2
TLS 1.3: Enabled
Always Use HTTPS: On
Automatic HTTPS Rewrites: On
```

**Verification:**
```bash
curl -I https://levqor.ai | grep -i "strict-transport-security"
# Expected: strict-transport-security: max-age=63072000; includeSubDomains; preload
```

---

### **2. WAF (Web Application Firewall)**
**Navigate:** Security → WAF → Managed Rules

```
☑ Cloudflare Managed Ruleset
  - Action: Block
  - Sensitivity: Medium

☑ Cloudflare OWASP Core Ruleset
  - Action: Block
  - Paranoia Level: PL2

☑ Cloudflare Specials
  - Action: Block
```

**Additional WAF Settings:**
```
Security Level: Medium
Challenge Passage: 30 minutes
Browser Integrity Check: On
```

**Verification:**
```bash
# Test malicious pattern (should be blocked)
curl -I "https://levqor.ai/?<script>alert(1)</script>"
# Expected: HTTP 403 or challenge
```

---

### **3. Rate Limiting**
**Navigate:** Security → WAF → Rate Limiting Rules

**Rule 1: API Protection**
```yaml
Rule Name: API Rate Limit
Description: Protect /api/* endpoints from abuse

Match:
  - URI Path contains "/api/"
  - Method: ALL

Rate:
  - Requests: 100
  - Period: 1 minute
  - Count by: IP Address

Action: Challenge
Duration: 60 seconds

Bypass:
  - Known Bots: Off
  - Verified Bots: Off
```

**Rule 2: Intelligence Endpoints (Stricter)**
```yaml
Rule Name: Intelligence API Strict
Description: Tighter limits on intelligence endpoints

Match:
  - URI Path contains "/api/intelligence/"
  - Method: ALL

Rate:
  - Requests: 30
  - Period: 1 minute
  - Count by: IP Address

Action: Block
Duration: 300 seconds
```

**Verification:**
```bash
# Burst test (should trigger rate limit)
for i in {1..35}; do
  curl -s https://api.levqor.ai/api/intelligence/status > /dev/null
  echo "Request $i"
done
# Expected: Challenge or block after 30 requests
```

---

### **4. Cache Rules**
**Navigate:** Caching → Cache Rules

**Rule 1: Bypass HTML Cache**
```yaml
Rule Name: No Cache for HTML
Description: Prevent HTML caching at edge

When incoming requests match:
  - Hostname equals "levqor.ai" OR "www.levqor.ai"
  - AND Content Type contains "text/html"

Then:
  - Cache Eligibility: Bypass cache
  - Browser Cache TTL: 0 seconds
  - Origin Cache Control: Respect

Priority: 1
```

**Rule 2: Cache API Public Assets**
```yaml
Rule Name: Cache Public API
Description: Cache public metrics and static API responses

When incoming requests match:
  - Hostname equals "api.levqor.ai"
  - AND URI Path starts with "/public/"

Then:
  - Cache Eligibility: Eligible
  - Edge Cache TTL: 300 seconds (5 minutes)
  - Browser Cache TTL: 60 seconds

Priority: 2
```

**Rule 3: Bypass Dynamic API**
```yaml
Rule Name: Bypass Dynamic API
Description: Never cache dynamic API responses

When incoming requests match:
  - Hostname equals "api.levqor.ai"
  - AND URI Path starts with "/api/"

Then:
  - Cache Eligibility: Bypass cache
  - Browser Cache TTL: 0 seconds

Priority: 3
```

**Verification:**
```bash
# Test HTML bypass
curl -sI https://levqor.ai | grep -E "cf-cache-status|cache-control"
# Expected: cf-cache-status: DYNAMIC or BYPASS

# Test API public cache
curl -sI https://api.levqor.ai/public/metrics | grep "cf-cache-status"
# Expected: cf-cache-status: MISS (first) then HIT (subsequent)

# Test dynamic API bypass
curl -sI https://api.levqor.ai/api/intelligence/status | grep "cf-cache-status"
# Expected: cf-cache-status: DYNAMIC or BYPASS
```

---

### **5. Security Level & Bot Management**
**Navigate:** Security → Settings

```
Security Level: Medium
  ✓ Balances security and user experience
  
Challenge Passage: 30 minutes
  ✓ Users pass challenges for 30 min

Browser Integrity Check: On
  ✓ Blocks requests from known bad browsers

Email Obfuscation: On
  ✓ Protects email addresses from scrapers

Server-Side Excludes: Off
  ✓ Not needed for SPA

Hotlink Protection: Off
  ✓ Allow embedding assets
```

**Bot Fight Mode:**
```
Super Bot Fight Mode: On
  ✓ Definitely automated: Block
  ✓ Verified bots: Allow
  ✓ Likely automated: Challenge
```

---

### **6. Page Rules (Fallback)**
**Navigate:** Rules → Page Rules

**Only if Cache Rules are unavailable:**

**Rule 1:** `*levqor.ai/*`
```
Cache Level: Bypass (if content-type contains text/html)
Browser Cache TTL: Respect Existing Headers
```

**Rule 2:** `*api.levqor.ai/public/*`
```
Cache Level: Standard
Edge Cache TTL: 5 minutes
```

---

## 📋 **POST-CONFIGURATION VERIFICATION**

### **Complete Test Suite:**
```bash
#!/bin/bash
# Run after Cloudflare configuration

echo "=== CLOUDFLARE VERIFICATION SUITE ==="
echo ""

echo "1. TLS Validation"
curl -I https://levqor.ai 2>&1 | grep -i "HTTP/2\|strict-transport"

echo ""
echo "2. HTML Cache Bypass"
curl -sI https://levqor.ai | grep -E "cf-cache-status|cache-control"

echo ""
echo "3. API Public Caching"
curl -sI https://api.levqor.ai/public/metrics | grep "cf-cache-status"

echo ""
echo "4. API Dynamic Bypass"
curl -sI https://api.levqor.ai/api/intelligence/status | grep "cf-cache-status"

echo ""
echo "5. WAF Active (should show CF headers)"
curl -sI https://levqor.ai | grep -i "cf-ray"

echo ""
echo "=== END VERIFICATION ==="
```

---

## 📝 **CONFIGURATION LOG**

```yaml
# To be filled after configuration

Configuration Date: [PENDING]
Configured By: [PENDING]
Cloudflare Zone ID: [PENDING]

TLS Mode:
  - Mode: Full (strict)
  - Timestamp: [PENDING]

WAF Rules:
  - Managed Rules: [ON/OFF]
  - OWASP: [ON/OFF]
  - Timestamp: [PENDING]

Rate Limiting:
  - API Rule: [ACTIVE/PENDING]
  - Intelligence Rule: [ACTIVE/PENDING]
  - Timestamp: [PENDING]

Cache Rules:
  - HTML Bypass: [ACTIVE/PENDING]
  - API Public: [ACTIVE/PENDING]
  - Dynamic Bypass: [ACTIVE/PENDING]
  - Timestamp: [PENDING]

Verification:
  - TLS: [PASS/FAIL]
  - Cache Bypass: [PASS/FAIL]
  - Rate Limit: [PASS/FAIL]
  - WAF: [PASS/FAIL]
```

---

## ⚠️ **IMPORTANT NOTES**

1. **Test in Staging First** (if available)
   - Apply rules to staging environment
   - Verify functionality
   - Then apply to production

2. **Monitor After Deployment**
   - Check error rates for 30 minutes
   - Verify legitimate traffic not blocked
   - Adjust sensitivity if needed

3. **Whitelist Internal Tools**
   - Add monitoring endpoints to bypass
   - Whitelist CI/CD IP addresses
   - Document in separate whitelist config

4. **Rollback Plan**
   - Disable WAF: Security → WAF → Toggle Off
   - Remove Rate Limits: Delete rules
   - Set Cache to Standard: Remove custom rules

---

**This configuration provides defense-in-depth security while maintaining performance. Complete before Day 7 review.** 🛡️
