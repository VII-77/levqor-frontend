#!/usr/bin/env python3
"""Production Alerts - Monitor webhook failures, payment errors, revenue dips"""
import json, os, time, hashlib, glob
from datetime import datetime, timedelta, timezone

LOG = "logs/production_alerts.ndjson"
SCH = "logs/scheduler.log"
WEB = "logs/stripe_webhooks.ndjson"
NOW = datetime.now(timezone.utc)

def ndjson_write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f: 
        f.write(json.dumps(obj, ensure_ascii=False)+"\n")

def read_tail_lines(path, max_lines=5000):
    try:
        with open(path,"r") as f: 
            return f.readlines()[-max_lines:]
    except FileNotFoundError: 
        return []

def window(lines, minutes):
    start = NOW - timedelta(minutes=minutes)
    out=[]
    for ln in lines:
        try:
            j=json.loads(ln)
            ts_str = j.get("ts","").replace("Z","+00:00")
            if not ts_str:
                continue
            ts = datetime.fromisoformat(ts_str)
            if ts>=start: 
                out.append(j)
        except Exception: 
            pass
    return out

def main():
    # 1) Webhook failures (>3 in 5m)
    web = window(read_tail_lines(WEB), 5)
    fails = sum(1 for e in web if e.get("ok") is False or e.get("status") not in (200, "200"))

    # 2) Payment error rate (>5% last hour) — derive from webhooks if present
    hwin = window(read_tail_lines(WEB), 60)
    total = len(hwin) or 1
    errors = sum(1 for e in hwin if e.get("ok") is False)
    err_rate = errors/total

    # 3) Revenue dip (>30% DoD) — simple file-based rollup from finance logs if present
    rev_today = 0.0
    rev_yday  = 0.0
    for p in glob.glob("logs/payments_*.ndjson"):
        for ln in read_tail_lines(p, 20000):
            try:
                j=json.loads(ln)
                amt=j.get("amount_usd",0.0)
                d=j.get("date") or j.get("ts","")[:10]
                if d==NOW.strftime("%Y-%m-%d"): 
                    rev_today += float(amt)
                elif d==(NOW - timedelta(days=1)).strftime("%Y-%m-%d"): 
                    rev_yday += float(amt)
            except Exception: 
                pass
    revenue_change = 0.0 if rev_yday==0 else (rev_today-rev_yday)/rev_yday

    sev_webhook = "CRITICAL" if fails>3 else "OK"
    sev_payerr  = "CRITICAL" if err_rate>0.05 else "OK"
    sev_revdip  = "WARNING"  if revenue_change<-0.30 else "OK"

    out = {
        "ts": NOW.isoformat().replace("+00:00","Z"),
        "event":"production_alerts",
        "webhook_failures_5m": fails,
        "payment_error_rate_1h": round(err_rate,4),
        "revenue_change_DoD": round(revenue_change,4),
        "severity": {
            "webhook":sev_webhook,
            "payments":sev_payerr,
            "revenue":sev_revdip
        }
    }
    ndjson_write(LOG, out)
    print(json.dumps(out))

if __name__=="__main__": 
    main()
