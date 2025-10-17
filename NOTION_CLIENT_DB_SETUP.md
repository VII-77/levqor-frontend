# 📊 Notion Client Database Setup (5 Minutes)

**Mobile-friendly guide for Galaxy Fold 6**

---

## 📱 Step 1: Create Database in Notion

### On Your Phone or Computer:

1. **Open Notion app/website**

2. **Go to your workspace** (where your other EchoPilot databases are)

3. **Create new database:**
   - Tap **+** (plus icon)
   - Select **Table** → **New database**
   - Or: Type `/table` and select "Table - Inline"

4. **Name it:** `EchoPilot Clients`

---

## ⚙️ Step 2: Add Properties

Your database needs exactly **4 properties**:

### Property 1: Client Name ✅
- **Type:** Title (auto-created)
- **Already there!** Just rename to "Client Name" if needed

### Property 2: Email 📧
- **Click +** (add property)
- **Name:** Email
- **Type:** Email
- **Click "Email" type** from dropdown

### Property 3: Rate USD/min 💰
- **Click +** (add property)
- **Name:** Rate USD/min
- **Type:** Number
- **Format:** Number (default is fine)

### Property 4: Active ✅
- **Click +** (add property)
- **Name:** Active
- **Type:** Checkbox

---

## ✅ Step 3: Verify Properties

Your database should look like this:

| Property Name | Type | Icon |
|--------------|------|------|
| Client Name | Title | Aa |
| Email | Email | ✉️ |
| Rate USD/min | Number | 123 |
| Active | Checkbox | ☐ |

---

## 👤 Step 4: Add Test Client

Create your first client row:

1. **Click "+ New"** (or tap empty row)

2. **Fill in:**
   - **Client Name:** Test Client
   - **Email:** your-email@example.com
   - **Rate USD/min:** 5.0
   - **Active:** ✅ Check the box

3. **Save/Close**

---

## 🔑 Step 5: Copy Database ID

### On Mobile (Galaxy Fold):

1. **Open the database as full page:**
   - Tap the database title at top
   - Select "Open as page" or tap ⋯ → "Open as page"

2. **Copy the URL:**
   - Tap address bar
   - Copy full URL
   - URL looks like: `https://notion.so/xxxxx?v=yyy`

3. **Extract the ID:**
   - The database ID is the part before the `?`
   - It's 32 characters (no dashes, no spaces)
   - Example: `1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p`

### On Computer:

1. **Open database as full page**
2. **Copy URL from address bar**
3. **Get the 32-character ID** before the `?v=`

---

## 🔐 Step 6: Add to Replit Secrets

### On Your Galaxy Fold:

1. **Open Replit app**

2. **Tap ⋮ (three dots)** → **Secrets**

3. **Add first secret:**
   ```
   Name: NOTION_CLIENT_DB_ID
   Value: (paste your 32-character database ID)
   ```

4. **Add second secret (optional but recommended):**
   ```
   Name: DEFAULT_RATE_USD_PER_MIN
   Value: 5.0
   ```

---

## 📊 Step 7: Extend Job Log Database

### Add Revenue Tracking Fields:

1. **Open your Job Log database** in Notion
   - This is the database with your completed jobs

2. **Add these properties** (click + after each):

### Revenue Fields (6 properties):

| Property Name | Type | Settings |
|--------------|------|----------|
| **Client** | Relation | → Select "EchoPilot Clients" database |
| **Client Email** | Email | - |
| **Client Rate USD/min** | Number | Number format |
| **Gross USD** | Number | Number format |
| **Profit USD** | Number | Number format |
| **Margin %** | Number | Number format |

### Payment Fields (2 properties - add if missing):

| Property Name | Type | Settings |
|--------------|------|----------|
| **Payment Link** | URL | - |
| **Payment Status** | Select | Options: Pending, Paid, Failed, Cancelled |

---

## ✅ Verification Checklist

Before you're done, check:

### Clients Database ✅
- [ ] Named "EchoPilot Clients"
- [ ] Has 4 properties: Client Name, Email, Rate USD/min, Active
- [ ] Has at least 1 test client
- [ ] Database ID copied (32 characters)

### Replit Secrets ✅
- [ ] NOTION_CLIENT_DB_ID added
- [ ] DEFAULT_RATE_USD_PER_MIN added (optional)

### Job Log Database ✅
- [ ] Has "Client" relation to Clients DB
- [ ] Has 6 revenue fields
- [ ] Has 2 payment fields

---

## 🧪 Test It!

Run this in Replit Shell:
```bash
python autoconfig.py
```

Should show:
```
✅ Active: Client Management
```

Full test:
```bash
python test_integration.py
```

Should show:
```
✅ PASS: Client Management (Configured)
```

---

## 🎯 What Happens Next

Once configured, for every job:

1. ✅ **Looks up client rate** from Clients database
2. ✅ **Calculates revenue:**
   - Gross = Duration (min) × Client Rate ($/min)
   - Profit = Gross - AI Cost
   - Margin % = (Profit / Gross) × 100
3. ✅ **Creates payment link** (3x AI cost via Stripe)
4. ✅ **Generates PDF invoice** with:
   - Job details
   - Financial breakdown
   - Payment link
5. ✅ **Emails invoice** to client automatically
6. ✅ **Logs everything** to Job Log database

---

## 💡 Example Calculation

**Job Details:**
- Duration: 2.5 minutes
- AI Cost: $0.10
- Client Rate: $5.00/min (from Clients DB)

**Automatic Calculations:**
- Gross USD: 2.5 × $5.00 = **$12.50**
- Payment Link: $0.10 × 3 = **$0.30** (via Stripe)
- Profit USD: $12.50 - $0.10 = **$12.40**
- Margin %: ($12.40 / $12.50) × 100 = **99.2%**

**Client receives:**
- Email with PDF invoice
- Payment link for $0.30 (the small processing fee)
- You track $12.50 revenue in Notion

---

## 🆘 Troubleshooting

### Database ID not working?
- Must be exactly 32 characters
- No dashes, no spaces, no `?v=` part
- Should be the ID from the URL, not the page title

### Client relation not working?
- Make sure Clients database is in same workspace
- Relation should show "EchoPilot Clients" when you select it

### Revenue not calculating?
- Client must be linked via the "Client" relation field
- Client must have "Rate USD/min" filled in
- Client must have "Active" checkbox checked

---

## 📞 Need Help?

Check bot status:
```bash
python quick_setup.py
```

View logs:
```bash
cat /tmp/logs/EchoPilot_Bot_*.log | grep -i client
```

Telegram:
- Send `/status` to @Echopilotai_bot

---

**🎉 Once both databases are set up, your full monetization system is active!**

Payment + Client Management + Revenue Tracking + Invoice Generation = Complete! 💰
