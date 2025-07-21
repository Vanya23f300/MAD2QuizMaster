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
    
    # Additional database configurations
    SQLALCHEMY_ECHO = False  # Set to True for SQL query logging
    SQLALCHEMY_TRACK_MODIFICATIONS = False