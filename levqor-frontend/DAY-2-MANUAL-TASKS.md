# 🔧 Day 2 Manual Tasks - Quick Action Guide

**Status:** 1/3 Complete  
**Completed:** ✅ Database Backup Test  
**Pending:** ⏳ Cloudflare Configuration, ⏳ 2FA Enablement  

---

## ✅ **COMPLETED: Database Backup Test**

**File:** `backups/2025-11/levqor-db-20251111-172532.sql.gz`  
**Size:** 3.2K  
**Checksum:** `86670017b1b813646a7b4b2593bae17291d79c1412cdd1c35fdf023bcb8967d4`  
**Tables:** 12 (all critical tables backed up)  
**Status:** ✅ PASS  

**Documented in:** `SECURITY-HARDENING-REPORT.md`

---

## ⏳ **PENDING: Cloudflare Configuration**

### **Quick Setup (15 minutes):**

1. **Login to Cloudflare Dashboard** → Select `levqor.ai` zone

2. **SSL/TLS Settings** (`SSL/TLS` → `Overview`)
   ```
   Encryption Mode: Full (strict)
   Minimum TLS: 1.2
   TLS 1.3: Enabled
   Always Use HTTPS: On
   ```

3. **WAF Rules** (`Security` → `WAF` → `Managed Rules`)
   ```
   ☑ Cloudflare Managed Ruleset
   ☑ Cloudflare OWASP Core Ruleset
   Security Level: Medium
   ```

4. **Rate Limiting** (`Security` → `WAF` → `Rate Limiting Rules`)
   ```
   Click "Create rule"
   
   Rule name: API Rate Limit
   
   If incoming requests match:
     Field: URI Path
     Operator: contains
     Value: /api/
   
   Then:
     Choose action: Challenge
     Requests: 100
     Period: 1 minute
     Duration: 60 seconds
   
   Click "Deploy"
   ```

5. **Cache Rules** (`Caching` → `Cache Rules`)
   ```
   Click "Create rule"
   
   Rule 1: Bypass HTML Cache
     When incoming requests match:
       Field: Content Type
       Operator: contains
       Value: text/html
     Then:
       Cache eligibility: Bypass cache
     
   Click "Save"
   
   Rule 2: Cache Public API
     When incoming requests match:
       Field: URI Path
       Operator: starts with
       Value: /public/
     Then:
       Cache eligibility: Eligible
       Edge Cache TTL: 5 minutes
       
   Click "Save"
   ```

### **Verification:**
```bash
# Run these commands after configuration:

# 1. Check Cloudflare active
curl -sI https://levqor.ai | grep -i "cf-cache-status\|cf-ray"

# 2. Verify HTML bypass
curl -sI https://levqor.ai | grep "cf-cache-status"
# Expected: DYNAMIC or BYPASS

# 3. Copy full output for documentation
curl -sI https://levqor.ai
```

**Time Required:** ~15 minutes  
**Document:** Copy `cf-cache-status` output to `SECURITY-HARDENING-REPORT.md`

---

## ⏳ **PENDING: 2FA Enablement (6 Platforms)**

### **Quick Checklist:**

For each platform below:
1. Login → Navigate to Security settings
2. Enable Two-Factor Authentication
3. Scan QR code with authenticator app (Authy, Google Authenticator, 1Password)
4. Save backup codes securely
5. Test login (should require password + 2FA code)

---

### **Platform 1: Vercel**
```
URL: https://vercel.com/account/security
Navigate: Settings → Security → Two-Factor Authentication
Method: Authenticator App (recommended)
Time: 3 minutes

Steps:
1. Click "Enable Two-Factor Authentication"
2. Scan QR code with authenticator app
3. Enter 6-digit code to verify
4. Download backup codes
5. Test: Logout and login (should require 2FA)
```

---

### **Platform 2: Cloudflare**
```
URL: https://dash.cloudflare.com/profile/authentication
Navigate: My Profile → Authentication
Method: Authenticator App
Time: 3 minutes

Steps:
1. Click "Enable" under Two-Factor Authentication
2. Scan QR code
3. Enter verification code
4. Save backup codes
5. Review API tokens (revoke unused)
```

---

### **Platform 3: Stripe**
```
URL: https://dashboard.stripe.com/settings/team
Navigate: Settings → Team → Security
Method: Authenticator App
Time: 3 minutes

Steps:
1. Your profile → Security → Two-factor authentication
2. Add authentication app
3. Scan QR code
4. Enter verification code
5. Save recovery codes
6. Review team members (remove inactive)
```

---

### **Platform 4: GitHub**
```
URL: https://github.com/settings/security
Navigate: Settings → Password and authentication
Method: Authenticator App
Time: 3 minutes

Steps:
1. Two-factor authentication → Enable
2. Set up using an app
3. Scan QR code
4. Enter verification code
5. Download recovery codes
6. Audit: SSH keys, Personal Access Tokens
```

---

### **Platform 5: Neon (Database)**
```
URL: https://console.neon.tech/app/settings/profile
Navigate: Settings → Profile
Method: Authenticator App
Time: 3 minutes

Steps:
1. Account Security → Enable 2FA
2. Scan QR code
3. Enter verification code
4. Save recovery codes
5. Check: Database password age
   - If > 90 days, rotate password
```

---

### **Platform 6: Replit**
```
URL: https://replit.com/account
Navigate: Account → Security
Method: Authenticator App
Time: 3 minutes

Steps:
1. Security → Two-Factor Authentication
2. Enable 2FA
3. Scan QR code
4. Enter verification code
5. Save recovery codes
6. Review: API tokens, collaborators
```

---

## 📝 **Documentation Template**

After completing 2FA on all platforms, add this to `SECURITY-HARDENING-REPORT.md`:

```markdown
### 2FA Enablement Results

**Completion Date:** [DATE] [TIME] UTC

**Platforms:**
- Vercel: ✅ Enabled ([DATE])
- Cloudflare: ✅ Enabled ([DATE])
- Stripe: ✅ Enabled ([DATE])
- GitHub: ✅ Enabled ([DATE])
- Neon: ✅ Enabled ([DATE])
- Replit: ✅ Enabled ([DATE])

**Backup Codes:** ✅ Downloaded and stored securely
**Test Logins:** ✅ All platforms require 2FA

**API Keys Rotated:**
- [List any keys rotated]

**Users Removed:**
- [List any inactive users removed]

**Status:** ✅ COMPLETE
```

---

## ⏱️ **Time Estimate:**

```
Cloudflare Configuration:  15 minutes
2FA Enablement (6 platforms): 20 minutes
Documentation: 5 minutes
-----------------------------------
Total: ~40 minutes
```

---

## ✅ **Completion Checklist:**

```
☐ Cloudflare TLS → Full (strict)
☐ Cloudflare WAF → Managed Rules ON
☐ Cloudflare Rate Limit → API 100/min
☐ Cloudflare Cache → HTML bypass
☐ Verify: curl -sI https://levqor.ai | grep cf-cache-status
☐ Vercel 2FA → Enabled
☐ Cloudflare 2FA → Enabled
☐ Stripe 2FA → Enabled
☐ GitHub 2FA → Enabled
☐ Neon 2FA → Enabled
☐ Replit 2FA → Enabled
☐ Document results in SECURITY-HARDENING-REPORT.md
```

---

## 🚀 **After Completion:**

**Report back with:**
1. Cloudflare verification output:
   ```bash
   curl -sI https://levqor.ai | grep -i "cf-cache-status\|cf-ray"
   ```

2. 2FA completion confirmation:
   ```
   All 6 platforms enabled: [YES/NO]
   Backup codes saved: [YES/NO]
   ```

3. Any keys rotated or users removed

**Then:** Ready for Day 3 Monitoring Calibration 🎯

---

**Quick reference guide for completing Day 2 manual tasks. Estimated 40 minutes total.** ⚡
