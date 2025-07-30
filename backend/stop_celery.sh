#!/bin/bash

# Kill any existing celery worker processes
echo "Stopping Celery worker..."
pkill -f "celery.*worker" || echo "No Celery worker processes found"

# Remove PID file if it exists
if [ -f "celery_worker.pid" ]; then
    rm -f celery_worker.pid
    echo "Removed PID file: celery_worker.pid"
fi

echo "Celery worker stopped successfully" 