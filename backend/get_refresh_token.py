import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow

# Load .env values
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# Use Web application flow
flow = Flow.from_client_config(
    {
        "web": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [REDIRECT_URI]
        }
    },
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)

auth_url, _ = flow.authorization_url(prompt="consent")
print("Please go to this URL and authorize the app:", auth_url)

# After pasting the code from the redirect URL
code = input("Enter the authorization code here: ")
flow.fetch_token(code=code)

creds = flow.credentials
print("Refresh token:", creds.refresh_token)
