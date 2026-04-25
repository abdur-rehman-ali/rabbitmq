import pika
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def get_connection():
    """
    Establish a connection to RabbitMQ.
    Return a BlockingConnection using settings.RABBITMQ_URL.
    Use this everywhere — never build ConnectionParameters inline.
    """

    params = pika.URLParameters(settings.RABBITMQ_URL)

    # Heartbeat keeps the connection alive through idle periods.
    # 600s is a safe default; set to 0 ONLY for quick local scripts.
    params.heartbeat = 600

    params.blocked_connection_timeout = 300

    try:
        connection = pika.BlockingConnection(params)
        logger.info("Successfully connected to RabbitMQ")
        return connection
    except Exception as e:
        logger.error(f"Error connecting to RabbitMQ: {e}")
        raise


def get_channel():
    """
    Get a channel from the RabbitMQ connection.
    This is where you can declare your queues and exchanges.
    """

    connection = get_connection()
    channel = connection.channel()

    return channel

    # Declare the queue to ensure it exists before we publish/consume
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE, durable=True)

    logger.info(f"Channel created and queue '{settings.RABBITMQ_QUEUE}' declared")
    return channel
