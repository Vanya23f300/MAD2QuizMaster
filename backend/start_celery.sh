#!/bin/bash

# Kill any existing celery processes
pkill -f "celery worker"

# Ensure Python can find our modules
export PYTHONPATH=$(pwd)

# Start Celery worker using the new entry point
celery -A celery_worker.celery worker --loglevel=info --pidfile=celery_worker.pid --logfile=celery_worker.log &

echo "Celery worker started with PID file: celery_worker.pid" 