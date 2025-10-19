# 🔐 Environment Variable Updates Required

## 1. HEALTH_TOKEN (Security Enhancement)

**Add this to your Replit Secrets:**

```
HEALTH_TOKEN=kBH09gN1vrWGxx5_rG4N9Qxi4sp56mot46WrR0rZVmM
```

**Purpose:** Secures verbose /health endpoint access

**Usage:** `/health?token=<HEALTH_TOKEN>` for detailed diagnostics

---

## 2. Missing Notion Database IDs (For 95% Readiness)

**Current Status:** 3/13 databases verified (23.1% schema score)

**Need to create and add these 8 database IDs:**

```bash
# Enterprise Features Databases
NOTION_FINANCE_DB_ID=
NOTION_OPS_MONITOR_DB_ID=
NOTION_GOVERNANCE_DB_ID=
NOTION_REGION_COMPLIANCE_DB_ID=
NOTION_PARTNERS_DB_ID=
NOTION_REFERRALS_DB_ID=
NOTION_GROWTH_METRICS_DB_ID=
NOTION_PRICING_DB_ID=
NOTION_COST_DB_ID=
```

**Plus fix this existing database:**
- AUTOMATION_QUEUE_DB_ID exists but is not accessible (check Notion integration permissions)

---

## How to Create Databases

### Option A: Automated (5 minutes)

1. Create an empty page in Notion
2. Get the page ID from the URL: `https://notion.so/workspace/<PAGE_ID>?v=...`
3. Add to Replit Secrets:
   ```
   NOTION_PARENT_PAGE_ID=<PAGE_ID>
   ```
4. Run:
   ```bash
   python bot/database_setup.py
   ```
5. Copy the generated database IDs to Replit Secrets

### Option B: Manual (30 minutes)

1. Create each database manually in Notion using the schemas in `bot/database_setup.py`
2. Copy each database ID from the URL
3. Add all IDs to Replit Secrets

---

## Impact on Readiness Score

**Current:** 38.3%

**After adding HEALTH_TOKEN + endpoint fixes:** ~55%

**After creating all 8 databases:** ~95% ✅

---

## Priority

1. **High Priority:** Add HEALTH_TOKEN (5 seconds)
2. **Critical for 95%:** Create 8 Notion databases (15-30 min)
3. **Optional:** Fix Automation Queue access permissions

