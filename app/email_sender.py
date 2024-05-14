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

    def send_email(self, receiver_email, subject, body):
        message = MIMEMultipart()
        message['From'] = self.username
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = message.as_string()
            server.sendmail(self.username, receiver_email, text)  # Отправляем письмо нескольким получателям
            print('Письмо успешно отправлено!')
        except Exception as e:
            print(f'Ошибка при отправке письма: {e}')
        finally:
            server.quit()

