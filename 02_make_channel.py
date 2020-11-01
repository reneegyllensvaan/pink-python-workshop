import pika
from workshop_helper import make_connection

connection = make_connection()

channel = connection.channel()
channel.queue_declare(queue='chat')
