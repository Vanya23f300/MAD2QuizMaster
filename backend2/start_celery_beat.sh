#!/bin/bash

# Directory containing this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Set Python path to include the current directory
export PYTHONPATH=$DIR:$PYTHONPATH

# Function to check if Redis is running
check_redis() {
  if command -v redis-cli >/dev/null 2>&1; then
    if redis-cli ping >/dev/null 2>&1; then
      echo "✅ Redis is running"
      return 0
    else
      echo "❌ Redis is not running. Start Redis first."
      return 1
    fi
  else
    echo "⚠️ redis-cli not found, cannot check Redis status."
    echo "Assuming Redis is running, but this may cause issues if it's not."
    return 0
  fi
}

# Function to check if venv exists and activate it
activate_venv() {
  if [ -d "$DIR/venv" ]; then
    echo "✅ Found virtual environment"
    source "$DIR/venv/bin/activate"
    echo "✅ Activated virtual environment"
  else
    echo "❌ No virtual environment found at $DIR/venv"
    echo "You should create one with: python -m venv venv"
    echo "Then install dependencies: venv/bin/pip install -r requirements.txt"
    exit 1
  fi
}

# Kill existing Celery Beat scheduler if running
kill_existing() {
  if [ -f "$DIR/celerybeat.pid" ]; then
    echo "Found existing Celery Beat PID file"
    OLD_PID=$(cat "$DIR/celerybeat.pid")
    if ps -p "$OLD_PID" >/dev/null 2>&1; then
      echo "Stopping existing Celery Beat process (PID: $OLD_PID)"
      kill -TERM "$OLD_PID"
      sleep 2
      if ps -p "$OLD_PID" >/dev/null 2>&1; then
        echo "Force killing Celery Beat process"
        kill -9 "$OLD_PID" 2>/dev/null
      fi
    fi
    rm -f "$DIR/celerybeat.pid"
  fi
}

# Make sure Redis is running
check_redis || exit 1

# Make sure venv is activated
activate_venv

# Kill existing Celery Beat scheduler
kill_existing

# Start Celery Beat scheduler
echo "Starting Celery Beat scheduler..."

celery -A application.celery_tasks beat \
  --loglevel=info \
  --pidfile="$DIR/celerybeat.pid" \
  --logfile="$DIR/celerybeat.log" \
  --detach

if [ $? -eq 0 ]; then
  echo "✅ Celery Beat started successfully!"
  echo "Log file: $DIR/celerybeat.log"
  echo "PID file: $DIR/celerybeat.pid"
else
  echo "❌ Failed to start Celery Beat"
  exit 1
fi 