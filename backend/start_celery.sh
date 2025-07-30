#!/bin/bash

# Kill any existing celery processes
pkill -f "celery worker"

# Activate virtual environment
source venv/bin/activate

# Ensure Python can find our modules
export PYTHONPATH=$(pwd)

# Start Celery worker using Python module approach
python3 -m celery -A celery_worker.celery worker --loglevel=info --pidfile=celery_worker.pid --logfile=celery_worker.log &

echo "Celery worker started with PID file: celery_worker.pid" 