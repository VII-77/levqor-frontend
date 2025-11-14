"""
Data Retention and Cleanup Module
GDPR-compliant automatic data deletion system
"""

from retention.cleanup import cleanup_expired_records
from retention.config import DATA_RETENTION, get_retention_days, is_protected

__all__ = ['cleanup_expired_records', 'DATA_RETENTION', 'get_retention_days', 'is_protected']
