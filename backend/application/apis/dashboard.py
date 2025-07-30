from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Users, Subjects, Chapters, Quizzes, Questions, Scores
from ..database import db
from ..cache import cache_with_expiry
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta, date
import logging

logger = logging.getLogger(__name__)

def create_dashboard_routes(app):
    
    @app.route('/api/dashboard/stats', methods=['GET'])
    @jwt_required()
    @cache_with_expiry(expiry_seconds=300, key_prefix="dashboard_stats")
    def dashboard_get_stats():
        """
        Get dashboard statistics for admin dashboard
        """
        try:
            # Get current user's identity
            current_user_email = get_jwt_identity()
            current_user = Users.query.filter_by(email=current_user_email).first()
            
            if not current_user:
                return jsonify({
                    'message': 'User not found',
                    'error': 'USER_NOT_FOUND'
                }), 404
            
            # Only admins can access dashboard stats
            if not current_user.is_admin:
                return jsonify({
                    'message': 'Admin access required',
                    'error': 'ADMIN_REQUIRED'
                }), 403
            
            # Get various statistics
            users_stats = {
                'total': Users.query.filter_by(is_admin=False).count(),
                'active': db.session.query(func.count(func.distinct(Scores.user_id)))
                    .filter(Scores.time_stamp_of_attempt >= date.today() - timedelta(days=30))
                    .scalar() or 0,
                'admin': Users.query.filter_by(is_admin=True).count()
            }
            
            subjects_stats = {
                'total': Subjects.query.count(),
                'active': db.session.query(func.count(func.distinct(Subjects.id)))
                    .join(Chapters, Subjects.id == Chapters.subject_id)
                    .join(Quizzes, Chapters.id == Quizzes.chapter_id).scalar() or 0
            }
            
            chapters_stats = {
                'total': Chapters.query.count()
            }
            
            quizzes_stats = {
                'total': Quizzes.query.count(),
                'active': db.session.query(func.count(func.distinct(Quizzes.id)))
                    .join(Scores, Quizzes.id == Scores.quiz_id).scalar() or 0
            }
            
            scores_stats = {
                'total_attempts': Scores.query.count(),
                'avg_score': db.session.query(func.avg(Scores.percentage)).scalar() or 0
            }
            
            return jsonify({
                'message': 'Dashboard statistics retrieved successfully',
                'users': users_stats,
                'subjects': subjects_stats,
                'chapters': chapters_stats,
                'quizzes': quizzes_stats,
                'scores': scores_stats,
                'generated_at': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Dashboard stats error: {str(e)}")
            return jsonify({
                'message': 'Failed to retrieve dashboard statistics',
                'error': str(e)
            }), 500
    
    @app.route('/api/dashboard/activities', methods=['GET'])
    @jwt_required()
    @cache_with_expiry(expiry_seconds=60, key_prefix="dashboard_activities")
    def dashboard_get_activities():
        """
        Get recent activities for dashboard
        """
        try:
            # Get current user's identity
            current_user_email = get_jwt_identity()
            current_user = Users.query.filter_by(email=current_user_email).first()
            
            if not current_user:
                return jsonify({
                    'message': 'User not found',
                    'error': 'USER_NOT_FOUND'
                }), 404
            
            # Only admins can access recent activities
            if not current_user.is_admin:
                return jsonify({
                    'message': 'Admin access required',
                    'error': 'ADMIN_REQUIRED'
                }), 403
            
            # Get recent quiz attempts with user and quiz information
            recent_attempts = db.session.query(
                Scores.time_stamp_of_attempt,
                Users.username,
                Quizzes.name.label('quiz_name'),
                Subjects.name.label('subject_name'),
                Scores.percentage,
                Scores.passed
            ).join(Users, Scores.user_id == Users.id)\
             .join(Quizzes, Scores.quiz_id == Quizzes.id)\
             .join(Chapters, Quizzes.chapter_id == Chapters.id)\
             .join(Subjects, Chapters.subject_id == Subjects.id)\
             .filter(Users.is_admin == False)\
             .order_by(desc(Scores.time_stamp_of_attempt))\
             .limit(20).all()
            
            # Format activities
            activities = []
            for attempt in recent_attempts:
                status = "passed" if attempt.passed else "failed"
                description = f"{attempt.username} {status} '{attempt.quiz_name}' quiz in {attempt.subject_name} with {attempt.percentage:.1f}%"
                
                activities.append({
                    'description': description,
                    'timestamp': attempt.time_stamp_of_attempt.isoformat(),
                    'user': attempt.username,
                    'quiz': attempt.quiz_name,
                    'subject': attempt.subject_name,
                    'score': attempt.percentage,
                    'status': status
                })
            
            return jsonify(activities)
            
        except Exception as e:
            logger.error(f"Recent activities error: {str(e)}")
            return jsonify({
                'message': 'Failed to retrieve recent activities',
                'error': str(e)
            }), 500
    
    @app.route('/api/dashboard/user/performance', methods=['GET'])
    @jwt_required()
    @cache_with_expiry(expiry_seconds=300, key_prefix="user_performance")
    def dashboard_get_user_performance():
        """
        Get user performance statistics for user dashboard
        """
        try:
            # Get current user's identity
            current_user_email = get_jwt_identity()
            current_user = Users.query.filter_by(email=current_user_email).first()
            
            if not current_user:
                return jsonify({
                    'message': 'User not found',
                    'error': 'USER_NOT_FOUND'
                }), 404
            
            # Get user's quiz scores
            user_scores = Scores.query.filter_by(user_id=current_user.id).all()
            
            if not user_scores:
                return jsonify({
                    'message': 'Performance statistics retrieved successfully',
                    'stats': {
                        'quizzes_taken': 0,
                        'average_score': 0,
                        'pass_rate': 0,
                        'time_spent': 0,
                        'best_score': 0,
                        'total_attempts': 0,
                        'passed_quizzes': 0
                    }
                })
            
            # Calculate statistics
            total_attempts = len(user_scores)
            passed_quizzes = len([s for s in user_scores if s.passed])
            average_score = sum(s.percentage for s in user_scores if s.percentage) / total_attempts
            pass_rate = (passed_quizzes / total_attempts) * 100
            time_spent = sum(s.time_taken for s in user_scores if s.time_taken) or 0
            best_score = max(s.percentage for s in user_scores if s.percentage) if user_scores else 0
            
            return jsonify({
                'message': 'Performance statistics retrieved successfully',
                'stats': {
                    'quizzes_taken': total_attempts,
                    'average_score': round(average_score, 2),
                    'pass_rate': round(pass_rate, 2),
                    'time_spent': time_spent,
                    'best_score': round(best_score, 2),
                    'total_attempts': total_attempts,
                    'passed_quizzes': passed_quizzes
                }
            })
            
        except Exception as e:
            logger.error(f"User performance error: {str(e)}")
            return jsonify({
                'message': 'Failed to retrieve performance statistics',
                'error': str(e)
            }), 500
    
    @app.route('/api/dashboard/user/recent-scores', methods=['GET'])
    @jwt_required()
    @cache_with_expiry(expiry_seconds=300, key_prefix="user_recent_scores")
    def dashboard_get_user_recent_scores():
        """
        Get user's recent quiz scores for dashboard
        """
        try:
            # Get current user's identity
            current_user_email = get_jwt_identity()
            current_user = Users.query.filter_by(email=current_user_email).first()
            
            if not current_user:
                return jsonify({
                    'message': 'User not found',
                    'error': 'USER_NOT_FOUND'
                }), 404
            
            # Get limit from query params (default 10)
            limit = min(int(request.args.get('limit', 10)), 50)
            
            # Get user's recent scores with quiz information
            recent_scores = db.session.query(
                Scores.percentage,
                Scores.time_stamp_of_attempt,
                Scores.passed,
                Scores.time_taken,
                Quizzes.name.label('quiz_name'),
                Subjects.name.label('subject_name'),
                Chapters.name.label('chapter_name')
            ).join(Quizzes, Scores.quiz_id == Quizzes.id)\
             .join(Chapters, Quizzes.chapter_id == Chapters.id)\
             .join(Subjects, Chapters.subject_id == Subjects.id)\
             .filter(Scores.user_id == current_user.id)\
             .order_by(desc(Scores.time_stamp_of_attempt))\
             .limit(limit).all()
            
            # Format scores data
            scores_data = []
            for score in recent_scores:
                scores_data.append({
                    'quiz_name': score.quiz_name,
                    'subject_name': score.subject_name,
                    'chapter_name': score.chapter_name,
                    'percentage': round(score.percentage, 2) if score.percentage else 0,
                    'passed': score.passed,
                    'time_taken': score.time_taken,
                    'date': score.time_stamp_of_attempt.strftime('%Y-%m-%d'),
                    'timestamp': score.time_stamp_of_attempt.isoformat()
                })
            
            return jsonify({
                'message': 'Recent scores retrieved successfully',
                'data': scores_data,
                'count': len(scores_data)
            })
            
        except Exception as e:
            logger.error(f"User recent scores error: {str(e)}")
            return jsonify({
                'message': 'Failed to retrieve recent scores',
                'error': str(e)
            }), 500

    return app 