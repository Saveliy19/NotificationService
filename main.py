from app.message_consumer import EmailConsumer
from app.logger import setup_logging

def main():
    # Настройка логирования
    setup_logging()
    
    # Создание и запуск потребителя сообщений
    consumer = EmailConsumer()
    consumer.start_consuming()

if __name__ == "__main__":
    main()
