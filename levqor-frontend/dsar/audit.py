"""
DSAR Audit Logging
Comprehensive logging for compliance and regulatory requirements
"""
from uuid import uuid4
from time import time


def log_dsar_event(db_connection, user_id, email, action, ip_address=None, user_agent=None, request_id=None, export_id=None, details=None):
    """
    Log a DSAR-related event to the audit log
    
    Args:
        db_connection: SQLite database connection
        user_id: User ID
        email: User email
        action: Action type (e.g., 'request_created', 'export_downloaded')
        ip_address: Optional IP address
        user_agent: Optional user agent string
        request_id: Optional DSAR request ID
        export_id: Optional DSAR export ID
        details: Optional JSON string with additional details
    """
    log_id = str(uuid4())
    timestamp = time()
    
    db_connection.execute("""
        INSERT INTO dsar_audit_log 
        (id, user_id, email, action, timestamp, ip_address, user_agent, request_id, export_id, details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (log_id, user_id, email, action, timestamp, ip_address, user_agent, request_id, export_id, details))
    
    db_connection.commit()
    
    # Also log to console for ops visibility
    print(f"[DSAR AUDIT] {action} | User: {user_id} | Email: {email} | IP: {ip_address or 'N/A'} | Time: {timestamp}")
