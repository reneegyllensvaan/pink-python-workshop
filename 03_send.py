import pika
from workshop_helper import make_connection

queue_name = 'chat'

connection = make_connection()

channel = connection.channel()
channel.queue_declare(queue=queue_name)

def send(chan, routing_key, message):
    chan.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
    )
