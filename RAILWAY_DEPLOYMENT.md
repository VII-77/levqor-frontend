# 🚂 EchoPilot Railway Deployment Guide

## ⚠️ Important: Authentication Differences

**Current Setup (Replit):**
- Uses Replit Connectors with OAuth for Notion, Google Drive, and Gmail
- Automatic token refresh handled by Replit

**Railway Setup:**
- Requires direct API keys and service account credentials
- You'll need to modify authentication code OR use environment variable fallbacks

---

## 📋 Step-by-Step Deployment

### 1. Create Dockerfile & Requirements ✅

Already created:
- `Dockerfile` - Production container with Gunicorn
- `requirements.txt` - All Python dependencies

### 2. Deploy to Railway

1. Go to [Railway.app](https://railway.app)
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your EchoPilot repository
4. Railway will auto-detect the Dockerfile and deploy

### 3. Set Environment Variables

Go to your Railway project → **Variables** tab and add:

#### Required - Core Services

```bash
# OpenAI (via Replit AI Integrations or direct)
AI_INTEGRATIONS_OPENAI_API_KEY=sk-...
AI_INTEGRATIONS_OPENAI_BASE_URL=https://api.openai.com/v1

# Notion Databases
AUTOMATION_QUEUE_DB_ID=your-queue-db-id
AUTOMATION_LOG_DB_ID=your-log-db-id  
JOB_LOG_DB_ID=your-job-log-db-id
NOTION_STATUS_DB_ID=your-status-board-db-id  # Optional for diagnostics
```

#### Required - Notion Authentication

**Option A: Replit Connector (if available)**
```bash
REPLIT_CONNECTORS_HOSTNAME=connectors-svc.replit.com
REPL_IDENTITY=your-repl-identity-token
```

**Option B: Direct Notion API (recommended for Railway)**
```bash
NOTION_API_KEY=secret_...  # From notion.so/my-integrations
```

> ⚠️ **Code Modification Required**: The current code uses Replit Connectors. To use direct API keys, you'll need to update `bot/notion_api.py` to fall back to `NOTION_API_KEY` if Replit tokens aren't available.

#### Optional - Gmail Alerts

```bash
# Gmail via SMTP (alternative to Gmail API)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password  # Generate at myaccount.google.com/apppasswords
ALERT_TO=recipient@gmail.com
```

> 💡 **Note**: Current code uses Gmail API via Replit Connector. For Railway, either:
> - Modify `bot/gmail_client.py` to use SMTP with these credentials, OR
> - Set up Google service account authentication

#### Optional - Telegram Alerts

```bash
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...  # From @BotFather
TELEGRAM_CHAT_ID=your-chat-id  # From @userinfobot
```

#### Optional - Google Drive (if used)

```bash
GDRIVE_SA_JSON={"type":"service_account",...}  # Full service account JSON
GDRIVE_INPUT_FOLDER_ID=folder-id
GDRIVE_OUTPUT_FOLDER_ID=folder-id
```

> ⚠️ **Code Modification Required**: Current code uses Replit Connector OAuth. Update `bot/google_drive_client.py` to use service account if provided.

#### Optional - Miscellaneous

```bash
ALLOW_DIRTY=true  # Allow running without clean Git state
ALERT_WEBHOOK_URL=https://your-webhook.com/alerts  # For webhook alerts
```

### 4. Get Railway URL & Configure

After first deployment:

1. Copy your Railway public URL (e.g., `https://echopilot-production.up.railway.app`)
2. Add this variable:
   ```bash
   APP_BASE_URL=https://echopilot-production.up.railway.app
   ```
3. Redeploy (Railway auto-redeploys on variable changes)

### 5. Post-Deployment Verification

**Health Checks:**

Open in browser:
- `https://your-app.railway.app/` → Should show healthy status with commit hash
- `https://your-app.railway.app/health` → Should return `{"status": "ok"}`

**Check Logs:**

In Railway dashboard → **Deployments** → **View Logs**

Look for:
```
🤖 EchoPilot AI Automation Bot Starting...
📝 Commit: [hash]
🌿 Branch: main
✅ Bot initialized successfully!
📊 Polling interval: 60 seconds
```

**Test Alerts:**

- Telegram: Send `/status` command to your bot
- Gmail: Check if daily reports arrive at 06:45 UTC
- Notion: Verify hourly heartbeats in Status Board

---

## 🔧 Code Modifications Needed for Full Railway Support

The current codebase uses Replit Connectors. To fully support Railway, you'll need to update these files:

### 1. `bot/notion_api.py`

Add fallback to direct API key:

```python
def get_client(self):
    # Try Replit Connector first
    if os.getenv('REPL_IDENTITY') or os.getenv('WEB_REPL_RENEWAL'):
        # Existing Replit Connector logic
        ...
    # Fallback to direct API key
    elif os.getenv('NOTION_API_KEY'):
        from notion_client import Client
        return Client(auth=os.getenv('NOTION_API_KEY'))
    else:
        raise Exception('No Notion authentication available')
```

### 2. `bot/gmail_client.py`

Add SMTP fallback:

```python
def send_email(self, to, subject, body):
    # Try Gmail API via Replit first
    if os.getenv('REPL_IDENTITY'):
        # Existing Gmail API logic
        ...
    # Fallback to SMTP
    elif os.getenv('SMTP_USER') and os.getenv('SMTP_PASS'):
        import smtplib
        from email.mime.text import MIMEText
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = os.getenv('SMTP_USER')
        msg['To'] = to
        
        with smtplib.SMTP(os.getenv('SMTP_HOST', 'smtp.gmail.com'), 
                          int(os.getenv('SMTP_PORT', 587))) as server:
            server.starttls()
            server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASS'))
            server.send_message(msg)
        
        return {'ok': True}
```

### 3. `bot/google_drive_client.py`

Add service account authentication:

```python
def get_credentials(self):
    # Try Replit Connector first
    if os.getenv('REPL_IDENTITY'):
        # Existing OAuth logic
        ...
    # Fallback to service account
    elif os.getenv('GDRIVE_SA_JSON'):
        import json
        from google.oauth2 import service_account
        
        sa_info = json.loads(os.getenv('GDRIVE_SA_JSON'))
        return service_account.Credentials.from_service_account_info(
            sa_info,
            scopes=['https://www.googleapis.com/auth/drive']
        )
```

---

## 🚀 Quick Start (Minimal Setup)

If you just want to get it running with minimal features:

**Required Variables:**
```bash
AI_INTEGRATIONS_OPENAI_API_KEY=sk-...
AI_INTEGRATIONS_OPENAI_BASE_URL=https://api.openai.com/v1
AUTOMATION_QUEUE_DB_ID=...
AUTOMATION_LOG_DB_ID=...
JOB_LOG_DB_ID=...
```

**Then add authentication** (choose one):
- Replit Connector tokens (if you have them)
- Direct `NOTION_API_KEY` (after code modification)

**Deploy and monitor** via Railway logs.

---

## 📊 Monitoring on Railway

**Built-in Metrics:**
- Railway dashboard shows CPU, Memory, Network usage
- Deployment logs show application output

**Application Health:**
- EchoPilot posts hourly heartbeats to Notion Status Board
- Daily supervisor reports via email (if configured)
- Telegram alerts for failures (if configured)

**Cost Optimization:**
- Railway charges per minute of usage
- EchoPilot runs 24/7 with 60-second polling
- Consider Reserved VM on Replit for more predictable costs

---

## ❓ Troubleshooting

**Bot not polling:**
- Check Railway logs for startup errors
- Verify all required environment variables are set
- Check Notion database permissions

**Authentication errors:**
- Replit Connectors don't work on Railway
- Use direct API keys instead (requires code modification)
- Verify API key format and permissions

**Memory issues:**
- Railway default: 512MB RAM
- Increase if needed: Settings → Memory limit

**Port issues:**
- Dockerfile uses PORT env var (default: 8000)
- Railway automatically sets PORT
- Don't hardcode port numbers

---

## ✅ Success Checklist

- [ ] Dockerfile and requirements.txt created
- [ ] Railway project created from GitHub repo
- [ ] All required environment variables set
- [ ] Code modified for direct API keys (if not using Replit Connectors)
- [ ] Railway URL obtained and APP_BASE_URL set
- [ ] Health endpoint returns healthy status
- [ ] Bot logs show successful polling
- [ ] Notion heartbeats appearing in Status Board
- [ ] Telegram/Gmail alerts working (if configured)

---

**Note**: This deployment assumes you'll either use Replit Connector tokens (if available) or modify the code to support direct API keys. The current codebase is optimized for Replit's infrastructure.
