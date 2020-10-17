import pika, faker, time, sys
fake = faker.Faker()

def on_close(*args, **kwargs):
    print("CONNECTION_CLOSED")
    print(args)
    print(kwargs)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='pink.renee.dev',
        credentials=pika.PlainCredentials('pink', 'programming'),
        heartbeat=580,
    ))

channel = connection.channel()

channel.exchange_declare(exchange='broadcast_chat', exchange_type='fanout')
queue = channel.queue_declare(queue='', exclusive=True).method.queue
channel.queue_bind(queue=queue, exchange='broadcast_chat')

def send(channel, key, body):
    channel.basic_publish(exchange='broadcast_chat', routing_key=key, body=body)

def callback(ch, method, properties, body):
    if body == 'has entered the chat' or body == 'has left the chat':
        print(" " +method.routing_key+ " " + body + ".")
    else:
        print(" [\x1b[1;"+str(31+(hash(method.routing_key)%6))+";40m" +method.routing_key+ "\x1b[0m] " + body + "")

def receive(channel, queue, on_message):
    print("Listening on queue "+queue)
    channel.basic_consume(
        queue=queue,
        on_message_callback=on_message,
        auto_ack=True,
    )
    channel.start_consuming()

# Run actual program
if sys.argv[1] == 'send':
    while 1:
        name = fake.name()
        send(channel, name, "Hello, my name is "+name)
        time.sleep(0.5)
elif sys.argv[1] == 'write':
    print('Enter your name:'),
    name = raw_input()
    send(channel, name, 'has entered the chat')
    try:
        while 1:
            print(name+'>'),
            message = raw_input()
            if message == 'exit':
                raise None
            send(channel, name, message)
    except:
        send(channel, name, 'has left the chat')
else:
    receive(channel, queue, callback)

connection.close()
