"""
Compliance and incident management database models
Handles SLA credits, disputes, incidents, and emergency reports
"""

def init_compliance_tables(db_connection):
    """Initialize compliance-related tables"""
    
    # SLA credit requests table
    db_connection.execute("""
        CREATE TABLE IF NOT EXISTS sla_credit_requests(
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            created_at REAL NOT NULL,
            period_start TEXT NOT NULL,
            period_end TEXT NOT NULL,
            claimed_issue TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            decision_note TEXT,
            credited_amount_cents INTEGER DEFAULT 0,
            decided_at REAL,
            decided_by TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_sla_requests_user_id ON sla_credit_requests(user_id)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_sla_requests_status ON sla_credit_requests(status)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_sla_requests_created_at ON sla_credit_requests(created_at)")
    
    # Disputes table
    db_connection.execute("""
        CREATE TABLE IF NOT EXISTS disputes(
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            created_at REAL NOT NULL,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            acknowledged_at REAL,
            resolved_at REAL,
            resolution_note TEXT,
            escalated INTEGER DEFAULT 0,
            escalated_at REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_disputes_user_id ON disputes(user_id)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_disputes_status ON disputes(status)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_disputes_created_at ON disputes(created_at)")
    
    # Incidents table (for status page)
    db_connection.execute("""
        CREATE TABLE IF NOT EXISTS incidents(
            id TEXT PRIMARY KEY,
            started_at REAL NOT NULL,
            resolved_at REAL,
            title TEXT NOT NULL,
            description TEXT,
            severity INTEGER NOT NULL DEFAULT 2,
            status TEXT NOT NULL DEFAULT 'investigating',
            impact TEXT,
            affected_systems TEXT,
            user_reported INTEGER DEFAULT 0,
            reported_by_user_id TEXT,
            updates TEXT,
            FOREIGN KEY (reported_by_user_id) REFERENCES users(id)
        )
    """)
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_incidents_started_at ON incidents(started_at)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_incidents_severity ON incidents(severity)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents(status)")
    
    db_connection.commit()
