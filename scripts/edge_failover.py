#!/usr/bin/env python3
"""
EchoPilot Edge Failover Monitor
Phase 109: Monitors primary health endpoint and triggers Railway failover if needed
Runs every 5 minutes via scheduler
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

# Configuration
def get_primary_url():
    """Get primary URL with proper scheme"""
    domain = os.getenv('REPLIT_DOMAINS', '')
    
    if not domain:
        return 'http://localhost:5000'
    
    # Take first domain if multiple
    domain = domain.split(',')[0].strip()
    
    # Add https:// if no scheme
    if not domain.startswith('http://') and not domain.startswith('https://'):
        domain = f'https://{domain}'
    
    return domain

PRIMARY_URL = get_primary_url()
RAILWAY_FALLBACK_URL = os.getenv('RAILWAY_FALLBACK_URL', '')
HEALTH_ENDPOINT = '/health'
TIMEOUT_SECONDS = 10
MAX_FAILURES = 3

# Logging
LOG_FILE = Path('logs/edge_failover.ndjson')
LOG_FILE.parent.mkdir(exist_ok=True)

# State tracking
STATE_FILE = Path('logs/edge_failover_state.json')

def log_event(event, data=None):
    """Write NDJSON log entry"""
    entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event': event
    }
    if data:
        entry.update(data)
    
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    
    print(json.dumps(entry), flush=True)

def load_state():
    """Load failover state from disk"""
    if not STATE_FILE.exists():
        return {
            'consecutive_failures': 0,
            'last_check': None,
            'failover_active': False,
            'last_failover_time': None
        }
    
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {
            'consecutive_failures': 0,
            'last_check': None,
            'failover_active': False,
            'last_failover_time': None
        }

def save_state(state):
    """Save failover state to disk"""
    state['last_check'] = datetime.utcnow().isoformat() + 'Z'
    
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def check_health(url):
    """
    Check health endpoint
    Returns (is_healthy, response_time_ms, details)
    """
    try:
        start = datetime.utcnow()
        response = requests.get(
            f"{url}{HEALTH_ENDPOINT}",
            timeout=TIMEOUT_SECONDS
        )
        end = datetime.utcnow()
        
        response_time_ms = int((end - start).total_seconds() * 1000)
        
        if response.status_code == 200:
            data = response.json()
            return True, response_time_ms, data
        else:
            return False, response_time_ms, {
                'status_code': response.status_code,
                'error': 'Non-200 response'
            }
    
    except requests.Timeout:
        return False, TIMEOUT_SECONDS * 1000, {'error': 'timeout'}
    
    except Exception as e:
        return False, 0, {'error': str(e)}

def trigger_failover():
    """
    Trigger failover to Railway
    This would typically update DNS or load balancer config
    For now, we just log and alert
    """
    log_event('failover_triggered', {
        'primary_url': PRIMARY_URL,
        'fallback_url': RAILWAY_FALLBACK_URL,
        'action': 'alert_ops_team'
    })
    
    # Send alert to Telegram if configured
    try:
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        telegram_chat = os.getenv('TELEGRAM_CHAT_ID')
        
        if telegram_token and telegram_chat:
            alert_message = f"""
🚨 FAILOVER TRIGGERED

Primary: {PRIMARY_URL}
Status: DOWN
Fallback: {RAILWAY_FALLBACK_URL}

Action: Manual intervention required
"""
            
            requests.post(
                f'https://api.telegram.org/bot{telegram_token}/sendMessage',
                json={
                    'chat_id': telegram_chat,
                    'text': alert_message
                },
                timeout=5
            )
    except Exception as e:
        log_event('failover_alert_failed', {'error': str(e)})

def check_failover_health():
    """Check if Railway fallback is healthy"""
    if not RAILWAY_FALLBACK_URL:
        return False, 0, {'error': 'No fallback URL configured'}
    
    return check_health(RAILWAY_FALLBACK_URL)

def main():
    """Main edge failover monitoring logic"""
    log_event('monitor_started', {'ok': True})
    
    # Load state
    state = load_state()
    
    try:
        # Check primary health
        log_event('checking_primary', {'url': PRIMARY_URL})
        is_healthy, response_time_ms, details = check_health(PRIMARY_URL)
        
        if is_healthy:
            # Primary is healthy
            log_event('primary_healthy', {
                'response_time_ms': response_time_ms,
                'uptime_seconds': details.get('uptime_seconds'),
                'dependencies': details.get('dependencies')
            })
            
            # Reset failure counter
            state['consecutive_failures'] = 0
            state['failover_active'] = False
            
        else:
            # Primary is unhealthy
            state['consecutive_failures'] += 1
            
            log_event('primary_unhealthy', {
                'consecutive_failures': state['consecutive_failures'],
                'max_failures': MAX_FAILURES,
                'error': details.get('error')
            })
            
            # Trigger failover if exceeded threshold
            if state['consecutive_failures'] >= MAX_FAILURES and not state['failover_active']:
                # Check if fallback is healthy
                fallback_healthy, fallback_time, fallback_details = check_failover_health()
                
                if fallback_healthy:
                    trigger_failover()
                    state['failover_active'] = True
                    state['last_failover_time'] = datetime.utcnow().isoformat() + 'Z'
                else:
                    log_event('failover_unavailable', {
                        'error': 'Both primary and fallback are down',
                        'fallback_details': fallback_details
                    })
        
        # Save updated state
        save_state(state)
        
        # Summary
        print(f"\n✅ Edge Failover Monitor:", flush=True)
        print(f"   Primary: {'✅ healthy' if is_healthy else '❌ unhealthy'}", flush=True)
        print(f"   Response time: {response_time_ms}ms", flush=True)
        print(f"   Consecutive failures: {state['consecutive_failures']}/{MAX_FAILURES}", flush=True)
        print(f"   Failover active: {state['failover_active']}", flush=True)
        
        log_event('monitor_complete', {
            'ok': True,
            'healthy': is_healthy,
            'response_time_ms': response_time_ms,
            'consecutive_failures': state['consecutive_failures'],
            'failover_active': state['failover_active']
        })
        
    except Exception as e:
        log_event('monitor_error', {'error': str(e), 'type': type(e).__name__})
        print(f"❌ Edge failover monitor failed: {e}", file=sys.stderr, flush=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
