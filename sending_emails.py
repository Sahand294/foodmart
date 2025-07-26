import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from models.sitesetting import SiteSetting


class Send:
    @staticmethod
    def send_mail(subject, sender_email, body):
        smtp_user = str(SiteSetting.query.filter_by(key="smtp_user").first())
        smtp_pass = str(SiteSetting.query.filter_by(key="smtp_pass").first())
        receiver_email = str(SiteSetting.query.filter_by(key="receiver_email").first())

        smtp_server = str(SiteSetting.query.filter_by(key="smtp_server").first())
        smtp_port = str(SiteSetting.query.filter_by(key="smtp_port").first())
        # smtp_user = "foodmartstore874@gmail.com"
        # smtp_pass = "kgfomdvfxsmnlvzb"  # Remove spaces when using it in code
        # receiver_email = "sahandha1391@gmail.com"
        #
        # smtp_server = "smtp.gmail.com"
        # smtp_port = 587
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg["Reply-To"] = sender_email

        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
                print("✅ Email sent successfully.")
        except Exception as e:
            print(f"❌ Error sending email: {e}")



