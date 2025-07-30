#!/bin/bash

# Kill any existing celery beat processes
echo "Stopping Celery Beat scheduler..."
pkill -f "celery.*beat" || echo "No Celery Beat processes found"

# Remove PID file if it exists
if [ -f "celerybeat.pid" ]; then
    rm -f celerybeat.pid
    echo "Removed PID file: celerybeat.pid"
fi

echo "Celery Beat scheduler stopped successfully" 