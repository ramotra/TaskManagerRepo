import csv, time, logging
from celery import shared_task
from .models import Task
import pika
from rest_framework.response import Response
from rest_framework import status


@shared_task
def generate_csv(user_id):
    filename = f"user_tasks_{user_id}.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Description', 'Completed'])

        tasks = Task.objects.filter(created_by_id=user_id)
        for task in tasks:
            writer.writerow([task.title, task.description, task.completed])
    

@shared_task
def time_consuming_task(data):
    logging.info("Recieved time consuming task request...................")
    
    time.sleep(10)

    logging.info("Task completed and Pushing to RabbitMQ")

    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='app_to_service', durable=True)
    channel.basic_publish(exchange='',
                          routing_key='app_to_service',
                          body=data)
    connection.close()
    logging.info("Task completed and data pushed to RabbitMQ")
    return True