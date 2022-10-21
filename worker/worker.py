import logging
import os
import random
import time

import kombu
import kombu.mixins

log = logging.getLogger(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")


class Worker(kombu.mixins.ConsumerProducerMixin):
    def __init__(self, connection):
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

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                queues=self.prompt_queue,
                accept=["json"],
                callbacks=[self.process_task],
                prefetch_count=1,
            )
        ]

    def process_task(self, body, message):
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
            exchange="",
            routing_key="images",
            retry=True,
            serializer="json",
        )

        print(f"Sent response for {body['prompt']}")
        message.ack()


if __name__ == "__main__":
    worker = Worker(None)
    worker.run()
