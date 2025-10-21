#!/usr/bin/env python3
"""
EchoPilot Advanced DR Restore Check (Phase 115)
Verifies backup integrity with dry-run restore tests
"""

import os
import sys
import json
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path

def log_event(event_type, details=None):
    """Log DR events"""
    log_entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event_type': event_type,
        'details': details or {}
    }
    
    log_file = Path('logs/dr_restore_check.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def find_latest_backup():
    """Find the most recent backup file"""
    backup_dir = Path('dr_backups')
    if not backup_dir.exists():
        return None
    
    backups = list(backup_dir.glob('backup_*.tar.gz'))
    if not backups:
        return None
    
    # Sort by modification time
    latest = max(backups, key=lambda p: p.stat().st_mtime)
    return latest

def verify_tarball_integrity(backup_file):
    """Verify tarball can be opened and has expected structure"""
    try:
        with tarfile.open(backup_file, 'r:gz') as tar:
            members = tar.getmembers()
            
            # Check for critical files
            critical_files = ['metadata.json', 'db_snapshot.sql']
            found_files = {m.name for m in members}
            
            missing = []
            for critical in critical_files:
                if critical not in found_files:
                    missing.append(critical)
            
            return {
                'valid': len(missing) == 0,
                'total_files': len(members),
                'missing_critical': missing
            }
            
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }

def dry_run_restore(backup_file):
    """Perform dry-run restore to verify backup contents"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            with tarfile.open(backup_file, 'r:gz') as tar:
                # Extract to temp directory
                tar.extractall(temp_dir)
                
                # Verify metadata
                metadata_file = Path(temp_dir) / 'metadata.json'
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                else:
                    metadata = {}
                
                # Check database snapshot size
                db_file = Path(temp_dir) / 'db_snapshot.sql'
                db_size = db_file.stat().st_size if db_file.exists() else 0
                
                # Check logs
                log_files = list(Path(temp_dir).glob('logs/*.ndjson'))
                
                return {
                    'status': 'ok',
                    'metadata': metadata,
                    'db_snapshot_size': db_size,
                    'log_files': len(log_files),
                    'extractable': True
                }
                
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'extractable': False
        }

def run_restore_check():
    """Main restore check routine"""
    try:
        print("Running DR restore check...")
        
        # Find latest backup
        print("\n1. Finding latest backup...")
        backup_file = find_latest_backup()
        
        if not backup_file:
            print("✗ No backups found")
            log_event('no_backups_found', {})
            return 1
        
        print(f"✓ Found backup: {backup_file.name}")
        
        # Verify tarball integrity
        print("\n2. Verifying tarball integrity...")
        integrity = verify_tarball_integrity(backup_file)
        
        if not integrity['valid']:
            print(f"✗ Integrity check failed: {integrity}")
            log_event('integrity_check_failed', integrity)
            return 1
        
        print(f"✓ Tarball valid ({integrity['total_files']} files)")
        
        # Dry-run restore
        print("\n3. Performing dry-run restore...")
        restore_result = dry_run_restore(backup_file)
        
        if restore_result.get('status') != 'ok':
            print(f"✗ Dry-run restore failed: {restore_result.get('error')}")
            log_event('restore_check_failed', restore_result)
            return 1
        
        print(f"✓ Dry-run restore successful")
        print(f"  - DB snapshot: {restore_result['db_snapshot_size']} bytes")
        print(f"  - Log files: {restore_result['log_files']}")
        
        # Build report
        report = {
            'ts': datetime.utcnow().isoformat() + 'Z',
            'backup_file': str(backup_file),
            'backup_age_hours': (datetime.now() - datetime.fromtimestamp(backup_file.stat().st_mtime)).total_seconds() / 3600,
            'integrity': integrity,
            'restore_test': restore_result,
            'status': 'ok'
        }
        
        # Log success
        log_event('restore_check_complete', report)
        
        # Save report
        report_file = Path('logs/dr_restore_report.json')
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✓ DR restore check complete. Report: {report_file}")
        return 0
        
    except Exception as e:
        log_event('restore_check_error', {'error': str(e)})
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(run_restore_check())
