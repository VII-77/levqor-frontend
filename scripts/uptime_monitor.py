#!/usr/bin/env python3
import os, time, json, urllib.request, sys
BASE = os.getenv("BASE_URL", "http://localhost:5000")
LOG = "logs/uptime.ndjson"
TG = os.getenv("TELEGRAM_BOT_TOKEN"); CHAT=os.getenv("TELEGRAM_CHAT_ID")
STRIKES = int(os.getenv("UPTIME_STRIKES","2"))
INTERVAL = int(os.getenv("UPTIME_INTERVAL_SEC","60"))

def alert(msg):
    if not (TG and CHAT): return
    try:
        data = urllib.parse.urlencode({"chat_id":CHAT,"text":msg}).encode()
        urllib.request.urlopen(f"https://api.telegram.org/bot{TG}/sendMessage", data=data, timeout=10)
    except Exception: pass

def ping_once():
    t0=time.time()
    ok=False; code=None
    try:
        with urllib.request.urlopen(f"{BASE}/", timeout=10) as r:
            code=r.getcode(); ok = (200<=code<500) and (r.read()[:0] or True)
    except Exception: ok=False
    entry={"ts":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
           "latency_ms": int((time.time()-t0)*1000), "ok":ok, "code":code}
    os.makedirs("logs",exist_ok=True)
    with open(LOG,"a") as f: f.write(json.dumps(entry)+"\n")
    return ok, entry

def main(run_once=False):
    strikes=0
    while True:
        ok, e = ping_once()
        strikes = 0 if ok else strikes+1
        if strikes>=STRIKES:
            alert(f"🚨 EchoPilot UPTIME: {strikes} consecutive failures @ {e.get('ts')}")
            strikes=0  # avoid spam; next consecutive block will alert again
        if run_once: return 0 if ok else 1
        time.sleep(INTERVAL)

if __name__=="__main__":
    sys.exit(main("--once" in sys.argv))
