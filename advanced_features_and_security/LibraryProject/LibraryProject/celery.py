import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
# Replace 'LibraryProject.settings' with your actual settings path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

# Create Celery application instance
app = Celery('LibraryProject')

# Load task configurations from Django settings file
# The configuration keys must start with CELERY_ (e.g., CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover task modules from all installed Django apps
app.autodiscover_tasks()