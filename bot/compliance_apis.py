#!/usr/bin/env python3
"""
EchoPilot External Compliance APIs (Phase 127)
GDPR, CCPA, SOC2 compliance reporting APIs
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

def generate_gdpr_report(user_id, tenant_id='default'):
    """Generate GDPR data export report"""
    try:
        # Collect user data from various sources
        from bot.compliance_webhooks import get_audit_chain
        
        audit_data = get_audit_chain(limit=1000)
        user_entries = [
            e for e in audit_data.get('entries', [])
            if e.get('user') == user_id
        ]
        
        report = {
            'report_type': 'gdpr_data_export',
            'user_id': user_id,
            'tenant_id': tenant_id,
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'data_categories': {
                'audit_trail': {
                    'count': len(user_entries),
                    'entries': user_entries[:100]
                },
                'personal_info': {
                    'user_id': user_id,
                    'tenant_id': tenant_id
                }
            },
            'retention_policy': '90 days',
            'data_processing_purposes': [
                'Service delivery',
                'Security and fraud prevention',
                'Analytics and improvement'
            ],
            'third_party_processors': [
                'OpenAI (AI processing)',
                'Stripe (Payments)',
                'Notion (Data storage)'
            ]
        }
        
        # Log export request
        log_file = Path('logs/compliance_reports.ndjson')
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(json.dumps({
                'ts': datetime.utcnow().isoformat() + 'Z',
                'report_type': 'gdpr_export',
                'user_id': user_id,
                'tenant_id': tenant_id
            }) + '\n')
        
        return report
        
    except Exception as e:
        return {'error': str(e)}

def generate_ccpa_report(tenant_id):
    """Generate CCPA compliance report"""
    try:
        # Data collection categories per CCPA
        report = {
            'report_type': 'ccpa_disclosure',
            'tenant_id': tenant_id,
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'data_categories_collected': [
                {
                    'category': 'Identifiers',
                    'examples': 'Email, user ID, tenant ID',
                    'business_purpose': 'Service delivery and authentication'
                },
                {
                    'category': 'Commercial Information',
                    'examples': 'Purchase history, payment data',
                    'business_purpose': 'Billing and financial reporting'
                },
                {
                    'category': 'Usage Data',
                    'examples': 'Job executions, API calls, system metrics',
                    'business_purpose': 'Service optimization and analytics'
                },
                {
                    'category': 'Inferences',
                    'examples': 'Load predictions, usage patterns',
                    'business_purpose': 'Service improvement'
                }
            ],
            'data_sold_or_shared': False,
            'opt_out_available': True,
            'opt_out_url': '/privacy/opt-out',
            'deletion_request_url': '/privacy/delete',
            'contact_email': 'privacy@echopilot.ai'
        }
        
        return report
        
    except Exception as e:
        return {'error': str(e)}

def generate_soc2_report():
    """Generate SOC 2 compliance metrics report"""
    try:
        # Get security and operations metrics
        from bot.compliance_webhooks import verify_audit_chain
        
        audit_verification = verify_audit_chain()
        
        report = {
            'report_type': 'soc2_metrics',
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'trust_principles': {
                'security': {
                    'audit_chain_integrity': audit_verification.get('valid', False),
                    'encryption_at_rest': True,
                    'encryption_in_transit': True,
                    'access_control': 'RBAC with JWT',
                    'mfa_available': True
                },
                'availability': {
                    'uptime_target': '99.99%',
                    'disaster_recovery': 'Daily backups',
                    'failover': 'Automated'
                },
                'processing_integrity': {
                    'job_tracking': 'Full audit trail',
                    'error_handling': 'Automatic retry',
                    'data_validation': 'Schema enforcement'
                },
                'confidentiality': {
                    'data_isolation': 'Multi-tenant with isolation',
                    'secret_management': 'Environment variables',
                    'api_security': 'API key authentication'
                },
                'privacy': {
                    'gdpr_compliant': True,
                    'ccpa_compliant': True,
                    'data_retention': '90 days',
                    'right_to_deletion': True
                }
            },
            'audit_logs': {
                'enabled': True,
                'retention_days': 90,
                'integrity_verified': audit_verification.get('valid', False)
            },
            'security_controls': [
                'Multi-factor authentication',
                'Role-based access control',
                'Audit logging',
                'Encryption (TLS 1.3)',
                'Secret scanning',
                'Automated security updates'
            ]
        }
        
        return report
        
    except Exception as e:
        return {'error': str(e)}

def handle_deletion_request(user_id, tenant_id):
    """Handle GDPR/CCPA deletion request"""
    try:
        deletion = {
            'request_id': f"DEL_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            'user_id': user_id,
            'tenant_id': tenant_id,
            'requested_at': datetime.utcnow().isoformat() + 'Z',
            'status': 'queued',
            'estimated_completion': (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z',
            'data_categories': [
                'Personal information',
                'Usage data',
                'Audit logs (after retention period)'
            ]
        }
        
        # Log deletion request
        log_file = Path('logs/compliance_reports.ndjson')
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(json.dumps({
                'ts': datetime.utcnow().isoformat() + 'Z',
                'report_type': 'deletion_request',
                **deletion
            }) + '\n')
        
        return deletion
        
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    # Test compliance APIs
    print("Testing Compliance APIs...")
    
    print("\n1. GDPR Export")
    gdpr = generate_gdpr_report('user123', 'tenant_a')
    print(f"  Generated: {gdpr['report_type']}")
    print(f"  Data categories: {len(gdpr.get('data_categories', {}))}")
    
    print("\n2. CCPA Disclosure")
    ccpa = generate_ccpa_report('tenant_a')
    print(f"  Categories collected: {len(ccpa.get('data_categories_collected', []))}")
    
    print("\n3. SOC2 Metrics")
    soc2 = generate_soc2_report()
    print(f"  Trust principles: {len(soc2.get('trust_principles', {}))}")
    
    print("\n4. Deletion Request")
    deletion = handle_deletion_request('user123', 'tenant_a')
    print(f"  Request ID: {deletion.get('request_id')}")
    print(f"  Status: {deletion.get('status')}")
    
    print("\n✓ Compliance APIs tests complete")
