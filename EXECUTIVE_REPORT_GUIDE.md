# 📊 Executive Report System

**Status:** ✅ **ACTIVE** - Daily PDF reports scheduled

---

## Overview

The Executive Report system generates professional PDF summaries of your EchoPilot performance and emails them automatically. Perfect for daily business insights and tracking revenue metrics.

---

## 🎯 What It Does

### **Daily Automated Reports (06:55 UTC)**
Every morning at 06:55 UTC, you'll receive a PDF executive report containing:

**7-Day Performance Summary:**
- Total jobs processed
- Jobs completed (Done status)
- Average QA score
- Gross revenue
- AI costs
- Profit margin %
- Unpaid invoices count
- Top 5 clients by revenue

**PDF Format:**
- Professional layout (A4 size)
- Clear data visualization
- Easy to read on mobile or desktop
- Includes generation timestamp

**Email Delivery:**
- Sent via Gmail API (OAuth, no SMTP needed)
- Delivered to `ALERT_TO` email address
- Includes summary in email body
- PDF attached for detailed view

---

## 📱 How to Use

### **Automatic Daily Reports**
✅ **Already configured!** You'll receive reports daily at 06:55 UTC

**Recipient:** Your `ALERT_TO` email (currently configured)

### **On-Demand Reports**
You can trigger a report anytime:

**Option 1: Web Endpoint**
```bash
# Visit in browser or curl
curl https://Echopilotai.replit.app/exec-report
```

**Option 2: Python Command**
```bash
python -m bot.executive_report
```

Both methods will:
1. Generate the PDF report
2. Send it to your email
3. Return a summary JSON

---

## 📊 Sample Report

```
EchoPilot — Daily Executive Report
Generated: 2025-10-17 06:55Z

Jobs (7d): 15  |  Done: 12
Avg QA: 92.5   |  Gross (7d): $487.50  |  Cost: $8.30  |  Margin: 98.3%
Unpaid invoices: 2

Top Clients (by Gross):
  • Client:abc123 — $250.00
  • Client:def456 — $150.00
  • Client:Unknown — $87.50
```

---

## ⚙️ Configuration

### **Current Settings:**
- **Schedule:** Daily at 06:55 UTC
- **Email:** Uses Gmail API (no SMTP credentials needed)
- **Recipient:** `ALERT_TO` environment variable
- **Data Source:** Last 7 days from Job Log database
- **PDF Generator:** ReportLab library

### **To Change Email Recipient:**
1. Update `ALERT_TO` in Replit Secrets
2. Restart workflow (auto-restart on secret change)

### **To Change Schedule Time:**
1. Edit `bot/main.py`
2. Find: `schedule.every().day.at("06:55").do(daily_exec_report)`
3. Change time (e.g., "08:00" for 8 AM UTC)
4. Restart workflow

---

## 🔗 Integration with EchoPilot

The executive report integrates seamlessly with your existing systems:

**Data Sources:**
- ✅ Job Log database (Notion)
- ✅ Client revenue tracking
- ✅ Payment status monitoring
- ✅ QA score metrics

**Authentication:**
- ✅ Gmail API via Replit Connector (OAuth)
- ✅ Notion API via Replit Connector (OAuth)
- ✅ No additional credentials needed

**Scheduling:**
- ✅ Runs alongside supervisor reports (06:45 UTC)
- ✅ Runs before payment reconciliation (02:10 UTC)
- ✅ Uses same scheduler as main bot

---

## 📊 Revenue Metrics

The report includes comprehensive financial data:

**Gross Revenue:**
- Calculated as: Duration × Client Rate
- Aggregated across all jobs (7 days)

**AI Costs:**
- Actual OpenAI API costs per job
- Total costs for reporting period

**Profit Margin:**
- Formula: (Gross - Cost) / Gross × 100
- Percentage shown in report

**Top Clients:**
- Ranked by gross revenue
- Shows top 5 contributors
- Useful for identifying best clients

---

## 🚀 Live Status

**System Check:**
```
✅ Executive report system: ACTIVE
✅ Scheduled: Daily at 06:55 UTC
✅ Last test: 2025-10-17 (successful)
✅ PDF generation: Working (2016 bytes)
✅ Email delivery: Working (Gmail API)
```

**Test Result:**
```
[ExecReport] Summary: 0 jobs, 0 done, $0.00 gross
[ExecReport] PDF generated (2016 bytes)
✅ Email sent - Message ID: 199f36865ec04a6d
```

---

## 🛠️ Technical Details

### **Files:**
- `bot/executive_report.py` - Main report logic
- `bot/main.py` - Scheduler integration
- `run.py` - Web endpoint

### **Dependencies:**
- `reportlab` - PDF generation ✅ Installed
- `bot.gmail_client` - Email delivery
- `bot.notion_api` - Data fetching

### **Endpoints:**
- `GET /exec-report` - Generate and send report on-demand
- Returns JSON with summary data

### **Scheduler:**
```python
# Daily at 06:55 UTC
schedule.every().day.at("06:55").do(daily_exec_report)
```

---

## 📧 Email Format

**Subject:**
```
[EchoPilot] Daily Executive Report — 2025-10-17
```

**Body:**
```
Jobs(7d): 15  Done: 12  Avg QA: 92.5  
Gross: $487.50  Cost: $8.30  Margin: 98.3%  
Unpaid: 2

See attached PDF for full executive report.
```

**Attachment:**
```
EchoPilot_Daily_Executive_Report.pdf (2-3 KB)
```

---

## 🎯 Use Cases

### **Daily Business Review**
- Check performance at a glance each morning
- Track revenue trends over time
- Monitor client activity

### **Investor Updates**
- Professional PDF reports
- Financial metrics included
- Easy to forward to stakeholders

### **Performance Monitoring**
- QA score trends
- Profit margin tracking
- Cost management

### **Client Management**
- Identify top clients
- Track payment status
- Revenue attribution

---

## 🔧 Troubleshooting

### **Not Receiving Reports?**
1. Check `ALERT_TO` is set in Replit Secrets
2. Verify Gmail connector is active
3. Check spam/junk folder
4. Test manually: `curl https://Echopilotai.replit.app/exec-report`

### **Empty Report Data?**
- Reports show last 7 days
- If no jobs in 7 days, will show 0
- Create a test job to populate data

### **Want to Test Now?**
```bash
# Option 1: Web endpoint
curl https://Echopilotai.replit.app/exec-report

# Option 2: Direct Python
python -m bot.executive_report

# Check your email for the PDF!
```

---

## 📱 Mobile View

The PDF is optimized for viewing on your Galaxy Fold 6:
- Clear, readable fonts
- Compact layout fits mobile screens
- Professional formatting
- Easy to share

---

## 🎉 What's Next

**Currently Active:**
- ✅ Daily executive reports (06:55 UTC)
- ✅ Daily supervisor reports (06:45 UTC)
- ✅ Payment reconciliation (02:10 UTC)
- ✅ Auto-operator monitoring (every 5 min)
- ✅ Telegram bot commands
- ✅ 24/7 job processing

**Your EchoPilot system now has:**
- 📊 Executive reporting
- 💰 Revenue tracking
- 📧 Automated email delivery
- 📱 Mobile-optimized PDFs
- 🎯 Performance insights

**Everything is running smoothly!** 🚀
