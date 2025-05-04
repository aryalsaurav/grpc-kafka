import os

from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Create a Celery instance
app = Celery('core')

# Configure Celery
app.config_from_object(settings, namespace='CELERY')


# ##update settings
app.conf.update(
    task_serializer='json',
    result_backend='redis://localhost:6379/0',
    timezone='Asia/Kathmandu',
    enable_utc=True,
    accept_content=['json'],  # Ignore other content
    result_serializer='json',

)


## configure celery beat
app.conf.beat_schedule = {
    # 'add-every-30-seconds': {
    #     'task': 'core.tasks.add',
    #     'schedule': 30.0,
    #     'args': (16, 16)
    # },
}

# Load task modules from all registered Django app configs
app.autodiscover_tasks()


# Define tasks
@app.task
def your_task_name():
    # Task logic goes here
    pass

# You can define more tasks here

if __name__ == '__main__':
    app.start()
