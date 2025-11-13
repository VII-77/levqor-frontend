# Notion Integration - Quick Start

**⏱️ Setup Time:** 10 minutes  
**Last Updated:** November 11, 2025

---

## 🎯 Quick Setup (4 Steps)

### Step 1: Create Databases in Notion (5 min)

Open Notion → Create new page → Add 3 inline databases:

| Database | Title Column | Other Columns |
|----------|-------------|---------------|
| **System Health Log** | Name (Title) | Timestamp (Date), Endpoint (Text), Status (Select: Healthy/Degraded/Down), Latency (Number), Notes (Text) |
| **Cost Dashboard** | Date (Title/Date) | Replit (Number), Stripe Revenue (Number), Vercel (Number), Failed Payments (Number), Total Cost (Number), Alert (Checkbox) |
| **Pulse** | Week Ending (Title/Date) | Uptime (Number), Revenue (Number), Active Users (Number), Churn (Number), Net (Number), Summary (Text) |

---

### Step 2: Get Database IDs (2 min)

For each database:
1. Open database in Notion
2. Copy URL from browser
3. Extract 32-character ID between `/` and `?`

**Example URL:**
```
https://www.notion.so/workspace/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6?v=view_id
                                  ↑ This is your database ID ↑
```

---

### Step 3: Add to Replit Secrets (1 min)

In Replit → Tools → Secrets → Add:

```
NOTION_HEALTH_DB_ID = <your_system_health_log_id>
NOTION_COST_DB_ID = <your_cost_dashboard_id>
NOTION_PULSE_DB_ID = <your_pulse_id>
```

---

### Step 4: Test Integration (2 min)

Run test script:
```bash
python3 scripts/test_notion_connection.py
```

**Expected output:**
```
✅ All database IDs configured
✅ Notion API connection successful
🎉 Notion integration is ready to use!
```

---

## ✅ Verify It's Working

Test each automation:

```bash
# Test health monitor (should add 3 entries to Notion)
python3 scripts/automation/health_monitor.py

# Test cost collector (should add 1 entry to Notion)
python3 scripts/automation/cost_collector.py

# Test weekly pulse (should add 1 entry to Notion)
python3 scripts/automation/weekly_pulse.py
```

Check your Notion databases - you should see new entries!

---

## 🔄 Automation Schedule

Once configured, these run automatically:

| Script | Runs | Notion Database |
|--------|------|----------------|
| Health Monitor | Every 6 hours | System Health Log |
| Cost Collector | Daily 1 AM UTC | Cost Dashboard |
| Weekly Pulse | Friday 2 PM London | Pulse |

---

## 🐛 Troubleshooting

**"NOTION_HEALTH_DB_ID not configured"**
→ Add the database ID to Replit Secrets

**"Notion not connected"**
→ Notion integration already active, check REPLIT_CONNECTORS_HOSTNAME

**"Database not found"**
→ Verify database ID is exactly 32 characters (no dashes)

**Entries not appearing**
→ Check database permissions (integration has access)

---

## 📚 Full Documentation

For detailed setup instructions, see: **[NOTION-SETUP-GUIDE.md](./NOTION-SETUP-GUIDE.md)**

---

**Need help?** Run `python3 scripts/test_notion_connection.py` for diagnostics.
