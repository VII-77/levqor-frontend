#!/usr/bin/env python3
import os, hashlib, json, time, shutil, glob
SRC="backups"
TMP="tmp/restore_check"
LOG="logs/backup_verify.ndjson"

def sha256p(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20), b""): h.update(b)
    return h.hexdigest()

def run():
    os.makedirs("logs",exist_ok=True)
    if os.path.exists(TMP): shutil.rmtree(TMP)
    os.makedirs(TMP,exist_ok=True)
    mismatches=[]
    for f in glob.glob(f"{SRC}/**/*", recursive=True):
        if os.path.isdir(f): continue
        rel=os.path.relpath(f,SRC)
        dst=os.path.join(TMP,rel); os.makedirs(os.path.dirname(dst),exist_ok=True)
        shutil.copy2(f,dst)
        if sha256p(f)!=sha256p(dst): mismatches.append(rel)
    entry={"ts":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"ok": len(mismatches)==0,"mismatches":mismatches}
    with open(LOG,"a") as fo: fo.write(json.dumps(entry)+"\n")
    return entry

if __name__=="__main__":
    e=run()
    if not e["ok"]: print("MISMATCH", e["mismatches"]); exit(1)
