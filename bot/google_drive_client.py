import requests
import os
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from typing import Dict, List, Optional
from bot import config

class GoogleDriveClientWrapper:
    def __init__(self):
        self.connection_settings = None
    
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
            f'https://{hostname}/api/v2/connection?include_secrets=true&connector_names=google-drive',
            headers={
                'Accept': 'application/json',
                'X_REPLIT_TOKEN': x_replit_token
            }
        )
        
        data = response.json()
        items = data.get('items', [])
        
        if not items:
            raise Exception('Google Drive not connected')
        
        self.connection_settings = items[0]
        access_token = (
            self.connection_settings.get('settings', {}).get('access_token') or
            self.connection_settings.get('settings', {}).get('oauth', {}).get('credentials', {}).get('access_token')
        )
        
        if not access_token:
            raise Exception('Google Drive access token not found')
        
        return access_token
    
    def get_client(self):
        access_token = self.get_access_token()
        credentials = Credentials(token=access_token)
        return build('drive', 'v3', credentials=credentials)
    
    def list_files(self, query: Optional[str] = None, page_size: int = 10) -> List[Dict]:
        service = self.get_client()
        
        params = {'pageSize': page_size, 'fields': 'files(id, name, mimeType, createdTime)'}
        if query:
            params['q'] = query
        
        results = service.files().list(**params).execute()
        return results.get('files', [])
    
    def download_file(self, file_id: str) -> bytes:
        service = self.get_client()
        request = service.files().get_media(fileId=file_id)
        return request.execute()
