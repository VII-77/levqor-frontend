# 🚂 Railway Deployment Checklist

## ✅ Pre-Deployment (Already Done!)

- [x] Dockerfile created
- [x] requirements.txt created  
- [x] .dockerignore created
- [x] Environment variables documented
- [x] Health endpoints working

## 📋 Deploy to Railway (Do This Now!)

### Step 1: Create Railway Project (2 minutes)

1. [ ] Go to https://railway.app
2. [ ] Sign in with GitHub
3. [ ] Click "New Project"
4. [ ] Select "Deploy from GitHub repo"
5. [ ] Choose your EchoPilot repository
6. [ ] Click "Deploy Now"

✅ Railway will detect Dockerfile and start building!

---

### Step 2: Set Environment Variables (5 minutes)

In Railway dashboard → **Variables** tab

#### ⚡ Required (Minimum - Set These First):

```bash
AI_INTEGRATIONS_OPENAI_API_KEY=sk-...
AI_INTEGRATIONS_OPENAI_BASE_URL=https://api.openai.com/v1
AUTOMATION_QUEUE_DB_ID=
AUTOMATION_LOG_DB_ID=
JOB_LOG_DB_ID=
```

#### 🔧 Optional (Add Later):

```bash
NOTION_STATUS_DB_ID=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
ALERT_TO=
```

**💡 Tip:** Copy from `railway.env.example` file

---

### Step 3: Get Your Railway URL (1 minute)

1. [ ] Wait for first deploy to complete
2. [ ] Copy Railway URL (e.g., `https://echopilot-production.up.railway.app`)
3. [ ] Go to Variables tab
4. [ ] Add: `APP_BASE_URL=https://your-url.railway.app`
5. [ ] Railway auto-redeploys

---

### Step 4: Verify Everything Works (2 minutes)

#### Test Health Endpoints:

1. [ ] Open: `https://your-url.railway.app/health`
   - **Should see:** `{"status": "ok"}`

2. [ ] Open: `https://your-url.railway.app/`
   - **Should see:** JSON with status, commit, branch

#### Check Railway Logs:

3. [ ] Go to Railway → Deployments → View Logs
   - **Look for:** 
     ```
     🤖 EchoPilot AI Automation Bot Starting...
     ✅ Bot initialized successfully!
     📊 Polling interval: 60 seconds
     ```

#### Verify Monitoring:

4. [ ] Check Notion Status Board for new heartbeats
5. [ ] Send `/status` to Telegram bot (if configured)
6. [ ] Check for supervisor email at 06:45 UTC (if configured)

---

## ⚠️ Troubleshooting

### Problem: Authentication errors in logs

**Solution:** Your code uses Replit Connectors (OAuth). For Railway:

**Option 1:** Add Replit tokens to Railway variables
```bash
REPLIT_CONNECTORS_HOSTNAME=connectors-svc.replit.com
REPL_IDENTITY=<copy from Replit secrets>
```

**Option 2:** Modify code for direct API keys (see `RAILWAY_DEPLOYMENT.md`)

---

### Problem: Bot not polling

**Check:**
- All required environment variables set?
- Notion databases shared with integration?
- OpenAI API key valid?

---

### Problem: Port/binding issues

**Solution:** Railway sets `PORT` automatically. Dockerfile handles this.

---

## 🎯 Quick Success Check

✅ All 4 checks should pass:

1. [ ] Health endpoint returns `{"status": "ok"}`
2. [ ] Railway logs show "Bot initialized successfully"
3. [ ] Notion Status Board has new heartbeat
4. [ ] No errors in Railway logs

---

## 📊 Post-Deployment Monitoring

**Railway Dashboard:**
- CPU/Memory usage
- Request logs
- Build/deployment history

**EchoPilot Monitoring:**
- Notion Status Board (hourly heartbeats)
- Telegram alerts (instant failures)
- Email reports (daily at 06:45 UTC)

---

## 💰 Cost Estimate

**Railway Pricing:**
- Hobby Plan: $5/month
- Usage-based: ~$0.0002/minute
- Estimate: $10-20/month for 24/7 operation

**Alternative:** Keep using Replit Reserved VM (~$25/month)

---

## 🚀 You're Ready!

Go to https://railway.app and start Step 1!

Need help? Check `RAILWAY_DEPLOYMENT.md` for detailed troubleshooting.
