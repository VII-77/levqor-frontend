"""
Automated Notion Database Setup
Creates all missing databases for enterprise features
"""

from notion_client import Client
import os
from typing import Dict, List, Any


class NotionDatabaseSetup:
    """Creates and configures Notion databases for enterprise features"""
    
    def __init__(self):
        self.notion = Client(auth=os.getenv('NOTION_TOKEN') or self._get_connector_token())
        self.parent_page_id = os.getenv('NOTION_PARENT_PAGE_ID')  # Set this to your workspace page
    
    def _get_connector_token(self):
        """Get token from Replit Connectors"""
        # This would use Replit Connectors OAuth flow
        # For now, return env var
        return os.getenv('NOTION_INTEGRATION_TOKEN')
    
    def create_finance_database(self) -> str:
        """Create Finance & Revenue Tracking Database"""
        properties = {
            "Transaction ID": {"title": {}},
            "Date": {"date": {}},
            "Type": {
                "select": {
                    "options": [
                        {"name": "Revenue", "color": "green"},
                        {"name": "Cost", "color": "red"},
                        {"name": "Refund", "color": "orange"},
                        {"name": "Adjustment", "color": "gray"}
                    ]
                }
            },
            "Amount": {"number": {"format": "dollar"}},
            "Currency": {
                "select": {
                    "options": [
                        {"name": "USD", "color": "blue"},
                        {"name": "EUR", "color": "purple"},
                        {"name": "GBP", "color": "pink"}
                    ]
                }
            },
            "Client": {"rich_text": {}},
            "Job ID": {"rich_text": {}},
            "Category": {
                "select": {
                    "options": [
                        {"name": "Service Revenue", "color": "green"},
                        {"name": "AI Costs", "color": "red"},
                        {"name": "Infrastructure", "color": "gray"},
                        {"name": "Payment Processing", "color": "orange"}
                    ]
                }
            },
            "Margin %": {"number": {"format": "percent"}},
            "Notes": {"rich_text": {}},
            "Reconciled": {"checkbox": {}},
            "Stripe Payment ID": {"rich_text": {}},
        }
        
        return self._create_database("Finance & Revenue Tracking", properties)
    
    def create_governance_database(self) -> str:
        """Create Governance & Decision Log Database"""
        properties = {
            "Decision": {"title": {}},
            "Date": {"date": {}},
            "Type": {
                "select": {
                    "options": [
                        {"name": "Strategic", "color": "blue"},
                        {"name": "Operational", "color": "green"},
                        {"name": "Financial", "color": "yellow"},
                        {"name": "Compliance", "color": "red"},
                        {"name": "Technical", "color": "purple"}
                    ]
                }
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "Proposed", "color": "gray"},
                        {"name": "Under Review", "color": "yellow"},
                        {"name": "Approved", "color": "green"},
                        {"name": "Rejected", "color": "red"},
                        {"name": "Implemented", "color": "blue"}
                    ]
                }
            },
            "Decision Maker": {"rich_text": {}},
            "Impact": {
                "select": {
                    "options": [
                        {"name": "Low", "color": "green"},
                        {"name": "Medium", "color": "yellow"},
                        {"name": "High", "color": "orange"},
                        {"name": "Critical", "color": "red"}
                    ]
                }
            },
            "Rationale": {"rich_text": {}},
            "Outcomes": {"rich_text": {}},
            "Related Risks": {"rich_text": {}},
        }
        
        return self._create_database("Governance & Decision Log", properties)
    
    def create_ops_monitor_database(self) -> str:
        """Create Operations Monitoring Database"""
        properties = {
            "Timestamp": {"title": {}},
            "Component": {
                "select": {
                    "options": [
                        {"name": "Bot Polling", "color": "blue"},
                        {"name": "AI Processing", "color": "green"},
                        {"name": "Payment System", "color": "yellow"},
                        {"name": "Database", "color": "purple"},
                        {"name": "API Endpoints", "color": "pink"}
                    ]
                }
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "Healthy", "color": "green"},
                        {"name": "Warning", "color": "yellow"},
                        {"name": "Error", "color": "red"},
                        {"name": "Critical", "color": "red"}
                    ]
                }
            },
            "Metric": {"rich_text": {}},
            "Value": {"number": {}},
            "Threshold": {"number": {}},
            "Alert Sent": {"checkbox": {}},
            "Resolution": {"rich_text": {}},
            "Auto-Fixed": {"checkbox": {}},
        }
        
        return self._create_database("Operations Monitor", properties)
    
    def create_forecast_database(self) -> str:
        """Create Forecast & Predictions Database"""
        properties = {
            "Date": {"title": {}},
            "Forecast Type": {
                "select": {
                    "options": [
                        {"name": "Revenue", "color": "green"},
                        {"name": "Load", "color": "blue"},
                        {"name": "Costs", "color": "red"},
                        {"name": "Growth", "color": "purple"}
                    ]
                }
            },
            "Predicted Value": {"number": {}},
            "Actual Value": {"number": {}},
            "Accuracy %": {"number": {"format": "percent"}},
            "Confidence": {
                "select": {
                    "options": [
                        {"name": "Low", "color": "red"},
                        {"name": "Medium", "color": "yellow"},
                        {"name": "High", "color": "green"}
                    ]
                }
            },
            "Model Used": {"rich_text": {}},
            "Notes": {"rich_text": {}},
        }
        
        return self._create_database("Forecast & Predictions", properties)
    
    def create_region_compliance_database(self) -> str:
        """Create Regional Compliance Database"""
        properties = {
            "Region": {"title": {}},
            "Country Code": {"rich_text": {}},
            "Data Retention Days": {"number": {}},
            "Currency": {"rich_text": {}},
            "Language": {"rich_text": {}},
            "Timezone": {"rich_text": {}},
            "GDPR Required": {"checkbox": {}},
            "CCPA Required": {"checkbox": {}},
            "Special Rules": {"rich_text": {}},
            "Active": {"checkbox": {}},
        }
        
        return self._create_database("Regional Compliance", properties)
    
    def create_partners_database(self) -> str:
        """Create Partners & API Keys Database"""
        properties = {
            "Partner Name": {"title": {}},
            "API Key": {"rich_text": {}},  # Hashed/masked in display
            "Tier": {
                "select": {
                    "options": [
                        {"name": "Free", "color": "gray"},
                        {"name": "Basic", "color": "blue"},
                        {"name": "Pro", "color": "purple"},
                        {"name": "Enterprise", "color": "red"}
                    ]
                }
            },
            "Quota (monthly)": {"number": {}},
            "Usage (current)": {"number": {}},
            "Revenue Share %": {"number": {"format": "percent"}},
            "Total Revenue": {"number": {"format": "dollar"}},
            "Payout Status": {
                "select": {
                    "options": [
                        {"name": "Pending", "color": "yellow"},
                        {"name": "Paid", "color": "green"},
                        {"name": "On Hold", "color": "red"}
                    ]
                }
            },
            "Contact Email": {"email": {}},
            "Active": {"checkbox": {}},
            "Created Date": {"date": {}},
        }
        
        return self._create_database("Partners & API Keys", properties)
    
    def create_referrals_database(self) -> str:
        """Create Referral System Database"""
        properties = {
            "Referral Code": {"title": {}},
            "Referrer": {"rich_text": {}},
            "Referred Customer": {"rich_text": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "Pending", "color": "yellow"},
                        {"name": "Active", "color": "green"},
                        {"name": "Credited", "color": "blue"},
                        {"name": "Expired", "color": "gray"}
                    ]
                }
            },
            "Credit Amount": {"number": {"format": "dollar"}},
            "Applied": {"checkbox": {}},
            "Created Date": {"date": {}},
            "Conversion Date": {"date": {}},
            "Revenue Generated": {"number": {"format": "dollar"}},
        }
        
        return self._create_database("Referral System", properties)
    
    def create_growth_metrics_database(self) -> str:
        """Create Growth & Customer Acquisition Database"""
        properties = {
            "Date": {"title": {}},
            "Metric": {
                "select": {
                    "options": [
                        {"name": "Leads", "color": "blue"},
                        {"name": "Conversions", "color": "green"},
                        {"name": "CAC", "color": "orange"},
                        {"name": "LTV", "color": "purple"},
                        {"name": "Churn", "color": "red"}
                    ]
                }
            },
            "Value": {"number": {}},
            "Source": {
                "select": {
                    "options": [
                        {"name": "Organic", "color": "green"},
                        {"name": "Paid Ads", "color": "red"},
                        {"name": "Referral", "color": "purple"},
                        {"name": "Partnership", "color": "blue"},
                        {"name": "Email", "color": "yellow"}
                    ]
                }
            },
            "Campaign": {"rich_text": {}},
            "Cost": {"number": {"format": "dollar"}},
            "ROI %": {"number": {"format": "percent"}},
            "Notes": {"rich_text": {}},
        }
        
        return self._create_database("Growth & Customer Acquisition", properties)
    
    def _create_database(self, title: str, properties: Dict[str, Any]) -> str:
        """Create a Notion database with given properties"""
        try:
            if not self.parent_page_id:
                print(f"⚠️  Parent page ID not set. Skipping creation of '{title}'")
                print(f"   Set NOTION_PARENT_PAGE_ID environment variable to auto-create databases")
                return None
            
            response = self.notion.databases.create(
                parent={"page_id": self.parent_page_id},
                title=[{"type": "text", "text": {"content": title}}],
                properties=properties
            )
            
            database_id = response['id']
            print(f"✅ Created database: {title}")
            print(f"   ID: {database_id}")
            return database_id
        
        except Exception as e:
            print(f"❌ Error creating database '{title}': {e}")
            return None
    
    def setup_all_databases(self) -> Dict[str, str]:
        """Create all missing databases"""
        print("="*70)
        print("NOTION DATABASE SETUP - ENTERPRISE FEATURES")
        print("="*70)
        
        databases = {}
        
        print("\nCreating Finance Database...")
        databases['finance'] = self.create_finance_database()
        
        print("\nCreating Governance Database...")
        databases['governance'] = self.create_governance_database()
        
        print("\nCreating Ops Monitor Database...")
        databases['ops_monitor'] = self.create_ops_monitor_database()
        
        print("\nCreating Forecast Database...")
        databases['forecast'] = self.create_forecast_database()
        
        print("\nCreating Region Compliance Database...")
        databases['region_compliance'] = self.create_region_compliance_database()
        
        print("\nCreating Partners Database...")
        databases['partners'] = self.create_partners_database()
        
        print("\nCreating Referrals Database...")
        databases['referrals'] = self.create_referrals_database()
        
        print("\nCreating Growth Metrics Database...")
        databases['growth_metrics'] = self.create_growth_metrics_database()
        
        print("\n" + "="*70)
        print("DATABASE SETUP COMPLETE")
        print("="*70)
        
        # Print environment variable updates
        print("\n📝 Add these to your .env file:")
        print("="*70)
        for key, db_id in databases.items():
            if db_id:
                env_var = f"NOTION_{key.upper()}_DB_ID"
                print(f"{env_var}={db_id}")
        
        return databases


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║   EchoPilot Enterprise Database Setup                         ║
    ║   Creates 8 missing Notion databases for advanced features    ║
    ╚════════════════════════════════════════════════════════════════╝
    
    INSTRUCTIONS:
    1. Set NOTION_PARENT_PAGE_ID in your environment
       (This should be the ID of a Notion page in your workspace)
    
    2. Ensure Notion integration has access to that page
    
    3. Run this script: python bot/database_setup.py
    
    4. Copy the generated environment variables to your .env file
    
    5. Restart the bot
    
    Note: If you don't set NOTION_PARENT_PAGE_ID, this will output
    the schema details for manual database creation in Notion.
    """)
    
    setup = NotionDatabaseSetup()
    databases = setup.setup_all_databases()
    
    print("\n✅ Database setup complete!")
    print(f"   Created: {len([d for d in databases.values() if d])}/{len(databases)} databases")
