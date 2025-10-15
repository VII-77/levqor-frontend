# EchoPilot AI Automation Bot

An intelligent automation bot that polls Notion databases for tasks, processes them with AI, and logs results.

## 🚀 Features

- **Automated Task Processing**: Polls Notion every 60 seconds for triggered tasks
- **AI-Powered**: Uses OpenAI (via Replit AI Integrations) for task processing
- **Quality Assurance**: Automatic QA scoring with 95% target pass rate
- **Activity Logging**: Complete audit trail of all automation activities
- **Job Tracking**: Detailed performance metrics and cost tracking
- **Google Drive Integration**: File handling and storage capabilities

## 📋 Setup Instructions

### Step 1: Create Notion Databases

You need to create **3 databases** in your Notion workspace:

#### 1. **Automation Queue** Database
Properties needed:
- **Task Name** (Title)
- **Description** (Text)
- **Trigger** (Checkbox) - When checked, bot will process this task
- **Status** (Select) - Options: Pending, Processing, Completed, Failed

#### 2. **Automation Log** Database
Properties needed:
- **Task** (Title)
- **Status** (Select) - Options: Processing, Success, Error, Warning
- **Message** (Text)
- **Details** (Text)
- **Timestamp** (Date)

#### 3. **EchoPilot Job Log** Database
Properties needed:
- **Job Name** (Title)
- **QA Score** (Number)
- **Cost** (Number)
- **Status** (Select) - Options: Completed, Failed
- **Notes** (Text)
- **Timestamp** (Date)

### Step 2: Get Database IDs from Notion

For each database:
1. Open the database in Notion (full page view)
2. Look at the URL in your browser
3. Copy the database ID (32-character code after the last `/` and before `?`)
   - Example: `https://notion.so/myworkspace/DATABASE_ID?v=...`
   - The DATABASE_ID is what you need

### Step 3: Configure Replit Secrets

Add these secrets in Replit (🔒 Secrets in the left sidebar):

```
AUTOMATION_QUEUE_DB_ID=<your-automation-queue-database-id>
AUTOMATION_LOG_DB_ID=<your-automation-log-database-id>
JOB_LOG_DB_ID=<your-job-log-database-id>
```

### Step 4: Share Databases with Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Find your Replit integration
3. Share each of the 3 databases with this integration:
   - Open each database in Notion
   - Click "Share" button
   - Add your Replit integration

### Step 5: Start the Bot

The bot is already configured to run automatically via the `EchoPilot Bot` workflow:
1. Once you add the secrets (Step 3), the bot will start automatically
2. The bot will poll every 60 seconds for new tasks
3. It will process any tasks where `Trigger = true`
4. Results will be logged automatically to your Notion databases

To manually start/stop the bot:
- Use the Replit workflows panel
- Or run `python run.py` from the terminal

## 🎯 How to Use

1. **Create a task** in your Automation Queue database
2. **Fill in** the Task Name and Description
3. **Check the Trigger checkbox** ✅
4. **Wait** - Bot will process it within 60 seconds
5. **View results** in the Automation Log and Job Log databases

## 📊 Architecture

```
run.py                      # Entry point to start the bot
bot/
  ├── __init__.py          # Package initialization
  ├── main.py              # Main bot with polling loop
  ├── processor.py         # Task processing and AI integration
  ├── notion_api.py        # Notion API wrapper
  ├── google_drive_client.py # Google Drive integration
  └── config.py            # Configuration and environment variables
README.md                  # This file
replit.md                  # Project documentation and architecture
```

## 💰 Cost Information

- **Replit AI Integrations**: Billed to your Replit credits
- **Estimated cost per job**: ~$0.02 (varies by task complexity)
- **No external API keys needed**: OpenAI access via Replit AI Integrations

## 🔧 Configuration

Edit `config.py` to adjust:
- `POLL_INTERVAL_SECONDS`: How often to check for tasks (default: 60)
- `QA_TARGET_SCORE`: Target quality score (default: 95)

## 📝 Logs and Monitoring

- **Console Output**: Shows real-time bot activity
- **Notion Automation Log**: Complete activity history
- **Job Log**: Performance metrics and QA scores

## 🆘 Troubleshooting

**Bot not processing tasks?**
- Verify all 3 database IDs are set in Secrets
- Ensure databases are shared with Notion integration
- Check that Trigger checkbox is enabled
- Review console logs for errors

**QA scores too low?**
- Review task descriptions - be clear and specific
- Check AI output quality in logs
- Adjust QA criteria in processor.py if needed

## 🔐 Security

- All API keys managed securely via Replit Secrets
- Notion access via OAuth (no manual token management)
- Google Drive access via OAuth
- Access tokens auto-refresh

## ⚖️ Compliance & Legal (IMPORTANT)

**⚠️ BEFORE PROCESSING PERSONAL DATA:**

This bot requires legal compliance setup before production use with personal or sensitive data. See detailed compliance documentation:

### Quick Start (Critical Actions)
📋 **[COMPLIANCE_QUICK_START.md](COMPLIANCE_QUICK_START.md)** - Step-by-step compliance checklist

**Week 1 Critical Actions:**
1. ✅ Execute OpenAI Data Processing Addendum (DPA)
2. ✅ Execute Notion Data Processing Addendum (DPA)
3. ✅ Create and publish Privacy Policy
4. ✅ Create and publish Terms of Service
5. ✅ Document legal basis for data processing
6. ✅ Define data retention policy

### Full Audit Report
📊 **[COMPLIANCE_AUDIT_REPORT.md](COMPLIANCE_AUDIT_REPORT.md)** - Comprehensive security, privacy, and legal audit

**Current Compliance Score:** 55/100
- ✅ Strong technical security
- ⚠️ Missing legal documentation
- ❌ No Data Processing Agreements

**Compliance Status:**
- **GDPR:** Partially Compliant (Action Required)
- **CCPA:** Partially Compliant (Action Required)
- **Security:** Compliant
- **Data Protection:** Action Required

### What Data Is Processed
- Task descriptions (user input)
- AI-generated results (OpenAI GPT-4o)
- Activity logs and metrics
- Git commit metadata

### Third-Party Processors
- **OpenAI** - AI task processing
- **Notion** - Data storage and logging
- **Google Drive** - File handling (optional)
- **Replit** - Infrastructure and secrets

**Important:** If you process EU user data, UK user data, or California resident data, you MUST complete compliance steps before production use.

## 📚 Next Steps

After setup, consider:
- **Compliance:** Complete legal documentation (see above)
- Adding webhook support for real-time triggers
- Implementing batch processing
- Adding Slack/email notifications
- Creating analytics dashboards
