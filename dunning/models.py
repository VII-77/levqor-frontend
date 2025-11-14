"""
Dunning system database models
Tracks payment failures and dunning email sequences
"""

def init_dunning_tables(db_connection):
    """Initialize dunning-related tables"""
    
    # Payment failures table
    db_connection.execute("""
        CREATE TABLE IF NOT EXISTS payment_failures(
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            subscription_id TEXT,
            invoice_id TEXT,
            amount_cents INTEGER,
            currency TEXT DEFAULT 'gbp',
            failure_date REAL NOT NULL,
            failure_reason TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            resolved_at REAL,
            metadata TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_payment_failures_user_id ON payment_failures(user_id)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_payment_failures_status ON payment_failures(status)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_payment_failures_date ON payment_failures(failure_date)")
    
    # Dunning emails table
    db_connection.execute("""
        CREATE TABLE IF NOT EXISTS dunning_emails(
            id TEXT PRIMARY KEY,
            failure_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            email_type TEXT NOT NULL,
            sent_at REAL NOT NULL,
            opened_at REAL,
            clicked_at REAL,
            message_id TEXT,
            FOREIGN KEY (failure_id) REFERENCES payment_failures(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dunning_emails_failure_id ON dunning_emails(failure_id)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dunning_emails_user_id ON dunning_emails(user_id)")
    db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dunning_emails_type ON dunning_emails(email_type)")
    
    db_connection.commit()
