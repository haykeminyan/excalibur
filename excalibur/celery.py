import os
from celery import Celery


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'excalibur.settings')

RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'default_user')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'default_password')

# Check if the environment variables are None (or not found)
if RABBITMQ_USER is None or RABBITMQ_PASSWORD is None:
    raise ValueError("RABBITMQ_USER and RABBITMQ_PASSWORD must be set")

# Create Celery application
app = Celery('excalibur', broker=f'pyamqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@rabbitmq//')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
