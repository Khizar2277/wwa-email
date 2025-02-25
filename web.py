import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
ACCESS_CODE = "WWA987@"

def send_email(sender_email, sender_password, smtp_server, smtp_port, recipient_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        
        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

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

st.title("WWA AI Email Generator & Sender")

# Access code input
user_code = st.text_input("Enter access code to unlock additional functionality:", type="password")

if user_code == ACCESS_CODE:
    st.success("Access granted!")

    # Dropdown menu for categories
    category = st.selectbox("Select a category:", CATEGORIES)

    # User input
    prompt = st.text_area("Enter email details:", "Write a promotional email for a new product.")
    recipient_email = st.text_input("Recipient Email")
    subject = st.text_input("Email Subject")

    # Hostinger SMTP Details
    smtp_server = "smtp.hostinger.com"
    smtp_port = 587
    sender_email = "blog@worldwideadverts.info"
    sender_password = "Madaz[33-77]"

# Placeholder for generated email
    message = ""

    if st.button("Generate Email"):
        if prompt.strip():
            message = generate_email(category, prompt)
            st.session_state["generated_email"] = message  # Store in session state
            st.subheader("Generated Promotional Email:")
            st.write(message)
        else:
            st.error("Please enter a valid prompt.")

    if "generated_email" in st.session_state:
     message = st.session_state["generated_email"]

    if st.button("Send Email"):
        if recipient_email and subject and message:
        result = send_email(sender_email, sender_password, smtp_server, smtp_port, recipient_email, subject, message)
        st.success(result)
    else:
        st.error("Please fill in all email fields before sending.")
     else:
            st.error("Please enter both a topic and a keyword.")
    else:
        st.warning("Enter the correct access code to unlock blog generation.")

