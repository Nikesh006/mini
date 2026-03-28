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

def send_email(subject, html_body, to_email):
    """Sends an HTML email using the Flask application's configuration."""
    # Use current_app to access app config in a utility function
    smtp_server = current_app.config.get('MAIL_SERVER')
    smtp_port = current_app.config.get('MAIL_PORT')
    smtp_user = current_app.config.get('MAIL_USERNAME')
    smtp_password = current_app.config.get('MAIL_PASSWORD')
    sender_email = current_app.config.get('MAIL_DEFAULT_SENDER')

    if not all([smtp_server, smtp_port, smtp_user, smtp_password, sender_email]):
        print("Email configuration missing. Skipping email sending.")
        return False

    msg = MIMEMultipart()
    msg['From'] = f"Nammude Gym <{sender_email}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Attach HTML body
    msg.attach(MIMEText(html_body, 'html'))

    try:
        print(f"Attempting to send email to {to_email}...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=5)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        print(f"Email successfully sent to {to_email}!")
        return True
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        return False

def allowed_file(filename):
    """Checks if a filename has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
