#!/usr/bin/env python3
"""
EchoPilot Compliance Webhooks & Audit API (Phase 118)
Immutable audit chain and compliance event webhooks
"""

import json
import hmac
import hashlib
from datetime import datetime
from pathlib import Path
from collections import deque

def log_audit_event(event_type, user, action, resource, details=None):
    """
    Log audit event to immutable audit chain
    Each event is chained with hash of previous event for integrity
    """
    log_file = Path('logs/audit_chain.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Get hash of previous event for chaining
    prev_hash = get_last_audit_hash()
    
    # Build audit entry
    entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event_type': event_type,
        'user': user,
        'action': action,
        'resource': resource,
        'details': details or {},
        'prev_hash': prev_hash
    }
    
    # Calculate hash of this entry
    entry_str = json.dumps(entry, sort_keys=True)
    entry_hash = hashlib.sha256(entry_str.encode()).hexdigest()[:16]
    entry['hash'] = entry_hash
    
    # Write to audit log
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    
    return entry

def get_last_audit_hash():
    """Get hash of last audit entry for chaining"""
    try:
        log_file = Path('logs/audit_chain.ndjson')
        if not log_file.exists():
            return 'genesis'
        
        with open(log_file, 'r') as f:
            lines = deque(f, maxlen=1)
        
        if not lines:
            return 'genesis'
        
        last_entry = json.loads(lines[0])
        return last_entry.get('hash', 'genesis')
        
    except:
        return 'genesis'

def verify_audit_chain():
    """Verify integrity of audit chain"""
    try:
        log_file = Path('logs/audit_chain.ndjson')
        if not log_file.exists():
            return {
                'valid': True,
                'entries': 0,
                'message': 'No audit log exists yet'
            }
        
        entries = []
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except:
                    continue
        
        # Verify chain integrity
        for i, entry in enumerate(entries):
            # Skip first entry
            if i == 0:
                if entry.get('prev_hash') != 'genesis':
                    return {
                        'valid': False,
                        'error': f'First entry should reference genesis, got {entry.get("prev_hash")}',
                        'entry_index': i
                    }
                continue
            
            # Check previous hash matches
            prev_entry = entries[i - 1]
            expected_prev_hash = prev_entry.get('hash')
            actual_prev_hash = entry.get('prev_hash')
            
            if expected_prev_hash != actual_prev_hash:
                return {
                    'valid': False,
                    'error': f'Chain broken at entry {i}',
                    'expected_prev_hash': expected_prev_hash,
                    'actual_prev_hash': actual_prev_hash,
                    'entry_index': i
                }
        
        return {
            'valid': True,
            'entries': len(entries),
            'message': 'Audit chain integrity verified'
        }
        
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }

def get_audit_chain(limit=100, offset=0):
    """Get audit chain entries"""
    try:
        log_file = Path('logs/audit_chain.ndjson')
        if not log_file.exists():
            return {'entries': [], 'total': 0}
        
        entries = []
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except:
                    continue
        
        total = len(entries)
        
        # Apply offset and limit
        start = offset
        end = min(offset + limit, total)
        page = entries[start:end]
        
        return {
            'entries': page,
            'total': total,
            'offset': offset,
            'limit': limit,
            'has_more': end < total
        }
        
    except Exception as e:
        return {
            'entries': [],
            'total': 0,
            'error': str(e)
        }

def send_compliance_webhook(event_data, webhook_url=None):
    """
    Send compliance event to external webhook
    
    Args:
        event_data: Event data to send
        webhook_url: Target webhook URL (optional, defaults to env var)
    """
    import os
    import requests
    
    if not webhook_url:
        webhook_url = os.getenv('COMPLIANCE_WEBHOOK_URL')
    
    if not webhook_url:
        return {
            'sent': False,
            'reason': 'No webhook URL configured'
        }
    
    try:
        # Sign payload with HMAC
        secret = os.getenv('COMPLIANCE_WEBHOOK_SECRET', 'default_secret')
        payload = json.dumps(event_data)
        signature = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Send webhook
        response = requests.post(
            webhook_url,
            json=event_data,
            headers={
                'X-EchoPilot-Signature': signature,
                'Content-Type': 'application/json',
                'User-Agent': 'EchoPilot-Compliance/1.0'
            },
            timeout=10
        )
        
        return {
            'sent': True,
            'status_code': response.status_code,
            'response_time_ms': response.elapsed.total_seconds() * 1000
        }
        
    except Exception as e:
        return {
            'sent': False,
            'error': str(e)
        }

def log_compliance_event(event_type, severity, description, metadata=None):
    """Log compliance-relevant event and optionally send webhook"""
    # Log to compliance events
    log_entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event_type': event_type,
        'severity': severity,
        'description': description,
        'metadata': metadata or {}
    }
    
    log_file = Path('logs/compliance_events.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    # Send webhook for high-severity events
    if severity in ['high', 'critical']:
        webhook_result = send_compliance_webhook(log_entry)
        log_entry['webhook_sent'] = webhook_result.get('sent', False)
    
    return log_entry

if __name__ == '__main__':
    # Test audit chain
    print("Testing compliance webhooks and audit chain...")
    
    print("\n1. Adding audit entries")
    log_audit_event('data_access', 'user123', 'read', 'customer_data', {'record_count': 10})
    log_audit_event('data_modification', 'admin456', 'update', 'pricing', {'field': 'price', 'old': 100, 'new': 120})
    log_audit_event('data_deletion', 'admin456', 'delete', 'old_logs', {'count': 50})
    
    print("\n2. Verifying audit chain integrity")
    verification = verify_audit_chain()
    print(json.dumps(verification, indent=2))
    
    print("\n3. Getting audit chain")
    chain = get_audit_chain(limit=5)
    print(f"  Total entries: {chain['total']}")
    print(f"  Retrieved: {len(chain['entries'])}")
    
    print("\n4. Logging compliance event")
    comp_event = log_compliance_event(
        'gdpr_data_request',
        'high',
        'User requested data export under GDPR',
        {'user_id': 'user123', 'email': 'user@example.com'}
    )
    print(json.dumps(comp_event, indent=2))
    
    print("\n✓ Compliance tests complete")
