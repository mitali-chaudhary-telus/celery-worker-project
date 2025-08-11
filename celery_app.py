from celery import Celery
import os

# Set up Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'c:\Users\mitachau\OneDrive - Capgemini\Desktop\worker-project\keys\service-account-key.json'

# Create Celery app
app = Celery('celery_pubsub')

# Configure Celery using Google Pub/Sub
app.conf.update(
    broker_url='gcpubsub://projects/cto-tinaa-pltf-svc-lab-159cfb',
    broker_transport_options={
        'project': 'cto-tinaa-pltf-svc-lab-159cfb',
        'topic_name': 'tnso-celery-tasks',
        'subscription_name': 'tnso-celery-worker-sub',
        'create_topic': False,  # Topic already exists
        'create_subscription': False,  # Subscription already exists
        'ack_deadline': 600,  # Message acknowledgment deadline in seconds
        'visibility_timeout': 600,  # Message visibility timeout
        'use_default_routing': True,  # Use default routing
    },
    # Worker optimization settings
    worker_prefetch_multiplier=1,  # Fetch one message at a time
    worker_concurrency=4,  # Number of worker processes
    task_acks_late=True,  # Tasks are acknowledged after execution
    task_reject_on_worker_lost=True,  # Reject tasks if worker is terminated
    worker_max_tasks_per_child=100,  # Restart worker after processing 100 tasks
    worker_disable_rate_limits=True,  # Disable rate limiting
    worker_send_task_events=False,  # Disable task events
)

# Import tasks module to register tasks
import tasks