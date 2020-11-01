import pika
from workshop_helper import make_connection

exchange_name = 'broadcast_chat'

connection = make_connection()

channel = connection.channel()

channel.exchange_declare(exchange='broadcast_chat', exchange_type="fanout")

queue_declaration_result = channel.queue_declare(queue='', exclusive=True)
queue_name = queue_declaration_result.method.queue

channel.queue_bind(queue=queue_name, exchange=exchange_name)

def send(chan, routing_key, message):
    chan.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
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


