# QuizMaster Backend

This is the backend component for the QuizMaster application, built with Flask and SQLAlchemy.

## Prerequisites

- Python 3.8 or higher
- Redis server (for Celery task queue)

## Installation

1. Set up virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```
pip install -r requirements.txt
```

## Configuration

The application uses environment variables for configuration. Create a `.env` file in the project root with the following variables:

```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///instance/database.sqlite3

# Email configuration (for reminders and reports)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=QuizMaster <your-email@gmail.com>
```

## Running the Application

1. Start the Flask application:
```
python main.py
```

2. Start Celery worker for CSV export tasks:

**Easy way (recommended):**
```
# Start just the worker for CSV exports
./start_celery.sh

# Start worker and scheduler for CSV exports, reminders, and reports
./start_celery.sh --with-beat
```

**Manual way:**
```
# Start worker
source venv/bin/activate
celery -A application.celery_tasks worker --loglevel=info --concurrency=1

# Start scheduler (separate terminal)
celery -A application.celery_tasks beat --loglevel=info
```

**Stop Celery processes:**
```
# Stop worker
./stop_celery.sh

# Stop scheduler
./stop_celery_beat.sh
```

## CSV Export Feature

The application includes an asynchronous CSV export feature that allows users to export their quiz attempt data. The export functionality uses Celery for background processing to handle large datasets without blocking the UI.

### How it works:
1. Users request a CSV export via the API
2. A background Celery task is queued to generate the CSV file
3. Users can check the export status via API
4. Once complete, users can download the CSV file

### API Endpoints:
- `POST /api/exports/user-quizzes` - Request a new export
- `GET /api/exports/status/<task_id>` - Check export status
- `GET /api/exports/download/<filename>` - Download completed export

## Scheduled Tasks

The application includes scheduled tasks managed by Celery Beat:

### Daily Reminders
- Sends email reminders to users who haven't logged in recently
- Includes a list of available quizzes
- Runs automatically at 6:00 PM daily

### Monthly Reports
- Sends monthly activity reports to all users
- Includes quiz statistics for the previous month
- Runs automatically on the 1st of each month at 9:00 AM

### Manual Testing
To manually trigger the scheduled tasks for testing:

```
# Test daily reminders
celery -A application.celery_tasks call application.celery_tasks.send_daily_reminders

# Test monthly reports
celery -A application.celery_tasks call application.celery_tasks.send_monthly_reports
```

## API Documentation

API documentation is available at `/api/docs` when the application is running.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

