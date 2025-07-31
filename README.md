# Quiz Master V2

A multi-user exam preparation platform with admin and user roles, built with Flask, VueJS, SQLite, Redis, Celery, and Bootstrap.

## Features
- Admin and User dashboards
- Quiz, Subject, Chapter, Question management
- User registration and login
- Quiz attempt with timer
- Score tracking and summary
- Scheduled reminders and reports (Celery)
- Async CSV export
- API caching and optimization

## Tech Stack
- Flask (API)
- VueJS (Frontend)
- SQLite (Database)
- Redis (Caching, Celery broker)
- Celery (Background jobs)
- Bootstrap (Styling)

## Prerequisites

- Python 3.8 or higher
- Node.js and npm
- Redis server (for Celery task queue and caching)

## Setup and Installation

### 1. Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment configuration:
Create a `.env` file in the project root with the following variables:
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

### 2. Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

### 3. Redis Setup

Make sure Redis server is running on your system:

**On macOS (using Homebrew):**
```bash
brew install redis
brew services start redis
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

**On Windows:**
Download and install Redis from the official website or use WSL.

## Running the Application

### Step 1: Start Redis Server
Ensure Redis is running (if not started as a service):
```bash
redis-server
```

### Step 2: Start the Backend (Flask API)
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python main.py
```
The backend API will be available at: `http://localhost:8000`

### Step 3: Start Celery Worker
In a new terminal window/tab:
```bash
cd backend
./start_celery.sh
```

**Optional: Start Celery Beat (for scheduled tasks like reminders and reports):**
```bash
cd backend
./start_celery_beat.sh
```

### Step 4: Start the Frontend (Vue.js)
In another new terminal window/tab:
```bash
cd frontend
npm run serve
```
The frontend will be available at: `http://localhost:8080`

## Stopping the Application

### Stop Celery Processes:
```bash
cd backend
./stop_celery.sh      # Stop worker
./stop_celery_beat.sh # Stop scheduler
```

### Stop Backend:
Press `Ctrl+C` in the terminal running the Flask application.

### Stop Frontend:
Press `Ctrl+C` in the terminal running the Vue.js development server.

## API Documentation
API documentation is available at `http://localhost:8000/api/docs` when the backend is running.

## Additional Information
- Backend README: `backend/README.md` - Detailed backend setup and API information
- Frontend README: `frontend/README.md` - Frontend development commands and configuration