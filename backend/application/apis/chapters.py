from flask import jsonify, request
from application.database import db
from application.models import Chapters, Subjects, Users
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def register_chapter_routes(app):
    @app.route('/api/chapters', methods=['GET'])
    @jwt_required()
    def get_chapters():
        """
        Retrieve all chapters or filter by subject_id
        Requires JWT authentication
        """
        try:
            subject_id = request.args.get('subject_id', type=int)
            
            if subject_id:
                # Fetch chapters for specific subject
                subject = Subjects.query.get(subject_id)
                if not subject:
                    return jsonify({
                        "message": "Subject not found",
                        "error": "SUBJECT_NOT_FOUND"
                    }), 404
                
                chapters = Chapters.query.filter_by(subject_id=subject_id).order_by(Chapters.order, Chapters.name).all()
            else:
                # Fetch all chapters
                chapters = Chapters.query.order_by(Chapters.subject_id, Chapters.order, Chapters.name).all()
            
            return jsonify([
                {
                    **chapter.serialize(),
                    'subject_name': chapter.subject.name if chapter.subject else None
                } for chapter in chapters
            ]), 200
        
        except Exception as e:
            logger.error(f"Error fetching chapters: {str(e)}")
            return jsonify({
                "message": "Failed to retrieve chapters",
                "error": str(e)
            }), 500

    @app.route('/api/chapters', methods=['POST'])
    @jwt_required()
    def create_chapter():
        """
        Create a new chapter
        Requires JWT authentication and admin privileges
        """
        try:
            # Get current user's identity from JWT and find the user
            current_user_email = get_jwt_identity()  # Now this returns just the email string
            current_user = Users.query.filter_by(email=current_user_email).first()
            
            # Verify user is an admin
            if not current_user or not current_user.is_admin:
                return jsonify({
                    "message": "Unauthorized. Admin access required.",
                    "error": "ADMIN_REQUIRED"
                }), 403
            
            # Get chapter data from request
            data = request.get_json()
            
            # Validate input
            if not data or 'name' not in data or 'subject_id' not in data:
                return jsonify({
                    "message": "Chapter name and subject ID are required",
                    "error": "INVALID_INPUT"
                }), 400
            
            # Check if subject exists
            subject = Subjects.query.get(data['subject_id'])
            if not subject:
                return jsonify({
                    "message": "Subject not found",
                    "error": "SUBJECT_NOT_FOUND"
                }), 404
            
            # Check if chapter already exists in this subject
            existing_chapter = Chapters.query.filter_by(
                name=data['name'], 
                subject_id=data['subject_id']
            ).first()
            
            if existing_chapter:
                return jsonify({
                    "message": "Chapter with this name already exists in the subject",
                    "error": "CHAPTER_EXISTS"
                }), 409
            
            # Create new chapter
            new_chapter = Chapters(
                name=data['name'],
                subject_id=data['subject_id'],
                description=data.get('description', ''),
                order=data.get('order', 0),
                created_at=datetime.utcnow()
            )
            
            db.session.add(new_chapter)
            db.session.commit()
            
            logger.info(f"Chapter created: {new_chapter.name}")
            
            return jsonify({
                "message": "Chapter created successfully",
                "chapter": new_chapter.serialize()
            }), 201
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating chapter: {str(e)}")
            return jsonify({
                "message": "Failed to create chapter",
                "error": str(e)
            }), 500

    @app.route('/api/subjects/<int:subject_id>/chapters', methods=['GET'])
    @jwt_required()
    def get_chapters_by_subject(subject_id):
        """
        Retrieve chapters for a specific subject
        Requires JWT authentication
        """
        try:
            # Verify subject exists
            subject = Subjects.query.get(subject_id)
            if not subject:
                return jsonify({
                    "message": "Subject not found",
                    "error": "SUBJECT_NOT_FOUND"
                }), 404
            
            # Fetch chapters for the subject
            chapters = Chapters.query.filter_by(subject_id=subject_id).all()
            
            return jsonify([
                chapter.serialize() for chapter in chapters
            ]), 200
        
        except Exception as e:
            logger.error(f"Error fetching chapters: {str(e)}")
            return jsonify({
                "message": "Failed to retrieve chapters",
                "error": str(e)
            }), 500

    @app.route('/api/chapters/<int:chapter_id>', methods=['PUT'])
    @jwt_required()
    def update_chapter(chapter_id):
        """
        Update an existing chapter
        Requires JWT authentication and admin privileges
        """
        try:
            # Get current user's identity from JWT and find the user
            current_user_email = get_jwt_identity()  # Now this returns just the email string
            current_user = Users.query.filter_by(email=current_user_email).first()
            
            # Verify user is an admin
            if not current_user or not current_user.is_admin:
                return jsonify({
                    "message": "Unauthorized. Admin access required.",
                    "error": "ADMIN_REQUIRED"
                }), 403
            
            # Get the chapter to update
            chapter = Chapters.query.get(chapter_id)
            if not chapter:
                return jsonify({
                    "message": "Chapter not found",
                    "error": "CHAPTER_NOT_FOUND"
                }), 404
            
            # Get update data from request
            data = request.get_json()
            
            # Update chapter fields
            if 'name' in data:
                chapter.name = data['name']
            if 'description' in data:
                chapter.description = data['description']
            if 'order' in data:
                chapter.order = data['order']
            if 'subject_id' in data:
                # Verify new subject exists
                subject = Subjects.query.get(data['subject_id'])
                if not subject:
                    return jsonify({
                        "message": "Subject not found",
                        "error": "SUBJECT_NOT_FOUND"
                    }), 404
                chapter.subject_id = data['subject_id']
            
            db.session.commit()
            
            logger.info(f"Chapter updated: {chapter.name}")
            
            return jsonify({
                "message": "Chapter updated successfully",
                "chapter": chapter.serialize()
            }), 200
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating chapter: {str(e)}")
            return jsonify({
                "message": "Failed to update chapter",
                "error": str(e)
            }), 500

    @app.route('/api/chapters/<int:chapter_id>', methods=['DELETE'])
    @jwt_required()
    def delete_chapter(chapter_id):
        """
        Delete a chapter
        Requires JWT authentication and admin privileges
        """
        try:
            # Get current user's identity from JWT and find the user
            current_user_email = get_jwt_identity()  # Now this returns just the email string
            current_user = Users.query.filter_by(email=current_user_email).first()
            
            # Verify user is an admin
            if not current_user or not current_user.is_admin:
                return jsonify({
                    "message": "Unauthorized. Admin access required.",
                    "error": "ADMIN_REQUIRED"
                }), 403
            
            # Get the chapter to delete
            chapter = Chapters.query.get(chapter_id)
            if not chapter:
                return jsonify({
                    "message": "Chapter not found",
                    "error": "CHAPTER_NOT_FOUND"
                }), 404
            
            chapter_name = chapter.name
            db.session.delete(chapter)
            db.session.commit()
            
            logger.info(f"Chapter deleted: {chapter_name}")
            
            return jsonify({
                "message": "Chapter deleted successfully"
            }), 200
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting chapter: {str(e)}")
            return jsonify({
                "message": "Failed to delete chapter",
                "error": str(e)
            }), 500