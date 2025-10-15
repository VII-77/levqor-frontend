# 🚀 EchoPilot Setup Guide

## ✅ Current Status: RUNNING IN DEMO MODE

Your EchoPilot bot is **LIVE and WORKING** in demo mode!

### 🎮 What's Working Right Now

- ✅ Bot is running and polling every 60 seconds
- ✅ All integrations connected (OpenAI, Notion, Google Drive)
- ✅ Health monitoring active
- ✅ Console logs showing activity
- ✅ Ready to switch to production mode anytime

---

## 📋 Switch to Production Mode (3 Simple Steps)

### Step 1: Get Your Notion Database IDs

For each of your 3 databases in Notion:

1. **Open the database** in Notion (full page view)
2. **Look at the browser URL**:
   ```
   https://www.notion.so/workspace/abc123def456...?v=xyz
                                   ^^^^^^^^^^^^^^^^
                                   This is the database ID (32 characters)
   ```
3. **Copy the ID** (the long code between the last `/` and `?`)

You need IDs for:
- 🧱 Automation Queue database
- 🔁 Automation Log database
- 📘 EchoPilot Job Log database

### Step 2: Configure the IDs

**Option A: Using the Quick Setup Script** (Recommended)
```bash
python quick_setup.py
```
This will prompt you to paste each database ID.

**Option B: Manually Add to Secrets**
1. Click the 🔒 **Secrets** tab in Replit
2. Add these 3 secrets:
   ```
   AUTOMATION_QUEUE_DB_ID = <your-queue-database-id>
   AUTOMATION_LOG_DB_ID = <your-log-database-id>
   JOB_LOG_DB_ID = <your-job-database-id>
   ```

### Step 3: Restart the Bot

The workflow will automatically pick up the new configuration and switch to production mode!

---

## 🔧 Database Setup Instructions

If you don't have the databases yet, create them in Notion with these exact properties:

### 1️⃣ Automation Queue Database
- **Task Name** (Title)
- **Description** (Text)
- **Trigger** (Checkbox) - Check this to trigger the bot
- **Status** (Select) - Options: Pending, Processing, Completed, Failed

### 2️⃣ Automation Log Database
- **Task** (Title)
- **Status** (Select) - Options: Processing, Success, Error, Warning
- **Message** (Text)
- **Details** (Text)
- **Timestamp** (Date)

### 3️⃣ Job Log Database
- **Job Name** (Title)
- **QA Score** (Number)
- **Cost** (Number)
- **Status** (Select) - Options: Completed, Failed
- **Notes** (Text)
- **Timestamp** (Date)

**Important:** Share each database with your Notion integration!

---

## 🎯 How to Use (Once in Production)

1. Create a new page in your **Automation Queue** database
2. Fill in the **Task Name** and **Description**
3. Check the **Trigger** checkbox ✅
4. Wait up to 60 seconds
5. Check the **Automation Log** and **Job Log** for results!

---

## 📊 Monitoring

- **Workflow Console**: See real-time bot activity
- **Demo Mode**: Currently active, shows polling activity
- **Production Mode**: Processes real Notion tasks with AI

---

## 🆘 Troubleshooting

**Bot stuck in demo mode?**
- Check that all 3 database IDs are added to Secrets
- Restart the workflow

**Database IDs not working?**
- Verify the IDs are 32 characters long
- Make sure databases are shared with Notion integration
- Check for typos in the IDs

**Need help?**
- Check the console logs for detailed error messages
- Run `python quick_setup.py` to reconfigure

---

## 💡 Quick Commands

```bash
# Configure database IDs
python quick_setup.py

# Check current config
cat .env

# View logs
# Check the workflow console in Replit
```

---

Your bot is ready! Switch to production mode whenever you're ready to start automating! 🚀
