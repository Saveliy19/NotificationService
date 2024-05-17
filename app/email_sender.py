# email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import SMTP_PORT, SMTP_SERVER, USERNAME, PASSWORD

class EmailSender:
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.username = USERNAME
        self.password = PASSWORD

    def send_email(self, receiver_emails, subject, body):
        message = MIMEMultipart()
        message['From'] = self.username
        message['To'] = ", ".join(receiver_emails)
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = message.as_string()
            # Отправляем письмо каждому получателю в списке
            for receiver_email in receiver_emails:
                server.sendmail(self.username, receiver_email, text)
            server.quit()
        except:
            return False
        return True

