from celery import Celery
from celery.schedules import crontab
from application.config import LocalDevelopmentConfig
import os

def make_celery(app_name=__name__):
    """Create and configure Celery instance"""
    
    # Redis broker URL (fallback to in-memory for development if Redis not available)
    broker_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    result_backend = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    celery = Celery(
        app_name,
        broker=broker_url,
        backend=result_backend,
        include=['application.celery_tasks']
    )
    
    # Celery configuration
    celery.conf.update(
        # Task settings
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        
        # Worker settings
        worker_prefetch_multiplier=1,
        task_acks_late=True,
        worker_max_tasks_per_child=50,
        
        # Scheduled tasks (Celery Beat)
        beat_schedule={
            # Daily reminder task - runs every day at 6 PM
            'send-daily-reminders': {
                'task': 'application.celery_tasks.send_daily_reminders',
                'schedule': crontab(hour=18, minute=0),  # 6:00 PM daily
            },
            # Monthly activity report - runs on 1st of every month at 9 AM
            'send-monthly-reports': {
                'task': 'application.celery_tasks.send_monthly_activity_reports',
                'schedule': crontab(hour=9, minute=0, day_of_month=1),  # 1st day of month at 9 AM
            },
            # Cleanup old exports - runs weekly on Sunday at 2 AM
            'cleanup-old-exports': {
                'task': 'application.celery_tasks.cleanup_old_export_files',
                'schedule': crontab(hour=2, minute=0, day_of_week=0),  # Sunday at 2 AM
            },
        },
    )
    
    return celery

# Create global celery instance
celery = make_celery()