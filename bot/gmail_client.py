import requests
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
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
            f'https://{hostname}/api/v2/connection?include_secrets=true&connector_names=google-mail',
            headers={
                'Accept': 'application/json',
                'X_REPLIT_TOKEN': x_replit_token
            }
        )
        
        data = response.json()
        items = data.get('items', [])
        
        if not items:
            raise Exception('Gmail not connected')
        
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
        """Get the authenticated user's email address from environment or connection settings"""
        # Try to get from environment variable first
        email = os.getenv('SMTP_USER') or os.getenv('ALERT_TO')
        if email:
            return email
        
        # Try to get from connection settings
        try:
            if self.connection_settings:
                email = self.connection_settings.get('settings', {}).get('email')
                if email:
                    return email
        except:
            pass
        
        # Default fallback - user will need to set ALERT_TO env var
        raise Exception('Email address not found. Please set ALERT_TO environment variable.')
    
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
    
    def send_email_with_attachment(
        self,
        to_email: str,
        subject: str,
        body: str,
        attachment_data: bytes,
        attachment_filename: str = "attachment.pdf",
        attachment_mimetype: str = "application/pdf",
        from_email: str | None = None
    ) -> bool:
        """
        Send email with attachment via Gmail API
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body (plain text)
            attachment_data: Binary data for attachment
            attachment_filename: Filename for attachment
            attachment_mimetype: MIME type of attachment
            from_email: Optional sender email
            
        Returns:
            bool: True if sent successfully
        """
        try:
            service = self.get_gmail_client()
            
            # Get sender email if not provided
            if not from_email:
                from_email = self.get_user_email()
            
            # Create multipart message
            message = MIMEMultipart()
            message['to'] = to_email
            message['from'] = from_email
            message['subject'] = subject
            
            # Attach body
            message.attach(MIMEText(body, 'plain'))
            
            # Attach file
            attachment = MIMEApplication(attachment_data, _subtype=attachment_mimetype.split('/')[-1])
            attachment.add_header('Content-Disposition', 'attachment', filename=attachment_filename)
            message.attach(attachment)
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send via Gmail API
            result = service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            print(f"✅ Email with attachment sent to {to_email} - Message ID: {result.get('id')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email with attachment to {to_email}: {e}")
            return False
