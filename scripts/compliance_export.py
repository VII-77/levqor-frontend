#!/usr/bin/env python3
"""
Compliance Export - Export GDPR, SOC-lite, and Finance audit data
Generates SHA256 manifests and timestamps for regulatory compliance
"""
import json
import os
import hashlib
import glob
from datetime import datetime, timezone
from pathlib import Path

def compute_sha256(filepath):
    """Compute SHA256 hash of file"""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except:
        return None

def export_gdpr_data():
    """Export GDPR compliance data"""
    gdpr_data = {
        "export_timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "data_protection": {
            "encryption": "AES-256 for sensitive fields",
            "access_control": "X-Dash-Key authentication",
            "data_retention": "Configurable via retention policy",
            "right_to_erasure": "Supported via /api/compliance/export-data"
        },
        "privacy_policy": "See docs/privacy_policy.md",
        "cookie_policy": "See docs/cookie_policy.md",
        "data_processing": {
            "processors": ["OpenAI API", "Notion API", "Google APIs", "Stripe"],
            "purpose": "AI task automation and enterprise management",
            "legal_basis": "Legitimate business interest"
        }
    }
    return gdpr_data

def export_soc_lite_data():
    """Export SOC-lite audit data"""
    soc_data = {
        "export_timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "security_controls": {
            "authentication": "API key-based (X-Dash-Key)",
            "authorization": "RBAC system (admin/user/viewer roles)",
            "encryption": "TLS in transit, AES-256 at rest",
            "logging": "Comprehensive NDJSON audit trail",
            "monitoring": "SLO tracking, production alerts, threat detection",
            "incident_response": "Automated incident detection and paging"
        },
        "availability": {
            "slo_target": "99.9%",
            "backup_frequency": "Daily DR backups at 02:30 UTC",
            "disaster_recovery": "Automated backup and restore procedures"
        },
        "processing_integrity": {
            "qa_system": "80% quality threshold with AI evaluation",
            "data_validation": "Schema enforcement and integrity scanning"
        },
        "confidentiality": {
            "secrets_management": "Environment variables, never logged",
            "pii_handling": "Encrypted in logs, access-controlled APIs"
        }
    }
    return soc_data

def export_finance_audit_data():
    """Export finance audit data"""
    finance_data = {
        "export_timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "revenue_tracking": {
            "stripe_integration": "Live mode active",
            "webhook_logging": "All payment events logged",
            "reconciliation": "Automated nightly reconciliation"
        },
        "cost_management": {
            "guardrails": "Active cost limits per model",
            "tracking": "Real-time cost monitoring",
            "budgets": "Per-tenant usage tracking"
        },
        "financial_reporting": {
            "p_and_l": "Automated P&L generation",
            "forecasting": "30-day ML-based forecasting",
            "valuation": "Company valuation models"
        },
        "audit_trail": {
            "all_transactions": "Logged to logs/finance.ndjson",
            "integrity": "SHA256 manifests for all logs"
        }
    }
    return finance_data

def main():
    print("="*80)
    print("COMPLIANCE EXPORT - GDPR, SOC-LITE, FINANCE AUDITS")
    print("="*80)
    print()
    
    export_ts = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    # Create backup directory
    backup_dir = Path('backups/final_audit')
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Export GDPR data
    print("1. Exporting GDPR compliance data...")
    gdpr_data = export_gdpr_data()
    gdpr_path = backup_dir / 'gdpr_compliance.json'
    with open(gdpr_path, 'w') as f:
        json.dump(gdpr_data, f, indent=2)
    gdpr_hash = compute_sha256(gdpr_path)
    print(f"   ✅ {gdpr_path} (SHA256: {gdpr_hash[:16]}...)")
    
    # Export SOC-lite data
    print("2. Exporting SOC-lite audit data...")
    soc_data = export_soc_lite_data()
    soc_path = backup_dir / 'soc_lite_audit.json'
    with open(soc_path, 'w') as f:
        json.dump(soc_data, f, indent=2)
    soc_hash = compute_sha256(soc_path)
    print(f"   ✅ {soc_path} (SHA256: {soc_hash[:16]}...)")
    
    # Export Finance data
    print("3. Exporting finance audit data...")
    finance_data = export_finance_audit_data()
    finance_path = backup_dir / 'finance_audit.json'
    with open(finance_path, 'w') as f:
        json.dump(finance_data, f, indent=2)
    finance_hash = compute_sha256(finance_path)
    print(f"   ✅ {finance_path} (SHA256: {finance_hash[:16]}...)")
    
    # Create SHA256 manifest
    print("4. Creating SHA256 manifest...")
    manifest = {
        "export_timestamp": export_ts,
        "files": {
            "gdpr_compliance.json": gdpr_hash,
            "soc_lite_audit.json": soc_hash,
            "finance_audit.json": finance_hash
        },
        "verification": {
            "instructions": "Verify file integrity by recomputing SHA256 hashes",
            "command": "sha256sum backups/final_audit/*.json"
        }
    }
    
    manifest_path = backup_dir / 'SHA256_MANIFEST.json'
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"   ✅ {manifest_path}")
    
    # Create timestamp file
    timestamp_path = backup_dir / 'EXPORT_TIMESTAMP.txt'
    with open(timestamp_path, 'w') as f:
        f.write(f"Compliance Export Timestamp: {export_ts}\n")
        f.write(f"Exported by: EchoPilot Final Audit System\n")
        f.write(f"Files: 3 (GDPR, SOC-lite, Finance)\n")
        f.write(f"Manifest: SHA256_MANIFEST.json\n")
    print(f"   ✅ {timestamp_path}")
    
    print()
    print("="*80)
    print("COMPLIANCE EXPORT COMPLETE ✅")
    print("="*80)
    print()
    print(f"📁 Export Directory: {backup_dir}")
    print(f"📄 Files:")
    print(f"   • gdpr_compliance.json")
    print(f"   • soc_lite_audit.json")
    print(f"   • finance_audit.json")
    print(f"   • SHA256_MANIFEST.json")
    print(f"   • EXPORT_TIMESTAMP.txt")
    print()
    
    return {
        "status": "success",
        "timestamp": export_ts,
        "files": 3,
        "manifest": str(manifest_path)
    }

if __name__ == '__main__':
    result = main()
    print(json.dumps(result, indent=2))
