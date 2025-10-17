# EchoPilot Client Management & Billing System
## Complete Guide to Monetized Client Operations

---

## 📋 Overview

The Client Management System extends EchoPilot from an internal automation bot to a **fully monetized client service platform**. It automatically:

- **Tracks clients** with custom pricing tiers
- **Calculates revenue** (gross, profit, margin) per job
- **Generates PDF invoices** with professional formatting
- **Delivers invoices via email** using Gmail API
- **Logs all metrics** in Notion for ROI tracking

**Key Features:**
- ✅ Client database with custom rates
- ✅ Automatic revenue calculation (Duration × Rate - AI Cost = Profit)
- ✅ PDF invoice generation with ReportLab
- ✅ Email delivery via existing Gmail integration
- ✅ Comprehensive Notion tracking (gross, profit, margin%)
- ✅ Fully automated and mobile-friendly

---

## 🏗️ Architecture

### Components

1. **`bot/client_manager.py`** - Client CRUD, revenue calculations, invoice generation/delivery
2. **`bot/processor.py`** - Integrated client billing into job processing
3. **`bot/notion_api.py`** - Extended with client revenue fields
4. **`bot/config.py`** - Client system configuration

### Data Flow

```
Job Completed → Calculate Duration → 
  ├─ Get Client Rate from Notion/Env
  ├─ Calculate Revenue (Duration × Rate - AI Cost)
  ├─ Generate PDF Invoice
  ├─ Send Email to Client
  └─ Log to Notion (Gross, Profit, Margin%)
```

---

## 📊 Notion Database Setup

### STEP 1: Create Client Database

1. **Create new database** in Notion: "EchoPilot Clients"
2. **Add these properties:**

| Property Name | Type | Required | Description |
|--------------|------|----------|-------------|
| Client Name | Title | ✅ | Client full name |
| Email | Email | ✅ | Client email address |
| Rate USD/min | Number | ✅ | Billing rate per minute |
| Active | Checkbox | ✅ | Client active status |
| Notes | Rich Text | ⬜ | Additional notes |

3. **Get the database ID:**
   - Click "⋯" → "Copy link to view"
   - Extract ID from URL: `https://notion.so/YOUR_WORKSPACE/{DATABASE_ID}?v=...`
   - Copy the `{DATABASE_ID}` part (32-character string)

### STEP 2: Extend Job Log Database

Add these **new properties** to your existing "EchoPilot Job Log" database:

| Property Name | Type | Required | Description |
|--------------|------|----------|-------------|
| Client | Relation | ⬜ | Link to Clients DB |
| Client Email | Email | ⬜ | Client email (for tasks without relation) |
| Client Rate USD/min | Number | ⬜ | Rate used for this job |
| Gross USD | Number | ⬜ | Total revenue (Duration × Rate) |
| Profit USD | Number | ⬜ | Net profit (Gross - AI Cost) |
| Margin % | Number | ⬜ | Profit margin percentage |

**To create Relation:**
1. Click "+ New property" in Job Log database
2. Choose "Relation" type
3. Select "EchoPilot Clients" database
4. Name it "Client"

### STEP 3: Optional - Extend Queue Database

Optionally add to "Automation Queue" database for task-level client assignment:

| Property Name | Type | Description |
|--------------|------|-------------|
| Client | Relation | Link task to specific client |
| Client Email | Email | Override email for this task |

---

## ⚙️ Configuration

### Environment Variables

Add to **Replit Secrets** (🔒 tab):

```bash
# Required for Client System
NOTION_CLIENT_DB_ID=<your-clients-database-id>

# Optional: Default billing rate (fallback)
DEFAULT_RATE_USD_PER_MIN=5.0
```

### Pricing Configuration

**Default Rate:** `$5.00/min` (configurable via `DEFAULT_RATE_USD_PER_MIN`)

**Rate Priority:**
1. Client-specific rate in Clients DB (if linked via Relation)
2. Task-specific rate in Queue DB (if "Client Rate USD/min" field exists)
3. `DEFAULT_RATE_USD_PER_MIN` environment variable
4. Hardcoded fallback: $5.00/min

---

## 📱 Mobile Setup (Galaxy Fold 6)

### On Your Phone:

1. **Add Client Database ID:**
   - Tap **Secrets** tab (🔒 icon)
   - Tap **+ New Secret**
   - Name: `NOTION_CLIENT_DB_ID`
   - Value: `{your-clients-database-id}`

2. **Set Default Rate (Optional):**
   - Tap **+ New Secret**
   - Name: `DEFAULT_RATE_USD_PER_MIN`
   - Value: `5.0` (or your preferred rate)

3. **Restart Bot:**
   - Go to main tab
   - Stop and restart workflow

---

## 💼 Usage Examples

### Example 1: Create a New Client

**Via Python (Replit Shell):**

```python
from bot.client_manager import create_client

# Create client with $8/min rate
status, response = create_client(
    name="Acme Corp",
    email="billing@acmecorp.com",
    rate_usd_per_min=8.0,
    notes="Enterprise client - priority support"
)

print(f"Status: {status}")
print(f"Response: {response}")
```

**Manually in Notion:**
1. Open "EchoPilot Clients" database
2. Click "+ New"
3. Fill in:
   - Client Name: "Acme Corp"
   - Email: billing@acmecorp.com
   - Rate USD/min: 8
   - Active: ✅

### Example 2: Run a Client Job

**Method A: Link via Relation**
1. Create task in Automation Queue
2. Set **Client** relation → Select "Acme Corp"
3. Set **Trigger** = ✅
4. Bot processes → Invoices Acme Corp at their $8/min rate

**Method B: Direct Email**
1. Create task in Automation Queue
2. Set **Client Email** = billing@acmecorp.com
3. Set **Trigger** = ✅
4. Bot processes → Uses default rate, sends invoice to email

### Example 3: Check Revenue Metrics

**View in Job Log:**
1. Open "EchoPilot Job Log" database
2. Look at recent completed job
3. Check columns:
   - **Client Rate USD/min**: 8
   - **Gross USD**: 4.00 (30 sec × $8/min = $4)
   - **Profit USD**: 3.85 (Gross - AI Cost)
   - **Margin %**: 96.2% ((Profit / Gross) × 100)

---

## 📧 Invoice System

### How It Works

1. **Job Completes** → Status = "Done"
2. **Calculate Revenue:**
   - Duration: 45 seconds → 0.75 minutes
   - Rate: $8/min
   - Gross: 0.75 × $8 = **$6.00**
   - AI Cost: $0.12
   - Profit: $6.00 - $0.12 = **$5.88**
   - Margin: ($5.88 / $6.00) × 100 = **98%**

3. **Generate PDF Invoice:**
   - Client name, job ID
   - Duration, rate, gross
   - AI cost, profit, margin
   - Professional formatting

4. **Send Email:**
   - To: Client email
   - Subject: `[EchoPilot AI] Invoice - Job #abc123`
   - Attachment: `echopilot_invoice.pdf`
   - Body: Summary + thank you message

5. **Log Everything:**
   - Update Notion Job Log with all metrics
   - Client gets invoice via email
   - You track ROI in Notion

### Email Template

```
Subject: [EchoPilot AI] Invoice - Job #abc12345

Hello {Client Name},

Your EchoPilot AI automation job has been completed successfully!

Job Summary:
• Job ID: ...abc12345
• Gross Revenue: $6.00 USD
• Net Profit: $5.88 USD

Please find your detailed invoice attached.

Thank you for using EchoPilot AI!

---
This is an automated message from EchoPilot AI.
```

### PDF Invoice Format

```
┌─────────────────────────────────────────┐
│ EchoPilot AI - Invoice                  │
│ Generated: 2025-10-17 15:30 UTC         │
├─────────────────────────────────────────┤
│ Client: Acme Corp                       │
│ Job ID: ...abc12345                     │
│ Description: Data analysis task         │
├─────────────────────────────────────────┤
│ Job Details                             │
│   Duration: 0.75 minutes                │
│   Rate: $8.00 USD/minute                │
├─────────────────────────────────────────┤
│ Financial Summary                       │
│   Gross Revenue: $6.00 USD              │
│   AI Processing Cost: $0.12 USD         │
│   Net Profit: $5.88 USD                 │
│   Profit Margin: 98.0%                  │
├─────────────────────────────────────────┤
│ Thank you for using EchoPilot AI!       │
└─────────────────────────────────────────┘
```

---

## 🧪 Testing Guide

### Test 1: Revenue Calculation (30-Second Job)

```python
# In Replit Shell
from bot.client_manager import calculate_revenue

# Simulate 30-second job at $5/min with $0.05 AI cost
result = calculate_revenue(
    duration_minutes=0.5,      # 30 seconds
    client_rate_per_min=5.0,   # $5/min
    ai_cost_usd=0.05           # $0.05 AI cost
)

print(f"Gross: ${result['gross']:.2f}")        # Expected: $2.50
print(f"Profit: ${result['profit']:.2f}")      # Expected: $2.45
print(f"Margin: {result['margin_percent']:.1f}%")  # Expected: 98.0%
```

### Test 2: Full Invoice Workflow

1. **Create test client:**
   ```python
   from bot.client_manager import create_client
   
   create_client(
       name="Test Client",
       email="your-email@example.com",  # Use YOUR email
       rate_usd_per_min=5.0
   )
   ```

2. **Create test task:**
   - Go to Automation Queue in Notion
   - Click "+ New"
   - Task Name: "Test Revenue Tracking"
   - Description: "Quick test job"
   - Client Email: your-email@example.com
   - Trigger: ✅

3. **Wait ~60 seconds** (next poll cycle)

4. **Check results:**
   - Email inbox → Should receive invoice PDF
   - Job Log → Should show:
     - Gross USD
     - Profit USD
     - Margin %

### Test 3: Verify Notion Metrics

```python
# In Replit Shell
import os, requests, json

H = {
    "Authorization": f"Bearer {os.getenv('NOTION_TOKEN')}",  # If using direct token
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

db_id = os.getenv("JOB_LOG_DB_ID")

# Query last job
response = requests.post(
    f"https://api.notion.com/v1/databases/{db_id}/query",
    headers=H,
    json={
        "page_size": 1,
        "sorts": [{"timestamp": "last_edited_time", "direction": "descending"}]
    },
    timeout=30
).json()

# Extract revenue fields
props = response["results"][0]["properties"]
metrics = {
    "Gross USD": props.get("Gross USD", {}).get("number"),
    "Profit USD": props.get("Profit USD", {}).get("number"),
    "Margin %": props.get("Margin %", {}).get("number")
}

print(json.dumps(metrics, indent=2))
```

**Expected Output:**
```json
{
  "Gross USD": 2.50,
  "Profit USD": 2.45,
  "Margin %": 98.0
}
```

---

## 🔧 Customization

### Change Default Rate

**Option 1: Environment Variable**
```bash
# In Replit Secrets
DEFAULT_RATE_USD_PER_MIN=10.0
```

**Option 2: Per-Client Rate**
- Edit client in Clients DB
- Update "Rate USD/min" field

**Option 3: Per-Task Override**
- Add "Client Rate USD/min" to Automation Queue
- Set custom rate for specific task

### Customize Invoice Template

**Edit:** `bot/client_manager.py` → `generate_invoice_pdf()`

```python
# Change company name
pdf.drawString(50, y, "Your Company Name - Invoice")

# Change font
pdf.setFont("Helvetica-Bold", 14)

# Add logo (requires image file)
from reportlab.platypus import Image
logo = Image("logo.png", width=100, height=50)
# ... render logo
```

### Customize Email Template

**Edit:** `bot/client_manager.py` → `deliver_invoice_email()`

```python
body = f"""Dear {client_name},

Your custom message here...

Best regards,
Your Team
"""
```

---

## 📈 Revenue Tracking & Analytics

### Notion Formulas for Analytics

**Add to Job Log for automatic calculations:**

1. **Revenue Per Hour:**
   - Property: `Revenue/Hour` (Formula)
   - Formula: `prop("Gross USD") / (prop("Duration (ms)") / 3600000)`

2. **Cost Efficiency:**
   - Property: `Cost Efficiency` (Formula)
   - Formula: `prop("Profit USD") / prop("Cost")`

3. **High Margin Filter:**
   - Create view: "High Margin Jobs"
   - Filter: `Margin % > 90`

### Export to CSV

```python
# Export client revenue report
import csv
from bot.notion_api import get_notion_client

notion = get_notion_client()
db_id = os.getenv("JOB_LOG_DB_ID")

results = notion.databases.query(database_id=db_id)["results"]

with open("revenue_report.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Job", "Client Rate", "Gross", "Profit", "Margin%"])
    
    for page in results:
        props = page["properties"]
        writer.writerow([
            props["Job Name"]["title"][0]["text"]["content"],
            props.get("Client Rate USD/min", {}).get("number", 0),
            props.get("Gross USD", {}).get("number", 0),
            props.get("Profit USD", {}).get("number", 0),
            props.get("Margin %", {}).get("number", 0)
        ])

print("✅ Exported to revenue_report.csv")
```

---

## 🚨 Troubleshooting

### Invoice Not Sent

**Check:**
1. Client email configured correctly?
2. Gmail integration working? (Run `/health` in Telegram)
3. Check logs: `[Client] Invoice delivery failed: ...`

**Solution:**
```python
# Test email manually
from bot.client_manager import deliver_invoice_email

pdf_bytes = b"test"  # Minimal test
result = deliver_invoice_email(
    client_email="your-email@example.com",
    client_name="Test",
    job_id="test123",
    gross=10.0,
    profit=9.0,
    pdf_bytes=pdf_bytes
)
print(f"Sent: {result}")
```

### Revenue Fields Not Showing in Notion

**Check:**
1. Fields created in Job Log database?
2. Client system configured? (`NOTION_CLIENT_DB_ID` set?)
3. Check console: `💼 Client Management System: ✅ Configured`

**Solution:**
```bash
# Verify configuration
python - <<'PY'
from bot.client_manager import is_client_system_configured
print(f"Configured: {is_client_system_configured()}")
PY
```

### Wrong Rate Being Used

**Rate Priority (in order):**
1. Relation → Client Rate from Clients DB
2. Task field → "Client Rate USD/min" in Queue
3. Environment → `DEFAULT_RATE_USD_PER_MIN`
4. Fallback → $5.00/min

**Debug:**
```python
# Check what rate is being used
from bot.processor import TaskProcessor

processor = TaskProcessor()
task_id = "your-task-id"
task = processor.notion.notion.pages.retrieve(page_id=task_id)
client_id, client_email, rate = processor.extract_client_info(task["properties"])

print(f"Client ID: {client_id}")
print(f"Email: {client_email}")
print(f"Rate: ${rate}/min")
```

---

## 🎯 Next Steps

### Extend to Multi-Client Operations

1. **Client Dashboard:**
   - Create Notion view filtering by Client relation
   - Track revenue per client

2. **Monthly Billing:**
   - Aggregate jobs by month
   - Send consolidated invoice

3. **Automated Reminders:**
   - Check unpaid invoices
   - Send follow-up emails

4. **Client Portal:**
   - Build web interface
   - Let clients view invoices
   - Self-service job submission

### Advanced Features

1. **Tiered Pricing:**
   - Volume discounts
   - Peak/off-peak rates

2. **Multi-Currency:**
   - Convert rates
   - Track in different currencies

3. **Tax Calculation:**
   - Add tax percentage
   - Generate tax reports

4. **Payment Integration:**
   - Link to Stripe/PayPal (already installed!)
   - Auto-mark as paid when payment received

---

## 📚 Summary

**What You Built:**
- ✅ Complete client management system
- ✅ Automatic revenue tracking (gross, profit, margin)
- ✅ Professional PDF invoice generation
- ✅ Email delivery via Gmail
- ✅ Comprehensive Notion analytics
- ✅ Mobile-friendly configuration

**How It Works:**
1. Job completes → Calculate revenue
2. Generate PDF invoice
3. Email to client
4. Log all metrics to Notion
5. Track ROI and margins

**Configuration Required:**
- `NOTION_CLIENT_DB_ID` - Client database ID
- `DEFAULT_RATE_USD_PER_MIN` - Default billing rate (optional, default: $5/min)
- Notion database fields (see setup section)

**Your EchoPilot bot is now a full revenue-generating automation platform!** 💰🚀
