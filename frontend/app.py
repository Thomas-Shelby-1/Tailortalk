# tailortalk/frontend/app.py

import streamlit as st
import requests
import json

st.set_page_config(page_title="TailorTalk", layout="centered")
st.title("🧵 TailorTalk – Calendar Assistant")

# 1. Show sample prompt buttons
st.markdown("### Try one of these:")
sample_inputs = [
    "Schedule a meeting with John on Friday at 3 PM",
    "Cancel my 10 AM meeting tomorrow",
    "What meetings do I have next week?",
    "Reschedule team meeting to next Monday at 11 AM",
]
cols = st.columns(len(sample_inputs))
for i, prompt in enumerate(sample_inputs):
    if cols[i].button(prompt):
        st.session_state["quick_prompt"] = prompt

# 2. Handle chat input (either from manual input or button click)
user_input = st.chat_input("Type here to schedule a meeting...")
if "quick_prompt" in st.session_state:
    user_input = st.session_state.pop("quick_prompt")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 3. Send to backend if there's input
if user_input:
    st.session_state.chat_history.append(("user", user_input))

    try:
        response = requests.post("http://localhost:8000/chat", json={"message": user_input})
        result = response.json()
        reply = result.get("reply", "Sorry, I couldn't understand that.")
    except Exception as e:
        st.error(f"Backend error: {e}")
        reply = "Backend error. Check console logs."

    st.session_state.chat_history.append(("ai", reply))

# 4. Render chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(msg)
