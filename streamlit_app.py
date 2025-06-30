import streamlit as st
import requests

st.set_page_config(page_title="TailorTalk Calendar Assistant")

st.title("📅 TailorTalk - Smart Calendar Assistant")
st.markdown("Enter your command to schedule, view, or cancel an event.")

user_input = st.text_input("What would you like to do?", placeholder="e.g. Schedule a meeting with John on Friday at 3 PM")

if st.button("Submit") and user_input:
    try:
        response = requests.post(
            "http://localhost:8000/chat",  # Replace with your deployed FastAPI URL if needed
            json={"user_input": user_input}
        )
        if response.status_code == 200:
            result = response.json()
            st.success(result.get("reply", "Response received."))
            if "calendar" in result:
                st.write("📋 Calendar Details:")
                st.json(result["calendar"])
        else:
            st.error(f"Error: {response.status_code}")
    except Exception as e:
        st.error(f"Failed to reach backend: {e}")
