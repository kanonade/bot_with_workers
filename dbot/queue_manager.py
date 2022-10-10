import pika
import uuid
import os
import json

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")


class QueueManager:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="prompts", durable=True)

        result = self.channel.queue_declare(
            queue="images", durable=True
        )  # , exclusive=True)
        self.image_queue = result.method.queue

    def enqueue_prompt(self, req: dict):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange="",
            routing_key="prompts",
            body=json.dumps(req),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                reply_to=self.image_queue,
                correlation_id=self.corr_id,
                content_type="application/json",
            ),
        )
        print(f"Sent {req['prompt']} to queue")
