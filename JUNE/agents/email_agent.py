from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

class EmailAgent:
    def __init__(self):
        self.service = None
        # self._authenticate()  # Commented out to avoid errors on init without creds

    def _authenticate(self):
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
        import os, pickle

        SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)

    async def execute(self, action: str, **kwargs):
        if self.service is None:
            return "EmailAgent not authenticated. Configure credentials.json."

        if action == "read_unread":
            return await self.read_unread_emails(kwargs.get("limit", 10))
        elif action == "send":
            return await self.send_email(**kwargs)
        elif action == "search":
            return await self.search_emails(kwargs.get("query"))
        elif action == "summarize":
            return await self.summarize_inbox()
        return "Unknown action"

    async def read_unread_emails(self, limit: int = 10):
        results = self.service.users().messages().list(
            userId='me', labelIds=['UNREAD'], maxResults=limit
        ).execute()

        emails = []
        for msg in results.get('messages', []):
            email = self.service.users().messages().get(
                userId='me', id=msg['id'], format='full'
            ).execute()

            headers = {h['name']: h['value'] for h in email['payload']['headers']}
            emails.append({
                "id": msg['id'],
                "from": headers.get('From'),
                "subject": headers.get('Subject'),
                "date": headers.get('Date'),
                "snippet": email.get('snippet')
            })
        return emails

    async def send_email(self, to: str, subject: str, body: str):
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        self.service.users().messages().send(
            userId='me', body={'raw': raw}
        ).execute()
        return f"Email sent to {to}"

    async def summarize_inbox(self):
        emails = await self.read_unread_emails(20)
        from llm_router.claude_client import ClaudeClient
        claude = ClaudeClient()
        summary = await claude.complete(
            f"Summarize these emails and highlight urgent ones:\n{emails}"
        )
        return summary
