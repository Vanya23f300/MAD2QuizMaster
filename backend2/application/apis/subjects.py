from flask import jsonify, request
from application.database import db
from application.models import Subjects
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.auth import admin_required
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def register_subject_routes(app):
    
    @app.route('/api/subjects', methods=['GET'])
    @jwt_required()
    def get_subjects():
        """
        Retrieve all active subjects
        ---
        tags:
          - Subjects
        security:
          - bearerAuth: []
        responses:
          200:
            description: List of all active subjects
          403:
            description: Authentication required
        """
        try:
            # Fetch only active subjects
            subjects = Subjects.query.filter_by(is_active=True).all()
            return jsonify([
                {
                    'id': subject.id,
                    'name': subject.name,
                    'description': subject.description,
                    'created_at': subject.created_at.isoformat() if subject.created_at else None,
                    'is_active': subject.is_active
                } for subject in subjects
            ]), 200
        except Exception as e:
            logger.error(f"Error fetching subjects: {str(e)}")
            return jsonify({
                'message': 'Error fetching subjects',
                'error': str(e)
            }), 500

    @app.route('/api/subjects', methods=['POST'])
    @jwt_required()
    @admin_required
    def create_subject():
        """
        Create a new subject (Admin only)
        ---
        tags:
          - Subjects
        security:
          - bearerAuth: []
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                description:
                  type: string
        responses:
          201:
            description: Subject created successfully
          400:
            description: Invalid input
          403:
            description: Admin access required
          409:
            description: Subject already exists
        """
        try:
            data = request.get_json()
            
            # Validate input
            if not data or not data.get('name'):
                return jsonify({
                    'message': 'Subject name is required',
                    'error': 'INVALID_INPUT'
                }), 400
            
            # Check if subject already exists
            existing_subject = Subjects.query.filter_by(name=data['name']).first()
            if existing_subject:
                return jsonify({
                    'message': 'Subject already exists',
                    'error': 'DUPLICATE_SUBJECT'
                }), 409
            
            # Get current user's identity from JWT and find the user
            current_user_email = get_jwt_identity()  # Now this returns just the email string
            from application.models import Users
            current_user = Users.query.filter_by(email=current_user_email).first()
            
            if not current_user:
                return jsonify({
                    'message': 'User not found',
                    'error': 'USER_NOT_FOUND'
                }), 404
            
            # Create new subject with the current user as creator
            new_subject = Subjects(
                name=data['name'],
                description=data.get('description', ''),
                created_by=current_user.id,  # Set the creator
                created_at=datetime.utcnow(),
                is_active=True
            )
            
            db.session.add(new_subject)
            db.session.commit()
            
            logger.info(f"Subject created: {new_subject.name} by user {current_user.email}")
            
            return jsonify({
                'message': 'Subject created successfully',
                'subject': {
                    'id': new_subject.id,
                    'name': new_subject.name,
                    'description': new_subject.description,
                    'created_at': new_subject.created_at.isoformat(),
                    'created_by': current_user.username
                }
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating subject: {str(e)}")
            return jsonify({
                'message': 'Error creating subject',
                'error': str(e)
            }), 500

    @app.route('/api/subjects/available', methods=['GET'])
    @jwt_required()
    def get_available_subjects():
        """
        Retrieve all active subjects for students
        ---
        tags:
          - Subjects
        security:
          - bearerAuth: []
        responses:
          200:
            description: List of active subjects
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  description:
                    type: string
        """
        try:
            # Fetch only active subjects
            subjects = Subjects.query.filter_by(is_active=True).all()
            
            # Serialize subjects
            available_subjects = [
                {
                    'id': subject.id,
                    'name': subject.name,
                    'description': subject.description or '',
                    'created_at': subject.created_at.isoformat() if subject.created_at else None
                } for subject in subjects
            ]
            
            logger.info(f"Retrieved {len(available_subjects)} active subjects")
            
            return jsonify(available_subjects), 200
        except Exception as e:
            logger.error(f"Error fetching available subjects: {str(e)}")
            return jsonify({
                'message': 'Error retrieving subjects',
                'error': str(e)
            }), 500

    @app.route('/api/subjects', methods=['OPTIONS'])
    def subjects_options():
        """Handle preflight requests"""
        return '', 200