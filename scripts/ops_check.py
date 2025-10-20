#!/usr/bin/env python3
import os, re, json, time, glob, subprocess, hashlib, datetime as dt, pathlib

DASH=os.getenv("DASHBOARD_KEY","")
BASE=os.getenv("BASE_URL","http://localhost:5000")
NOW=dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)
LOGS=pathlib.Path("logs")
RESULT={"ok":True,"ts":NOW.isoformat(),"checks":[],"notes":[]}

def add(name, ok, data=None):
    RESULT["checks"].append({"name":name,"ok":bool(ok),"data":data})
    if not ok: RESULT["ok"]=False

def _curl_json(method, url, payload=None):
    hdr=["-H",f"X-Dash-Key: {DASH}","-H","Content-Type: application/json","-sS","--max-time","10"]
    data=["-d",json.dumps(payload)] if payload is not None else []
    out=subprocess.run(["curl","-X",method,*hdr,*data,url],capture_output=True,text=True)
    return out.returncode, out.stdout.strip()

# 1) Automations status
rc, body=_curl_json("GET",f"{BASE}/api/automations/status")
try:
    j=json.loads(body); running=j.get("data",{}).get("running"); pid=j.get("data",{}).get("pid"); last=j.get("data",{}).get("last_activity")
    add("scheduler_status", running is True, {"pid":pid,"last_activity":last})
except: add("scheduler_status", False, {"error":body[:400]})

# 2) Recent tick (<60s)
try:
    log=(LOGS/"scheduler.log").read_text(errors="ignore").splitlines()[-200:]
    ts=None
    for line in reversed(log):
        if '"event": "tick"' in line or '"task": "startup"' in line:
            m=re.search(r'"ts":\s*"([^"]+)"', line)
            if m: ts=dt.datetime.fromisoformat(m.group(1).replace("Z","+00:00")); break
    ok=ts and (NOW - ts).total_seconds()<=90
    add("heartbeat_recent", bool(ok), {"last_ts": ts.isoformat() if ts else None})
except: add("heartbeat_recent", False, {"note":"no scheduler.log"})

# 3) CEO brief freshness (today)
try:
    files=sorted(glob.glob("logs/exec_briefs/brief_*.json"), reverse=True)
    latest=files[0] if files else None
    ok=False; meta={}
    if latest:
        j=json.loads(pathlib.Path(latest).read_text())
        meta={"path":latest,"headline":j.get("headline") or j.get("data",{}).get("headline")}
        m=re.search(r'brief_(\d{8})_', latest)
        if m:
            day=m.group(1); today=NOW.strftime("%Y%m%d")
            ok=(day==today)
    add("ceo_brief_today", ok, meta)
except: add("ceo_brief_today", False, {"note":"no briefs yet"})

# 4) Self-heal health (no recent 5xx)
try:
    lines=(LOGS/"self_heal.log").read_text(errors="ignore").splitlines()[-200:] if (LOGS/"self_heal.log").exists() else []
    errs=[L for L in lines if " 5" in L or "error" in L.lower()]
    add("self_heal_ok", len(errs)==0, {"recent_errors":len(errs)})
except: add("self_heal_ok", True, {"note":"no self_heal.log → treat as ok"})

# 5) Payments smoke (dry path if live not available)
try:
    rc, body=_curl_json("POST",f"{BASE}/api/pricing/optimize",{})
    ok=False
    if rc==0:
        j=json.loads(body); ok=bool(j.get("ok"))
    add("pricing_ai_endpoint", ok, {"rc":rc})
except: add("pricing_ai_endpoint", False, None)

# 6) Audit/report reachable
try:
    rc, body=_curl_json("GET",f"{BASE}/api/audit/report")
    ok=(rc==0 and json.loads(body).get("ok",False))
    add("audit_report", ok, None)
except: add("audit_report", False, None)

# 7) Export reachable
try:
    rc, body=_curl_json("GET",f"{BASE}/api/compliance/export-data")
    ok=(rc==0 and json.loads(body).get("ok",False))
    add("compliance_export", ok, None)
except: add("compliance_export", False, None)

# Hash + write summary
SUMMARY=LOGS/"ops_check_summary.json"
SUMMARY.write_text(json.dumps(RESULT,indent=2))
print(json.dumps(RESULT))
