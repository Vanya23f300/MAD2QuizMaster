from flask import jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.models import Users, Quizzes, Chapters, Subjects, Scores
from application.database import db
from datetime import datetime
import os
import logging
import traceback

logger = logging.getLogger(__name__)

def register_export_routes(app):
    @app.route('/api/exports/user-quizzes', methods=['POST'])
    @jwt_required()
    def trigger_user_quiz_export():
        """
        Trigger an asynchronous export of user's quiz data
        """
        try:
            logger.info("Export request received")
            
            # Get current user
            user_email = get_jwt_identity()
            logger.info(f"User email from token: {user_email}")
            
            # Convert email to user ID
            current_user = Users.query.filter_by(email=user_email).first()
            if not current_user:
                return jsonify({
                    'message': 'User not found'
                }), 404
                
            user_id = current_user.id
            logger.info(f"User ID: {user_id}")
            
            # Create export request
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f'user_quiz_export_{user_id}_{timestamp}.csv'
            
            # Ensure export directory exists with proper permissions
            export_dir = os.path.join(app.instance_path, 'exports')
            try:
                os.makedirs(export_dir, exist_ok=True)
                os.chmod(export_dir, 0o777)  # Give full permissions to ensure Celery can write
                logger.info(f"Export directory created/verified: {export_dir}")
            except Exception as e:
                logger.error(f"Error creating export directory: {str(e)}")
                return jsonify({
                    'message': f'Failed to create export directory: {str(e)}'
                }), 500
            
            # Queue the export task
            logger.info(f"Queueing export task for user {user_id}")
            from application.celery_tasks import generate_user_quiz_export
            task = generate_user_quiz_export.delay(user_id, filename)
            logger.info(f"Task created with ID: {task.id}")
            
            return jsonify({
                'message': 'Export started successfully',
                'task_id': task.id,
                'filename': filename
            }), 202
            
        except Exception as e:
            logger.error(f"Export error: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'message': f'Failed to start export: {str(e)}'
            }), 500

    @app.route('/api/exports/status/<task_id>', methods=['GET'])
    @jwt_required()
    def get_export_status(task_id):
        """
        Get the status of an export task
        """
        try:
            logger.info(f"Status check for task: {task_id}")
            from application.celery_tasks import generate_user_quiz_export
            task = generate_user_quiz_export.AsyncResult(task_id)
            
            if task.state == 'PENDING':
                response = {
                    'state': 'pending',
                    'status': 'Export is pending...'
                }
            elif task.state == 'SUCCESS':
                result = task.result
                if result.get('filename') is None:
                    response = {
                        'state': 'completed',
                        'status': result.get('message', 'Export completed successfully'),
                        'result': result,
                        'no_data': True
                    }
                else:
                    response = {
                        'state': 'completed',
                        'status': 'Export completed successfully',
                        'result': result
                    }
            elif task.state == 'FAILURE':
                response = {
                    'state': 'failed',
                    'status': 'Export failed',
                    'error': str(task.result)
                }
            else:
                response = {
                    'state': 'in_progress',
                    'status': 'Export is in progress...'
                }
            
            logger.info(f"Task {task_id} status: {response['state']}")
            return jsonify(response), 200
            
        except Exception as e:
            logger.error(f"Status check error: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'message': f'Failed to check status: {str(e)}'
            }), 500

    @app.route('/api/exports/download/<filename>', methods=['GET'])
    @jwt_required()
    def download_export(filename):
        """
        Download a completed export file
        """
        try:
            user_email = get_jwt_identity()
            logger.info(f"Download request for {filename} by user {user_email}")
            
            # Get user ID from email
            current_user = Users.query.filter_by(email=user_email).first()
            if not current_user:
                return jsonify({
                    'message': 'User not found'
                }), 404
                
            user_id = current_user.id
            
            # Security check: ensure filename contains user_id
            if f'user_quiz_export_{user_id}_' not in filename:
                logger.warning(f"Unauthorized download attempt for {filename} by user {user_email}")
                return jsonify({
                    'message': 'Unauthorized to access this file'
                }), 403
            
            export_dir = os.path.join(app.instance_path, 'exports')
            file_path = os.path.join(export_dir, filename)
            
            logger.info(f"Looking for file at: {file_path}")
            
            if not os.path.exists(file_path):
                logger.warning(f"File not found: {file_path}")
                return jsonify({
                    'message': 'Export file not found'
                }), 404
            
            logger.info(f"File found, sending: {file_path}")
            return send_file(
                file_path,
                mimetype='text/csv',
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            logger.error(f"Download error: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'message': f'Failed to download file: {str(e)}'
            }), 500

    # Additional route to check if exports API is working
    @app.route('/api/exports/health', methods=['GET'])
    def export_health_check():
        """
        Simple health check endpoint for the exports API
        """
        return jsonify({
            'status': 'ok',
            'message': 'Exports API is operational'
        }), 200

    return app 