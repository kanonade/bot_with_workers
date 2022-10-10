import random
import os
import time
import pika
import logging
import json

log = logging.getLogger(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")


class Worker:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="prompts", durable=True)
        self.channel.queue_declare(queue="images", durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue="prompts", on_message_callback=self.callback)

    def callback(self, ch, method, properties, body):
        request = json.loads(body)
        print(f"Received {request['prompt']}")

        print("Waiting random time to simulate work")
        time.sleep(random.randint(1, 3))

        response = {
            "user": request["user"],
            "channel": request["channel"],
            "image": "Pretend I'm an image of " + request["prompt"],
        }

        ch.basic_publish(
            exchange="",
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=json.dumps(response),
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Sent response for {request['prompt']}")


if __name__ == "__main__":
    print("starting worker")
    worker = Worker()
    worker.channel.start_consuming()
    worker.channel.stop_consuming()
