#!/bin/bash

# Kill any existing celery beat processes
pkill -f "celery beat"

# Activate virtual environment
source venv/bin/activate

# Ensure Python can find our modules
export PYTHONPATH=$(pwd)

# Start Celery Beat scheduler using Python module approach
python3 -m celery -A celery_worker.celery beat --loglevel=info --pidfile=celerybeat.pid --logfile=celerybeat.log &

echo "Celery Beat scheduler started with PID file: celerybeat.pid" 