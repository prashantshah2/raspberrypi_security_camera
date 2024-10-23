import os
import smtplib
import ssl
import socket
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jproperties import Properties


def send_smtp_gmail(sender_email, receiver_email, password, subject, body):
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Create the email's MIMEText
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Gmail SMTP server and send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully")
    
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    configs = Properties()

    with open('app-config.properties', 'rb') as config_file:
        configs.load(config_file)
    sender_email = configs.get("FROM_EMAIL").data
    receiver_email = configs.get("TO_EMAIL").data
    password = os.environ.get('MAIL_APP_PASSWORD')
    subject = "Motion Detected"
    tim = datetime.now().strftime('%H:%M:%S %p')
    body = 'Raspberry PI ({}): Motion detected at {}'.format(socket.gethostname(), tim)

    send_smtp_gmail(sender_email, receiver_email, password, subject, body)

if __name__ == "__main__":
    main()