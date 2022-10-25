import logging
import os
import random
import time

import kombu
import kombu.mixins

log = logging.getLogger(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")


class Worker(kombu.mixins.ConsumerProducerMixin):
    def __init__(self, connection: kombu.Connection):
        amqp_host = f"amqp://{RABBITMQ_HOST}:5672"
        self.connection = kombu.Connection(amqp_host)

        self.channel = self.connection.channel()
        self.prompt_queue_name = "prompts"
        self.prompt_queue = self.ensure_queue(self.prompt_queue_name)

        self.image_queue_name = "images"
        self.image_queue = self.ensure_queue(self.image_queue_name)

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

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                queues=self.prompt_queue,
                accept=["json"],
                callbacks=[self.on_message],
                prefetch_count=1,
            )
        ]

    def on_message(self, body: dict, message: kombu.Message):
        """Take a message from the queue and pretend to process it. Then queue the result into the image queue.

        Args:
            body (dict): The message body decoded from json
            message (kombu.Message): The message object itself
        """
        print(f"Received {body['prompt']}")

        print("Waiting random time to simulate work")
        time.sleep(random.randint(1, 3))

        response = {
            "user": body["user"],
            "channel": body["channel"],
            "image": "Pretend I'm an image of " + body["prompt"],
        }

        self.producer.publish(
            response,
            exchange=self.image_queue_name,
            routing_key=self.image_queue_name,
            retry=True,
            serializer="json",
        )

        print(f"Sent response for {body['prompt']}")
        message.ack()


if __name__ == "__main__":
    worker = Worker(None)
    worker.run()
