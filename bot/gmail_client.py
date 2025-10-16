import requests
import os
import base64
from email.mime.text import MIMEText
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from bot import config

class GmailClientWrapper:
    """Gmail client using same OAuth as Google Drive - no additional credentials needed"""
    
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
            raise Exception('Google Drive not connected (needed for Gmail)')
        
        self.connection_settings = items[0]
        access_token = (
            self.connection_settings.get('settings', {}).get('access_token') or
            self.connection_settings.get('settings', {}).get('oauth', {}).get('credentials', {}).get('access_token')
        )
        
        if not access_token:
            raise Exception('Google access token not found')
        
        return access_token
    
    def get_gmail_client(self):
        """Get Gmail API client using existing Google OAuth"""
        access_token = self.get_access_token()
        credentials = Credentials(token=access_token)
        return build('gmail', 'v1', credentials=credentials)
    
    def get_user_email(self) -> str:
        """Get the authenticated user's email address"""
        service = self.get_gmail_client()
        profile = service.users().getProfile(userId='me').execute()
        return profile.get('emailAddress', 'unknown@gmail.com')
    
    def send_email(self, to: str, subject: str, body: str, from_email: str | None = None) -> dict:
        """
        Send email via Gmail API
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (plain text)
            from_email: Optional sender email (defaults to authenticated user)
        
        Returns:
            dict with 'ok' status and message details
        """
        try:
            service = self.get_gmail_client()
            
            # Get sender email if not provided
            if not from_email:
                from_email = self.get_user_email()
            
            # Create MIME message
            message = MIMEText(body)
            message['to'] = to
            message['from'] = from_email
            message['subject'] = subject
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send via Gmail API
            result = service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            print(f"✅ Email sent to {to} - Message ID: {result.get('id')}")
            
            return {
                'ok': True,
                'message_id': result.get('id'),
                'to': to,
                'subject': subject
            }
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Failed to send email to {to}: {error_msg}")
            
            return {
                'ok': False,
                'error': error_msg,
                'to': to,
                'subject': subject
            }
