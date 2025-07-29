import os
from celery import Celery
from celery.schedules import crontab

# Create Celery app
celery = Celery('tasks')

# Import task modules
celery.conf.imports = [
    'application.celery_tasks',
]

# Configure Celery to use Redis as broker
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', '6379')
redis_url = f"redis://{redis_host}:{redis_port}/0"

celery.conf.broker_url = redis_url
celery.conf.result_backend = redis_url

# Set timezone for scheduled tasks
celery.conf.timezone = 'UTC'

# Configure scheduled tasks
celery.conf.beat_schedule = {
    # Daily reminders at 6 PM every day
    'daily-reminders': {
        'task': 'application.celery_tasks.send_daily_reminders',
        'schedule': crontab(hour=18, minute=0),  # 6 PM daily
    },
    
    # Monthly reports on 1st of every month at 9 AM
    'monthly-reports': {
        'task': 'application.celery_tasks.send_monthly_reports',
        'schedule': crontab(day_of_month=1, hour=9, minute=0),  # 1st of month, 9 AM
    }
}

# Optional: Task routing configuration
celery.conf.task_routes = {
    'application.celery_tasks.generate_user_quiz_export': {'queue': 'exports'},
    'application.celery_tasks.send_daily_reminders': {'queue': 'notifications'},
    'application.celery_tasks.send_monthly_reports': {'queue': 'reports'},
}

# Optional: Task serialization format
celery.conf.accept_content = ['json']
celery.conf.task_serializer = 'json'
celery.conf.result_serializer = 'json'