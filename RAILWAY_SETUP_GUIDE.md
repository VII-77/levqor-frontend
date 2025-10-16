# 🚂 Railway Setup Guide - Step by Step

## ✅ What You Already Have

- [x] Dockerfile created
- [x] All dependencies in requirements.txt
- [x] All secrets configured in Replit
- [x] Health endpoints working

You're ready to deploy! Follow these steps exactly.

---

## 🚀 Step 1: Create Railway Account & Project (3 minutes)

### 1.1 Sign Up / Sign In

1. Go to: **https://railway.app**
2. Click **"Login"** or **"Start a New Project"**
3. Choose **"Login with GitHub"**
4. Authorize Railway to access your GitHub

### 1.2 Create New Project

1. Click **"New Project"** (big button in dashboard)
2. Select **"Deploy from GitHub repo"**
3. If this is your first time:
   - Click **"Configure GitHub App"**
   - Select which repositories Railway can access
   - Choose your EchoPilot repository
4. Select **"EchoPilot"** from the list
5. Click **"Deploy Now"**

✅ **What happens next:**
- Railway detects your Dockerfile
- Starts building the container
- This takes 2-3 minutes

---

## 🔑 Step 2: Set Environment Variables (5 minutes)

While the build is running, let's add your environment variables.

### 2.1 Open Variables Panel

1. In your Railway project dashboard
2. Click on your **service/deployment** (shows the container icon)
3. Click **"Variables"** tab at the top

### 2.2 Add Required Variables

Click **"New Variable"** for each of these:

#### Core Services (Required):

```
Variable Name: AI_INTEGRATIONS_OPENAI_API_KEY
Value: [Copy from Replit Secrets]
```

```
Variable Name: AI_INTEGRATIONS_OPENAI_BASE_URL
Value: [Copy from Replit Secrets]
```

```
Variable Name: AUTOMATION_QUEUE_DB_ID
Value: [Copy from Replit Secrets]
```

```
Variable Name: AUTOMATION_LOG_DB_ID
Value: [Copy from Replit Secrets]
```

```
Variable Name: JOB_LOG_DB_ID
Value: [Copy from Replit Secrets]
```

#### Authentication (Required):

```
Variable Name: REPLIT_CONNECTORS_HOSTNAME
Value: [Copy from Replit Secrets]
```

```
Variable Name: REPL_IDENTITY
Value: [Copy from Replit Secrets]
```

#### Monitoring (Optional but Recommended):

```
Variable Name: NOTION_STATUS_DB_ID
Value: [Copy from Replit Secrets]
```

```
Variable Name: TELEGRAM_BOT_TOKEN
Value: [Copy from Replit Secrets]
```

```
Variable Name: TELEGRAM_CHAT_ID
Value: [Copy from Replit Secrets]
```

```
Variable Name: ALERT_TO
Value: [Copy from Replit Secrets]
```

### 2.3 How to Copy from Replit

**Option A: One by one**
1. In Replit: Open **Tools → Secrets**
2. Find each secret name
3. Click to reveal value
4. Copy and paste to Railway

**Option B: Use the shell script**
```bash
bash export_to_railway.sh
```
This shows you which variables are set in Replit.

---

## 🌐 Step 3: Get Your Railway URL (2 minutes)

### 3.1 Wait for First Deploy

1. Go to **"Deployments"** tab
2. Wait for build to complete (you'll see ✅ **Success**)
3. Click on the successful deployment

### 3.2 Find Your Public URL

1. Look for **"Domains"** section (or **"Settings"** → **"Networking"**)
2. You'll see something like:
   ```
   https://echopilot-production-abc123.up.railway.app
   ```
3. **Copy this URL**

### 3.3 Add APP_BASE_URL Variable

1. Go back to **"Variables"** tab
2. Click **"New Variable"**
   ```
   Variable Name: APP_BASE_URL
   Value: https://your-railway-url.up.railway.app
   ```
3. Railway will automatically redeploy

---

## ✅ Step 4: Verify Everything Works (3 minutes)

### 4.1 Test Health Endpoints

Open your Railway URL in browser:

**Test 1: Simple Health Check**
```
https://your-railway-url.up.railway.app/health
```
✅ Should return: `{"status": "ok"}`

**Test 2: Full Status**
```
https://your-railway-url.up.railway.app/
```
✅ Should return JSON with:
- `"status": "healthy"`
- `"service": "EchoPilot AI Automation Bot"`
- `"commit": "..."`
- `"branch": "main"`

### 4.2 Check Railway Logs

1. Go to **"Deployments"** tab
2. Click on the latest successful deployment
3. Click **"View Logs"**

✅ Look for these messages:
```
🤖 EchoPilot AI Automation Bot Starting...
📝 Commit: [hash]
🌿 Branch: main
✅ Bot initialized successfully!
📊 Polling interval: 60 seconds
🤖 Telegram bot listening for commands...
```

### 4.3 Check Notion Status Board

1. Open your Notion Status Board database
2. Look for a new entry posted within the last hour
3. Should show:
   - Type: "Heartbeat"
   - Status: "Healthy"
   - Recent timestamp

### 4.4 Test Telegram Bot (if configured)

1. Open your Telegram chat with the bot
2. Send: `/status`
3. You should get a response within 30 seconds with:
   - Polling interval: 60 seconds
   - QA Target: 95%
   - Git commit
   - Branch: main

---

## 🎯 Success Checklist

All 5 should be ✅:

- [ ] `/health` endpoint returns `{"status": "ok"}`
- [ ] `/` endpoint shows full bot status
- [ ] Railway logs show "Bot initialized successfully"
- [ ] Notion Status Board has new heartbeat entry
- [ ] Telegram `/status` command works (if configured)

---

## ⚠️ Troubleshooting

### Problem: "Port already in use" or "bind failed"

**Solution:** Railway sets `PORT` environment variable automatically. Your Dockerfile already handles this. No action needed.

### Problem: "Authentication failed" in logs

**Check these variables are set correctly:**
- REPLIT_CONNECTORS_HOSTNAME
- REPL_IDENTITY
- All database IDs

**Make sure:**
- All Notion databases are shared with your Notion integration
- OpenAI API key is valid

### Problem: Bot not polling / No heartbeats

**Check:**
1. All required environment variables set?
2. Railway logs show successful startup?
3. Any errors in Railway logs?
4. Notion databases accessible?

### Problem: Telegram not working

**Check:**
- TELEGRAM_BOT_TOKEN is set correctly
- TELEGRAM_CHAT_ID is set correctly
- You've started the bot in Telegram by sending `/start`

### Problem: Can't access health endpoint

**Check:**
1. Deployment is successful (green checkmark)
2. Railway generated a public domain
3. No firewall blocking the domain
4. Try adding `/health` to the URL

---

## 📊 Monitoring Your Railway Deployment

### Railway Dashboard

**View Metrics:**
- CPU usage
- Memory usage  
- Network traffic
- Build/deploy history

**View Logs:**
- Real-time application logs
- Build logs
- Error logs

### EchoPilot Monitoring

**Notion Status Board:**
- Hourly heartbeats (every hour)
- 6-hour synthetic tests
- Shows Railway deployment is running

**Telegram:**
- Send `/status` anytime
- Get instant alerts for failures
- Send `/health` for system check

**Email:**
- Daily supervisor reports (06:45 UTC)
- Failure alerts (≥3 consecutive failures)

---

## 💰 Railway Pricing

**Hobby Plan:** $5/month
- Includes $5 credit
- Usage-based after that
- ~$0.0002 per minute

**Estimated Cost for EchoPilot:**
- Running 24/7: ~$10-15/month
- Light usage: $5-10/month

**Pro Tip:** Monitor your usage in Railway dashboard → Usage tab

---

## 🔄 Updating Your Deployment

When you push code changes to GitHub:

1. Railway automatically detects the change
2. Builds new Docker image
3. Deploys automatically
4. Zero downtime deployment

**Manual Redeploy:**
1. Go to deployments
2. Click **"Redeploy"** on any previous deployment

---

## 📝 Quick Command Reference

**View all variables:**
```bash
# In Replit
bash export_to_railway.sh
```

**Test health locally:**
```bash
curl https://your-railway-url.up.railway.app/health
```

**Check Railway CLI (optional):**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# View logs
railway logs

# View variables
railway variables
```

---

## 🎉 You're Done!

Your EchoPilot bot is now running on Railway with:

✅ 24/7 uptime
✅ Automatic deployments from GitHub
✅ Health monitoring
✅ Telegram alerts
✅ Email reports
✅ Notion status tracking

**Enjoy your fully deployed automation bot!** 🚀

---

## 📞 Need Help?

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Check RAILWAY_DEPLOYMENT.md for detailed troubleshooting
