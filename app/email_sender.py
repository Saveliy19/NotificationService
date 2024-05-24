import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import SMTP_PORT, SMTP_SERVER, USERNAME, PASSWORD
import logging

class EmailSender:
    def __init__(self):
        # Инициализация SMTP параметров
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.username = USERNAME
        self.password = PASSWORD

    def send_email(self, receiver_emails, subject, body):
        # Создание MIME-сообщения
        message = MIMEMultipart()
        message['From'] = self.username
        message['To'] = ", ".join(receiver_emails)
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            # Установка соединения с SMTP сервером и отправка письма
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = message.as_string()
            for receiver_email in receiver_emails:
                server.sendmail(self.username, receiver_email, text)
            server.quit()
            return True
        except Exception as e:
            # Логирование ошибки при отправке письма
            logging.error(f"Failed to send email: {e}")
            return False
