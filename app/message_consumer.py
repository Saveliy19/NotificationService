import pika
import json
import logging
from app.email_sender import EmailSender
from app.config import RMQ_NAME, RMQ_PASSWORD
import time

class EmailConsumer:
    def __init__(self):
        # Инициализация отправителя писем
        self.sender = EmailSender()
        # Установка соединения с RabbitMQ
        self.connection = None
        self.channel = None

    def connect(self):
        # Метод для установки соединения с RabbitMQ
        credentials = pika.PlainCredentials(RMQ_NAME, RMQ_PASSWORD)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='notification_queue', durable=True)
        self.channel.basic_qos(prefetch_count=1)

    def callback(self, ch, method, properties, body):
        # Обработка полученного сообщения
        data = json.loads(body)
        logging.info(f"Received notification: Emails: {data['email_addresses']}, Subject: {data['subject']}, Message: {data['message']}")
        if self.sender.send_email(data["email_addresses"], data["subject"], data["message"]):
            # Подтверждение успешной обработки сообщения
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logging.info("Email sent successfully and message acknowledged")
        else:
            # Обработка ошибки отправки письма
            logging.error("Error sending email")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            logging.info("Message requeued after error")

    def start_consuming(self):
        while True:
            try:
                if not self.connection or self.connection.is_closed:
                    self.connect()
                self.channel.basic_consume(queue='notification_queue', on_message_callback=self.callback)
                print("Working!")
                logging.info(' [*] Waiting for messages. To exit press CTRL+C')
                self.channel.start_consuming()
            except pika.exceptions.AMQPConnectionError as e:
                logging.error(f"Connection error: {e}")
                # Попытка повторного подключения через 5 секунд
                time.sleep(5)
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                break
