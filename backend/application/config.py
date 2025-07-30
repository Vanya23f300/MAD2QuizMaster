import os
from datetime import timedelta

# Determine the base directory for the project
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATABASE_DIR = os.path.join(BASE_DIR, 'instance')

# Ensure the instance directory exists
os.makedirs(DATABASE_DIR, exist_ok=True)

class Config():
    DEBUG = False
    SQLITE_DB_DIR = DATABASE_DIR
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Redis Configuration
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))

class LocalDevelopmentConfig(Config):
    # Full path to the SQLite database file
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(DATABASE_DIR, "database.sqlite3")}'
    DEBUG = True
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Token expires in 24 hours
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)   # Refresh token expires in 30 days
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', '1', 'on']
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', '1', 'on']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@quizmaster.com')
    
    # Additional database configurations
    SQLALCHEMY_ECHO = False  # Set to True for SQL query logging
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # DEMO MODE CONFIGURATION FOR MONTHLY REPORTS
    # Set DEMO_MODE = True when demonstrating to professors
    # Then set the DEMO_DATE and DEMO_TIME to your desired values
    DEMO_MODE = True  # Change to True for demonstration
    
    # Set this to the date you want to simulate (format: 'YYYY-MM-DD')
    # Example: '2024-07-01' will make the system think it's July 1st, 2024
    DEMO_DATE = '2025-08-01'  # Change this to your demo date
    
    # Set this to the time you want the report to trigger (format: 'HH:MM')
    # Example: '14:30' will trigger the report at 2:30 PM
    # Make sure to set this to 1-2 minutes after your current time for demo
    DEMO_TIME = '11:41'  # Change this to your demo time