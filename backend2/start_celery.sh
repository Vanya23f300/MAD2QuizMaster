#!/bin/bash

# Script to start Celery worker for QuizMaster CSV export and scheduled tasks
# Usage: ./start_celery.sh [--with-beat]

# Parse command line arguments
WITH_BEAT=false
for arg in "$@"; do
  case $arg in
    --with-beat)
      WITH_BEAT=true
      shift
      ;;
    *)
      # Unknown option
      ;;
  esac
done

echo "🚀 Starting Celery worker for QuizMaster..."

# Change to the backend2 directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run 'python3 -m venv venv' first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if Redis is running
echo "🔍 Checking Redis connection..."
if ! redis-cli ping > /dev/null 2>&1; then
    echo "❌ Redis is not running. Please start Redis first:"
    echo "   brew services start redis  # On macOS"
    echo "   sudo systemctl start redis # On Linux"
    exit 1
fi

echo "✅ Redis is running"

# Check if Celery is installed
if ! command -v celery &> /dev/null; then
    echo "❌ Celery not found. Installing..."
    pip install celery
fi

# Kill any existing Celery workers
echo "🧹 Cleaning up existing Celery workers..."
pkill -f "celery.*worker" || true

# Kill any existing Celery Beat processes if we're starting with beat
if [ "$WITH_BEAT" = true ] && [ -f "celerybeat.pid" ]; then
    echo "🧹 Cleaning up existing Celery Beat scheduler..."
    kill -TERM $(cat celerybeat.pid) 2>/dev/null || true
    rm -f celerybeat.pid
fi

# Start Celery worker
echo "🔧 Starting Celery worker..."
echo "📋 Tasks: CSV export, daily reminders, monthly reports"
echo "🌐 Broker: redis://localhost:6379/0"
echo "📊 Concurrency: 1"
echo ""

# Set PYTHONPATH and start worker
export PYTHONPATH=.
nohup celery -A application.celery_tasks worker \
    --loglevel=info \
    --concurrency=1 \
    --logfile=celery_worker.log \
    --pidfile=celery_worker.pid \
    > celery_output.log 2>&1 &

CELERY_PID=$!
echo "✅ Celery worker started with PID: $CELERY_PID"

# Start Celery Beat if requested
if [ "$WITH_BEAT" = true ]; then
    echo "🔔 Starting Celery Beat scheduler..."
    nohup celery -A application.celery_tasks beat \
        --loglevel=info \
        --pidfile=celerybeat.pid \
        --logfile=celerybeat.log \
        > celerybeat_output.log 2>&1 &
        
    BEAT_PID=$!
    echo "✅ Celery Beat started with PID: $BEAT_PID"
fi

# Wait a moment for startup
sleep 3

# Check if worker process is still running
if ps -p $CELERY_PID > /dev/null; then
    echo "🎉 Celery worker is running successfully!"
else
    echo "❌ Celery worker failed to start. Check logs:"
    echo "   cat celery_output.log"
    echo "   cat celery_worker.log"
    exit 1
fi

# Check if Beat process is still running (if started)
if [ "$WITH_BEAT" = true ]; then
    if ps -p $BEAT_PID > /dev/null; then
        echo "🎉 Celery Beat scheduler is running successfully!"
    else
        echo "❌ Celery Beat failed to start. Check logs:"
        echo "   cat celerybeat_output.log"
        echo "   cat celerybeat.log"
        exit 1
    fi
fi

# Show recent logs
echo ""
echo "📋 Recent worker logs:"
echo "===================="
tail -10 celery_worker.log 2>/dev/null || echo "No logs yet..."

if [ "$WITH_BEAT" = true ]; then
    echo ""
    echo "📋 Recent beat logs:"
    echo "===================="
    tail -10 celerybeat.log 2>/dev/null || echo "No beat logs yet..."
fi

echo ""
echo "🔍 To check status:"
echo "   ps aux | grep 'celery'"
echo "   celery -A application.celery_tasks inspect active"
echo ""
echo "📝 Log files:"
echo "   - Worker: celery_worker.log, celery_output.log"
if [ "$WITH_BEAT" = true ]; then
    echo "   - Beat: celerybeat.log, celerybeat_output.log"
fi
echo ""
echo "🛑 To stop:"
echo "   - Worker: ./stop_celery.sh"
if [ "$WITH_BEAT" = true ]; then
    echo "   - Beat: ./stop_celery_beat.sh"
fi 