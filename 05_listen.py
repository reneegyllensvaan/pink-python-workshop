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

def listen(chan):
    def on_message(channel, method, properties, body):
        print(' ['+ method.routing_key +']: ' + str(body, 'utf-8'))

    chan.basic_consume(
        queue=queue_name,
        on_message_callback=on_message,
        auto_ack=True,
    )

    chan.start_consuming()


