# 🚀 EchoPilot Bot - Production Deployment Instructions

## ⚠️ Important: Use Reserved VM Deployment

Your bot is a **background worker** that polls Notion every 60 seconds. It does NOT handle HTTP requests, so it **requires Reserved VM deployment** (not Autoscale).

---

## 📋 Step-by-Step Deployment:

### 1. Click the Deploy Button
- Look for the **Deploy** button at the top of your Replit workspace
- Click it to open the deployment configuration

### 2. Select Reserved VM Deployment
**CRITICAL:** Make sure you select:
- ✅ **Reserved VM** (or "Static" → "Reserved VM")
- ❌ **NOT** Autoscale (this won't work for background workers)

### 3. Configure Deployment Settings

The configuration should show:
```
Deployment Type: Reserved VM
Run Command: python run.py
```

### 4. Review Environment Variables

All secrets are already configured:
- ✅ AUTOMATION_QUEUE_DB_ID
- ✅ AUTOMATION_LOG_DB_ID  
- ✅ JOB_LOG_DB_ID
- ✅ ALLOW_DIRTY
- ✅ AI_INTEGRATIONS_OPENAI_API_KEY

### 5. Deploy!
- Click the **Deploy** button
- Wait for deployment to complete
- Your bot will be live 24/7!

---

## 🎯 What Your Bot Will Do:

Once deployed, your bot will:
- ✅ Run continuously 24/7
- ✅ Poll Notion every 60 seconds for triggered tasks
- ✅ Process tasks with AI (OpenAI GPT-4o)
- ✅ Log all activity to Automation Log
- ✅ Track metrics in Job Log (QA scores, costs, tokens, duration)
- ✅ Track Git commit hash for every operation

---

## ⚡ Quick Troubleshooting:

**If deployment fails with "not opening a port":**
- You selected **Autoscale** instead of **Reserved VM**
- Go back and select **Reserved VM** deployment type

**If deployment fails with "Git check failed":**
- Environment variable `ALLOW_DIRTY=true` is already set ✅

**If deployment fails with "Invalid database ID":**
- All database IDs are correctly configured ✅

---

## 📊 After Deployment:

1. **Create a test task** in your Automation Queue database
2. **Set Task Type** (Research, Drafting, etc.)
3. **Check the Trigger checkbox** ✅
4. **Watch it process** - Status changes: New → Processing → Completed
5. **Check results** in Result Summary and QC Score fields
6. **Review logs** in Automation Log database

---

## 💰 Cost Estimate:

**Reserved VM:** ~$20-30/month for 24/7 operation  
**Per Task:** $0.10-0.50 depending on complexity (AI costs)

---

**Ready to deploy! Select Reserved VM and click Deploy!** 🚀
