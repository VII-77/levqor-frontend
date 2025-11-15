# CLEANUP CANDIDATES - 2025-11-15

**Generated:** 2025-11-15 21:20 UTC  
**Purpose:** Identify safe candidates for archival (diagnostic reports, logs, historical docs)  
**Safety:** NO code, config, migrations, or deployment scripts will be touched

---

## CRITICAL DIRECTORIES (NEVER TOUCH)
The following contain production code and MUST remain untouched:
- `backend/`, `server/`, `src/`, `modules/`, `monitors/`, `migrations/`
- `templates/`, `scripts/`, `tests/`, `public/`, `api/`, `compliance/`
- `revenue-engine/`, `retention/`, `billing/`, `dunning/`, `dsar/`
- `levqor-site/` (active frontend)
- All `.py`, `.ts`, `.tsx`, `.js`, `.json`, `.sql` files

---

## INVENTORY SUMMARY

**Total markdown files in root:** 110 files  
**Suspected duplicate directories:** 3 (Levqor-backend/, levqor-fresh/, levqor-frontend/)  
**Live codebase:** Current directory (/home/runner/workspace)

---

## CLEANUP CANDIDATES (CONSERVATIVE)

### Category 1: Duplicate Historical Reports in Root (Root-level only)

These appear to be diagnostic/status reports from previous development phases:

| Path | Size | Reason | Safe? |
|------|------|--------|-------|
| DAY-1-DEPLOYMENT-CHECKLIST.md | 2.7K | Historical deployment doc | ✅ |
| DAY-1-VERIFICATION-REPORT.md | 11K | Historical verification | ✅ |
| DAY-2-COMPLETION-SUMMARY.md | 7.4K | Historical completion doc | ✅ |
| DAY-2-DEPLOYMENT-COMPLETE.md | 4.6K | Historical deployment doc | ✅ |
| DAY-2-FINAL-VERIFICATION.md | 5.4K | Historical verification | ✅ |
| DAY-2-FREE-TIER-COMPLETION.md | 8.3K | Historical completion doc | ✅ |
| PHASE_6_3_SUMMARY.md | 5.3K | Historical phase doc | ✅ |
| PHASE_6_4_SUMMARY.md | 9.6K | Historical phase doc | ✅ |
| PHASE_6_5_STATUS.md | 6.9K | Historical status doc | ✅ |
| PHASE_6_5_SUMMARY.md | 6.6K | Historical phase doc | ✅ |
| PHASE_7_PRICING_FINALIZED.md | 8.4K | Historical pricing doc | ✅ |
| BURN-IN-COMMENCED.md | 8.4K | Historical burn-in doc | ✅ |
| SOFT-START-STATUS.md | 6.2K | Historical status doc | ✅ |
| FOUR-ACTIONS-COMPLETE.md | 11K | Historical action doc | ✅ |
| EXPANSION-MONITORING-SUMMARY.md | 7.4K | Historical summary | ✅ |
| TRIAGE_COMPLETION_REPORT.md | 3.5K | Historical triage doc | ✅ |
| TRIAGE_GAP_ANALYSIS.md | 2.9K | Historical analysis | ✅ |
| V6_5_ROUTING_REPORT.md | 6.0K | Historical routing doc | ✅ |
| CI-FIX-REPORT.md | 15K | Historical CI fix doc | ✅ |
| CI-FIX-SUMMARY.md | 3.6K | Historical CI summary | ✅ |
| BUILD-WARNINGS-ANALYSIS.md | 15K | Historical build doc | ✅ |
| FRONTEND-NUCLEAR-CLEANUP-REPORT.md | 4.2K | Historical cleanup doc | ✅ |
| FRONTEND-STALE-BUILD-FIX.md | 2.1K | Historical fix doc | ✅ |
| NUCLEAR-AUDIT-REPORT.md | 15K | Historical audit doc | ✅ |
| NUCLEAR-CLEANUP-COMPLETE-GUIDE.md | 6.8K | Historical cleanup guide | ✅ |
| README-NUCLEAR-CLEANUP.md | 4.2K | Historical cleanup readme | ✅ |
| STRIPE-CHECKOUT-DIAGNOSIS.md | 8.2K | Historical diagnosis | ✅ |
| STRIPE_CHECKOUT_FIXED.md | 3.4K | Historical fix doc | ✅ |
| STRIPE-CHECKOUT-FIX.md | 4.6K | Historical fix doc | ✅ |
| STRIPE-CHECKOUT-SUCCESS.md | 5.2K | Historical success doc | ✅ |
| VERCEL-CLEANUP-GUIDE.md | 6.1K | Historical cleanup guide | ✅ |
| VERCEL-FIX-REPORT.md | 3.4K | Historical fix report | ✅ |
| BACKEND-INFRA-DIAGNOSTICS.md | 13K | Historical diagnostics | ✅ |
| PRODUCTION-VERIFICATION-QUICK.md | 2.1K | Historical verification (superseded) | ✅ |
| VALIDATION-STEP-1.md | 3.9K | Historical validation doc | ✅ |
| DEPLOYMENT_REPORT.md | ? | Historical deployment | ✅ |
| DEPLOYMENT_STATUS.md | ? | Historical status | ✅ |
| VERIFICATION_REPORT.md | 3.6K | Historical verification | ✅ |
| IMPLEMENTATION_SUMMARY.md | 4.0K | Historical implementation | ✅ |
| STATUS_SUMMARY.md | 1.3K | Historical status | ✅ |
| RELEASE-VALIDATION-REPORT.md | 11K | Historical validation | ✅ |
| FINAL_SHIP_SUMMARY.md | 6.7K | Historical ship summary | ✅ |

**Category 1 Total:** ~40 files, estimated ~260KB

---

### Category 2: Implementation Status Reports (May contain useful info - REVIEW FIRST)

These contain implementation details that might be referenced:

| Path | Size | Reason | Safe? |
|------|------|--------|-------|
| BACKEND-AUTOMATION-REPORT.md | 23K | Automation details | ⚠️ KEEP (may be referenced) |
| BILLING_DUNNING_IMPLEMENTATION_STATUS.md | 21K | Billing implementation | ⚠️ KEEP (may be referenced) |
| COMPLIANCE_IMPLEMENTATION_STATUS.md | 27K | Compliance details | ⚠️ KEEP (may be referenced) |
| DSAR_IMPLEMENTATION_SUMMARY.md | ? | DSAR implementation | ⚠️ KEEP (may be referenced) |
| HIGH_RISK_BLOCKING_IMPLEMENTATION_STATUS.md | 17K | Risk implementation | ⚠️ KEEP (may be referenced) |
| TRUST_UX_IMPLEMENTATION_STATUS.md | 23K | Trust UX details | ⚠️ KEEP (may be referenced) |
| FEATURES_STATUS_REPORT.md | 12K | Features status | ⚠️ KEEP (may be referenced) |
| SUPPORT-AI-IMPLEMENTATION-SUMMARY.md | 9.3K | Support AI details | ⚠️ KEEP (may be referenced) |
| STRIPE-CHECK-ENDPOINT-REPORT.md | 20K | NEW: Just created today | ⚠️ KEEP (current work) |

**Category 2: KEEP ALL - may contain useful implementation details**

---

### Category 3: Critical Documentation (NEVER MOVE)

These must remain in root for user access:

| Path | Reason |
|------|--------|
| README.md | Primary documentation |
| replit.md | Project memory/preferences |
| HOW_TO_DEPLOY.md | Deployment instructions |
| LAUNCH-CHECKLIST.md | Launch procedures |
| PRODUCTION_CHECKLIST.md | Production checklist |
| START_HERE.md | User entry point |
| BEGINNER_DEPLOYMENT_GUIDE.md | User guide |
| QUICK_SETUP_GUIDE.md | Setup guide |
| READY_TO_DEPLOY.md | Deployment status |
| LAUNCH_INSTRUCTIONS.md | Launch guide |
| PRODUCTION-VERIFICATION-REPORT.md | Current verification |
| LEVQOR-PRODUCTION-REALITY-REPORT.md | Production status |
| GENESIS-v8.0-READINESS.md | Current readiness |
| SECURITY-HARDENING-REPORT.md | Security details |
| INTEGRITY-PACK-GUIDE.md | Integrity guide |

**Category 3: KEEP ALL IN ROOT - critical for user**

---

### Category 4: Automation & Setup Guides (KEEP IN ROOT)

| Path | Reason |
|------|--------|
| AUTOMATION-SETUP.md | Automation guide |
| AUTOMATION-NOTION-SUMMARY.md | Notion automation |
| OPENAI-ENABLEMENT-COMPLETE.md | OpenAI setup |
| NOTION-QUICK-START.md | Notion quick start |
| NOTION-SETUP-GUIDE.md | Notion setup |
| STRIPE_3_TIER_SETUP.md | Stripe setup |
| STRIPE_SETUP_CHECKLIST.md | Stripe checklist |

**Category 4: KEEP ALL - active setup guides**

---

### Category 5: Monitoring & Operations (KEEP)

| Path | Reason |
|------|--------|
| ACCESS-REVIEW-CHECKLIST.md | Security checklist |
| 2FA-ENABLEMENT-GUIDE.md | Security guide |
| API_KEY_ROTATION.md | Security procedure |
| BACKUP-RESTORE-PROCEDURE.md | Backup guide |
| CACHE-PURGE-INSTRUCTIONS.md | Operations |
| COST_REPORTING_PLAN.md | Cost management |
| EXPANSION-ROADMAP.md | Roadmap |
| INTELLIGENCE-LOGGING-ENHANCED.md | Logging details |

**Category 5: KEEP ALL - operational procedures**

---

### Category 6: EchoPilot Reports (Check for duplication)

| Path | Size | Reason | Safe? |
|------|------|--------|-------|
| ECHOPILOT-FINAL-HEALTH-REPORT.md | ? | Final health report | ⚠️ CHECK |
| ECHOPILOT-FINAL-HEALTH-SUMMARY.md | ? | Summary version | ⚠️ CHECK |
| BACKEND-DEPLOYMENT-STATUS.md | 6.1K | Deployment status | ⚠️ CHECK |
| FRONTEND-API-CONNECTIVITY.md | 8.2K | API connectivity | ⚠️ CHECK |
| FRONTEND-DEPLOYMENT-STATUS.md | 2.9K | Frontend status | ⚠️ CHECK |

**Note:** These were just created - need to check if they're still useful or historical

---

### Category 7: Cloudflare & External Service Docs

| Path | Size | Reason | Safe? |
|------|------|--------|-------|
| CLOUDFLARE-CONFIGURATION.md | 6.9K | Configuration | ⚠️ KEEP (config reference) |
| CLOUDFLARE-MANUAL-TASKS.md | 6.9K | Manual tasks | ⚠️ KEEP (procedures) |
| ADD_TO_VERCEL.md | 1.9K | Vercel setup | ⚠️ KEEP (setup guide) |

**Category 7: KEEP ALL - configuration reference**

---

### Category 8: Logs (Safe to archive)

| Path | Size | Reason | Safe? |
|------|------|--------|-------|
| integrity_reports/ECHOPILOT-FINAL-HEALTH-RAW.log | 4K | Raw log file | ✅ Archive |
| .deploy.log (if in Levqor-backend/) | 4K | Deployment log | ✅ Archive |

**Category 8 Total:** ~8KB of logs

---

### Category 9: Duplicate Directory Structures (VERY DANGEROUS - DO NOT AUTO-DELETE)

**WARNING:** The following directories appear to be old copies but might contain unique files:
- `Levqor-backend/` (5,598 inodes) - Contains duplicate .md files
- `levqor-fresh/` (5,444 inodes) - Contains duplicate .md files
- `levqor-frontend/` (6,234 inodes) - Contains duplicate .md files

**Action:** DO NOT delete these directories without manual verification. They might contain:
- Unique historical records
- Different versions of implementations
- Important archival data

**Recommendation:** User should manually review these directories before any deletion.

---

## PROPOSED SAFE ACTIONS

### Phase 1: Archive Historical Reports (Conservative)

**Create archive:**
```
archive/2025-11-15-legacy-docs/
archive/2025-11-15-legacy-logs/
```

**Move Category 1 files only** (40 historical phase/diagnostic reports)
- All DAY-* reports
- All PHASE_* summaries
- Nuclear cleanup reports
- Historical fix/diagnosis reports
- Build/CI historical docs

**Total to move:** ~40 files, ~260KB

### Phase 2: Archive Logs

**Move Category 8 files:**
- integrity_reports/ECHOPILOT-FINAL-HEALTH-RAW.log
- Any .deploy.log files

**Total to move:** ~2 files, ~8KB

### Phase 3: Manual Review Needed

**User must manually review:**
1. Levqor-backend/, levqor-fresh/, levqor-frontend/ directories
2. Whether ECHOPILOT reports are still needed
3. Whether implementation status reports can be consolidated

---

## SAFETY VERIFICATION CHECKLIST

Before proceeding:
- ✅ Verified current directory is live codebase (run.py exists)
- ✅ Identified backend/ as production code (NEVER TOUCH)
- ✅ Only targeting historical .md reports and .log files
- ✅ NO code, config, or deployment scripts in candidates
- ✅ Keeping all critical documentation in root
- ✅ Using git mv (not rm) for traceability
- ✅ Will test backend /health after each phase

---

## ESTIMATED IMPACT

**Files to move:** ~42 files  
**Disk space reclaimed:** ~268KB (negligible - this is about cleanup, not space)  
**Risk level:** VERY LOW (only historical documentation)  
**Rollback:** Easy via git (all changes are moves, not deletes)

---

## NEXT STEPS

1. Review this candidates list
2. Confirm Category 1 files are safe to archive
3. Execute Phase 1 (move historical reports)
4. Test backend /health endpoint
5. Execute Phase 2 (move logs)
6. Test backend /health endpoint
7. Create summary report
8. Commit changes (DO NOT PUSH)

---

**Report Status:** READY FOR REVIEW  
**Recommendation:** Proceed with Phase 1 & 2 only (conservative approach)
