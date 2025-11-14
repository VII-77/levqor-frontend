"""
Data Retention Cleanup Engine
Automatically deletes expired records based on retention policies
"""

import sqlite3
import logging
import os
from time import time
from typing import Dict
from retention.config import DATA_RETENTION, TIMESTAMP_FIELDS, is_protected

log = logging.getLogger("levqor")

def cleanup_expired_records(db_path: str = None, dry_run: bool = False) -> Dict[str, int]:
    """
    Delete records older than their retention policy.
    
    Args:
        db_path: Path to SQLite database (defaults to DATAB ASE_PATH or levqor.db)
        dry_run: If True, only count records without deleting
        
    Returns:
        Dictionary with counts of deleted records per table
        
    SAFETY:
        - Never deletes billing/financial core records beyond retention
        - Never deletes user accounts
        - Only deletes operational logs and ephemeral data
        - Logs all deletions to audit trail
    """
    if db_path is None:
        db_path = os.getenv("DATABASE_PATH", "levqor.db")
    
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    now = time()
    
    deleted_counts = {}
    
    for table_name, retention_days in DATA_RETENTION.items():
        # Skip if no retention policy (keep forever)
        if retention_days is None:
            log.debug(f"[RETENTION] Skipping {table_name} (no retention policy)")
            continue
        
        # Skip protected tables
        if is_protected(table_name):
            log.warning(f"[RETENTION] Skipping protected table {table_name}")
            continue
        
        # Get timestamp field for this table
        timestamp_field = TIMESTAMP_FIELDS.get(table_name, "created_at")
        
        if timestamp_field is None:
            # Special handling for date fields (analytics_aggregates)
            if table_name == "analytics_aggregates":
                cutoff_date = now - (retention_days * 24 * 60 * 60)
                cutoff_str = time.strftime("%Y-%m-%d", time.gmtime(cutoff_date))
                
                try:
                    if dry_run:
                        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE day < ?", (cutoff_str,))
                        count = cursor.fetchone()[0]
                    else:
                        cursor.execute(f"DELETE FROM {table_name} WHERE day < ?", (cutoff_str,))
                        count = cursor.rowcount
                        db.commit()
                    
                    deleted_counts[table_name] = count
                    
                    if count > 0:
                        action = "Would delete" if dry_run else "Deleted"
                        log.info(f"[RETENTION] {action} {count} rows from {table_name} (older than {retention_days} days)")
                        
                        # Audit log entry
                        if not dry_run:
                            _log_cleanup_audit(cursor, table_name, count, retention_days, now)
                            db.commit()
                
                except sqlite3.OperationalError as e:
                    log.warning(f"[RETENTION] Table {table_name} not found or schema mismatch: {e}")
                    deleted_counts[table_name] = 0
                
                continue
        
        # Calculate cutoff timestamp
        cutoff_timestamp = now - (retention_days * 24 * 60 * 60)
        
        try:
            # Check if table and column exist
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in cursor.fetchall()]
            
            if not columns:
                log.warning(f"[RETENTION] Table {table_name} does not exist, skipping")
                deleted_counts[table_name] = 0
                continue
            
            if timestamp_field not in columns:
                log.warning(f"[RETENTION] Column {timestamp_field} not found in {table_name}, skipping")
                deleted_counts[table_name] = 0
                continue
            
            # Count/delete expired records
            if dry_run:
                cursor.execute(
                    f"SELECT COUNT(*) FROM {table_name} WHERE {timestamp_field} < ?",
                    (cutoff_timestamp,)
                )
                count = cursor.fetchone()[0]
            else:
                cursor.execute(
                    f"DELETE FROM {table_name} WHERE {timestamp_field} < ?",
                    (cutoff_timestamp,)
                )
                count = cursor.rowcount
                db.commit()
            
            deleted_counts[table_name] = count
            
            if count > 0:
                action = "Would delete" if dry_run else "Deleted"
                log.info(f"[RETENTION] {action} {count} rows from {table_name} (older than {retention_days} days)")
                
                # Audit log entry
                if not dry_run:
                    _log_cleanup_audit(cursor, table_name, count, retention_days, now)
                    db.commit()
        
        except sqlite3.OperationalError as e:
            log.error(f"[RETENTION] Error processing {table_name}: {e}")
            deleted_counts[table_name] = 0
        
        except Exception as e:
            log.error(f"[RETENTION] Unexpected error processing {table_name}: {e}")
            deleted_counts[table_name] = 0
    
    db.close()
    
    total_deleted = sum(deleted_counts.values())
    mode = "DRY RUN" if dry_run else "COMPLETED"
    log.info(f"[RETENTION] Cleanup {mode}: {total_deleted} total rows across {len(deleted_counts)} tables")
    
    return deleted_counts


def _log_cleanup_audit(cursor, table_name: str, count: int, retention_days: int, timestamp: float):
    """Write cleanup action to DSAR audit log for compliance"""
    try:
        from uuid import uuid4
        
        audit_id = str(uuid4())
        action = f"retention_cleanup_{table_name}"
        details = f"Deleted {count} rows older than {retention_days} days"
        
        cursor.execute("""
            INSERT INTO dsar_audit_log (id, user_id, email, action, timestamp, ip_address, user_agent, details)
            VALUES (?, NULL, 'system', ?, ?, '127.0.0.1', 'retention_cleanup', ?)
        """, (audit_id, action, timestamp, details))
        
    except Exception as e:
        log.warning(f"[RETENTION] Failed to write audit log: {e}")


# CLI test interface
if __name__ == "__main__":
    import sys
    
    dry_run = "--dry-run" in sys.argv
    
    print("="*60)
    print("Data Retention Cleanup Engine")
    print("="*60)
    print(f"Mode: {'DRY RUN (no deletions)' if dry_run else 'LIVE (will delete)'}")
    print()
    
    results = cleanup_expired_records(dry_run=dry_run)
    
    print("\nResults:")
    print("-"*60)
    for table, count in sorted(results.items()):
        if count > 0:
            print(f"  {table:30s} {count:6d} rows")
    
    total = sum(results.values())
    print("-"*60)
    print(f"  {'TOTAL':30s} {total:6d} rows")
    print()
    
    if dry_run:
        print("✓ Dry run complete - no data was deleted")
        print("  Run without --dry-run to perform actual deletion")
    else:
        print("✓ Cleanup complete")
