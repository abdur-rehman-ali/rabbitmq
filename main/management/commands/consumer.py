import json
import time
from django.core.management.base import BaseCommand
from rabbitmq.rabbitmq_connection import get_connection


class Command(BaseCommand):
    help = "Starts a RabbitMQ consumer that listens to the specified queue."

    def add_arguments(self, parser):
        parser.add_argument(
            "queue_name", type=str, help="Name of the RabbitMQ queue to consume from"
        )

    def handle(self, *args, **options):
        queue_name = options["queue_name"]
        connection = get_connection()
        channel = connection.channel()

        # Declare the queue to ensure it exists before we consume
        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=self.callback,
            auto_ack=False,  # ALWAYS False — ack manually after processing
        )

        self.stdout.write(
            self.style.SUCCESS(f"Waiting for messages in '{queue_name}'...")
        )

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            self.stdout.write("Consumer stopped.")
        finally:
            connection.close()

    def callback(self, ch, method, properties, body):
        """
        Called once per message. Ack ONLY after successful processing.
        """

        try:
            message = json.loads(body)
            self.stdout.write(self.style.SUCCESS(f"Received message: {message}"))

            # Simulate processing time
            self.process_message(message)

            ch.basic_ack(delivery_tag=method.delivery_tag)
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Failed to decode JSON message"))
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def process_message(self, message):
        """
        Placeholder for actual message processing logic.
        Replace this with your real processing code.
        """
        time.sleep(5)
        self.stdout.write(f"Processing message: {message}")
