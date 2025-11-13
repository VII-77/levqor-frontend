"""
Notion API Keys Database Helper
Logs API key creation, usage, and tier information
"""
import os
import requests
from datetime import datetime

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "").strip()
NOTION_API_KEYS_DB_ID = os.getenv("NOTION_API_KEYS_DB_ID", "").strip()

def log_api_key_creation(user_id: str, key_id: str, tier: str, calls_limit: int):
    """Log new API key creation to Notion"""
    if not NOTION_TOKEN or not NOTION_API_KEYS_DB_ID:
        print("⚠️ Notion credentials not configured for API keys tracking")
        return False
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    data = {
        "parent": {"database_id": NOTION_API_KEYS_DB_ID},
        "properties": {
            "Name": {
                "title": [{"text": {"content": f"{tier.upper()} Key - {key_id[:16]}"}}]
            },
            "User ID": {
                "rich_text": [{"text": {"content": user_id}}]
            },
            "Key ID": {
                "rich_text": [{"text": {"content": key_id}}]
            },
            "Tier": {
                "select": {"name": tier.capitalize()}
            },
            "Calls Used": {
                "number": 0
            },
            "Calls Limit": {
                "number": calls_limit if calls_limit != -1 else 999999
            },
            "Created At": {
                "date": {"start": datetime.utcnow().isoformat()}
            },
            "Status": {
                "select": {"name": "Active"}
            }
        }
    }
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            print(f"✅ Logged API key {key_id[:16]}... to Notion")
            return True
        else:
            print(f"❌ Failed to log to Notion: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Notion logging error: {e}")
        return False

def update_api_key_usage(key_id: str, calls_used: int, calls_limit: int):
    """Update API key usage in Notion"""
    if not NOTION_TOKEN or not NOTION_API_KEYS_DB_ID:
        return False
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Query for the page by Key ID
    query_data = {
        "database_id": NOTION_API_KEYS_DB_ID,
        "filter": {
            "property": "Key ID",
            "rich_text": {
                "equals": key_id
            }
        }
    }
    
    try:
        query_response = requests.post(
            "https://api.notion.com/v1/databases/query",
            headers=headers,
            json=query_data
        )
        
        if query_response.status_code != 200:
            return False
        
        results = query_response.json().get("results", [])
        if not results:
            return False
        
        page_id = results[0]["id"]
        
        # Update the page
        update_data = {
            "properties": {
                "Calls Used": {"number": calls_used},
                "Calls Limit": {"number": calls_limit if calls_limit != -1 else 999999}
            }
        }
        
        update_response = requests.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers=headers,
            json=update_data
        )
        
        return update_response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error updating Notion: {e}")
        return False

def revoke_api_key_in_notion(key_id: str):
    """Mark API key as revoked in Notion"""
    if not NOTION_TOKEN or not NOTION_API_KEYS_DB_ID:
        return False
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Query for the page
    query_data = {
        "database_id": NOTION_API_KEYS_DB_ID,
        "filter": {
            "property": "Key ID",
            "rich_text": {
                "equals": key_id
            }
        }
    }
    
    try:
        query_response = requests.post(
            "https://api.notion.com/v1/databases/query",
            headers=headers,
            json=query_data
        )
        
        if query_response.status_code != 200:
            return False
        
        results = query_response.json().get("results", [])
        if not results:
            return False
        
        page_id = results[0]["id"]
        
        # Update status to Revoked
        update_data = {
            "properties": {
                "Status": {"select": {"name": "Revoked"}}
            }
        }
        
        update_response = requests.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers=headers,
            json=update_data
        )
        
        if update_response.status_code == 200:
            print(f"✅ Marked API key {key_id[:16]}... as revoked in Notion")
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error revoking in Notion: {e}")
        return False
