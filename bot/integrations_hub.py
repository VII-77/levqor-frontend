#!/usr/bin/env python3
"""
EchoPilot Integrations Hub (Phase 122)
Integration marketplace with OAuth connectors and webhook management
"""

import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

def log_integration_event(event_type, details=None):
    """Log integration events"""
    log_entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event_type': event_type,
        'details': details or {}
    }
    
    log_file = Path('logs/integrations_hub.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

# Available integrations catalog
AVAILABLE_INTEGRATIONS = {
    'notion': {
        'id': 'notion',
        'name': 'Notion',
        'description': 'Sync tasks and databases with Notion',
        'category': 'productivity',
        'auth_type': 'oauth2',
        'icon': '📝',
        'status': 'active'
    },
    'slack': {
        'id': 'slack',
        'name': 'Slack',
        'description': 'Send notifications and alerts to Slack',
        'category': 'communication',
        'auth_type': 'oauth2',
        'icon': '💬',
        'status': 'active'
    },
    'gmail': {
        'id': 'gmail',
        'name': 'Gmail',
        'description': 'Send emails and manage inbox',
        'category': 'communication',
        'auth_type': 'oauth2',
        'icon': '📧',
        'status': 'active'
    },
    'stripe': {
        'id': 'stripe',
        'name': 'Stripe',
        'description': 'Process payments and manage subscriptions',
        'category': 'payments',
        'auth_type': 'api_key',
        'icon': '💳',
        'status': 'active'
    },
    'openai': {
        'id': 'openai',
        'name': 'OpenAI',
        'description': 'AI-powered task processing',
        'category': 'ai',
        'auth_type': 'api_key',
        'icon': '🤖',
        'status': 'active'
    },
    'google_drive': {
        'id': 'google_drive',
        'name': 'Google Drive',
        'description': 'File storage and sharing',
        'category': 'storage',
        'auth_type': 'oauth2',
        'icon': '📁',
        'status': 'active'
    },
    'telegram': {
        'id': 'telegram',
        'name': 'Telegram',
        'description': 'Bot notifications and commands',
        'category': 'communication',
        'auth_type': 'bot_token',
        'icon': '📱',
        'status': 'active'
    },
    'hubspot': {
        'id': 'hubspot',
        'name': 'HubSpot',
        'description': 'CRM and marketing automation',
        'category': 'crm',
        'auth_type': 'oauth2',
        'icon': '🎯',
        'status': 'coming_soon'
    },
    'salesforce': {
        'id': 'salesforce',
        'name': 'Salesforce',
        'description': 'Enterprise CRM integration',
        'category': 'crm',
        'auth_type': 'oauth2',
        'icon': '☁️',
        'status': 'coming_soon'
    }
}

def get_integrations_catalog(category=None, status='active'):
    """Get available integrations catalog"""
    integrations = AVAILABLE_INTEGRATIONS.copy()
    
    # Filter by category
    if category:
        integrations = {
            k: v for k, v in integrations.items()
            if v.get('category') == category
        }
    
    # Filter by status
    if status:
        integrations = {
            k: v for k, v in integrations.items()
            if v.get('status') == status
        }
    
    return {
        'integrations': list(integrations.values()),
        'total': len(integrations),
        'categories': list(set(i['category'] for i in integrations.values()))
    }

def install_integration(integration_id, tenant_id, config=None):
    """Install an integration for a tenant"""
    if integration_id not in AVAILABLE_INTEGRATIONS:
        return {
            'installed': False,
            'error': 'Integration not found'
        }
    
    integration = AVAILABLE_INTEGRATIONS[integration_id]
    
    installation = {
        'integration_id': integration_id,
        'tenant_id': tenant_id,
        'installed_at': datetime.utcnow().isoformat() + 'Z',
        'config': config or {},
        'status': 'installed',
        'auth_status': 'pending' if integration['auth_type'] == 'oauth2' else 'configured'
    }
    
    log_integration_event('integration_installed', installation)
    
    return {
        'installed': True,
        **installation
    }

def get_installed_integrations(tenant_id):
    """Get integrations installed for a tenant"""
    try:
        log_file = Path('logs/integrations_hub.ndjson')
        if not log_file.exists():
            return {'integrations': [], 'total': 0}
        
        installations = []
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get('event_type') == 'integration_installed':
                        details = entry.get('details', {})
                        if details.get('tenant_id') == tenant_id:
                            installations.append(details)
                except:
                    continue
        
        # De-duplicate by integration_id (keep latest)
        by_id = {}
        for inst in installations:
            by_id[inst['integration_id']] = inst
        
        return {
            'integrations': list(by_id.values()),
            'total': len(by_id)
        }
        
    except Exception as e:
        log_integration_event('get_installed_error', {'error': str(e)})
        return {'integrations': [], 'total': 0, 'error': str(e)}

def create_webhook(integration_id, tenant_id, events, target_url):
    """Create webhook for integration"""
    import uuid
    
    webhook_id = str(uuid.uuid4())[:8]
    
    webhook = {
        'webhook_id': webhook_id,
        'integration_id': integration_id,
        'tenant_id': tenant_id,
        'events': events,
        'target_url': target_url,
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'status': 'active'
    }
    
    log_integration_event('webhook_created', webhook)
    
    return {
        'created': True,
        **webhook
    }

def get_integration_stats():
    """Get integration usage statistics"""
    try:
        log_file = Path('logs/integrations_hub.ndjson')
        if not log_file.exists():
            return {
                'total_installations': 0,
                'total_webhooks': 0,
                'by_integration': {}
            }
        
        stats = {
            'installations': 0,
            'webhooks': 0,
            'by_integration': defaultdict(int),
            'by_tenant': defaultdict(int)
        }
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    event_type = entry.get('event_type')
                    details = entry.get('details', {})
                    
                    if event_type == 'integration_installed':
                        stats['installations'] += 1
                        stats['by_integration'][details.get('integration_id', 'unknown')] += 1
                        stats['by_tenant'][details.get('tenant_id', 'unknown')] += 1
                    
                    elif event_type == 'webhook_created':
                        stats['webhooks'] += 1
                        
                except:
                    continue
        
        return {
            'total_installations': stats['installations'],
            'total_webhooks': stats['webhooks'],
            'by_integration': dict(stats['by_integration']),
            'by_tenant': dict(stats['by_tenant'])
        }
        
    except Exception as e:
        log_integration_event('stats_error', {'error': str(e)})
        return {'error': str(e)}

if __name__ == '__main__':
    # Test integrations hub
    print("Testing Integrations Hub...")
    
    print("\n1. Get catalog")
    catalog = get_integrations_catalog()
    print(f"  Total integrations: {catalog['total']}")
    print(f"  Categories: {catalog['categories']}")
    
    print("\n2. Install integrations")
    install_integration('notion', 'tenant_a', {'workspace': 'test'})
    install_integration('slack', 'tenant_a', {'channel': '#alerts'})
    install_integration('openai', 'tenant_b', {'model': 'gpt-4o'})
    
    print("\n3. Get installed (tenant_a)")
    installed = get_installed_integrations('tenant_a')
    print(f"  Installed: {installed['total']}")
    for i in installed['integrations']:
        print(f"    - {i['integration_id']}")
    
    print("\n4. Create webhook")
    webhook = create_webhook('slack', 'tenant_a', ['job.completed', 'job.failed'], 'https://hooks.slack.com/test')
    print(f"  Webhook ID: {webhook['webhook_id']}")
    
    print("\n5. Get stats")
    stats = get_integration_stats()
    print(json.dumps(stats, indent=2))
    
    print("\n✓ Integrations Hub tests complete")
