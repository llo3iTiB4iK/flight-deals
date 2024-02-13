import os
from twilio.rest import Client
import smtplib

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MAIL_PASSWORD")


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.client = Client(account_sid, auth_token)

    def send_message(self, message, send_to=os.environ.get("MY_PHONE_NUM")):
        message = self.client.messages.create(
            from_=os.environ.get("TWILIO_PHONE_NUM"),
            body=message,
            to=send_to
        )
        return f"{message.sid} {message.status}"

    def send_emails(self, emails, message):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}".encode('utf-8')
                )
