# 🚀 Deploy EchoPilot to Railway - Simple 3-Step Process

## ✅ Best Method: Railway CLI with Manual Token

Since GitHub isn't connected yet, the fastest way is to use Railway CLI with a token.

---

## 📋 **3 Simple Steps:**

### **Step 1: Get Your Railway Token** 🔑

1. Open browser: https://railway.app/account/tokens
2. Sign in with GitHub
3. Click "Create Token"
4. Name it: "EchoPilot Deploy"
5. Copy the token (starts with "railway_...")

### **Step 2: Deploy with Token** 🚀

Run these commands in Replit Shell (paste the token you copied):

```bash
# Set your token (replace with your actual token)
export RAILWAY_TOKEN="paste-your-token-here"

# Verify it works
railway whoami

# Create new project
railway init

# Deploy your app
railway up
```

### **Step 3: Set Environment Variables** 🔑

After deployment, set your secrets:

```bash
# Required variables
railway variables --set AI_INTEGRATIONS_OPENAI_API_KEY="$AI_INTEGRATIONS_OPENAI_API_KEY"
railway variables --set AI_INTEGRATIONS_OPENAI_BASE_URL="$AI_INTEGRATIONS_OPENAI_BASE_URL"
railway variables --set AUTOMATION_QUEUE_DB_ID="$AUTOMATION_QUEUE_DB_ID"
railway variables --set AUTOMATION_LOG_DB_ID="$AUTOMATION_LOG_DB_ID"
railway variables --set JOB_LOG_DB_ID="$JOB_LOG_DB_ID"
railway variables --set REPLIT_CONNECTORS_HOSTNAME="$REPLIT_CONNECTORS_HOSTNAME"
railway variables --set REPL_IDENTITY="$REPL_IDENTITY"

# Optional variables
railway variables --set NOTION_STATUS_DB_ID="$NOTION_STATUS_DB_ID"
railway variables --set TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN"
railway variables --set TELEGRAM_CHAT_ID="$TELEGRAM_CHAT_ID"
railway variables --set ALERT_TO="$ALERT_TO"

# Get your URL
railway domain

# Set APP_BASE_URL (replace with your actual domain)
railway variables --set APP_BASE_URL="https://your-url.up.railway.app"
```

---

## 🎯 **All-in-One Deploy Script:**

I'll create a script that does everything automatically once you have the token!

Save this for after you get your token.

---

## ⏱️ **Timeline:**
- Step 1 (Get token): 1 minute
- Step 2 (Deploy): 3 minutes
- Step 3 (Set variables): 1 minute
- **Total: ~5 minutes**

---

## 🔄 **Alternative: GitHub Method (Takes Longer)**

If you prefer the GitHub + Railway website method:
1. Push code to GitHub first (requires GitHub setup)
2. Connect Railway to GitHub repo
3. Deploy from Railway dashboard

**But the token method above is faster and simpler!**

---

Ready? Get your token from: https://railway.app/account/tokens
