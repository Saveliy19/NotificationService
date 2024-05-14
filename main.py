# rabbitmq_consumer.py
import pika
from app.email_sender import EmailSender
from app.config import RMQ_NAME, RMQ_PASSWORD

def callback(ch, method, properties, body):
    receiver_email, subject, message = body.decode().split(',')
    print(f"Received notification: Email: {receiver_email}, Subject: {subject}, Message: {message}")
    sender = EmailSender()
    sender.send_email(receiver_email, subject, body.decode())

def consume():
    credentials = pika.PlainCredentials(RMQ_NAME, RMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='notification_queue', durable=True)
    channel.basic_consume(queue='notification_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    consume()