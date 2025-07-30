from flask import Flask, jsonify, request
from application.config import LocalDevelopmentConfig
from application.database import db
from application.cache import init_redis
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from application.simple_email import init_mail
from dotenv import load_dotenv
import os
from datetime import datetime, date, timedelta
import logging
from celery import Celery
from celery.schedules import crontab
from flask_mail import Mail

# Load environment variables from .env file first
load_dotenv(override=True)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
app = None
mail = None

# Celery Configuration
celery = Celery(
    __name__,
    backend=os.environ.get('RESULT_BACKEND', 'redis://localhost:6379/0'),
    broker=os.environ.get('BROKER_URL', 'redis://localhost:6379/0'),
    include=['application.celery_tasks'],
    imports = ('application.celery_tasks'),
)

def create_app():
    global app, mail
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    
    # Ensure email configuration is properly loaded from environment
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', '1', 'on']
    app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', '1', 'on']
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@quizmaster.com')
    
    # Celery configuration in Flask config - using new-style keys
    app.config['broker_url'] = os.environ.get('BROKER_URL', 'redis://localhost:6379/0')
    app.config['result_backend'] = os.environ.get('RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # Log email configuration for debugging
    logger.info("Flask app email configuration:")
    logger.info(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
    logger.info(f"MAIL_PORT: {app.config['MAIL_PORT']}")
    logger.info(f"MAIL_USE_TLS: {app.config['MAIL_USE_TLS']}")
    logger.info(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
    logger.info(f"MAIL_DEFAULT_SENDER: {app.config['MAIL_DEFAULT_SENDER']}")
    
    # Initialize extensions
    CORS(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    
    # Database initialization
    db.init_app(app)
    
    # Initialize Redis (will gracefully handle if Redis is not running)
    init_redis(app)
    
    # Initialize Flask-Mail (make it globally accessible)
    mail = Mail(app)
    
    celery.conf.beat_schedule = {
        'daily-quiz-reminders': {
            'task': 'application.celery_tasks.send_daily_reminders',
            # 'schedule': 10,  # Every 10 seconds for testing
            'schedule': crontab(hour=9, minute=0),  # 9 AM daily (original)
        },
        'monthly-quiz-reports': {
            'task': 'application.celery_tasks.send_monthly_reports',
            # 'schedule': 180,  # Every 3 minutes for testing
            'schedule': crontab(day_of_month=1, hour=0, minute=0),  # 1st of month at midnight (original)
        }
    }
    
    # Create application context
    with app.app_context():
        # Import models here to ensure they're registered with db
        from application.models import Users, Subjects, Chapters, Quizzes, Questions, Scores
        
        # Create all database tables
        db.create_all()
        
        # Create default admin user if it doesn't exist
        admin_user = Users.query.filter_by(email='admin@email.com').first()
        if not admin_user:
            admin_user = Users.create_admin(
                email='admin@email.com',
                username='admin',
                password='admin'
            )
            logger.info("Default admin user created: admin@email.com / admin")
    
    # Push app context as per documentation pattern
    app.app_context().push()
    
    return app

# Create the app
app = create_app()

# Register routes after app creation
from application.apis.users import register_user_routes
from application.apis.subjects import register_subject_routes  
from application.apis.chapters import register_chapter_routes
from application.apis.questions import create_question_routes
from application.apis.quizzes import create_quiz_routes
from application.apis.analytics import create_analytics_routes
from application.apis.search import create_search_routes
from application.apis.exports import register_export_routes

register_user_routes(app)
register_subject_routes(app)
register_chapter_routes(app)
create_question_routes(app)
create_quiz_routes(app)
create_analytics_routes(app)
create_search_routes(app)
register_export_routes(app)

@app.route('/api/test', methods=['GET'])
def test_route():
    return jsonify({
        'message': 'QuizMaster Backend is running!',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    # CRITICAL FIX: Update celery configuration with app config HERE
    # This matches the pattern used by the working implementation
    celery.conf.update(app.config)
    logger.info(f"Celery configured with database: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    logger.info(f"Celery broker: {app.config['broker_url']}")
    logger.info(f"Celery backend: {app.config['result_backend']}")
    
    app.run(debug=True, host='0.0.0.0', port=8000)
