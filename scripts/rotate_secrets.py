#!/usr/bin/env python3
import os, time, json, secrets, string
LOG="logs/secret_rotations.ndjson"
def gen_key(n=48):
    alphabet=string.ascii_letters+string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(n))

def safe_write(path, val):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: f.write(val)

def main():
    ts=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
    changes={}
    if os.getenv("ROTATE_DASHBOARD_KEY","1")=="1":
        dk=gen_key()
        safe_write("secrets/runtime/DASHBOARD_KEY", dk)
        changes["DASHBOARD_KEY"]="rotated"
    if os.getenv("ROTATE_STRIPE_WEBHOOK","1")=="1":
        wh=gen_key(64)
        safe_write("secrets/runtime/STRIPE_WEBHOOK_SECRET", wh)
        changes["STRIPE_WEBHOOK_SECRET"]="rotated"
    entry={"ts":ts,"changes":list(changes.keys())}
    os.makedirs("logs",exist_ok=True)
    with open(LOG,"a") as f: f.write(json.dumps(entry)+"\n")
if __name__=="__main__": main()
