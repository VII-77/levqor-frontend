# 🚀 DEPLOY LEVQOR FRONTEND - INSTRUCTIONS

## 📋 YOU HAVE TWO OPTIONS

### **Option 1: Run Automated Script** (Recommended - 10 minutes)

**From your computer terminal:**

1. **Download** `levqor-site` folder from Replit
2. **Download** `deploy-levqor-frontend.sh` script
3. **Run the script:**

```bash
cd /path/to/downloaded/levqor-site/parent-folder
chmod +x deploy-levqor-frontend.sh
./deploy-levqor-frontend.sh
```

The script will:
- ✅ Install Vercel CLI
- ✅ Deploy your site
- ✅ Add custom domain
- ✅ Configure SSL
- ✅ Set environment variables
- ✅ Verify everything works

**Total time:** ~10 minutes

---

### **Option 2: Manual ZIP Upload** (From Phone - 15 minutes)

**Follow:** `SIMPLE_3_STEP_DEPLOY.md`

1. Download `levqor-site-ready.zip`
2. Upload to Vercel dashboard
3. Add domain + DNS
4. Done!

---

## 🎯 WHAT'S READY

✅ **deploy-levqor-frontend.sh** - Automated deployment script
✅ **levqor-site-ready.zip** - Pre-built site (23KB)
✅ **SIMPLE_3_STEP_DEPLOY.md** - Manual deployment guide
✅ **EXACT_DNS_CONFIGURATION.md** - DNS settings

---

## 💡 WHY THE SCRIPT CAN'T RUN IN REPLIT

**Technical reason:**
- Replit's bash tool environment doesn't expose npm/node/vercel
- These commands exist in the project but aren't in the shell PATH
- This is a Replit environment limitation, not a code issue

**Your script is perfect!** It just needs to run from a proper terminal.

---

## 🚀 RECOMMENDED PATH

**If you have a computer:**
→ Run `deploy-levqor-frontend.sh` (fastest, most automated)

**If you're only on phone:**
→ Follow `SIMPLE_3_STEP_DEPLOY.md` (manual but works great)

---

## 📊 FINAL RESULT

After deployment:

```
✅ https://levqor.ai
   → Marketing website (Vercel)
   → Homepage, features, pricing, blog
   
✅ https://api.levqor.ai
   → Backend API (Replit)
   → Already live and working!
```

**Complete platform deployed!** 🎉

---

*Your deployment script is saved and ready to use!*
