# celery_app.py
from celery import Celery

celery = Celery(
    'predictions',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery.conf.update(
    task_routes={
        'tasks.process_data': {'queue': 'default'},
    }
)

celery.autodiscover_tasks(['tasks'])
