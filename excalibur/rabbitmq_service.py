import logging
import os

import pika

from apps.facture.models import LocalFacture, WorldFacture

logger = logging.getLogger(__name__)

# RabbitMQ configuration
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'password')

# Get the individual queue names from the environment variables
queue_local_facture = os.getenv('RABBITMQ_QUEUE_LOCAL_FACTURE', 'local_facture')
queue_world_facture = os.getenv('RABBITMQ_QUEUE_WORLD_FACTURE', 'world_facture')
queue_deductions = os.getenv('RABBITMQ_QUEUE_DEDUCTIONS', 'deductions')

# Log RabbitMQ configuration for debugging
logger.info(
    f"RabbitMQ Config: Host={RABBITMQ_HOST}, Queues: {queue_local_facture}, {queue_world_facture}, {queue_deductions}, User={RABBITMQ_USER}",
)


def send_rabbitmq_message(model, message):
    if model == LocalFacture:
        queue_to_use = queue_local_facture
    elif model == WorldFacture:
        queue_to_use = queue_world_facture
    else:
        queue_to_use = queue_deductions

    return create_queue_rabbitmq(queue_to_use, message)


def create_queue_rabbitmq(queue_name, message):
    """
    Sends a message to the specified RabbitMQ queue.
    """
    try:
        # Create credentials using the provided user and password
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)

        # Establish a connection to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                credentials=credentials,
            ),
        )
        channel = connection.channel()

        # Declare the queue (ensure it exists)
        channel.queue_declare(queue=queue_name, durable=True)

        # Publish the message to the queue
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make the message persistent
            ),
        )
        logger.info(f"Message sent to RabbitMQ queue '{queue_name}': {message}")
        connection.close()
    except Exception as e:
        logger.error(f"Failed to send message to RabbitMQ queue '{queue_name}': {e}")


# Example usage: send messages to each queue
send_rabbitmq_message(queue_local_facture, 'Test message for local_facture')
send_rabbitmq_message(queue_world_facture, 'Test message for world_facture')
send_rabbitmq_message(queue_deductions, 'Test message for deductions')
