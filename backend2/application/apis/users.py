from flask import jsonify, request
from application.database import db
from application.models import Users
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import logging
from datetime import datetime, timedelta
import traceback
import json
from application.models import Scores, Quizzes

# Configure logging
logger = logging.getLogger(__name__)

# We'll get the app instance from main after it's created
# This avoids circular import issues
bcrypt = Bcrypt()

def register_user_routes(app):
    
    @app.route('/api/login', methods=['POST'])
    def login():
        """
        User/Admin Login Endpoint
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
        responses:
          200:
            description: Successful login
          401:
            description: Invalid credentials
        """
        try:
            # Log the raw request data for debugging
            logger.debug(f"Raw request data: {request.data}")
            logger.debug(f"Request content type: {request.content_type}")
            logger.debug(f"Request is JSON: {request.is_json}")

            # Handle different input scenarios
            if request.is_json:
                data = request.get_json(silent=True)
            elif request.content_type == 'application/x-www-form-urlencoded':
                data = request.form.to_dict()
            else:
                # Try to parse raw data as JSON
                try:
                    data = json.loads(request.data.decode('utf-8'))
                except Exception as parse_error:
                    logger.error(f"Failed to parse request data: {parse_error}")
                    return jsonify({
                        'message': 'Unable to parse request data',
                        'error': 'INVALID_REQUEST'
                    }), 400

            # Validate data
            if not data:
                logger.error("No data received in login request")
                return jsonify({
                    'message': 'No login data received',
                    'error': 'INVALID_INPUT'
                }), 400

            # Extract email and password
            email = data.get('email') if isinstance(data, dict) else None
            password = data.get('password') if isinstance(data, dict) else None

            # Additional validation
            if not email or not password:
                logger.error(f"Invalid login attempt. Email: {email}, Password: {'*' if password else 'None'}")
                return jsonify({
                    'message': 'Email and password are required',
                    'error': 'INVALID_INPUT'
                }), 400
            
            # Find user by email
            user = Users.query.filter_by(email=email).first()
            
            # Check credentials
            if not user or not bcrypt.check_password_hash(user.password, password):
                logger.warning(f"Failed login attempt for email: {email}")
                return jsonify({
                    'message': 'Invalid email or password',
                    'error': 'UNAUTHORIZED'
                }), 401
            
            # Check if user is active
            if not user.is_active:
                logger.warning(f"Login attempt for inactive user: {email}")
                return jsonify({
                    'message': 'User account is inactive',
                    'error': 'ACCOUNT_INACTIVE'
                }), 403
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Create access token with string identity and additional claims
            additional_claims = {
                'is_admin': user.is_admin,
                'user_id': user.id,
                'username': user.username
            }
            
            access_token = create_access_token(
                identity=user.email,  # Use string instead of dict
                additional_claims=additional_claims,
                expires_delta=timedelta(hours=24)
            )
            
            # Prepare response
            response_data = {
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'is_admin': user.is_admin,
                    'last_login': user.last_login.isoformat() if user.last_login else None,
                    'registration_date': user.registration_date.isoformat() if user.registration_date else None
                },
                'redirect': '/admin/dashboard' if user.is_admin else '/user/dashboard'
            }
            
            logger.info(f"Successful login for user: {user.email}")
            
            return jsonify(response_data), 200
        
        except Exception as e:
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return jsonify({
                'message': 'Login failed',
                'error': str(e)
            }), 500

    @app.route('/api/signup', methods=['POST'])
    def signup():
        """
        User Registration Endpoint
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                email:
                  type: string
                username:
                  type: string
                password:
                  type: string
                dob:
                  type: string
                qualification:
                  type: string
        responses:
          201:
            description: User created successfully
          400:
            description: Invalid input
          409:
            description: User already exists
        """
        try:
            # Handle different input scenarios
            if request.is_json:
                data = request.get_json(silent=True)
            else:
                try:
                    data = json.loads(request.data.decode('utf-8'))
                except:
                    data = request.form.to_dict()

            if not data:
                return jsonify({
                    'message': 'No registration data received',
                    'error': 'INVALID_INPUT'
                }), 400

            # Extract required fields
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            dob = data.get('dob')
            qualification = data.get('qualification')

            # Validate required fields
            if not email or not username or not password:
                return jsonify({
                    'message': 'Email, username, and password are required',
                    'error': 'INVALID_INPUT'
                }), 400

            # Check if user already exists
            existing_user = Users.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({
                    'message': 'User with this email already exists',
                    'error': 'USER_EXISTS'
                }), 409

            existing_username = Users.query.filter_by(username=username).first()
            if existing_username:
                return jsonify({
                    'message': 'Username already taken',
                    'error': 'USERNAME_EXISTS'
                }), 409

            # Hash password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # Parse date of birth if provided
            dob_date = None
            if dob:
                try:
                    dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({
                        'message': 'Invalid date format. Use YYYY-MM-DD',
                        'error': 'INVALID_DATE'
                    }), 400

            # Create new user
            new_user = Users(
                email=email,
                username=username,
                password=hashed_password,
                dob=dob_date,
                qualification=qualification or '',
                is_admin=False,  # Regular users are not admin
                is_active=True,
                registration_date=datetime.utcnow()
            )

            db.session.add(new_user)
            db.session.commit()

            logger.info(f"New user registered: {email}")

            return jsonify({
                'message': 'User registered successfully',
                'user': {
                    'id': new_user.id,
                    'email': new_user.email,
                    'username': new_user.username
                }
            }), 201

        except Exception as e:
            db.session.rollback()
            logger.error(f"Signup error: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'message': 'Registration failed',
                'error': str(e)
            }), 500

    @app.route('/admin/initialize', methods=['POST'])
    def initialize_admin():
        """
        Initialize the single admin user for the application
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                email:
                  type: string
                username:
                  type: string
                password:
                  type: string
        responses:
          201:
            description: Admin user created successfully
          400:
            description: Admin already exists or invalid input
        """
        try:
            data = request.get_json()
            
            # Validate input
            if not data or not data.get('email') or not data.get('password'):
                return jsonify({
                    'message': 'Email and password are required',
                    'error': 'INVALID_INPUT'
                }), 400
            
            # Check if admin already exists
            existing_admin = Users.query.filter_by(is_admin=True).first()
            if existing_admin:
                return jsonify({
                    'message': 'Admin user already exists',
                    'error': 'ADMIN_EXISTS'
                }), 400
            
            # Hash password
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            
            # Create admin user
            admin = Users(
                email=data.get('email', 'admin@quizmaster.com'),
                username=data.get('username', 'QuizMaster'),
                password=hashed_password,
                is_admin=True,
                is_active=True,
                qualification='Quiz Master Administrator',
                registration_date=datetime.utcnow()
            )
            
            db.session.add(admin)
            db.session.commit()
            
            logger.info(f"Admin initialized: {admin.email}")
            
            return jsonify({
                'message': 'Admin user created successfully',
                'admin': {
                    'id': admin.id,
                    'email': admin.email,
                    'username': admin.username
                }
            }), 201
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Admin initialization error: {str(e)}")
            return jsonify({
                'message': 'Failed to initialize admin',
                'error': str(e)
            }), 500

    @app.route('/users', methods=['GET'])
    @jwt_required()
    def get_users():
        try:
            users = Users.query.all()
            return jsonify([user.serialize() for user in users]), 200
        except Exception as e:
            logger.error(f"Error fetching users: {str(e)}")
            return jsonify({'message': 'Something went wrong'}), 500

    @app.route('/users/<int:id>', methods=['GET'])
    @jwt_required()
    def get_user(id):
        try:
            user = Users.query.get(id)
            if user:
                return jsonify({'user': user.serialize()}), 200
            else:
                return jsonify({'message': 'User not found'}), 404
        except Exception as e:
            logger.error(f"Error fetching user: {str(e)}")
            return jsonify({'message': 'Something went wrong'}), 500
        
    @app.route('/current_user', methods=['GET'])
    @jwt_required()
    def get_current_user():
        try:
            user = Users.query.filter_by(email=get_jwt_identity()['email']).first()
            return jsonify({'user': user.serialize()}), 200
        except Exception as e:
            logger.error(f"Error fetching current user: {str(e)}")
            return jsonify({'message': 'Something went wrong'}), 500

    @app.route('/dashboard/stats', methods=['GET'])
    @jwt_required()
    def get_dashboard_stats():
        """
        Retrieve dashboard statistics
        """
        try:
            # Get current user's identity
            current_user_identity = get_jwt_identity()
            logger.info(f"Dashboard stats request from user: {current_user_identity}")
            
            # Count total non-admin users
            total_users = Users.query.filter_by(is_admin=False).count()
            
            # Count active non-admin users
            active_users = Users.query.filter_by(is_admin=False, is_active=True).count()
            
            # Log detailed user information for debugging
            all_users = Users.query.filter_by(is_admin=False).all()
            user_details = [
                {
                    'id': user.id, 
                    'email': user.email, 
                    'is_active': user.is_active
                } for user in all_users
            ]
            
            logger.info(f"Dashboard Stats - Total Users: {total_users}, Active Users: {active_users}")
            logger.info(f"User Details: {user_details}")
            
            return jsonify({
                'totalUsers': total_users,
                'activeUsers': active_users,
                'userDetails': user_details,
                'userGrowth': 0,
                'totalQuizzes': 0,
                'avgQuizCompletion': 0
            }), 200
        except Exception as e:
            logger.error(f"Error fetching dashboard stats: {str(e)}")
            return jsonify({
                'message': 'Failed to retrieve dashboard statistics',
                'error': str(e)
            }), 500

    @app.route('/dashboard/activities', methods=['GET'])
    @jwt_required()
    def get_recent_activities():
        """
        Retrieve recent platform activities
        """
        try:
            # Placeholder for recent activities
            activities = [
                {
                    'id': 1,
                    'type': 'User',
                    'description': 'New user registration',
                    'timestamp': datetime.utcnow().isoformat()
                }
            ]
            
            return jsonify(activities), 200
        except Exception as e:
            logger.error(f"Error fetching recent activities: {str(e)}")
            return jsonify({
                'message': 'Failed to retrieve recent activities',
                'error': str(e)
            }), 500

    @app.route('/users/create', methods=['POST'])
    @jwt_required()
    def create_user():
        """
        Create a new user (Admin only)
        """
        try:
            # Get current user's identity
            current_user_identity = get_jwt_identity()
            current_user = Users.query.filter_by(email=current_user_identity['email']).first()
            
            # Ensure only admin can create users
            if not current_user or not current_user.is_admin:
                return jsonify({
                    'message': 'Unauthorized. Admin access required.',
                    'error': 'ADMIN_REQUIRED'
                }), 403
            
            # Get user data from request
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['email', 'username', 'password', 'dob', 'qualification']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({
                        'message': f'Missing required field: {field}',
                        'error': 'INVALID_INPUT'
                    }), 400
            
            # Check if user already exists
            existing_user = Users.query.filter(
                (Users.email == data['email']) | (Users.username == data['username'])
            ).first()
            
            if existing_user:
                return jsonify({
                    'message': 'User with this email or username already exists',
                    'error': 'USER_EXISTS'
                }), 409
            
            # Hash the password
            b = Bcrypt()
            hashed_password = b.generate_password_hash(data['password']).decode('utf-8')
            
            # Parse date of birth
            try:
                dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'message': 'Invalid date format. Use YYYY-MM-DD',
                    'error': 'INVALID_DATE'
                }), 400
            
            # Create new user
            new_user = Users(
                email=data['email'],
                username=data['username'],
                password=hashed_password,
                dob=dob,
                qualification=data['qualification'],
                is_admin=data.get('is_admin', False),
                is_active=data.get('is_active', True),
                last_login=datetime.utcnow(),
                registration_date=datetime.utcnow()
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            logger.info(f"New user created: {new_user.email}")
            
            return jsonify({
                'message': 'User created successfully',
                'user': {
                    'id': new_user.id,
                    'email': new_user.email,
                    'username': new_user.username
                }
            }), 201
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating user: {str(e)}")
            return jsonify({
                'message': 'Failed to create user',
                'error': str(e)
            }), 500

    @app.route('/api/user/profile', methods=['GET', 'PUT'])
    @jwt_required()
    def user_profile():
        """
        Get or update current user's profile
        """
        try:
            # Get current user's email from JWT
            current_user_email = get_jwt_identity()
            user = Users.query.filter_by(email=current_user_email).first()
            
            if not user:
                return jsonify({
                    'message': 'User not found',
                    'error': 'USER_NOT_FOUND'
                }), 404

            if request.method == 'GET':
                return jsonify({
                    'id': user.id,
                    'username': user.email,
                    'full_name': user.username,
                    'created_at': user.registration_date.isoformat() if user.registration_date else None,
                    'updated_at': user.last_login.isoformat() if user.last_login else None
                }), 200
            
            elif request.method == 'PUT':
                data = request.get_json()
                
                # Verify current password
                if not data.get('current_password'):
                    return jsonify({
                        'message': 'Current password is required',
                        'errors': {'current_password': 'Current password is required'}
                    }), 400
                
                if not bcrypt.check_password_hash(user.password, data['current_password']):
                    return jsonify({
                        'message': 'Current password is incorrect',
                        'errors': {'current_password': 'Current password is incorrect'}
                    }), 400
                
                # Update fields
                if 'full_name' in data:
                    user.username = data['full_name']
                
                db.session.commit()
                
                return jsonify({
                    'message': 'Profile updated successfully',
                    'user': {
                        'id': user.id,
                        'username': user.email,
                        'full_name': user.username,
                        'created_at': user.registration_date.isoformat() if user.registration_date else None,
                        'updated_at': user.last_login.isoformat() if user.last_login else None
                    }
                }), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error handling user profile: {str(e)}")
            return jsonify({
                'message': 'Failed to handle profile request',
                'error': str(e)
            }), 500

    @app.route('/api/user/change-password', methods=['POST'])
    @jwt_required()
    def change_password():
        """
        Change user's password
        """
        try:
            # Get current user
            user_id = get_jwt_identity()
            user = Users.query.get_or_404(user_id)
            
            data = request.get_json()
            
            # Validate input
            if not all(k in data for k in ['old_password', 'new_password', 'confirm_password']):
                return jsonify({
                    'message': 'Missing required fields',
                    'errors': {
                        'old_password': 'Current password is required',
                        'new_password': 'New password is required',
                        'confirm_password': 'Password confirmation is required'
                    }
                }), 400
            
            # Verify current password
            if not bcrypt.check_password_hash(user.password, data['old_password']):
                return jsonify({
                    'message': 'Current password is incorrect',
                    'errors': {'old_password': 'Current password is incorrect'}
                }), 400
            
            # Validate new password
            if len(data['new_password']) < 6:
                return jsonify({
                    'message': 'Password is too short',
                    'errors': {'new_password': 'Password must be at least 6 characters'}
                }), 400
            
            if data['new_password'] != data['confirm_password']:
                return jsonify({
                    'message': 'Passwords do not match',
                    'errors': {'confirm_password': 'Passwords do not match'}
                }), 400
            
            # Update password
            user.password = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')
            db.session.commit()
            
            return jsonify({
                'message': 'Password changed successfully'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error changing password: {str(e)}")
            return jsonify({
                'message': 'Failed to change password',
                'error': str(e)
            }), 500

    @app.route('/api/user/statistics', methods=['GET'])
    @jwt_required()
    def get_user_statistics():
        """
        Get user's quiz statistics
        """
        try:
            # Get current user
            user_id = get_jwt_identity()
            
            # Get all scores for the user
            scores = Scores.query.filter_by(user_id=user_id).all()
            
            # Calculate statistics
            total_attempts = len(scores)
            if total_attempts > 0:
                total_score = sum(score.percentage for score in scores)
                average_score = round(total_score / total_attempts, 1)
                best_score = max(score.percentage for score in scores)
                
                # Get unique subjects attempted
                subject_ids = set()
                for score in scores:
                    quiz = Quizzes.query.get(score.quiz_id)
                    if quiz and quiz.chapter:
                        subject_ids.add(quiz.chapter.subject_id)
                
                subjects_attempted = len(subject_ids)
            else:
                average_score = 0
                best_score = 0
                subjects_attempted = 0
            
            return jsonify({
                'totalAttempts': total_attempts,
                'averageScore': average_score,
                'bestScore': best_score,
                'subjectsAttempted': subjects_attempted
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching user statistics: {str(e)}")
            return jsonify({
                'message': 'Failed to retrieve statistics',
                'error': str(e)
            }), 500

    @app.route('/api/user/activity', methods=['GET'])
    @jwt_required()
    def get_user_activity():
        """
        Get user's recent activity
        """
        try:
            # Get current user
            user_id = get_jwt_identity()
            
            # Get limit parameter (default 5)
            limit = min(int(request.args.get('limit', 5)), 20)  # Max 20 activities
            
            # Get recent quiz attempts
            recent_scores = Scores.query.filter_by(user_id=user_id)\
                .order_by(Scores.time_stamp_of_attempt.desc())\
                .limit(limit)\
                .all()
            
            activities = []
            for score in recent_scores:
                quiz = Quizzes.query.get(score.quiz_id)
                if quiz:
                    activity = {
                        'id': score.id,
                        'description': f"Completed {quiz.name} - {score.percentage}%",
                        'date': score.time_stamp_of_attempt.isoformat()
                    }
                    activities.append(activity)
            
            return jsonify(activities), 200
            
        except Exception as e:
            logger.error(f"Error fetching user activity: {str(e)}")
            return jsonify({
                'message': 'Failed to retrieve activity',
                'error': str(e)
            }), 500