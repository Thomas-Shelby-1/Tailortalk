from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from dotenv import load_dotenv
from calendar_utils import create_event, list_events, get_upcoming_events

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:8501"] for streamlit only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "TailorTalk API is running"}

@app.post("/chat")
async def chat_endpoint(request: Request):
    body = await request.json()
    prompt = body.get("message")

    try:
        response = model.generate_content(prompt)
        reply = response.text.strip()

        # BASIC INTENT DETECTION
        lower = reply.lower()

        if "scheduled" in lower or "created" in lower:
            # Fake example: Gemini returns these in response if asked to "schedule..."
            event_link = create_event(
                summary="Meeting from TailorTalk",
                description=prompt,
                start_time="2025-06-27T15:00:00+05:30",  # placeholder
                end_time="2025-06-27T16:00:00+05:30"
            )
            reply += f"\n\n📅 [View your event]({event_link})"

        elif "you have" in lower and "meeting" in lower:
            events = get_upcoming_events()
            if events:
                event_list = "\n".join(
                    [f"- {e['summary']} at {e['start'].get('dateTime', 'unknown')}" for e in events]
                )
                reply = "Here are your upcoming events:\n" + event_list
            else:
                reply = "No upcoming events found."

        return {"reply": reply}

    except Exception as e:
        print("Gemini or Calendar error:", e)
        return {"reply": f"Error: {str(e)}"}
