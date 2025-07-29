from flask import Flask, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.models import Questions, Subjects, Chapters, Quizzes, Scores, Users
from sqlalchemy import or_, func
import logging
from datetime import datetime, timedelta

# Configure logging
logger = logging.getLogger(__name__)

def create_search_routes(app):
    """
    Create routes for search functionality
    """
    
    @app.route('/api/search', methods=['GET'])
    @jwt_required()
    def search():
        """
        Search across questions, subjects, chapters, and quizzes
        """
        try:
            # Get query param
            query = request.args.get('q', '')
            
            if not query or len(query) < 2:
                return jsonify({
                    'message': 'Search query must be at least 2 characters'
                }), 400
            
            # Create search term with wildcards for SQL LIKE
            search_term = f'%{query}%'
            
            # Search in questions
            questions = Questions.query.filter(
                or_(
                    Questions.question_text.ilike(search_term),
                    Questions.option1.ilike(search_term),
                    Questions.option2.ilike(search_term),
                    Questions.option3.ilike(search_term),
                    Questions.option4.ilike(search_term)
                )
            ).all()
            
            # Search in subjects
            subjects = Subjects.query.filter(
                or_(
                    Subjects.name.ilike(search_term),
                    Subjects.description.ilike(search_term)
                )
            ).all()
            
            # Search in chapters
            chapters = Chapters.query.filter(
                or_(
                    Chapters.name.ilike(search_term),
                    Chapters.description.ilike(search_term)
                )
            ).all()
            
            # Search in quizzes
            quizzes = Quizzes.query.filter(
                or_(
                    Quizzes.name.ilike(search_term),
                    Quizzes.description.ilike(search_term),
                    Quizzes.remarks.ilike(search_term)
                )
            ).all()
            
            # Prepare response
            results = {
                'questions': [q.serialize() for q in questions],
                'subjects': [s.serialize() for s in subjects],
                'chapters': [c.serialize() for c in chapters],
                'quizzes': [q.serialize() for q in quizzes],
                'total_count': len(questions) + len(subjects) + len(chapters) + len(quizzes)
            }
            
            return jsonify(results), 200
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return jsonify({
                'message': f'Search failed: {str(e)}'
            }), 500

    @app.route('/api/dashboard/user/performance', methods=['GET'])
    @jwt_required()
    def get_user_performance():
        """
        Get user performance statistics
        """
        try:
            # Get current user's email from JWT
            user_email = get_jwt_identity()
            
            # Get the user from database
            user = Users.query.filter_by(email=user_email).first()
            if not user:
                return jsonify({
                    'message': 'User not found',
                    'error': 'USER_NOT_FOUND'
                }), 404
                
            user_id = user.id
            user_email = user.email  # Get email for alternative check
            
            # Get all scores for the user - check by ID or email
            scores = Scores.query.filter(
                (Scores.user_id == user_id) | 
                (Scores.user_id == user_email)  # Check for email as user_id
            ).all()
            
            # Log for debugging
            print(f"User ID: {user_id}, Email: {user_email}")
            print(f"Found {len(scores)} scores for this user")
            
            # Calculate statistics
            total_quizzes = len(scores)
            total_score = sum(score.percentage for score in scores) if scores else 0
            passed_quizzes = len([score for score in scores if score.passed]) if scores else 0
            total_time = sum(score.time_taken for score in scores if score.time_taken is not None) if scores else 0
            
            # Calculate averages
            average_score = round(total_score / total_quizzes, 1) if total_quizzes > 0 else 0
            pass_rate = round((passed_quizzes / total_quizzes) * 100, 1) if total_quizzes > 0 else 0
            
            # Prepare response
            response = {
                'stats': {
                    'quizzes_taken': total_quizzes,
                    'average_score': average_score,
                    'pass_rate': pass_rate,
                    'time_spent': total_time
                }
            }
            
            return jsonify(response), 200
            
        except Exception as e:
            logger.error(f"User performance data error: {str(e)}")
            return jsonify({
                'message': f'Failed to get performance data: {str(e)}'
            }), 500

    @app.route('/api/dashboard/user/recent-scores', methods=['GET'])
    @jwt_required()
    def get_recent_scores():
        """
        Get user's recent quiz scores
        """
        try:
            # Get current user's email from JWT
            user_email = get_jwt_identity()
            
            # Get the user from database
            user = Users.query.filter_by(email=user_email).first()
            if not user:
                return jsonify({
                    'message': 'User not found',
                    'error': 'USER_NOT_FOUND'
                }), 404
                
            user_id = user.id
            user_email = user.email  # Get email for alternative check
            
            # Get limit parameter
            limit = min(int(request.args.get('limit', 5)), 20)  # Max 20 scores
            
            # Get recent scores for the user - check by ID or email
            scores = Scores.query.filter(
                (Scores.user_id == user_id) | 
                (Scores.user_id == user_email)  # Check for email as user_id
            ).order_by(Scores.time_stamp_of_attempt.desc()).limit(limit).all()
            
            # Prepare response with quiz names
            results = []
            for score in scores:
                quiz = Quizzes.query.get(score.quiz_id)
                quiz_name = quiz.name if quiz else 'Unknown Quiz'
                
                results.append({
                    'id': score.id,
                    'quiz_id': score.quiz_id,
                    'quiz_name': quiz_name,
                    'percentage': score.percentage,
                    'passed': score.passed,
                    'time_stamp_of_attempt': score.time_stamp_of_attempt.isoformat(),
                    'time_taken': score.time_taken
                })
            
            return jsonify(results), 200
            
        except Exception as e:
            logger.error(f"Recent scores error: {str(e)}")
            return jsonify({
                'message': f'Failed to get recent scores: {str(e)}'
            }), 500
    
    return app