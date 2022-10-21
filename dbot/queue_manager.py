import os
from typing import Tuple, Union

import kombu

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")


class QueueManager:
    def __init__(self):
        amqp_host = f"amqp://{RABBITMQ_HOST}:5672"
        self.connection = kombu.Connection(amqp_host)
        self.channel = self.connection.channel()
        self.prompt_queue_name = "prompts"
        self.prompt_queue = kombu.Queue(
            self.prompt_queue_name,
            durable=True,
            exchange=self.prompt_queue_name,
            routing_key=self.prompt_queue_name,
            consumer_arguments={"prefetch_count": 1},
            channel=self.channel,
        )
        self.prompt_queue.declare()
        self.publisher = kombu.Producer(self.channel, self.prompt_queue)

        self.image_queue_name = "images"
        self.image_queue = kombu.Queue(
            self.image_queue_name,
            durable=True,
            exchange=self.image_queue_name,
            routing_key=self.image_queue_name,
            consumer_arguments={"prefetch_count": 1},
            channel=self.channel,
        )
        self.image_queue.declare()

    def enqueue_prompt(self, req: dict):
        self.publisher.publish(
            req,
            retry=True,
            exchange=self.prompt_queue_name,
            routing_key=self.prompt_queue_name,
            delivery_mode=2,
            properties={"content_type": "application/json"},
        )
        print(f"Sent {req['prompt']} to queue")

    def dequeue_image(self) -> Union[Tuple[kombu.Message, dict], Tuple[None, None]]:
        msg = self.image_queue.get()
        if msg is None:
            return None, None

        body = msg.payload
        return msg, body
