import pika

def make_connection():
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host="pink.renee.dev",
            credentials=pika.PlainCredentials("pink", "programming"),
            heartbeat=580,
        )
    )
