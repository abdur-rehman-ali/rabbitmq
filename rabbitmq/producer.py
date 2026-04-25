import pika
import json
import logging
from rabbitmq.rabbitmq_connection import get_connection

logger = logging.getLogger(__name__)


def publish_message(queue: str, message: dict):
    """
    Publish a JSON message to the given queue.
    Always declare the queue before publishing —
    this is idempotent and ensures it exists.
    """
    connection = get_connection()

    channel = connection.channel()

    # Declare queue — durable=True so it survives broker restart
    channel.queue_declare(queue=queue, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent,  # survive broker restart
            content_type="application/json",
        ),
    )
    logger.info(f"Published to '{queue}': {json.dumps(message)}")

    connection.close()
