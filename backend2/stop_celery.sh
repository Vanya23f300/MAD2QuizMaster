#!/bin/bash

# Script to stop Celery worker for QuizMaster
# Usage: ./stop_celery.sh

echo "🛑 Stopping Celery worker..."

# Change to the backend2 directory
cd "$(dirname "$0")"

# Check if PID file exists
if [ -f "celery_worker.pid" ]; then
    CELERY_PID=$(cat celery_worker.pid)
    echo "📋 Found PID file: $CELERY_PID"
    
    # Check if process is running
    if ps -p $CELERY_PID > /dev/null 2>&1; then
        echo "🔍 Process $CELERY_PID is running, stopping..."
        kill $CELERY_PID
        sleep 2
        
        # Force kill if still running
        if ps -p $CELERY_PID > /dev/null 2>&1; then
            echo "⚡ Force killing process..."
            kill -9 $CELERY_PID
        fi
        
        rm -f celery_worker.pid
        echo "✅ Celery worker stopped"
    else
        echo "⚠️  Process $CELERY_PID not found, cleaning up PID file"
        rm -f celery_worker.pid
    fi
else
    echo "📋 No PID file found, stopping all Celery workers..."
fi

# Kill any remaining Celery workers
REMAINING=$(pkill -f "celery.*worker" 2>/dev/null; echo $?)
if [ $REMAINING -eq 0 ]; then
    echo "🧹 Stopped remaining Celery workers"
else
    echo "ℹ️  No Celery workers were running"
fi

# Clean up log files (optional)
read -p "🗑️  Clean up log files? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f celery_worker.log celery_output.log
    echo "✅ Log files cleaned up"
fi

echo "🎉 All done!" 