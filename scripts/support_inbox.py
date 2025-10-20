#!/usr/bin/env python3
"""
Phase 61: Support Inbox Digest
Monitors support email inbox via IMAP (dry-run safe)
"""
import os
import sys
import json
import time
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def fetch_inbox():
    """Fetch unread emails from support inbox"""
    try:
        host = os.getenv('IMAP_HOST', '')
        user = os.getenv('IMAP_USER', '')
        password = os.getenv('IMAP_PASS', '')
        
        items = []
        dry_run = not all([host, user, password])
        
        if not dry_run:
            try:
                import imaplib
                import email as email_lib
                
                # Connect to IMAP server
                mail = imaplib.IMAP4_SSL(host)
                mail.login(user, password)
                mail.select('INBOX')
                
                # Search for unseen emails
                typ, data = mail.search(None, '(UNSEEN)')
                
                # Process up to 20 unread emails
                for num in data[0].split()[:20]:
                    _, msg_data = mail.fetch(num, '(RFC822)')
                    email_body = msg_data[0][1]
                    email_message = email_lib.message_from_bytes(email_body)
                    
                    items.append({
                        "from": email_message.get('From', 'unknown'),
                        "subject": email_message.get('Subject', '(no subject)'),
                        "date": email_message.get('Date', ''),
                        "message_id": email_message.get('Message-ID', '')
                    })
                
                mail.logout()
            
            except Exception as e:
                items.append({
                    "error": "imap_failed",
                    "detail": str(e)
                })
        else:
            # Dry-run mode - generate sample data
            items = [{
                "from": "dryrun@example.com",
                "subject": "Sample Support Request",
                "date": datetime.utcnow().isoformat(),
                "message_id": "<dryrun@example.com>"
            }]
        
        # Save digest
        result = {
            "ts": time.time(),
            "ts_iso": datetime.utcnow().isoformat() + "Z",
            "count": len(items),
            "dry_run": dry_run,
            "items": items
        }
        
        os.makedirs('logs', exist_ok=True)
        with open('logs/support_digest.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        # Also append to NDJSON
        with open('logs/support_digest.ndjson', 'a') as f:
            f.write(json.dumps({"ts": result['ts_iso'], "count": result['count'], "dry_run": dry_run}) + '\n')
        
        return {
            "ok": True,
            "count": len(items),
            "dry_run": dry_run
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = fetch_inbox()
    print(json.dumps(result, indent=2))
