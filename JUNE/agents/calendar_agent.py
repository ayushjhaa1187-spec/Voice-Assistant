from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

class CalendarAgent:
    def __init__(self):
        # self.service = self._build_service()
        self.service = None

    def _build_service(self):
        import pickle, os
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow

        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None

        if os.path.exists('calendar_token.pickle'):
            with open('calendar_token.pickle', 'rb') as f:
                creds = pickle.load(f)

        if not creds or not creds.valid:
            if creds and creds.expired:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('calendar_token.pickle', 'wb') as f:
                pickle.dump(creds, f)

        return build('calendar', 'v3', credentials=creds)

    async def execute(self, action: str, **kwargs):
        if self.service is None:
             if os.path.exists('credentials.json'):
                 try:
                     self.service = self._build_service()
                 except Exception as e:
                     return f"Failed to authenticate Calendar: {e}"
             else:
                 return "CalendarAgent not authenticated. Missing credentials.json."

        if action == "get_today":
            return await self.get_today_events()
        elif action == "schedule":
            return await self.create_event(**kwargs)
        elif action == "get_week":
            return await self.get_week_events()
        elif action == "free_slots":
            return await self.find_free_slots(kwargs.get("date"))
        return "Unknown action"

    async def get_today_events(self):
        now = datetime.utcnow().isoformat() + 'Z'
        end = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'

        events_result = self.service.events().list(
            calendarId='primary', timeMin=now, timeMax=end,
            singleEvents=True, orderBy='startTime'
        ).execute()

        return events_result.get('items', [])

    async def create_event(self, title: str, start: str, end: str, description: str = ""):
        event = {
            'summary': title,
            'description': description,
            'start': {'dateTime': start, 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end, 'timeZone': 'Asia/Kolkata'},
        }
        created = self.service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {created.get('htmlLink')}"
