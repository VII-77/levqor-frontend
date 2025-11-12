# Notion Integration Setup Guide

**Last Updated:** November 11, 2025  
**Status:** Ready for configuration

---

## 📋 Step 1: Create Databases in Notion

Open your Notion workspace and create these three databases under an "Automations" page:

### Database 1: System Health Log

**Purpose:** Track endpoint health checks every 6 hours

| Column Name | Type | Description |
|------------|------|-------------|
| **Name** | Title | Endpoint name (auto-filled) |
| **Timestamp** | Date | When the check occurred |
| **Endpoint** | Text | Full URL checked |
| **Status** | Select | Options: `Healthy`, `Degraded`, `Down` |
| **Latency** | Number | Response time in milliseconds |
| **Notes** | Text | Error details if unhealthy |

**Create in Notion:**
```
1. Click "+ New Page" in your workspace
2. Select "Database - Inline"
3. Name it: "System Health Log"
4. Add the columns above with their types
5. For Status column, create 3 options:
   - Healthy (Green)
   - Degraded (Yellow)
   - Down (Red)
```

---

### Database 2: Cost Dashboard

**Purpose:** Daily cost tracking across all services

| Column Name | Type | Description |
|------------|------|-------------|
| **Date** | Title (Date) | Date of record |
| **Replit** | Number | Replit spend in $ |
| **Stripe Revenue** | Number | Revenue from Stripe in $ |
| **Vercel** | Number | Vercel costs in $ |
| **Failed Payments** | Number | Count of failed transactions |
| **Total Cost** | Number | Sum of all costs |
| **Alert** | Checkbox | Checked if threshold exceeded |

**Create in Notion:**
```
1. Create new database named "Cost Dashboard"
2. Set first column as Date type
3. Add all number columns
4. Add Alert checkbox column
```

---

### Database 3: Pulse

**Purpose:** Weekly performance summaries every Friday

| Column Name | Type | Description |
|------------|------|-------------|
| **Week Ending** | Title (Date) | Friday date |
| **Uptime** | Number | 7-day uptime percentage |
| **Revenue** | Number | Weekly revenue in $ |
| **Active Users** | Number | Count of active users |
| **Churn** | Number | Cancelled subscriptions |
| **Net** | Number | Revenue minus costs |
| **Summary** | Rich Text | Human-readable summary |

**Create in Notion:**
```
1. Create new database named "Pulse"
2. Set first column as Date type
3. Add all number columns
4. Add Summary as text column
```

---

## 🔑 Step 2: Get Database IDs

For each database you created:

1. **Open the database** in Notion (click to open full page)
2. **Copy the URL** from your browser address bar
3. **Extract the 32-character ID** from the URL

**URL Format:**
```
https://www.notion.so/workspace-name/DATABASE_ID?v=view_id
                                    ↑ This is your database ID (32 chars)
```

**Example:**
```
URL: https://www.notion.so/levqor/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6?v=...
Database ID: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

**Extract without dashes:**
```
If URL shows: a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6
Use clean ID: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

---

## ⚙️ Step 3: Configure Environment Variables

Add these three secrets to your Replit environment:

### Add via Replit Secrets UI:

| Secret Name | Value | Description |
|------------|-------|-------------|
| `NOTION_HEALTH_DB_ID` | Your 32-char ID | System Health Log database |
| `NOTION_COST_DB_ID` | Your 32-char ID | Cost Dashboard database |
| `NOTION_PULSE_DB_ID` | Your 32-char ID | Pulse database |

**How to Add:**
1. Open Replit project
2. Click "Tools" → "Secrets"
3. Add each secret with its database ID
4. Save

**Note:** The Notion access token is already configured via the Notion integration connector.

---

## ✅ Step 4: Verify Integration

Test each automation script manually to confirm Notion logging works:

### Test Health Monitor
```bash
python3 scripts/automation/health_monitor.py
```

**Expected Output:**
```
✅ Health check logged to Notion (3 entries added)
```

**Verify in Notion:**
- Open "System Health Log" database
- Should see 3 new entries (Frontend, Backend, Metrics)

### Test Cost Collector
```bash
python3 scripts/automation/cost_collector.py
```

**Expected Output:**
```
✅ Cost data logged to Notion
```

**Verify in Notion:**
- Open "Cost Dashboard" database
- Should see today's entry with current costs

### Test Weekly Pulse
```bash
python3 scripts/automation/weekly_pulse.py
```

**Expected Output:**
```
✅ Pulse logged to Notion
```

**Verify in Notion:**
- Open "Pulse" database
- Should see this week's summary

---

## 🔄 Step 5: Restart Backend

After configuration, restart the backend to activate automation:

```bash
# Via Replit UI: Click "Stop" then "Start" on levqor-backend workflow
```

**Verify Scheduler:**
Check logs for confirmation:
```
✅ APScheduler initialized with 11 jobs
✅ Notion integration active
```

---

## 📧 Step 6: Optional Email Notifications

To enable email summaries via Resend (already configured):

**Current Setup:**
- Resend API already integrated (used by ops_summary.py)
- RESEND_API_KEY and RECEIVING_EMAIL already configured

**Enable in Weekly Pulse:**
1. Weekly pulse already generates summary text
2. Email will be sent automatically to RECEIVING_EMAIL
3. No additional configuration needed

**Test Email:**
```bash
# Pulse script will send email on next Friday run
# Or test manually by running the script
```

---

## 🎯 Automation Schedule Summary

Once configured, these jobs run automatically:

| Job | Schedule | Notion Database | Notes |
|-----|----------|----------------|-------|
| Health Monitor | Every 6 hours | System Health Log | Logs all endpoint checks |
| Cost Collector | Daily 1:00 AM UTC | Cost Dashboard | Tracks daily costs |
| Weekly Pulse | Friday 2:00 PM | Pulse | Weekly summary + email |

---

## 🐛 Troubleshooting

### "Notion not connected" Error
- Verify Notion integration is active in Replit
- Check that REPLIT_CONNECTORS_HOSTNAME is set
- Reconnect Notion integration if needed

### "Database not found" Error
- Verify database ID is exactly 32 characters
- Check that ID has no dashes or extra characters
- Ensure database is shared with the integration

### Entries Not Appearing in Notion
- Check that automation scripts don't show errors
- Verify database permissions (integration has write access)
- Check database ID is correct in environment variables

### Testing Connection
```bash
# Run test script to verify Notion API access
python3 scripts/test_notion_connection.py
```

---

## 📊 Expected Results

After 24 hours of operation, you should see:

**System Health Log:**
- 4 entries per day (every 6 hours)
- All endpoints showing "Healthy" status
- Latency < 1000ms

**Cost Dashboard:**
- 1 entry per day at 1:00 AM UTC
- Cost tracking across all services
- Alerts if thresholds exceeded

**Pulse:**
- 1 entry per week on Friday
- Uptime, revenue, user metrics
- Email summary sent automatically

---

## 🚀 Next Steps

After Notion integration is working:

1. **Customize Views:** Create filtered views in Notion for:
   - Last 7 days of health checks
   - Monthly cost trends
   - Weekly pulse summaries

2. **Add Formulas:** Calculate in Notion:
   - Net revenue (Revenue - Total Cost)
   - Average uptime over time
   - Cost per user

3. **Create Dashboards:** Build Notion dashboard pages with:
   - Embedded database views
   - Charts and graphs (via Notion charts)
   - Quick health status indicators

4. **Set up Alerts:** Use Notion notifications for:
   - Cost threshold breaches
   - Downtime alerts
   - Weekly pulse reminders

---

**Need Help?** Check logs at `/tmp/logs/levqor-backend_*.log` or run manual tests to debug issues.
