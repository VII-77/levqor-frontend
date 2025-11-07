# 📝 EXACT DNS CONFIGURATION

## 🎯 COPY THESE EXACT SETTINGS

When you add your domain to Vercel, they'll give you DNS records. Here's what to add in Cloudflare:

---

## ✅ MOST LIKELY: A RECORD

**Vercel usually gives you this:**

```
Type: A
Name: @
Value: 76.76.21.21
```

### In Cloudflare, add:

| Field | Value |
|-------|-------|
| Type | `A` |
| Name | `@` |
| IPv4 address | `76.76.21.21` |
| Proxy status | **DNS only** (gray cloud) ⚠️ |
| TTL | Auto |

**Click "Save"**

---

## 🔄 ALTERNATIVE: CNAME RECORD

**If Vercel gives you CNAME instead:**

```
Type: CNAME
Name: @
Value: cname.vercel-dns.com
```

### In Cloudflare, add:

| Field | Value |
|-------|-------|
| Type | `CNAME` |
| Name | `@` |
| Target | `cname.vercel-dns.com` |
| Proxy status | **DNS only** (gray cloud) ⚠️ |
| TTL | Auto |

**Click "Save"**

---

## ⚠️ CRITICAL: PROXY SETTING

**MUST BE "DNS only" (gray cloud)**

❌ **WRONG:** Orange cloud (Proxied)  
✅ **CORRECT:** Gray cloud (DNS only)

**Why?** Vercel needs direct DNS access to provision SSL certificates.

---

## 🚫 DO NOT CHANGE THIS RECORD

**Your API subdomain - LEAVE IT ALONE:**

```
Type: A
Name: api
Value: [Your Replit IP]
Proxy: DNS only
```

**This is your backend API - don't touch it!**

---

## 📊 FINAL DNS SETUP

After adding the root domain record, you should have:

```
✅ api.levqor.ai    A    [Replit IP]         DNS only
✅ levqor.ai        A    76.76.21.21         DNS only
   (or CNAME to cname.vercel-dns.com)
```

---

## 🔍 HOW TO CHECK IN CLOUDFLARE

1. Go to: **DNS** → **Records**
2. Look for record with Name: **@** or **levqor.ai**
3. Check: Gray cloud icon (not orange)
4. Check: Points to Vercel IP or CNAME

---

## ⏱️ PROPAGATION TIME

After adding DNS record:
- Vercel checks: ~1-5 minutes
- SSL provision: ~5-10 minutes
- Full propagation: ~5-60 minutes

**Be patient!** DNS changes take time.

---

## ✅ VERIFICATION

**When it's working:**

1. In Vercel → Domains → Shows: **"Valid Configuration"**
2. Visit: https://levqor.ai → Shows your site
3. SSL: https works (padlock icon in browser)
4. API: https://api.levqor.ai → Still works

---

*Copy this guide when setting up DNS!* 📋
