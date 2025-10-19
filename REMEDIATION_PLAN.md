# 🛠️ EchoPilot Remediation Plan

## Current Status: 38.3% → Target: ≥90%

### Breakdown by Category

| Category | Current | Weight | Target | Impact |
|----------|---------|--------|--------|--------|
| **Schema** | 23.1% | 30% | 100% | +23.1 pts |
| **Connectivity** | 40.0% | 25% | 100% | +15.0 pts |
| **Security** | 70.0% | 20% | 90% | +4.0 pts |
| **Cost Guardrails** | 33.3% | 15% | 100% | +10.0 pts |
| **Marketing** | 23.3% | 10% | 70% | +4.7 pts |

**Projected Final Score:** 38.3 + 23.1 + 15.0 + 4.0 + 10.0 + 4.7 = **95.1%** ✅

---

## HIGH-IMPACT ACTIONS (Required for ≥90%)

### 1️⃣ Create 8 Missing Databases (+23.1 pts)
**Status:** 3/13 verified → Need 10/13 for 100%

**Action:** Cannot auto-create without NOTION_PARENT_PAGE_ID
**Solution:** Document schemas for manual creation OR get parent page ID

**Missing DBs:**
- ❌ Finance (NOTION_FINANCE_DB_ID)
- ❌ Ops Monitor (NOTION_OPS_MONITOR_DB_ID)
- ❌ Governance Ledger (NOTION_GOVERNANCE_DB_ID)
- ❌ Region Compliance (NOTION_REGION_COMPLIANCE_DB_ID)
- ❌ Partner Keys (NOTION_PARTNERS_DB_ID)
- ❌ Referrals (NOTION_REFERRALS_DB_ID)
- ❌ Growth Metrics (NOTION_GROWTH_METRICS_DB_ID)
- ❌ Pricing (NOTION_PRICING_DB_ID)
- ❌ Cost Dashboard (NOTION_COST_DB_ID)

**Plus Fix:**
- ⚠️  Automation Queue (exists but not accessible)

**Time:** 15-30 minutes manual OR instant with parent page ID
**Cost:** FREE

### 2️⃣ Fix Failing Endpoints (+15 pts)
**Status:** 2/5 passing → Need 5/5 for 100%

**Issues:**
- ❌ /supervisor → HTTP 404 (actually returns HTML, test expects JSON)
- ❌ /ops-report → HTTP 503 (auto_operator module error)
- ❌ /forecast → HTTP 404 (forecast_engine error)

**Fixes:**
1. Update /supervisor to return JSON when `?format=json` param
2. Fix auto_operator.py missing function
3. Fix forecast_engine.py errors

**Time:** 30 minutes
**Cost:** FREE

### 3️⃣ Add Cost Guardrails (+10 pts)
**Status:** 33.3% → Need 100%

**Implement:**
1. Model policy: Default gpt-4o-mini, upgrade only for QA refine
2. Whisper caching: SHA256 deduplication
3. (Already have: 60s polling ✅)

**Time:** 1 hour
**Cost:** FREE (saves $20-50/month)

### 4️⃣ Add HEALTH_TOKEN (+2 pts)
**Status:** Security 70% → 90%

**Action:** Add HEALTH_TOKEN to environment, require for verbose /health

**Time:** 5 minutes
**Cost:** FREE

### 5️⃣ Basic Marketing Automation (+4.7 pts)
**Status:** 23.3% → Need 70%

**Minimum Viable:**
1. Growth Metrics views (schema exists, add views)
2. Referral auto-credit logic
3. (Skip email outreach for now)

**Time:** 1 hour
**Cost:** FREE

---

## EXECUTION PRIORITY

### Phase 1: Quick Wins (30 min)
1. ✅ Add HEALTH_TOKEN secret
2. ✅ Fix /supervisor endpoint (JSON response option)
3. ✅ Fix /ops-report endpoint  
4. ✅ Fix /forecast endpoint

**Impact:** +17 pts → 55.3%

### Phase 2: Database Creation (Manual, 15-30 min)
1. ❌ User must create 8 databases OR provide NOTION_PARENT_PAGE_ID
2. ❌ User must fix Automation Queue access

**Impact:** +23.1 pts → 78.4%

### Phase 3: Code Implementations (2 hours)
1. ✅ Model policy (gpt-4o-mini default)
2. ✅ Whisper caching
3. ✅ Marketing automation basics

**Impact:** +14.7 pts → 93.1% ✅

---

## WHAT I CAN DO NOW

✅ **Automated Fixes (Phase 1 + 3):**
- Fix endpoints
- Add security tokens
- Implement cost guardrails
- Build marketing automation
- **Result: ~70% readiness**

❌ **Blocked (Phase 2 - User Required):**
- Create Notion databases (need parent page ID or manual creation)
- **Blocks final ~23 points**

---

## RECOMMENDATION

### Option A: User Provides NOTION_PARENT_PAGE_ID
1. User creates empty Notion page
2. User shares page ID
3. I auto-create all 8 databases
4. **Result: 95%+ readiness in 1 hour**

### Option B: Manual Database Creation
1. I provide exact schemas (already in database_setup.py)
2. User creates 8 databases manually
3. User adds IDs to environment
4. **Result: 95%+ readiness in 2 hours**

### Option C: Proceed Without Databases
1. I fix everything else
2. **Result: ~70% readiness**
3. User creates databases later to reach 95%

---

## NEXT STEPS

**Recommend:** Proceed with Option A or C
- Option A gets us to 95% fastest (if user has 5 min now)
- Option C gets us to 70% now, 95% later

**What should I do?**
