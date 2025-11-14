"""
Backend Configuration
Centralized configuration for backend features
"""

import os

# DSAR Export Retention
# Number of days to keep DSAR export ZIP files before automatic deletion
# Default: 30 days (GDPR compliance best practice)
# DB rows are kept for audit purposes, only ZIP files are deleted
GDPR_DSAR_EXPORT_RETENTION_DAYS = int(os.getenv("GDPR_DSAR_EXPORT_RETENTION_DAYS", "30"))
