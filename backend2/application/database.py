from flask_sqlalchemy import SQLAlchemy

# Create a single SQLAlchemy instance to be used across the app
db = SQLAlchemy()

# No need for separate Base or engine - they're already managed by Flask-SQLAlchemy