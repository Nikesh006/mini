from app import app, send_email

def test_mail():
    # Replace with your own email to test
    test_recipient = "nammudegym@gmail.com" 
    subject = "Nammude Gym: Email Connectivity Test"
    body = """
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
            <h2 style="color: #ff4b2b;">Connectivity Test Successful!</h2>
            <p>Your Gym Management System is now configured to send automated emails.</p>
            <p>This includes OTPs, booking confirmations, and member approvals.</p>
            <hr>
            <p style="font-size: 12px; color: #777;">Sent from Nammude Gym Admin System</p>
        </div>
    </body>
    </html>
    """
    
    with app.app_context():
        print(f"Starting email test to {test_recipient}...")
        success = send_email(subject, body, test_recipient)
        if success:
            print("SUCCESS: The system can send emails!")
        else:
            print("FAILURE: Email sending failed. Check your credentials or internet connection.")

if __name__ == "__main__":
    test_mail()
