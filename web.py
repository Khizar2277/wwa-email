import streamlit as st
import requests
import json

# Gemini API Configuration
GEMINI_API_KEY = "AIzaSyAFJYqU0SENf15D29ZAtPPP914XMPVHbnk"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def generate_email(prompt):
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
    if response.status_code == 200:
        response_json = response.json()
        return response_json["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI
st.title("WWA Email Writer")

# User input
prompt = st.text_area("Enter your email prompt:", "Write a professional email for a job application.")

if st.button("Generate Email"):
    if prompt.strip():
        email_content = generate_email(prompt)
        st.subheader("Generated Email:")
        st.write(email_content)
    else:
        st.error("Please enter a valid prompt.")
