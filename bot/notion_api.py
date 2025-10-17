import requests
import os
from datetime import datetime
from notion_client import Client as NotionClient
from typing import Dict, List, Optional, Any
from bot import config

class NotionClientWrapper:
    def __init__(self):
        self.connection_settings = None
        self.client = None
    
    def get_x_replit_token(self) -> str:
        if config.REPL_IDENTITY:
            return f'repl {config.REPL_IDENTITY}'
        elif config.WEB_REPL_RENEWAL:
            return f'depl {config.WEB_REPL_RENEWAL}'
        else:
            raise Exception('X_REPLIT_TOKEN not found for repl/depl')
    
    def get_access_token(self) -> str:
        if (self.connection_settings and 
            self.connection_settings.get('settings', {}).get('expires_at') and
            datetime.fromisoformat(self.connection_settings['settings']['expires_at'].replace('Z', '+00:00')).timestamp() > datetime.now().timestamp()):
            return self.connection_settings['settings']['access_token']
        
        hostname = config.REPLIT_CONNECTORS_HOSTNAME
        x_replit_token = self.get_x_replit_token()
        
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
            raise Exception('Notion not connected')
        
        self.connection_settings = items[0]
        access_token = (
            self.connection_settings.get('settings', {}).get('access_token') or
            self.connection_settings.get('settings', {}).get('oauth', {}).get('credentials', {}).get('access_token')
        )
        
        if not access_token:
            raise Exception('Notion access token not found')
        
        return access_token
    
    def get_client(self) -> Any:
        access_token = self.get_access_token()
        return NotionClient(auth=access_token)
    
    def query_database(self, database_id: str, filter_criteria: Optional[Dict] = None) -> List[Dict]:
        client = self.get_client()
        
        query_params: Dict[str, Any] = {"database_id": database_id}
        if filter_criteria:
            query_params["filter"] = filter_criteria
        
        response = client.databases.query(**query_params)
        return response.get('results', [])
    
    def get_triggered_tasks(self) -> List[Dict]:
        if not config.AUTOMATION_QUEUE_DB_ID:
            raise ValueError("AUTOMATION_QUEUE_DB_ID is not configured")
        
        filter_criteria = {
            "property": "Trigger",
            "checkbox": {
                "equals": True
            }
        }
        return self.query_database(config.AUTOMATION_QUEUE_DB_ID, filter_criteria)
    
    def update_page(self, page_id: str, properties: Dict) -> Dict:
        client = self.get_client()
        return client.pages.update(page_id=page_id, properties=properties)
    
    def create_page(self, database_id: str, properties: Dict) -> Dict:
        client = self.get_client()
        return client.pages.create(parent={"database_id": database_id}, properties=properties)
    
    def log_activity(self, task_name: str, status: str, message: str, details: Optional[str] = None, commit: Optional[str] = None):
        if not config.AUTOMATION_LOG_DB_ID:
            raise ValueError("AUTOMATION_LOG_DB_ID is not configured")
        
        properties = {
            "Log Entry": {"title": [{"text": {"content": task_name}}]},
            "Status": {"select": {"name": status}},
            "Message": {"rich_text": [{"text": {"content": message}}]},
            "Timestamp": {"date": {"start": datetime.now().isoformat()}}
        }
        
        if details:
            properties["Details"] = {"rich_text": [{"text": {"content": details[:2000]}}]}
        
        if commit:
            properties["Commit"] = {"rich_text": [{"text": {"content": commit[:40]}}]}
        
        return self.create_page(config.AUTOMATION_LOG_DB_ID, properties)
    
    def log_completed_job(self, job_data: Dict):
        if not config.JOB_LOG_DB_ID:
            raise ValueError("JOB_LOG_DB_ID is not configured")
        
        properties = {
            "Job Name": {"title": [{"text": {"content": job_data.get('job_name', 'Unnamed Job')}}]},
            "QA Score": {"number": job_data.get('qa_score', 0)},
            "Cost": {"number": job_data.get('cost', 0)},
            "Status": {"select": {"name": job_data.get('status', 'Done')}}
        }
        
        if job_data.get('notes'):
            properties["Notes"] = {"rich_text": [{"text": {"content": job_data['notes'][:2000]}}]}
        
        if job_data.get('commit'):
            properties["Commit"] = {"rich_text": [{"text": {"content": job_data['commit'][:40]}}]}
        
        if job_data.get('task_type'):
            properties["Task Type"] = {"select": {"name": job_data['task_type']}}
        
        if job_data.get('duration_ms'):
            properties["Duration (ms)"] = {"number": job_data['duration_ms']}
        
        if job_data.get('tokens_in'):
            properties["Tokens In"] = {"number": job_data['tokens_in']}
        
        if job_data.get('tokens_out'):
            properties["Tokens Out"] = {"number": job_data['tokens_out']}
        
        return self.create_page(config.JOB_LOG_DB_ID, properties)
