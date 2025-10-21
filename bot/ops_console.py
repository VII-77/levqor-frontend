#!/usr/bin/env python3
"""
EchoPilot Operator Console (Phase 112)
Secure admin copilot for running operational commands with audit trail
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Allow-listed commands
ALLOWED_COMMANDS = {
    'restart_scheduler': {
        'description': 'Restart the scheduler workflow',
        'command': ['pkill', '-HUP', '-f', 'exec_scheduler.py'],
        'dry_run_safe': True
    },
    'run_backup': {
        'description': 'Trigger manual DR backup',
        'command': ['python3', 'scripts/dr_backups.py'],
        'dry_run_safe': True
    },
    'reconcile_payments': {
        'description': 'Run payment reconciliation',
        'command': ['python3', 'scripts/payment_reconciliation.py'],
        'dry_run_safe': True
    },
    'tail_logs': {
        'description': 'Get last 50 lines of scheduler log',
        'command': ['tail', '-n', '50', 'logs/scheduler.log'],
        'dry_run_safe': True
    },
    'clear_cache': {
        'description': 'Clear application cache',
        'command': ['rm', '-rf', '/tmp/echopilot_cache'],
        'dry_run_safe': True
    },
    'sync_warehouse': {
        'description': 'Trigger data warehouse sync',
        'command': ['python3', 'scripts/warehouse_sync.py'],
        'dry_run_safe': True
    }
}

def audit_log(action, user, details, dry_run=False):
    """Log all operator actions to audit trail"""
    log_entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'action': action,
        'user': user,
        'dry_run': dry_run,
        'details': details
    }
    
    log_file = Path('logs/ops_console.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    return log_entry

def execute_command(verb, user='system', confirm=False):
    """
    Execute operator command with dry-run support
    
    Args:
        verb: Command verb from ALLOWED_COMMANDS
        user: Username or identifier
        confirm: If True, actually execute. If False, dry-run only.
    
    Returns:
        dict with ok, message, output, dry_run fields
    """
    if verb not in ALLOWED_COMMANDS:
        audit_log('invalid_command', user, {'verb': verb}, dry_run=True)
        return {
            'ok': False,
            'error': f'Invalid command: {verb}',
            'allowed': list(ALLOWED_COMMANDS.keys())
        }
    
    cmd_info = ALLOWED_COMMANDS[verb]
    command = cmd_info['command']
    description = cmd_info['description']
    
    if not confirm:
        # Dry-run mode
        audit_log(verb, user, {
            'description': description,
            'command': ' '.join(command),
            'status': 'dry_run'
        }, dry_run=True)
        
        return {
            'ok': True,
            'message': f'Dry-run: {description}',
            'command': ' '.join(command),
            'dry_run': True,
            'note': 'Set confirm=true to execute'
        }
    
    # Actual execution
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout if result.returncode == 0 else result.stderr
        
        audit_log(verb, user, {
            'description': description,
            'command': ' '.join(command),
            'status': 'executed',
            'exit_code': result.returncode,
            'output_length': len(output)
        }, dry_run=False)
        
        return {
            'ok': result.returncode == 0,
            'message': f'Executed: {description}',
            'command': ' '.join(command),
            'dry_run': False,
            'exit_code': result.returncode,
            'output': output[:1000]  # Limit output to 1000 chars
        }
        
    except subprocess.TimeoutExpired:
        audit_log(verb, user, {
            'description': description,
            'command': ' '.join(command),
            'status': 'timeout',
            'error': 'Command timed out after 60s'
        }, dry_run=False)
        
        return {
            'ok': False,
            'error': 'Command timed out after 60 seconds',
            'dry_run': False
        }
        
    except Exception as e:
        audit_log(verb, user, {
            'description': description,
            'command': ' '.join(command),
            'status': 'error',
            'error': str(e)
        }, dry_run=False)
        
        return {
            'ok': False,
            'error': str(e),
            'dry_run': False
        }

def get_command_list():
    """Get list of available commands"""
    return {
        verb: {
            'description': info['description'],
            'dry_run_safe': info['dry_run_safe']
        }
        for verb, info in ALLOWED_COMMANDS.items()
    }

if __name__ == '__main__':
    # Test dry-run
    print("Testing dry-run mode:")
    result = execute_command('tail_logs', user='test_user', confirm=False)
    print(json.dumps(result, indent=2))
    
    print("\nAvailable commands:")
    print(json.dumps(get_command_list(), indent=2))
