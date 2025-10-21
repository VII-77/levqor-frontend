#!/usr/bin/env python3
import json
import time
import statistics
import subprocess
import requests
import os
import psutil
import datetime

LOG = "logs/anomaly_guard.ndjson"
os.makedirs("logs", exist_ok=True)

def log(entry):
    """Append entry to NDJSON log file"""
    with open(LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

def check_latency():
    """Check health endpoint latency and status"""
    try:
        t0 = time.time()
        r = requests.get("http://localhost:5000/health", timeout=10)
        latency = (time.time() - t0) * 1000
        status = r.json().get("status", "unknown")
        ok = status.lower() == "healthy"
        return {"latency_ms": latency, "ok": ok}
    except Exception as e:
        return {"latency_ms": 9999, "ok": False, "error": str(e)}

def check_resources():
    """Check system resource usage"""
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "mem": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
    }

def anomaly_score(vals, mean, stdev):
    """Calculate anomaly score using z-score (number of standard deviations from mean)"""
    if stdev == 0:
        return 0
    return abs(vals - mean) / stdev

def main():
    """Main anomaly detection routine"""
    ts = datetime.datetime.utcnow().isoformat()
    lat = check_latency()
    res = check_resources()
    data = {"ts": ts, "lat": lat, "res": res}

    # Calculate anomaly score based on historical latency
    try:
        with open(LOG, "r") as f:
            hist = [json.loads(l)["lat"]["latency_ms"] for l in f if "lat" in json.loads(l)][-50:]
        mean = statistics.mean(hist)
        stdev = statistics.pstdev(hist)
        score = anomaly_score(lat["latency_ms"], mean, stdev)
    except Exception:
        mean = stdev = score = 0

    data["score"] = score
    data["mean"] = mean
    data["stdev"] = stdev
    log(data)

    # Auto-heal triggers
    trigger_heal = False
    reasons = []
    
    if not lat["ok"]:
        trigger_heal = True
        reasons.append("health_check_failed")
    
    if score > 3:
        trigger_heal = True
        reasons.append(f"latency_anomaly_3sigma (score={score:.2f})")
    
    if res["cpu"] > 90:
        trigger_heal = True
        reasons.append(f"cpu_critical ({res['cpu']:.1f}%)")
    
    if res["mem"] > 90:
        trigger_heal = True
        reasons.append(f"memory_critical ({res['mem']:.1f}%)")
    
    if res["disk"] > 90:
        reasons.append(f"disk_warning ({res['disk']:.1f}%)")

    if trigger_heal:
        alert = {
            "event": "anomaly_trigger",
            "ts": ts,
            "reasons": reasons,
            "latency": lat["latency_ms"],
            "score": score,
            "cpu": res["cpu"],
            "mem": res["mem"],
            "disk": res["disk"],
        }
        log(alert)
        print(f"⚠️  Auto-Heal triggered: {', '.join(reasons)}")
        
        # Trigger self-heal
        try:
            subprocess.run(["python3", "scripts/self_heal.py"], check=False, timeout=60)
        except Exception as e:
            print(f"❌ Self-heal failed: {e}")
    else:
        print(f"✅ All metrics normal: {round(lat['latency_ms'], 1)}ms, CPU:{res['cpu']:.1f}%, MEM:{res['mem']:.1f}%")

if __name__ == "__main__":
    main()
