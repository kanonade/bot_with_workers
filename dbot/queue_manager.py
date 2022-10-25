import os
from typing import Optional, Tuple, Union

import kombu

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")


class QueueManager:
    def __init__(self, user: Optional[str] = None, password: Optional[str] = None):
        amqp_host = f"amqp://{RABBITMQ_HOST}:5672"
        self.connection = kombu.Connection(amqp_host, userid=user, password=password)
        self.channel = self.connection.channel()

        self.prompt_queue_name = "prompts"
        self.prompt_queue = self.ensure_queue(self.prompt_queue_name)

        self.image_queue_name = "images"
        self.image_queue = self.ensure_queue(self.image_queue_name)

        self.prompt_queue.declare()
        self.publisher = kombu.Producer(self.channel, self.prompt_queue)

    def ensure_queue(self, name: str) -> kombu.Queue:
        """Ensure a queue exists and return it.

        Args:
            name (str): The name of the queue

        Returns:
            kombu.Queue: The queue
        """
        queue = kombu.Queue(
            name,
            durable=True,
            exchange=name,
            routing_key=name,
            consumer_arguments={"prefetch_count": 1},
            channel=self.channel,
        )
        queue.declare()
        return queue

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