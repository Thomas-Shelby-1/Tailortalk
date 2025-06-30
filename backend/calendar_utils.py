from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def get_calendar_service():
    creds = Credentials(
        None,
        refresh_token=os.getenv("GOOGLE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    service = build("calendar", "v3", credentials=creds)
    return service

def list_events(max_results=10):
    service = get_calendar_service()
    events_result = service.events().list(
        calendarId="primary",
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    return events_result.get("items", [])

def create_event(summary, description, start_time, end_time):
    service = get_calendar_service()
    event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')

def get_upcoming_events(max_results=5):
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])
