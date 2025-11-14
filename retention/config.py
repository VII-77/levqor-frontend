"""
Data Retention Configuration
GDPR-compliant retention periods for different data categories
"""

# Retention periods in days
DATA_RETENTION = {
    # Operational logs and temporary data
    "api_usage_log": 90,              # API usage/access logs
    "risk_blocks": 90,                # High-risk data rejection logs  
    "status_snapshots": 30,            # System health snapshots
    
    # User data and business records
    "referrals": 730,                  # 2 years - marketing/growth data
    "analytics_aggregates": 730,       # 2 years - aggregated metrics
    
    # Billing and financial (keep longer for legal/tax reasons)
    "billing_events": 2555,            # 7 years - legal requirement
    "billing_dunning_state": 2555,     # 7 years - payment failure history
    "marketplace_orders": 2555,        # 7 years - financial transactions
    
    # DSAR and compliance
    "dsar_requests": 365,              # 1 year - request history
    "dsar_exports": 30,                # 30 days - exported ZIP files
    "dsar_audit_log": 2555,            # 7 years - compliance audit trail
    
    # Deletion tracking
    "deletion_jobs": 90,               # 90 days - deletion job history
    
    # Marketing consent (keep indefinitely for PECR compliance)
    "user_marketing_consent": None,    # Never auto-delete consent records
}

# Table-to-timestamp field mapping
TIMESTAMP_FIELDS = {
    "api_usage_log": "created_at",
    "risk_blocks": "created_at",
    "status_snapshots": "timestamp",
    "referrals": "created_at",
    "analytics_aggregates": None,      # Uses DATE field, handled separately
    "billing_events": "created_at",
    "billing_dunning_state": "created_at",
    "marketplace_orders": "created_at",
    "dsar_requests": "requested_at",
    "dsar_exports": "created_at",
    "dsar_audit_log": "timestamp",
    "deletion_jobs": "requested_at",
    "user_marketing_consent": "created_at",
}

# Categories that should NEVER be auto-deleted
PROTECTED_TABLES = {
    "users",                    # Core user accounts
    "partners",                 # Partner business relationships
    "listings",                 # Marketplace listings
    "developer_keys",           # API keys (managed separately)
}

def get_retention_days(table_name: str) -> int:
    """Get retention period for a table, returns None if never delete"""
    return DATA_RETENTION.get(table_name)

def get_timestamp_field(table_name: str) -> str:
    """Get the timestamp field name for a table"""
    return TIMESTAMP_FIELDS.get(table_name, "created_at")

def is_protected(table_name: str) -> bool:
    """Check if table is protected from auto-deletion"""
    return table_name in PROTECTED_TABLES
