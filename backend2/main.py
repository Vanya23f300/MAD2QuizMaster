from flask import Flask, jsonify, request
from application.config import LocalDevelopmentConfig
from application.database import db
from application.cache import init_redis
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from dotenv import load_dotenv
import os
from datetime import datetime, date, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Global app variable
app = None

def create_app():
    global app
    app = Flask(__name__)
    
    print("starting local development")
    
    # Load configuration
    app.config.from_object(LocalDevelopmentConfig)
    app.config["UPLOAD_FOLDER"] = "static/images"
    
    # Enhanced CORS Configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:8080",
                "http://127.0.0.1:8080",
                "http://localhost:3000",
                "http://127.0.0.1:3000"
            ],
            "allow_headers": [
                "Content-Type",
                "Authorization",
                "Access-Control-Allow-Headers",
                "Access-Control-Allow-Origin",
                "Access-Control-Allow-Methods"
            ],
            "expose_headers": [
                "Content-Type",
                "Authorization"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "supports_credentials": True,
            "max_age": 86400  # Cache preflight requests for 24 hours
        }
    })

    # Handle OPTIONS requests globally
    @app.route('/api/<path:path>', methods=['OPTIONS'])
    def handle_options(path):
        return '', 200

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # JWT Error Handlers for better debugging
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        logger.warning("JWT token has expired")
        return jsonify({
            'message': 'Token has expired',
            'error': 'TOKEN_EXPIRED'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        logger.warning(f"Invalid JWT token: {error}")
        return jsonify({
            'message': 'Invalid token',
            'error': 'INVALID_TOKEN'
        }), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        logger.warning(f"Missing JWT token: {error}")
        return jsonify({
            'message': 'Authorization token is required',
            'error': 'TOKEN_MISSING'
        }), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        logger.warning("Fresh token required")
        return jsonify({
            'message': 'Fresh token required',
            'error': 'FRESH_TOKEN_REQUIRED'
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        logger.warning("Token has been revoked")
        return jsonify({
            'message': 'Token has been revoked',
            'error': 'TOKEN_REVOKED'
        }), 401

    # Initialize Redis (will gracefully handle if Redis is not running)
    init_redis(app)
    
    # Create application context
    with app.app_context():
        # Ensure database is created
        db.create_all()
        
        # Check if admin user exists, if not create one
        from application.models import Users
        existing_admin = Users.query.filter_by(email="admin@email.com").first()
        
        if not existing_admin:
            b = Bcrypt()
            password = b.generate_password_hash("admin123").decode('utf-8')
            
            admin_user = Users(
                email="admin@email.com",
                username="admin",
                password=password,
                dob=date(1990, 1, 1),
                qualification="System Administrator",
                is_admin=True,
                last_login=datetime.utcnow(),
                is_active=True,
                registration_date=datetime.utcnow()
            )
            
            db.session.add(admin_user)
            db.session.commit()
            logger.info("Admin user created successfully")
        else:
            logger.info("Admin user already exists")
    
    return app

# Create the app
app = create_app()

# Import and register routes manually
from application.apis.users import register_user_routes
from application.apis.subjects import register_subject_routes
from application.apis.chapters import register_chapter_routes
from application.apis.quizzes import create_quiz_routes
from application.apis.questions import create_question_routes
from application.apis.exports import create_export_routes
from application.apis.search import create_search_routes
from application.apis.analytics import create_analytics_routes

# Register all routes
register_user_routes(app)
register_subject_routes(app)
register_chapter_routes(app)
create_quiz_routes(app)
create_question_routes(app)
create_export_routes(app)
create_search_routes(app)
create_analytics_routes(app)

# Dashboard statistics route
@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def fetch_dashboard_stats():
    """
    Retrieve dashboard statistics
    ---
    tags:
      - Dashboard
    security:
      - bearerAuth: []
    responses:
      200:
        description: Dashboard statistics
      403:
        description: Admin access required
    """
    try:
        # Get current user's identity
        current_user_email = get_jwt_identity()  # Now this is just the email string
        
        # Import models here to avoid circular imports
        from application.models import Users, Subjects, Chapters, Quizzes, Scores
        
        # Verify admin access
        current_user = Users.query.filter_by(email=current_user_email).first()
        if not current_user or not current_user.is_admin:
            return jsonify({
                'message': 'Access denied. Admin privileges required.',
                'error': 'UNAUTHORIZED'
            }), 403
        
        # Gather dashboard statistics
        stats = {
            'users': {
                'total': Users.query.count(),
                'active': Users.query.filter_by(is_active=True).count(),
                'admin': Users.query.filter_by(is_admin=True).count()
            },
            'subjects': {
                'total': Subjects.query.count(),
                'active': Subjects.query.filter_by(is_active=True).count()
            },
            'chapters': {
                'total': Chapters.query.count()
            },
            'quizzes': {
                'total': Quizzes.query.count(),
                'active': Quizzes.query.filter_by(is_active=True).count()
            },
            'scores': {
                'total_attempts': Scores.query.count(),
                'avg_score': db.session.query(db.func.avg(Scores.total_scored)).scalar() or 0
            }
        }
        
        logger.info(f"Dashboard stats retrieved for admin: {current_user.email}")
        
        return jsonify(stats), 200
    
    except Exception as e:
        logger.error(f"Dashboard stats error: {str(e)}")
        return jsonify({
            'message': 'Error retrieving dashboard stats',
            'error': str(e)
        }), 500

# Recent activities route
@app.route('/api/dashboard/activities', methods=['GET'])
@jwt_required()
def fetch_recent_activities():
    """
    Retrieve recent platform activities
    ---
    tags:
      - Dashboard
    security:
      - bearerAuth: []
    responses:
      200:
        description: Recent platform activities
      403:
        description: Admin access required
    """
    try:
        # Get current user's identity
        current_user_email = get_jwt_identity()  # Now this is just the email string
        
        # Import models here to avoid circular imports
        from application.models import Users, Subjects, Chapters, Quizzes, Scores
        
        # Verify admin access
        current_user = Users.query.filter_by(email=current_user_email).first()
        if not current_user or not current_user.is_admin:
            return jsonify({
                'message': 'Access denied. Admin privileges required.',
                'error': 'UNAUTHORIZED'
            }), 403
        
        # Simulate recent activities (you'll want to replace this with actual tracking)
        activities = [
            {
                'description': 'New user registered',
                'timestamp': datetime.utcnow() - timedelta(hours=2)
            },
            {
                'description': 'Subject "Python Programming" created',
                'timestamp': datetime.utcnow() - timedelta(hours=5)
            },
            {
                'description': 'Quiz "Basic Python" published',
                'timestamp': datetime.utcnow() - timedelta(days=1)
            }
        ]
        
        logger.info(f"Recent activities retrieved for admin: {current_user.email}")
        
        return jsonify(activities), 200
    
    except Exception as e:
        logger.error(f"Recent activities error: {str(e)}")
        return jsonify({
            'message': 'Error retrieving recent activities',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
