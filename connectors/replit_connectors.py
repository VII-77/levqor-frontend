"""
Replit-managed connector integrations
Handles OAuth-based services via Replit Connectors API
"""
import os
import json
import requests


def get_replit_token():
    """Get Replit identity token for connector API"""
    if os.environ.get("REPL_IDENTITY"):
        return f"repl {os.environ['REPL_IDENTITY']}"
    elif os.environ.get("WEB_REPL_RENEWAL"):
        return f"depl {os.environ['WEB_REPL_RENEWAL']}"
    return None


def get_notion_token():
    """Get Notion OAuth token from Replit Connectors"""
    hostname = os.environ.get("REPLIT_CONNECTORS_HOSTNAME")
    x_replit_token = get_replit_token()
    
    if not hostname or not x_replit_token:
        return None
    
    try:
        resp = requests.get(
            f"https://{hostname}/api/v2/connection",
            params={"include_secrets": "true", "connector_names": "notion"},
            headers={
                "Accept": "application/json",
                "X_REPLIT_TOKEN": x_replit_token
            },
            timeout=5
        )
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("items") and len(data["items"]) > 0:
            settings = data["items"][0].get("settings", {})
            return settings.get("access_token") or settings.get("oauth", {}).get("credentials", {}).get("access_token")
    except Exception:
        pass
    
    return None


def get_google_sheets_token():
    """Get Google Sheets OAuth token from Replit Connectors"""
    hostname = os.environ.get("REPLIT_CONNECTORS_HOSTNAME")
    x_replit_token = get_replit_token()
    
    if not hostname or not x_replit_token:
        return None
    
    try:
        resp = requests.get(
            f"https://{hostname}/api/v2/connection",
            params={"include_secrets": "true", "connector_names": "google-sheet"},
            headers={
                "Accept": "application/json",
                "X_REPLIT_TOKEN": x_replit_token
            },
            timeout=5
        )
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("items") and len(data["items"]) > 0:
            settings = data["items"][0].get("settings", {})
            return settings.get("access_token") or settings.get("oauth", {}).get("credentials", {}).get("access_token")
    except Exception:
        pass
    
    return None
