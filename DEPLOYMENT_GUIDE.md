# EchoPilot Deployment Guide

## ✅ Deployment Configuration Fixed!

Your bot is now properly configured for deployment as a **Reserved VM Background Worker**.

---

## 🚀 Deployment Configuration

**Type:** Reserved VM (Always Running)  
**Run Command:** `python run.py`  
**Why VM?** Your bot is a scheduled polling worker that runs continuously, not a web server that responds to HTTP requests.

---

## 🔑 Required: Add Deployment Secrets

Your bot needs **3 Notion database IDs** to work in production. You must add these as deployment secrets:

### Step 1: Get Your Notion Database IDs

1. Open each Notion database in your browser
2. Look at the URL - it will look like:
   ```
   https://www.notion.so/workspace/abc123def456...?v=...
                                  ↑ This is the database ID
   ```
3. Copy the 32-character ID (the part after your workspace name)

### Step 2: Add Secrets to Deployment

**Option A: Using Replit Secrets (For Deployment)**

1. Click the **🔒 Secrets** tab (lock icon on left sidebar)
2. Add these 3 secrets:

   **Secret 1:**
   - Key: `AUTOMATION_QUEUE_DB_ID`
   - Value: [Your Automation Queue database ID]

   **Secret 2:**
   - Key: `AUTOMATION_LOG_DB_ID`
   - Value: [Your Automation Log database ID]

   **Secret 3:**
   - Key: `JOB_LOG_DB_ID`
   - Value: [Your EchoPilot Job Log database ID]

**Option B: Using Quick Setup Tool**

```bash
python quick_setup.py
```

This will guide you through adding the database IDs to your `.env` file for development.

**⚠️ Important:** For deployment, you MUST use Replit Secrets (Option A). The `.env` file only works in development mode.

---

## 📊 Notion Database Structure

Make sure your 3 Notion databases have these exact properties:

### Database 1: Automation Queue
- **Task Name** (Title)
- **Description** (Text/Rich Text)
- **Trigger** (Checkbox)
- **Status** (Select: Pending, Processing, Completed, Failed)

### Database 2: Automation Log
- **Task** (Title)
- **Status** (Select: Processing, Success, Error, Warning)
- **Message** (Text/Rich Text)
- **Details** (Text/Rich Text)
- **Timestamp** (Date)

### Database 3: EchoPilot Job Log
- **Job Name** (Title)
- **QA Score** (Number)
- **Cost** (Number)
- **Status** (Select: Completed, Failed)
- **Notes** (Text/Rich Text)
- **Timestamp** (Date)

---

## 🚀 Deploy Your Bot

Once you've added the 3 secrets:

1. Click the **Deploy** button (or go to the Deploy tab)
2. Configure deployment settings:
   - **Type:** Already set to Reserved VM ✅
   - **Region:** Choose your preferred region
   - **Autoscale:** Not applicable for VM deployments
3. Click **Deploy**
4. Wait for deployment to complete

---

## ✅ Verify Deployment

After deployment:

1. Check the deployment logs for startup messages
2. You should see:
   ```
   🤖 EchoPilot AI Automation Bot Starting...
   Health Check: Healthy - All systems operational
   ✅ Bot initialized successfully!
   📊 Polling interval: 60 seconds
   ```

3. Create a test task in your Automation Queue database
4. Check the **Trigger** checkbox
5. Wait up to 60 seconds
6. Check Automation Log for processing updates
7. Check Job Log for completion metrics

---

## 🔧 Troubleshooting

### "Configuration Error" on Deployment
- **Cause:** Missing Notion database ID secrets
- **Fix:** Add all 3 secrets to Replit Secrets (🔒 tab)

### "Notion not connected" Error
- **Cause:** Integration not authorized in deployment
- **Fix:** Reauthorize the Notion integration and redeploy

### Bot Not Processing Tasks
- **Cause:** Database permissions not granted
- **Fix:** Share all 3 Notion databases with your Notion integration

### "Demo Mode" in Production
- **Cause:** Database IDs not found in deployment environment
- **Fix:** Ensure secrets are added to deployment (not just .env file)

---

## 📝 Deployment Checklist

Before deploying, ensure:

- ✅ All 3 Notion databases created with correct properties
- ✅ Databases shared with Notion integration
- ✅ 3 database ID secrets added to Replit Secrets
- ✅ Notion integration authorized
- ✅ Google Drive integration authorized (optional)
- ✅ Deployment type set to VM (already configured)
- ✅ Run command set to `python run.py` (already configured)

---

## 💡 Cost Considerations

**Replit Costs:**
- Reserved VM deployment (always running)
- OpenAI API usage (charged to Replit credits)

**Estimated Monthly Cost:**
- VM hosting: Check current Replit pricing
- AI usage: Varies based on task volume (~$0.02 per task as estimated)

---

## 🎯 Next Steps

1. **Add the 3 Notion database ID secrets** to Replit Secrets (🔒 tab)
2. **Click Deploy** to publish your bot
3. **Create test tasks** in Notion to verify it works
4. **Monitor the logs** to ensure smooth operation

Your deployment configuration is ready - just add those secrets and deploy! 🚀
