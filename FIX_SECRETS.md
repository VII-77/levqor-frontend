# ⚠️ URGENT: Fix Your Replit Secrets

## The Problem:

Your secrets have incorrect values. The bot needs clean database IDs, but they currently contain:

❌ **AUTOMATION_QUEUE_DB_ID** = `curl -H "Authorization: Bearer YOUR_ADMIN_TOKEN" https://your-app/cleanup`
❌ **AUTOMATION_LOG_DB_ID** = `https://www.notion.so/407255e34f904930b291999d025ea805?v=067d6dcbc33b41f2886513ec60c1a876`
✅ **JOB_LOG_DB_ID** = `5687ff69fb5d4403a9a0ac13f74b07be` (This one is correct!)

---

## How to Fix:

### Step 1: Open Replit Secrets
1. Click on the **🔒 Secrets** tab (left sidebar)
2. You'll see the 3 secrets listed

### Step 2: Edit Each Secret

**For AUTOMATION_QUEUE_DB_ID:**
- Click the pencil/edit icon next to it
- **DELETE** everything currently in the value field
- **PASTE** this exact value: `28d6155c-cf54-8112-8db2-d267cacce334`
- Click Save

**For AUTOMATION_LOG_DB_ID:**
- Click the pencil/edit icon next to it
- **DELETE** everything currently in the value field
- **PASTE** this exact value: `407255e34f904930b291999d025ea805`
- Click Save

**For JOB_LOG_DB_ID:**
- This one is already correct, leave it as is!

### Step 3: Restart the Bot
- The bot should automatically restart when secrets change
- OR click the Stop/Run button to restart manually

---

## ✅ Correct Values Summary:

```
AUTOMATION_QUEUE_DB_ID = 28d6155c-cf54-8112-8db2-d267cacce334
AUTOMATION_LOG_DB_ID = 407255e34f904930b291999d025ea805
JOB_LOG_DB_ID = 5687ff69fb5d4403a9a0ac13f74b07be
```

**Important:** No quotes, no URLs, no extra text - just the database ID!

---

Once you've updated these, let me know and I'll verify the bot is working! 🚀
