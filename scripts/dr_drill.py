#!/usr/bin/env python3
import os, time, json, glob, random
os.makedirs("logs",exist_ok=True); os.makedirs("replica",exist_ok=True)
def health():
    # simple simulated checks (extend with real pings / file loads)
    checks=[
        {"name":"config_load","ok":True},
        {"name":"files_present","ok": len(glob.glob("backups/**/*",recursive=True))>=1},
        {"name":"boot_probe","ok":True},
    ]
    return checks

def main():
    res={"ts":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
         "region":"replica-a","checks":health()}
    res["ok"]=all(c["ok"] for c in res["checks"])
    path=f"logs/dr_report_{int(time.time())}.json"
    with open(path,"w") as f: json.dump(res,f,indent=2)
    print(path)
if __name__=="__main__": main()
