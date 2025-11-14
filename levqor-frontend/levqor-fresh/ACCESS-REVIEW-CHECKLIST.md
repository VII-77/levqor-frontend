# 🔐 Access Control + 2FA Review Checklist

**Target:** Day 2 Burn-In  
**Frequency:** Initial setup + quarterly review  
**Priority:** High (Security Hardening)  

---

## ✅ **2FA ENABLEMENT CHECKLIST**

### **1. Vercel**
**Navigate:** Settings → Security

```
☐ Two-Factor Authentication: ENABLED
  - Method: Authenticator App (recommended)
  - Backup codes: Downloaded and stored securely
  
☐ Security Log: Reviewed for suspicious activity
☐ Sessions: Active sessions reviewed, unknown devices removed

Verification:
  - Login attempt without 2FA code: Should be blocked
  - Backup code test: Verify one backup code works
```

**Status:** [ ] Completed  
**Date:** ___________  
**Verified By:** ___________  

---

### **2. Cloudflare**
**Navigate:** My Profile → Authentication

```
☐ Two-Factor Authentication: ENABLED
  - Method: Authenticator App (recommended)
  - Backup codes: Downloaded and stored securely
  
☐ API Tokens: Reviewed, unused tokens revoked
☐ Active Sessions: Reviewed, unknown devices removed
☐ Security Events: Reviewed for anomalies

Verification:
  - Login requires: Password + 2FA code
  - API token scope: Limited to necessary permissions only
```

**Status:** [ ] Completed  
**Date:** ___________  
**Verified By:** ___________  

---

### **3. Stripe**
**Navigate:** Settings → Team → Security

```
☐ Two-Factor Authentication: ENABLED
  - Method: Authenticator App (recommended)
  - SMS backup: Optional (less secure)
  
☐ Team Members: Reviewed, inactive users removed
☐ API Keys: Reviewed, test keys rotated
☐ Webhooks: Verified all endpoints using HTTPS
☐ Webhook Signing Secret: Rotated if > 90 days old

Verification:
  - Dashboard login requires 2FA
  - API keys: Test vs Live properly segregated
  - Webhook endpoints: Only levqor.ai domains
```

**Status:** [ ] Completed  
**Date:** ___________  
**Verified By:** ___________  

---

### **4. GitHub / Git Provider**
**Navigate:** Settings → Password and authentication

```
☐ Two-Factor Authentication: ENABLED
  - Method: Authenticator App (recommended)
  - Hardware key: Optional (Yubikey for critical repos)
  - Backup codes: Downloaded and stored
  
☐ SSH Keys: Reviewed, unused keys removed
☐ Personal Access Tokens: Reviewed, unused tokens revoked
☐ Authorized Applications: Reviewed, revoked unused OAuth apps
☐ Security Log: Reviewed for suspicious pushes

Repository-Specific:
☐ Branch Protection: main branch requires PR + reviews
☐ Signed Commits: Enforced (optional but recommended)
☐ Deploy Keys: Reviewed, read-only where possible

Verification:
  - Push to main: Should require PR approval
  - Git operations: Require 2FA or SSH key
```

**Status:** [ ] Completed  
**Date:** ___________  
**Verified By:** ___________  

---

### **5. Database (Neon / PostgreSQL)**
**Navigate:** Neon Dashboard → Settings

```
☐ Account 2FA: ENABLED
☐ Database Passwords: Rotated if > 90 days
☐ IP Allowlist: Configured (if available)
☐ Connection Pooling: Enabled with auth
☐ Branch Protection: Main branch restricted

Database User Audit:
☐ Admin users: Only 1-2 trusted accounts
☐ Read-only users: For analytics/reporting
☐ Application user: Least privilege (no DROP/ALTER)

Verification:
  - Connection string uses TLS (sslmode=require)
  - Password complexity: Strong (20+ characters)
  - No plaintext passwords in code
```

**Status:** [ ] Completed  
**Date:** ___________  
**Verified By:** ___________  

---

### **6. Replit**
**Navigate:** Account → Security

```
☐ Two-Factor Authentication: ENABLED
  - Method: Authenticator App
  
☐ API Tokens: Reviewed, unused tokens revoked
☐ Secrets: Reviewed, no exposed credentials
☐ Collaborators: Reviewed, removed inactive users

Deployment-Specific:
☐ Autoscale deployment: Protected (requires auth to redeploy)
☐ Environment variables: All secrets use Secrets pane
☐ .env files: In .gitignore (never committed)

Verification:
  - Repl access requires 2FA login
  - Secrets visible only to authorized users
```

**Status:** [ ] Completed  
**Date:** ___________  
**Verified By:** ___________  

---

## 🔑 **API KEY & SECRET AUDIT**

### **Key Rotation Policy**
```
Rotate every 90 days:
☐ Stripe API Keys (test + live)
☐ Vercel API Tokens
☐ Cloudflare API Tokens
☐ GitHub Personal Access Tokens
☐ Database Passwords
☐ JWT Secrets
☐ Session Secrets
☐ Admin Tokens
```

### **Audit Spreadsheet Template**

| Service | Key Type | Created Date | Last Rotated | Age (days) | Status | Action |
|---------|----------|--------------|--------------|------------|--------|--------|
| Stripe | Secret Key (Live) | 2025-01-15 | 2025-01-15 | 300 | ⚠️ OLD | Rotate |
| Stripe | Secret Key (Test) | 2025-01-15 | 2025-01-15 | 300 | ⚠️ OLD | Rotate |
| Vercel | Deploy Token | 2025-03-01 | 2025-03-01 | 255 | ⚠️ OLD | Rotate |
| GitHub | PAT (Deployments) | 2025-10-01 | 2025-10-01 | 41 | ✅ OK | Monitor |
| Neon | DB Password | 2025-09-01 | 2025-09-01 | 71 | ✅ OK | Monitor |
| JWT | Secret | 2025-11-01 | 2025-11-01 | 10 | ✅ OK | Monitor |

**Rotation Procedure:**
1. Generate new key in service dashboard
2. Update Replit Secrets pane
3. Restart backend workflow
4. Verify new key works
5. Delete old key
6. Update audit spreadsheet

---

## 👥 **USER ACCESS REVIEW**

### **Team Members**
```
Review across all platforms:
☐ Vercel: ___ users, ___ removed
☐ Cloudflare: ___ users, ___ removed
☐ Stripe: ___ users, ___ removed
☐ GitHub: ___ collaborators, ___ removed
☐ Neon: ___ users, ___ removed

Criteria for removal:
- Inactive > 90 days
- Left organization
- Changed role (no longer needs access)
- Contractor engagement ended
```

### **Role-Based Access**
```
Principle: Least Privilege

Admin Access (Full control):
☐ List: ___________
☐ Justified: Yes/No

Developer Access (Deploy + Read):
☐ List: ___________
☐ Justified: Yes/No

Read-Only Access (Monitoring):
☐ List: ___________
☐ Justified: Yes/No

Revoked:
☐ List: ___________
☐ Date: ___________
```

---

## 🔍 **SESSION & DEVICE REVIEW**

### **Active Sessions Audit**
```
For each platform, review active sessions:

Vercel:
☐ Known devices: ___
☐ Unknown devices removed: ___

GitHub:
☐ Known devices: ___
☐ Unknown devices removed: ___

Cloudflare:
☐ Known devices: ___
☐ Unknown devices removed: ___

Action: Revoke all sessions, force re-login with 2FA
```

---

## 📝 **SECURITY EVENT LOG**

### **Template for SECURITY-HARDENING-REPORT.md**

```markdown
### Access Control + 2FA Review Results

**Review Date:** 2025-11-12 09:00 UTC  
**Reviewer:** Release Captain  

**2FA Status:**
- Vercel: ✅ ENABLED (2025-11-12)
- Cloudflare: ✅ ENABLED (2025-11-12)
- Stripe: ✅ ENABLED (2025-11-12)
- GitHub: ✅ ENABLED (2025-11-12)
- Neon: ✅ ENABLED (2025-11-12)
- Replit: ✅ ENABLED (2025-11-12)

**Key Rotation:**
- Stripe Secret Key: Rotated (age: 300 → 0 days)
- Vercel Token: Rotated (age: 255 → 0 days)
- GitHub PAT: OK (age: 41 days)
- Database Password: OK (age: 71 days)
- JWT Secret: OK (age: 10 days)

**User Access:**
- Total users reviewed: 8
- Users removed: 2 (inactive contractors)
- Active users: 6
- Admin access: 2 (justified)

**Sessions:**
- Unknown devices revoked: 3
- Active sessions: 4 (all verified)

**Status:** PASS ✅  
**Next Review:** 2026-02-12 (quarterly)
```

---

## ⚠️ **COMMON PITFALLS**

1. **Backup Codes Not Stored**
   - Always download and securely store backup codes
   - Test one backup code to verify it works

2. **API Keys in Code**
   - Never commit secrets to Git
   - Use environment variables only
   - Scan repos with `git-secrets` or `trufflehog`

3. **Shared Accounts**
   - Each person needs individual account
   - Shared credentials = security risk
   - Audit trails become useless

4. **SMS 2FA Only**
   - SMS vulnerable to SIM swap attacks
   - Always use authenticator app as primary
   - Hardware keys (Yubikey) for critical accounts

5. **Forgotten Service Accounts**
   - Review integration tokens quarterly
   - Document all API keys with purpose
   - Revoke immediately when service discontinued

---

## 🚀 **AUTOMATION SCRIPT**

```bash
#!/bin/bash
# scripts/audit_secrets.sh
# Check for common secret leaks

echo "=== SECRET AUDIT ==="
echo ""

# Check .env files not in .gitignore
if git ls-files | grep -q "\.env$"; then
  echo "⚠️  .env files tracked in Git:"
  git ls-files | grep "\.env$"
else
  echo "✅ No .env files in Git"
fi

# Check for potential secrets in code
echo ""
echo "Scanning for potential secrets..."
grep -r -E "(api_key|apikey|secret|password|token)" . \
  --include="*.js" --include="*.ts" --include="*.py" \
  --exclude-dir=node_modules --exclude-dir=.git \
  | grep -v "// " | grep -v "# " | head -10

echo ""
echo "=== END AUDIT ==="
```

---

**Complete access review during Day 2 and document in SECURITY-HARDENING-REPORT.md** 🔒
