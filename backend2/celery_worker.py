from main import create_app, celery

# Create Flask app and push context
app = create_app()
app.app_context().push()

# CRITICAL FIX: Explicitly update celery config with app config in worker
celery.conf.update(app.config)

# This file is used to start the Celery worker
# Run with: celery -A celery_worker.celery worker --loglevel=info 