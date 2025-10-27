"""
Marketplace & Partner API System
Public API for partners to submit jobs and retrieve results
"""

import os
import hashlib
import secrets
from datetime import datetime
from typing import Dict, List, Any, Optional
from flask import Request


class MarketplaceAPI:
    """Partner API management and quota enforcement"""
    
    def __init__(self, notion_client=None):
        if notion_client:
            self.notion = notion_client
        else:
            from bot.notion_api import get_notion_client
            self.notion = get_notion_client()
        self.partners_db_id = os.getenv('NOTION_PARTNERS_DB_ID')
        self.queue_db_id = os.getenv('AUTOMATION_QUEUE_DB_ID')
        self.job_log_db_id = os.getenv('JOB_LOG_DB_ID')
    
    def generate_api_key(self, partner_name: str) -> str:
        """Generate secure API key for partner"""
        random_token = secrets.token_urlsafe(32)
        prefix = "ep_" + partner_name[:3].lower()
        api_key = f"{prefix}_{random_token}"
        return api_key
    
    def hash_api_key(self, api_key: str) -> str:
        """Hash API key for secure storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    def create_partner(
        self,
        partner_name: str,
        tier: str = "Free",
        quota_monthly: int = 100,
        revenue_share_pct: float = 0.0,
        contact_email: str = ""
    ) -> Dict[str, Any]:
        """Create new partner account"""
        
        if not self.partners_db_id:
            return {"ok": False, "error": "Partners database not configured"}
        
        try:
            # Generate API key
            api_key = self.generate_api_key(partner_name)
            api_key_hash = self.hash_api_key(api_key)
            
            properties = {
                "Partner Name": {"title": [{"text": {"content": partner_name}}]},
                "API Key": {"rich_text": [{"text": {"content": api_key_hash}}]},  # Store hash
                "Tier": {"select": {"name": tier}},
                "Quota (monthly)": {"number": quota_monthly},
                "Usage (current)": {"number": 0},
                "Revenue Share %": {"number": revenue_share_pct},
                "Total Revenue": {"number": 0},
                "Payout Status": {"select": {"name": "Pending"}},
                "Active": {"checkbox": True},
                "Created Date": {"date": {"start": datetime.utcnow().isoformat()}},
            }
            
            if contact_email:
                properties["Contact Email"] = {"email": contact_email}
            
            page = self.notion.pages.create(
                parent={"database_id": self.partners_db_id},
                properties=properties
            )
            
            return {
                "ok": True,
                "partner_id": page['id'],
                "api_key": api_key,  # Return plain key ONCE - never again!
                "message": "Save this API key securely. It will not be shown again."
            }
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def validate_api_key(self, api_key: str) -> Dict[str, Any]:
        """Validate API key and check quota"""
        
        if not self.partners_db_id or not api_key:
            return {"ok": False, "error": "Invalid API key"}
        
        try:
            api_key_hash = self.hash_api_key(api_key)
            
            # Find partner by hashed key
            response = self.notion.databases.query(
                database_id=self.partners_db_id,
                filter={
                    "property": "API Key",
                    "rich_text": {"equals": api_key_hash}
                }
            )
            
            if not response['results']:
                return {"ok": False, "error": "Invalid API key"}
            
            partner = response['results'][0]
            props = partner['properties']
            
            # Check if active
            if not props.get('Active', {}).get('checkbox'):
                return {"ok": False, "error": "Partner account inactive"}
            
            # Check quota
            quota = props.get('Quota (monthly)', {}).get('number', 0)
            usage = props.get('Usage (current)', {}).get('number', 0)
            
            if usage >= quota:
                return {
                    "ok": False,
                    "error": "Monthly quota exceeded",
                    "quota": quota,
                    "usage": usage
                }
            
            return {
                "ok": True,
                "partner_id": partner['id'],
                "partner_name": props.get('Partner Name', {}).get('title', [{}])[0].get('text', {}).get('content', 'Unknown'),
                "tier": props.get('Tier', {}).get('select', {}).get('name', 'Free'),
                "quota": quota,
                "usage": usage,
                "remaining": quota - usage
            }
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def increment_usage(self, partner_id: str) -> Dict[str, Any]:
        """Increment partner's usage counter"""
        
        try:
            # Get current usage
            partner = self.notion.pages.retrieve(page_id=partner_id)
            current_usage = partner['properties'].get('Usage (current)', {}).get('number', 0)
            
            # Update
            self.notion.pages.update(
                page_id=partner_id,
                properties={
                    "Usage (current)": {"number": current_usage + 1}
                }
            )
            
            return {"ok": True, "new_usage": current_usage + 1}
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def submit_job_via_api(
        self,
        api_key: str,
        job_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Submit job through partner API"""
        
        # Validate API key and quota
        validation = self.validate_api_key(api_key)
        
        if not validation['ok']:
            return validation
        
        # Create job in queue
        if not self.queue_db_id:
            return {"ok": False, "error": "Queue database not configured"}
        
        try:
            properties = {
                "Task Name": {"title": [{"text": {"content": job_data.get('task_name', 'API Job')}}]},
                "Task Details": {"rich_text": [{"text": {"content": job_data.get('task_details', '')}}]},
                "Task Type": {"select": {"name": job_data.get('task_type', 'API')}},
                "Trigger": {"checkbox": True},  # Auto-trigger
                "Status": {"select": {"name": "Triggered"}},
                "Created Time": {"date": {"start": datetime.utcnow().isoformat()}},
                "Client": {"rich_text": [{"text": {"content": validation['partner_name']}}]},
            }
            
            page = self.notion.pages.create(
                parent={"database_id": self.queue_db_id},
                properties=properties
            )
            
            # Increment usage
            self.increment_usage(validation['partner_id'])
            
            return {
                "ok": True,
                "job_id": page['id'],
                "status": "queued",
                "message": "Job submitted successfully",
                "remaining_quota": validation['remaining'] - 1
            }
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def get_job_results(self, api_key: str, job_id: str) -> Dict[str, Any]:
        """Get results for a submitted job"""
        
        # Validate API key
        validation = self.validate_api_key(api_key)
        
        if not validation['ok']:
            return validation
        
        # Get job from queue or log
        try:
            page = self.notion.pages.retrieve(page_id=job_id)
            props = page['properties']
            
            # Verify ownership (client matches partner name)
            client = props.get('Client', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
            if client != validation['partner_name']:
                return {"ok": False, "error": "Unauthorized - job belongs to another partner"}
            
            status = props.get('Status', {}).get('select', {}).get('name', 'Unknown')
            result = props.get('AI Output', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
            qa_score = props.get('QA Score', {}).get('number')
            
            return {
                "ok": True,
                "job_id": job_id,
                "status": status.lower(),
                "result": result,
                "qa_score": qa_score,
                "completed": status in ["Done-Success", "Done-High QA"]
            }
        
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def get_partner_stats(self, api_key: str) -> Dict[str, Any]:
        """Get partner usage statistics"""
        
        validation = self.validate_api_key(api_key)
        
        if not validation['ok']:
            return validation
        
        return {
            "ok": True,
            "partner": validation['partner_name'],
            "tier": validation['tier'],
            "quota": {
                "monthly_limit": validation['quota'],
                "used": validation['usage'],
                "remaining": validation['remaining'],
                "usage_pct": round((validation['usage'] / validation['quota'] * 100) if validation['quota'] > 0 else 0, 2)
            }
        }


# Middleware for quota enforcement
def require_api_key(request: Request) -> Optional[Dict[str, Any]]:
    """Flask middleware to validate API key"""
    
    api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
    
    if not api_key:
        return {"ok": False, "error": "Missing API key. Include X-API-Key header or api_key parameter."}
    
    marketplace = MarketplaceAPI()
    validation = marketplace.validate_api_key(api_key)
    
    if not validation['ok']:
        return validation
    
    # Attach partner info to request
    request.partner_info = validation
    return None  # None = validation passed


# Singleton
_marketplace_api = None

def get_marketplace_api() -> MarketplaceAPI:
    """Get or create marketplace API instance"""
    global _marketplace_api
    if _marketplace_api is None:
        _marketplace_api = MarketplaceAPI()
    return _marketplace_api
