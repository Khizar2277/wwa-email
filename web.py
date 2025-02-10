import streamlit as st
import requests
import json

# Gemini API Configuration
GEMINI_API_KEY = "AIzaSyAFJYqU0SENf15D29ZAtPPP914XMPVHbnk"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# Categories for the dropdown menu
CATEGORIES = [
    "Business", "Deals", "Events", "For Sale", "IT/Tech", "Classified", "Jobs",
    "Property", "Resort/Travel", "Services", "Vehicle", "Investment"
]

def generate_email(category, prompt):
    full_prompt = f"Write a promotional email for the '{category}' category. {prompt}"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "contents": [{"parts": [{"text": full_prompt}]}]
    }
    
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
    if response.status_code == 200:
        response_json = response.json()
        return response_json["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI
st.title("AI Promotional Email Generator")

# Dropdown menu for categories
category = st.selectbox("Select a category:", CATEGORIES)

# User input
prompt = st.text_area("Enter email details:", "Write a promotional email for a new product.")

if st.button("Generate Email"):
    if prompt.strip():
        email_content = generate_email(category, prompt)
        st.subheader("Generated Promotional Email:")
        st.write(email_content)
    else:
        st.error("Please enter a valid prompt.")
