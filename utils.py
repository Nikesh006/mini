import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, timezone
from flask import current_app

# Define IST offset
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_time():
    return datetime.now(IST).replace(tzinfo=None)

import requests

def send_email(subject, html_body, to_email):
    """Sends an HTML email using the Resend HTTP API over HTTPS to bypass SMTP blocking."""
    api_key = os.environ.get('RESEND_API_KEY')
    
    if not api_key:
        print("RESEND_API_KEY environment variable missing. Email skipped.")
        return False

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        # Using Resend's default onboarding testing domain. Note: Test mode will only deliver to the 
        # registered email address on your Resend account!
        "from": "Nammude Gym <onboarding@resend.dev>",
        "to": [to_email],
        "subject": subject,
        "html": html_body
    }

    try:
        print(f"Attempting cross-platform API delivery to {to_email}...")
        res = requests.post("https://api.resend.com/emails", json=payload, headers=headers, timeout=10)
        
        if res.status_code == 200:
            print(f"Email API dispatch verified for {to_email}!")
            return True
        else:
            print(f"Resend API Error ({res.status_code}): {res.text}")
            return False
            
    except Exception as e:
        print(f"Fatal delivery error via API endpoints: {e}")
        return False

def allowed_file(filename):
    """Checks if a filename has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
