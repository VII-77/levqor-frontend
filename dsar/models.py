"""
DSAR database models and schema
Handles Data Subject Access Request tracking and export management
"""

def init_dsar_tables(db_connection):
    """Initialize DSAR-related tables in the database"""
    
    # DSAR Requests table - tracks all data export requests
    db_connection.execute("""
        CREATE TABLE IF NOT EXISTS dsar_requests(
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            email TEXT NOT NULL,
            requested_at REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            type TEXT NOT NULL DEFAULT 'export',
            ip_address TEXT,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dsar_requests_user_id ON dsar_requests(user_id)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dsar_requests_status ON dsar_requests(status)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dsar_requests_requested_at ON dsar_requests(requested_at)")
    
    # DSAR Exports table - contains export file metadata and security tokens
    db_connection.execute("""
        CREATE TABLE IF NOT EXISTS dsar_exports(
            id TEXT PRIMARY KEY,
            request_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            created_at REAL NOT NULL,
            expires_at REAL NOT NULL,
            storage_path TEXT NOT NULL,
            download_token TEXT UNIQUE NOT NULL,
            download_token_expires_at REAL NOT NULL,
            otp_hash TEXT NOT NULL,
            otp_expires_at REAL NOT NULL,
            downloaded_at REAL,
            data_categories TEXT,
            FOREIGN KEY (request_id) REFERENCES dsar_requests(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    db_connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_dsar_exports_download_token ON dsar_exports(download_token)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dsar_exports_user_id ON dsar_exports(user_id)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dsar_exports_expires_at ON dsar_exports(expires_at)")
    
    # DSAR Audit Log - comprehensive logging for compliance
    db_connection.execute("""
        CREATE TABLE IF NOT EXISTS dsar_audit_log(
            id TEXT PRIMARY KEY,
            user_id TEXT,
            email TEXT,
            action TEXT NOT NULL,
            timestamp REAL NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            request_id TEXT,
            export_id TEXT,
            details TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (request_id) REFERENCES dsar_requests(id),
            FOREIGN KEY (export_id) REFERENCES dsar_exports(id)
        )
    """)
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dsar_audit_user_id ON dsar_audit_log(user_id)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dsar_audit_action ON dsar_audit_log(action)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dsar_audit_timestamp ON dsar_audit_log(timestamp)")
    
    db_connection.commit()
