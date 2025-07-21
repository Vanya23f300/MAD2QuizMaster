from flask import jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Users, Scores, Quizzes, Chapters, Subjects
from ..database import db
from ..celery_tasks import generate_user_csv_export
from ..cache import get_cache_stats
import csv
import io
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def create_export_routes(app):
    
    @app.route('/api/export/user-quiz-details', methods=['POST'])
    @jwt_required()
    def export_user_quiz_details():
        """
        Export user's quiz attempts as CSV (User Triggered Async Job)
        """
        try:
            current_user_identity = get_jwt_identity()
            user = Users.query.filter_by(email=current_user_identity['email']).first()
            
            if not user:
                return jsonify({
                    'message': 'User not found',
                    'error': 'USER_NOT_FOUND'
                }), 404
            
            # Get all quiz attempts by the user
            scores = db.session.query(Scores, Quizzes, Chapters, Subjects)\
                .join(Quizzes, Scores.quiz_id == Quizzes.id)\
                .join(Chapters, Quizzes.chapter_id == Chapters.id)\
                .join(Subjects, Chapters.subject_id == Subjects.id)\
                .filter(Scores.user_id == user.id)\
                .order_by(Scores.time_stamp_of_attempt.desc())\
                .all()
            
            if not scores:
                return jsonify({
                    'message': 'No quiz attempts found',
                    'error': 'NO_DATA'
                }), 404
            
            # Create CSV content
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write headers
            writer.writerow([
                'Quiz ID', 'Quiz Name', 'Chapter Name', 'Subject Name',
                'Date of Quiz', 'Attempt Date', 'Score', 'Total Score',
                'Percentage', 'Time Taken (seconds)', 'Passed', 'Remarks'
            ])
            
            # Write data rows
            for score, quiz, chapter, subject in scores:
                writer.writerow([
                    quiz.id,
                    quiz.name,
                    chapter.name,
                    subject.name,
                    quiz.date_of_quiz.strftime('%Y-%m-%d') if quiz.date_of_quiz else 'N/A',
                    score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S'),
                    score.total_scored,
                    score.total_possible_score,
                    f"{score.percentage:.2f}%" if score.percentage else '0.00%',
                    score.time_taken or 0,
                    'Yes' if score.passed else 'No',
                    quiz.remarks or ''
                ])
            
            # Prepare file for download
            output.seek(0)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"quiz_details_{user.username}_{timestamp}.csv"
            
            # Create a BytesIO object for file download
            mem = io.BytesIO()
            mem.write(output.getvalue().encode('utf-8'))
            mem.seek(0)
            output.close()
            
            logger.info(f"CSV export generated for user: {user.email}")
            
            return send_file(
                mem,
                as_attachment=True,
                download_name=filename,
                mimetype='text/csv'
            )
            
        except Exception as e:
            logger.error(f"Error generating CSV export: {str(e)}")
            return jsonify({
                'message': 'Failed to generate CSV export',
                'error': str(e)
            }), 500

    @app.route('/api/export/admin-user-details', methods=['POST'])
    @jwt_required()
    def export_admin_user_details():
        """
        Export all users' quiz performance as CSV (Admin only)
        """
        try:
            current_user_identity = get_jwt_identity()
            current_user = Users.query.filter_by(email=current_user_identity['email']).first()
            
            if not current_user or not current_user.is_admin:
                return jsonify({
                    'message': 'Unauthorized. Admin access required.',
                    'error': 'ADMIN_REQUIRED'
                }), 403
            
            # Get user statistics
            user_stats = db.session.query(
                Users.id,
                Users.username,
                Users.email,
                Users.qualification,
                Users.registration_date,
                Users.last_login,
                db.func.count(Scores.id).label('quizzes_taken'),
                db.func.avg(Scores.percentage).label('avg_score'),
                db.func.max(Scores.percentage).label('best_score'),
                db.func.min(Scores.percentage).label('worst_score')
            )\
            .outerjoin(Scores, Users.id == Scores.user_id)\
            .filter(Users.is_admin == False)\
            .group_by(Users.id)\
            .all()
            
            # Create CSV content
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write headers
            writer.writerow([
                'User ID', 'Username', 'Email', 'Qualification',
                'Registration Date', 'Last Login', 'Quizzes Taken',
                'Average Score (%)', 'Best Score (%)', 'Worst Score (%)'
            ])
            
            # Write data rows
            for stat in user_stats:
                writer.writerow([
                    stat.id,
                    stat.username,
                    stat.email,
                    stat.qualification,
                    stat.registration_date.strftime('%Y-%m-%d') if stat.registration_date else 'N/A',
                    stat.last_login.strftime('%Y-%m-%d %H:%M:%S') if stat.last_login else 'Never',
                    stat.quizzes_taken or 0,
                    f"{stat.avg_score:.2f}" if stat.avg_score else '0.00',
                    f"{stat.best_score:.2f}" if stat.best_score else '0.00',
                    f"{stat.worst_score:.2f}" if stat.worst_score else '0.00'
                ])
            
            # Prepare file for download
            output.seek(0)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"user_performance_report_{timestamp}.csv"
            
            # Create a BytesIO object for file download
            mem = io.BytesIO()
            mem.write(output.getvalue().encode('utf-8'))
            mem.seek(0)
            output.close()
            
            logger.info(f"Admin CSV export generated by: {current_user.email}")
            
            return send_file(
                mem,
                as_attachment=True,
                download_name=filename,
                mimetype='text/csv'
            )
            
        except Exception as e:
            logger.error(f"Error generating admin CSV export: {str(e)}")
            return jsonify({
                'message': 'Failed to generate CSV export',
                'error': str(e)
            }), 500

    @app.route('/api/export/async-user-quiz-details', methods=['POST'])
    @jwt_required()
    def export_user_quiz_details_async():
        """
        Trigger async CSV export for user's quiz details
        """
        try:
            current_user_identity = get_jwt_identity()
            user = Users.query.filter_by(email=current_user_identity['email']).first()
            
            if not user:
                return jsonify({
                    'message': 'User not found',
                    'error': 'USER_NOT_FOUND'
                }), 404
            
            # Start async task
            task = generate_user_csv_export.delay(user.id, 'quiz_details')
            
            logger.info(f"Async CSV export started for user: {user.email}, task_id: {task.id}")
            
            return jsonify({
                'message': 'Export task started successfully',
                'task_id': task.id,
                'status': 'processing',
                'estimated_time': '1-2 minutes'
            }), 202
            
        except Exception as e:
            logger.error(f"Error starting async CSV export: {str(e)}")
            return jsonify({
                'message': 'Failed to start export task',
                'error': str(e)
            }), 500
    
    @app.route('/api/export/task-status/<task_id>', methods=['GET'])
    @jwt_required()
    def get_export_task_status(task_id):
        """
        Check status of async export task
        """
        try:
            from ..celery_config import celery
            task = celery.AsyncResult(task_id)
            
            if task.state == 'PENDING':
                response = {
                    'state': task.state,
                    'status': 'Task is waiting to be processed',
                    'progress': 0
                }
            elif task.state == 'PROGRESS':
                response = {
                    'state': task.state,
                    'status': task.info.get('status', ''),
                    'progress': task.info.get('progress', 0)
                }
            elif task.state == 'SUCCESS':
                response = {
                    'state': task.state,
                    'status': 'Task completed successfully',
                    'progress': 100,
                    'result': task.info
                }
            else:
                # Task failed
                response = {
                    'state': task.state,
                    'status': str(task.info),
                    'progress': 100
                }
            
            return jsonify(response)
            
        except Exception as e:
            logger.error(f"Error checking task status: {str(e)}")
            return jsonify({
                'state': 'FAILURE',
                'status': str(e)
            }), 500
    
    @app.route('/api/cache/stats', methods=['GET'])
    @jwt_required()
    def get_cache_statistics():
        """
        Get Redis cache statistics (Admin only for now)
        """
        try:
            current_user_identity = get_jwt_identity()
            current_user = Users.query.filter_by(email=current_user_identity['email']).first()
            
            if not current_user or not current_user.is_admin:
                return jsonify({
                    'message': 'Unauthorized. Admin access required.',
                    'error': 'ADMIN_REQUIRED'
                }), 403
            
            stats = get_cache_stats()
            
            return jsonify({
                'message': 'Cache statistics retrieved successfully',
                'cache_stats': stats
            })
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {str(e)}")
            return jsonify({
                'message': 'Failed to get cache statistics',
                'error': str(e)
            }), 500

    return app