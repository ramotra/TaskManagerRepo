import pika
import smtplib
from email.message import EmailMessage

def callback(ch, method, properties, body):
    normal_string = body.decode('utf-8')
    print(normal_string)
    print("Email sent to Opika with data = {}".format(normal_string))
    return True

# # # # # # # # # # # # # # # Connect to RabbitMQ # # # # # # 

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='app_to_service', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.basic_consume(queue='app_to_service', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
