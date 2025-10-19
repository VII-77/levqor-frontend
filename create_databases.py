"""
Standalone script to create 8 Notion databases using Replit Connectors
"""

import os
import sys
import requests
from notion_client import Client

# Add bot directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def get_notion_token():
    """Get Notion access token from Replit Connectors"""
    try:
        # Get Replit token
        repl_identity = os.getenv('REPL_IDENTITY')
        repl_renewal = os.getenv('WEB_REPL_RENEWAL')
        
        if repl_identity:
            x_replit_token = f'repl {repl_identity}'
        elif repl_renewal:
            x_replit_token = f'depl {repl_renewal}'
        else:
            raise Exception('No Replit authentication found')
        
        # Get Notion connector
        hostname = os.getenv('REPLIT_CONNECTORS_HOSTNAME', 'connectors.replit.com')
        
        response = requests.get(
            f'https://{hostname}/api/v2/connection?include_secrets=true&connector_names=notion',
            headers={
                'Accept': 'application/json',
                'X_REPLIT_TOKEN': x_replit_token
            }
        )
        
        data = response.json()
        items = data.get('items', [])
        
        if not items:
            raise Exception('Notion not connected via Replit Connectors')
        
        settings = items[0].get('settings', {})
        access_token = settings.get('access_token') or settings.get('oauth', {}).get('credentials', {}).get('access_token')
        
        if not access_token:
            raise Exception('No access token found')
        
        return access_token
    
    except Exception as e:
        print(f"Error getting Notion token: {e}")
        return None


def create_databases(parent_page_id):
    """Create all 8 enterprise databases"""
    
    # Get Notion token
    access_token = get_notion_token()
    if not access_token:
        print("❌ Could not get Notion access token")
        return {}
    
    notion = Client(auth=access_token)
    
    databases_config = {
        "Finance & Revenue Tracking": {
            "Transaction ID": {"title": {}},
            "Date": {"date": {}},
            "Type": {"select": {"options": [
                {"name": "Revenue", "color": "green"},
                {"name": "Cost", "color": "red"},
                {"name": "Refund", "color": "orange"}
            ]}},
            "Amount": {"number": {"format": "dollar"}},
            "Currency": {"select": {"options": [
                {"name": "USD", "color": "blue"},
                {"name": "EUR", "color": "purple"}
            ]}},
            "Client": {"rich_text": {}},
            "Job ID": {"rich_text": {}},
            "Margin %": {"number": {"format": "percent"}},
            "Reconciled": {"checkbox": {}}
        },
        "Governance & Decision Log": {
            "Decision": {"title": {}},
            "Date": {"date": {}},
            "Type": {"select": {"options": [
                {"name": "Strategic", "color": "blue"},
                {"name": "Operational", "color": "green"},
                {"name": "Financial", "color": "yellow"}
            ]}},
            "Status": {"select": {"options": [
                {"name": "Proposed", "color": "gray"},
                {"name": "Approved", "color": "green"},
                {"name": "Implemented", "color": "blue"}
            ]}},
            "Decision Maker": {"rich_text": {}},
            "Impact": {"select": {"options": [
                {"name": "Low", "color": "green"},
                {"name": "High", "color": "red"}
            ]}}
        },
        "Operations Monitor": {
            "Timestamp": {"title": {}},
            "Component": {"select": {"options": [
                {"name": "Bot Polling", "color": "blue"},
                {"name": "AI Processing", "color": "green"},
                {"name": "Payment System", "color": "yellow"}
            ]}},
            "Status": {"select": {"options": [
                {"name": "Healthy", "color": "green"},
                {"name": "Warning", "color": "yellow"},
                {"name": "Error", "color": "red"}
            ]}},
            "Metric": {"rich_text": {}},
            "Value": {"number": {}},
            "Alert Sent": {"checkbox": {}}
        },
        "Forecast & Predictions": {
            "Date": {"title": {}},
            "Forecast Type": {"select": {"options": [
                {"name": "Revenue", "color": "green"},
                {"name": "Load", "color": "blue"},
                {"name": "Costs", "color": "red"}
            ]}},
            "Predicted Value": {"number": {}},
            "Actual Value": {"number": {}},
            "Accuracy %": {"number": {"format": "percent"}},
            "Confidence": {"select": {"options": [
                {"name": "Low", "color": "red"},
                {"name": "Medium", "color": "yellow"},
                {"name": "High", "color": "green"}
            ]}}
        },
        "Regional Compliance": {
            "Region": {"title": {}},
            "Country Code": {"rich_text": {}},
            "Data Retention Days": {"number": {}},
            "Currency": {"rich_text": {}},
            "Language": {"rich_text": {}},
            "GDPR Required": {"checkbox": {}},
            "CCPA Required": {"checkbox": {}},
            "Active": {"checkbox": {}}
        },
        "Partners & API Keys": {
            "Partner Name": {"title": {}},
            "API Key": {"rich_text": {}},
            "Tier": {"select": {"options": [
                {"name": "Free", "color": "gray"},
                {"name": "Pro", "color": "purple"},
                {"name": "Enterprise", "color": "red"}
            ]}},
            "Quota (monthly)": {"number": {}},
            "Usage (current)": {"number": {}},
            "Revenue Share %": {"number": {"format": "percent"}},
            "Contact Email": {"email": {}},
            "Active": {"checkbox": {}}
        },
        "Referral System": {
            "Referral Code": {"title": {}},
            "Referrer": {"rich_text": {}},
            "Referred Customer": {"rich_text": {}},
            "Status": {"select": {"options": [
                {"name": "Pending", "color": "yellow"},
                {"name": "Active", "color": "green"},
                {"name": "Credited", "color": "blue"}
            ]}},
            "Credit Amount": {"number": {"format": "dollar"}},
            "Applied": {"checkbox": {}},
            "Created Date": {"date": {}}
        },
        "Growth & Customer Acquisition": {
            "Date": {"title": {}},
            "Metric": {"select": {"options": [
                {"name": "Leads", "color": "blue"},
                {"name": "Conversions", "color": "green"},
                {"name": "CAC", "color": "orange"},
                {"name": "LTV", "color": "purple"}
            ]}},
            "Value": {"number": {}},
            "Source": {"select": {"options": [
                {"name": "Organic", "color": "green"},
                {"name": "Paid Ads", "color": "red"},
                {"name": "Referral", "color": "purple"}
            ]}},
            "Cost": {"number": {"format": "dollar"}},
            "ROI %": {"number": {"format": "percent"}}
        }
    }
    
    created_dbs = {}
    
    print("="*70)
    print("CREATING 8 NOTION DATABASES")
    print("="*70)
    
    for db_name, properties in databases_config.items():
        try:
            response = notion.databases.create(
                parent={"page_id": parent_page_id},
                title=[{"type": "text", "text": {"content": db_name}}],
                properties=properties
            )
            
            db_id = response['id']
            created_dbs[db_name] = db_id
            print(f"✅ Created: {db_name}")
            print(f"   ID: {db_id}")
        
        except Exception as e:
            print(f"❌ Failed: {db_name}")
            print(f"   Error: {e}")
    
    print("\n" + "="*70)
    print(f"CREATED {len(created_dbs)}/8 DATABASES")
    print("="*70)
    
    # Print environment variables
    if created_dbs:
        print("\n📝 ADD THESE TO REPLIT SECRETS:")
        print("="*70)
        
        env_mapping = {
            "Finance & Revenue Tracking": "NOTION_FINANCE_DB_ID",
            "Governance & Decision Log": "NOTION_GOVERNANCE_DB_ID",
            "Operations Monitor": "NOTION_OPS_MONITOR_DB_ID",
            "Forecast & Predictions": "NOTION_FORECAST_DB_ID",
            "Regional Compliance": "NOTION_REGION_COMPLIANCE_DB_ID",
            "Partners & API Keys": "NOTION_PARTNERS_DB_ID",
            "Referral System": "NOTION_REFERRALS_DB_ID",
            "Growth & Customer Acquisition": "NOTION_GROWTH_METRICS_DB_ID"
        }
        
        for db_name, env_var in env_mapping.items():
            if db_name in created_dbs:
                print(f"{env_var}={created_dbs[db_name]}")
    
    return created_dbs


if __name__ == "__main__":
    parent_id = os.getenv('NOTION_PARENT_PAGE_ID')
    
    if not parent_id:
        print("❌ NOTION_PARENT_PAGE_ID not set")
        print("   Set it first: export NOTION_PARENT_PAGE_ID=your_page_id")
        sys.exit(1)
    
    print(f"📄 Parent Page ID: {parent_id}")
    print(f"🔐 Getting Notion access token...")
    
    created = create_databases(parent_id)
    
    if created:
        print(f"\n✅ SUCCESS! Created {len(created)} databases")
    else:
        print(f"\n❌ FAILED! No databases created")
        sys.exit(1)
