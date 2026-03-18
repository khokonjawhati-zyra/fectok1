import os
import base64
import logging
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

logger = logging.getLogger("QuantumSync")

class GmailEngine:
    def __init__(self):
        # We search inside /app on the server
        self.creds_file = 'client_secret.json'
        self.token_file = 'token.json'
        # On server, they might be in /app (WORKDIR) or we can specify /app/token.json
        self.creds_path = os.path.join(os.getcwd(), self.creds_file)
        self.token_path = os.path.join(os.getcwd(), self.token_file)
        
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        self.service = None
        self._authenticate()

    def _authenticate(self):
        try:
            creds = None
            if os.path.exists(self.token_path):
                creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    with open(self.token_path, 'w') as token:
                        token.write(creds.to_json())
                    logger.info("GmailEngine: Access token refreshed successfully.")
                else:
                    logger.error("GmailEngine: 'token.json' missing or invalid on server. Manual re-auth required.")
                    return False
            
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("GmailEngine: Activated and Ready (HTTPS Pulse).")
            return True
        except Exception as e:
            logger.error(f"GmailEngine ERROR: {e}")
            return False

    def send_email(self, sender_email, to_email, subject, body_html):
        if not self.service:
            if not self._authenticate():
                logger.error("GmailEngine: Cannot send email without valid authentication.")
                return False

        try:
            message = MIMEText(body_html, 'html')
            message['to'] = to_email
            message['from'] = sender_email
            message['subject'] = subject
            
            # Encode base64
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            self.service.users().messages().send(userId='me', body={'raw': raw}).execute()
            logger.info(f"GmailEngine: Pulse sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"GmailEngine SEND ERROR: {e}")
            return False

# Global Singleton for easy import in main.py
gmail_engine = GmailEngine()
