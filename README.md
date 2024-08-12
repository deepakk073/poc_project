import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(smtp_server, smtp_port, sender_email, sender_password, receiver_email, subject, body):
    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    
    # Attach the body with the msg instance
    message.attach(MIMEText(body, 'plain'))
    
    # Create the SMTP session
    try:
        session = smtplib.SMTP(smtp_server, smtp_port)  # Connect to your SMTP server with specified port
        session.starttls()  # Enable security if the server supports it
        session.login(sender_email, sender_password)  # Login to the email account
        text = message.as_string()
        session.sendmail(sender_email, receiver_email, text)
        session.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    smtp_server = "smtp.yourserver.com"  # Replace with your SMTP server address
    smtp_port = 587  # Replace with your SMTP server port (e.g., 587 for TLS or 465 for SSL)
    sender_email = "your_email@yourserver.com"
    sender_password = "your_password"
    receiver_email = "receiver_email@example.com"
    subject = "Test Email"
    body = "This is a test email sent using Python."
    
    send_email(smtp_server, smtp_port, sender_email, sender_password, receiver_email, subject, body)
