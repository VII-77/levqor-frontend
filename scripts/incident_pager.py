#!/usr/bin/env python3
"""
Phase 77: Incident Inbox & Pager
Routes CRITICAL incidents to Telegram/Email with deduplication
"""
import os
import sys
import json
import time
import hashlib
import requests
from datetime import datetime, timedelta

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
SMTP_HOST = os.getenv('SMTP_HOST', '')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASS = os.getenv('SMTP_PASS', '')
SMTP_FROM = os.getenv('SMTP_FROM', SMTP_USER)

def get_fingerprint(severity, msg, source):
    """Generate incident fingerprint for deduplication"""
    data = f"{severity}:{source}:{msg[:50]}"
    return hashlib.sha256(data.encode()).hexdigest()[:12]

def send_telegram(message):
    """Send Telegram notification"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return {"ok": False, "error": "Telegram not configured"}
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        for attempt in range(5):
            resp = requests.post(url, json=data, timeout=10)
            if resp.status_code == 200:
                return {"ok": True, "channel": "telegram", "status": 200}
            time.sleep(0.5 * (2 ** attempt))  # Exponential backoff
        
        return {"ok": False, "error": f"Failed after 5 attempts: {resp.status_code}"}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def send_email(subject, body):
    """Send email notification (optional)"""
    if not SMTP_HOST or not SMTP_USER:
        return {"ok": False, "error": "SMTP not configured"}
    
    try:
        import smtplib
        from email.mime.text import MIMEText
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SMTP_FROM
        msg['To'] = SMTP_USER  # Send to self for now
        
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        
        return {"ok": True, "channel": "email", "status": 200}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def raise_incident(severity, msg, source, meta=None):
    """Raise and route an incident"""
    try:
        fingerprint = get_fingerprint(severity, msg, source)
        ts = datetime.utcnow().isoformat() + "Z"
        
        # Check for duplicates in last hour
        cutoff_time = time.time() - 3600
        is_duplicate = False
        
        if os.path.exists('logs/incidents.ndjson'):
            with open('logs/incidents.ndjson', 'r') as f:
                for line in f:
                    try:
                        inc = json.loads(line)
                        if inc.get('fingerprint') == fingerprint:
                            inc_time = datetime.fromisoformat(inc['ts'].replace('Z', '+00:00')).timestamp()
                            if inc_time > cutoff_time:
                                is_duplicate = True
                                break
                    except:
                        continue
        
        # Build incident record
        incident = {
            "event": "incident",
            "ts": ts,
            "fingerprint": fingerprint,
            "severity": severity,
            "msg": msg,
            "source": source,
            "meta": meta or {},
            "duplicate": is_duplicate
        }
        
        # Log incident
        os.makedirs('logs', exist_ok=True)
        with open('logs/incidents.ndjson', 'a') as f:
            f.write(json.dumps(incident) + '\n')
        
        # Route CRITICAL incidents (skip duplicates)
        paging_results = []
        if severity == "CRITICAL" and not is_duplicate:
            message = f"🚨 *CRITICAL INCIDENT*\n\n{msg}\n\nSource: {source}\nFingerprint: {fingerprint}"
            
            # Try Telegram
            telegram_result = send_telegram(message)
            if telegram_result['ok']:
                paging_results.append(telegram_result)
                
                # Log successful page
                with open('logs/incidents.ndjson', 'a') as f:
                    f.write(json.dumps({
                        "event": "page",
                        "ts": ts,
                        "sev": severity,
                        "channel": "telegram",
                        "id": fingerprint,
                        "status": 200
                    }) + '\n')
            
            # Try Email if configured
            if SMTP_HOST:
                email_result = send_email(
                    f"CRITICAL: {msg[:50]}",
                    f"CRITICAL INCIDENT\n\n{msg}\n\nSource: {source}\nTime: {ts}"
                )
                if email_result['ok']:
                    paging_results.append(email_result)
        
        return {
            "ok": True,
            "incident": incident,
            "paged": len(paging_results) > 0,
            "channels": paging_results
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def summarize_incidents():
    """Summarize incidents from last 24 hours"""
    try:
        cutoff_time = time.time() - 86400
        incidents = []
        fingerprints = {}
        
        if os.path.exists('logs/incidents.ndjson'):
            with open('logs/incidents.ndjson', 'r') as f:
                for line in f:
                    try:
                        inc = json.loads(line)
                        if inc.get('event') != 'incident':
                            continue
                        
                        ts = inc.get('ts', '')
                        inc_time = datetime.fromisoformat(ts.replace('Z', '+00:00')).timestamp()
                        
                        if inc_time > cutoff_time:
                            incidents.append(inc)
                            fp = inc.get('fingerprint', 'unknown')
                            if fp not in fingerprints:
                                fingerprints[fp] = {
                                    "count": 0,
                                    "severity": inc.get('severity'),
                                    "msg": inc.get('msg'),
                                    "first_seen": ts,
                                    "last_seen": ts
                                }
                            fingerprints[fp]['count'] += 1
                            fingerprints[fp]['last_seen'] = ts
                    except:
                        continue
        
        summary = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "period_hours": 24,
            "total_incidents": len(incidents),
            "unique_fingerprints": len(fingerprints),
            "by_severity": {},
            "top_incidents": []
        }
        
        # Group by severity
        for inc in incidents:
            sev = inc.get('severity', 'UNKNOWN')
            summary['by_severity'][sev] = summary['by_severity'].get(sev, 0) + 1
        
        # Top incidents by count
        sorted_fps = sorted(fingerprints.items(), key=lambda x: x[1]['count'], reverse=True)
        summary['top_incidents'] = [
            {
                "fingerprint": fp,
                "count": data['count'],
                "severity": data['severity'],
                "msg": data['msg'][:100],
                "first_seen": data['first_seen'],
                "last_seen": data['last_seen']
            }
            for fp, data in sorted_fps[:10]
        ]
        
        # Save summary
        os.makedirs('logs', exist_ok=True)
        with open('logs/incident_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        return {"ok": True, "summary": summary}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    # Run pager check
    result = summarize_incidents()
    print(json.dumps(result, indent=2))
