#!/bin/bash

# Directory containing this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Function to stop Celery Beat
stop_celery_beat() {
  if [ -f "$DIR/celerybeat.pid" ]; then
    PID=$(cat "$DIR/celerybeat.pid")
    if ps -p "$PID" > /dev/null; then
      echo "Stopping Celery Beat (PID: $PID)..."
      kill -TERM "$PID"
      sleep 2
      
      if ps -p "$PID" > /dev/null; then
        echo "Celery Beat process did not terminate gracefully. Force killing..."
        kill -9 "$PID" 2>/dev/null
      fi
      
      echo "✅ Celery Beat stopped"
    else
      echo "⚠️ PID file exists but process is not running"
    fi
    
    # Clean up PID file
    rm -f "$DIR/celerybeat.pid"
    echo "✅ Removed PID file"
  else
    echo "❌ No Celery Beat PID file found"
    echo "Either Celery Beat is not running or the PID file was deleted"
    
    # Try to find and kill any celery beat processes anyway
    BEAT_PIDS=$(ps aux | grep "celery -A application.celery_tasks beat" | grep -v grep | awk '{print $2}')
    
    if [ -n "$BEAT_PIDS" ]; then
      echo "Found Celery Beat processes without PID file: $BEAT_PIDS"
      echo "Attempting to stop them..."
      
      for pid in $BEAT_PIDS; do
        kill -TERM "$pid" 2>/dev/null
        echo "Sent TERM signal to process $pid"
      done
      
      sleep 2
      
      # Check if any processes are still running and force kill
      REMAINING_PIDS=$(ps aux | grep "celery -A application.celery_tasks beat" | grep -v grep | awk '{print $2}')
      if [ -n "$REMAINING_PIDS" ]; then
        for pid in $REMAINING_PIDS; do
          kill -9 "$pid" 2>/dev/null
          echo "Force killed process $pid"
        done
      fi
    fi
  fi
}

# Call the function to stop Celery Beat
stop_celery_beat

# Ask if user wants to remove log files
read -p "Do you want to remove the log files? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  rm -f "$DIR/celerybeat.log"
  rm -f "$DIR/celerybeat-schedule"
  echo "✅ Removed log files"
fi

echo "Celery Beat shutdown process completed." 