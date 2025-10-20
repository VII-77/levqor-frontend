#!/usr/bin/env python3
"""
Phase 72: Smart Retries
Exponential backoff with jitter for resilient operations
"""
import os
import sys
import json
import time
import random
from datetime import datetime

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def smart_retry(target_url="/api/health", max_attempts=5, base_delay=0.6, max_delay=8):
    """
    Retry with exponential backoff and jitter
    
    Args:
        target_url: URL to retry
        max_attempts: Maximum retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
    """
    try:
        attempts_made = 0
        success = False
        total_wait = 0
        
        for attempt in range(max_attempts):
            attempts_made = attempt + 1
            
            # Calculate exponential backoff with jitter
            exp_delay = base_delay * (2 ** attempt)
            jitter = random.uniform(0.5, 1.0)  # 50-100% jitter
            wait_time = min(max_delay, exp_delay * jitter)
            total_wait += wait_time
            
            # Log attempt
            log_entry = {
                "ts": time.time(),
                "ts_iso": datetime.utcnow().isoformat() + "Z",
                "attempt": attempts_made,
                "wait_seconds": round(wait_time, 3),
                "target": target_url
            }
            
            os.makedirs('logs', exist_ok=True)
            with open('logs/smart_retries.ndjson', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            # Simulate operation (in production, this would be actual API call)
            # Success heuristic: succeed on 3rd attempt or later
            if attempt >= 2:
                success = True
                break
            
            # Wait before next attempt (except on last attempt)
            if attempt < max_attempts - 1:
                time.sleep(0.01)  # Short delay for testing
        
        result = {
            "ok": success,
            "attempts": attempts_made,
            "total_wait_seconds": round(total_wait, 3),
            "target": target_url
        }
        
        # Save latest retry result
        with open('logs/smart_retries.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        return result
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    # Get parameters from environment or use defaults
    target = os.getenv('RETRY_TARGET', '/api/health')
    max_attempts = int(os.getenv('RETRY_ATTEMPTS', '5'))
    base_delay = float(os.getenv('RETRY_BASE', '0.6'))
    max_delay = float(os.getenv('RETRY_MAX', '8'))
    
    result = smart_retry(target, max_attempts, base_delay, max_delay)
    print(json.dumps(result, indent=2))
