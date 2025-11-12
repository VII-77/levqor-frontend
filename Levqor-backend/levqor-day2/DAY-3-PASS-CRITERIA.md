# Day 3 Pass Criteria - Reference Card

**Quick verification for Nov 12, 09:00 UTC**

---

## ONE-LINER SMOKE TEST

```bash
curl -sI https://levqor.ai | grep -E "age:|x-vercel-cache:" && \
curl -s https://api.levqor.ai/api/intelligence/status | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ Status: {d['meta']['version']}, CID: {d['meta']['correlation_id'][:16]}...\")" && \
curl -s https://api.levqor.ai/api/intelligence/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ Health: ok={d['ok']}\")" && \
curl -s https://api.levqor.ai/public/metrics | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ Metrics: uptime={d['uptime_rolling_7d']}%\")"
```

**Expected Output:**
```
age: 0
x-vercel-cache: MISS
✅ Status: v8.0-burnin, CID: [16 chars]...
✅ Health: ok=True
✅ Metrics: uptime=99.99%
```

---

## DETAILED CRITERIA

### 1. Frontend Freshness
```bash
curl -sI https://levqor.ai | grep -E "age:|x-vercel-cache:"
```
**✅ PASS:** `age: 0` AND `x-vercel-cache: MISS`  
**❌ FAIL:** `age: > 0` OR `x-vercel-cache: HIT`

---

### 2. Intelligence Status (Correlation ID Echo)
```bash
CID="day3-check-$(date +%s)"
curl -s -H "X-Request-ID: $CID" https://api.levqor.ai/api/intelligence/status
```
**✅ PASS:** HTTP 200 + `meta.correlation_id == $CID`  
**❌ FAIL:** Non-200 OR correlation_id mismatch OR missing meta

---

### 3. Intelligence Health (No Criticals)
```bash
curl -s https://api.levqor.ai/api/intelligence/health
```
**✅ PASS:** HTTP 200 + `ok: true` + `count: 0` (or no criticals array)  
**❌ FAIL:** Non-200 OR `ok: false` OR criticals present

---

### 4. Public Metrics (Updated Timestamp)
```bash
curl -s https://api.levqor.ai/public/metrics
```
**✅ PASS:** HTTP 200 + `last_updated` within last 5 minutes + `uptime_rolling_7d ≥ 99.98`  
**❌ FAIL:** Non-200 OR stale timestamp OR uptime < 99.98

---

### 5. Error Rate
```bash
./scripts/daily_burnin_check.sh | grep "Error Rate"
```
**✅ PASS:** ≤ 0.5%  
**❌ FAIL:** > 0.5%

---

### 6. P1 Incidents
```bash
./scripts/daily_burnin_check.sh | grep "P1 Incidents"
```
**✅ PASS:** = 0  
**❌ FAIL:** > 0

---

### 7. Daily Cost
```bash
./scripts/daily_burnin_check.sh | grep "Daily Cost"
```
**✅ PASS:** ≤ $10.0  
**❌ FAIL:** > $10.0

---

## IF ANY CRITERIA FAILS

**Send the failing output block:**

1. **Frontend stale:**
   ```bash
   curl -sI https://levqor.ai | head -20
   ```

2. **Status endpoint:**
   ```bash
   curl -s https://api.levqor.ai/api/intelligence/status
   ```

3. **Health endpoint:**
   ```bash
   curl -s https://api.levqor.ai/api/intelligence/health
   ```

4. **Metrics endpoint:**
   ```bash
   curl -s https://api.levqor.ai/public/metrics
   ```

**One-liner fix will be provided for each failure mode.**

---

## CURRENT BASELINE (Day 2)

```
Frontend: age: 0, x-vercel-cache: MISS ✅
Status: correlation_id matched ✅
Health: ok: true, criticals: 0 ✅
Metrics: uptime: 99.99%, timestamp: 1762899161 ✅
Error Rate: 0.0% ✅
P1 Incidents: 0 ✅
Cost: $7.0 ✅

All 7 criteria: PASS
```

**Target for Day 3:** Maintain all green, no regressions

---

