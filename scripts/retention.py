#!/usr/bin/env python3
"""
EchoPilot Retention Cleanup
Keeps newest 30 files for each pattern, deletes older ones.
"""

import os
import json
from pathlib import Path
from datetime import datetime

# Retention config
KEEP_COUNT = 30
PATTERNS = [
    'logs/exec_briefs/brief_*.json',
    'logs/exec_briefs/brief_*.html',
    'logs/exec_ingest_*.json',
    'logs/exec_analysis_*.json',
    'logs/daily_report_*.json',
]

log_file = Path('logs/retention.log')
log_file.parent.mkdir(exist_ok=True)

def log_retention(data):
    """Log retention actions"""
    entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        **data
    }
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def cleanup_pattern(pattern):
    """Cleanup files matching pattern"""
    files = sorted(Path('.').glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    
    if len(files) <= KEEP_COUNT:
        log_retention({
            'pattern': pattern,
            'total': len(files),
            'deleted': 0,
            'kept': len(files),
            'action': 'skip'
        })
        return 0
    
    to_delete = files[KEEP_COUNT:]
    deleted_count = 0
    deleted_size = 0
    
    for file_path in to_delete:
        try:
            size = file_path.stat().st_size
            file_path.unlink()
            deleted_count += 1
            deleted_size += size
        except Exception as e:
            log_retention({
                'pattern': pattern,
                'file': str(file_path),
                'error': str(e),
                'action': 'delete_failed'
            })
    
    log_retention({
        'pattern': pattern,
        'total': len(files),
        'deleted': deleted_count,
        'kept': KEEP_COUNT,
        'size_freed_kb': deleted_size // 1024,
        'action': 'cleanup'
    })
    
    return deleted_count

def main():
    """Run retention cleanup"""
    print(f"🧹 EchoPilot Retention Cleanup (keep newest {KEEP_COUNT})")
    
    total_deleted = 0
    for pattern in PATTERNS:
        deleted = cleanup_pattern(pattern)
        total_deleted += deleted
        if deleted > 0:
            print(f"   ✅ {pattern}: deleted {deleted} old files")
        else:
            print(f"   ⏭  {pattern}: no cleanup needed")
    
    if total_deleted > 0:
        print(f"\n✅ Cleanup complete: {total_deleted} files deleted")
    else:
        print(f"\n✅ All clean: no files to delete")
    
    log_retention({
        'action': 'summary',
        'total_deleted': total_deleted,
        'patterns_checked': len(PATTERNS)
    })

if __name__ == '__main__':
    main()
