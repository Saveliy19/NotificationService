import pika
from app.email_sender import EmailSender
from app.config import RMQ_NAME, RMQ_PASSWORD
import logging
import json
import time

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),  # Логирование в файл
                        logging.StreamHandler()          # Логирование в консоль
                    ])

def callback(ch, method, properties, body):
    data = json.loads(body)
    sender = EmailSender()
    logging.info(f"Received notification: Emails: {data['email_addresses']}, Subject: {data['subject']}, Message: {data['message']}")
    if sender.send_email(data["email_addresses"], data["subject"], data["message"]):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logging.info("Email sent successfully and message acknowledged")
    else:
        logging.error("Error sending email")
        # Если произошла ошибка, отправляем сообщение обратно в очередь
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        logging.info("Message requeued after error")

def consume():
    credentials = pika.PlainCredentials(RMQ_NAME, RMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='notification_queue', durable=True)
    
    # Установка ограничения на количество неподтверждённых сообщений (prefetch count)
    channel.basic_qos(prefetch_count=1)
    
    channel.basic_consume(queue='notification_queue', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    consume()
