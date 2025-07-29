from celery import Celery
from application.database import db
from application.models import Users, Quizzes, Chapters, Subjects, Scores
from datetime import datetime, timedelta
from sqlalchemy import desc, func, and_, or_
import csv
import os
import logging

logger = logging.getLogger(__name__)

# Configure celery from celery_config.py
from application.celery_config import celery

@celery.task(bind=True)
def generate_user_quiz_export(self, user_id, filename):
    """
    Generate CSV export of user's quiz attempts
    """
    try:
        import os  # Ensure os is imported directly within the task scope
        import csv  # Ensure csv is also available
        from flask import Flask
        from application.config import LocalDevelopmentConfig
        
        # Create a Flask app for this task
        app = Flask(__name__)
        app.config.from_object(LocalDevelopmentConfig)
        
        # Explicitly set the database URI if not already set
        if 'SQLALCHEMY_DATABASE_URI' not in app.config or not app.config['SQLALCHEMY_DATABASE_URI']:
            # Set the database URI to point to the instance folder
            BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.sqlite3')
            app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
        
        db.init_app(app)
    except ImportError as e:
        logger.error(f"Import error in export task: {str(e)}")
        return {
            'status': 'failed',
            'message': f'Import error: {str(e)}. Please contact support.'
        }
    
    try:
        logger.info(f"Starting quiz export for user {user_id}")
        
        # Use the Flask application context
        with app.app_context():
            # Get all quiz attempts by the user with related data
            scores = db.session.query(Scores, Quizzes, Chapters, Subjects)\
                .join(Quizzes, Scores.quiz_id == Quizzes.id)\
                .join(Chapters, Quizzes.chapter_id == Chapters.id)\
                .join(Subjects, Chapters.subject_id == Subjects.id)\
                .filter(Scores.user_id == user_id)\
                .order_by(Scores.time_stamp_of_attempt.desc())\
                .all()
            
            if not scores:
                logger.warning(f"No quiz attempts found for user {user_id}")
                return {
                    'status': 'completed',
                    'message': 'No quiz attempts found',
                    'filename': None
                }
            
            # Ensure exports directory exists
            export_dir = os.path.join('instance', 'exports')
            os.makedirs(export_dir, exist_ok=True)
            try:
                os.chmod(export_dir, 0o777)  # Make sure directory is writable
            except:
                pass  # Ignore permission errors, just try to create

            # Create CSV file
            file_path = os.path.join(export_dir, filename)
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write headers
                writer.writerow([
                    'Quiz ID',
                    'Quiz Name',
                    'Chapter ID',
                    'Chapter Name',
                    'Subject ID',
                    'Subject Name',
                    'Date of Quiz',
                    'Attempt Date',
                    'Score',
                    'Total Score',
                    'Percentage',
                    'Passed',
                    'Time Taken (minutes)',
                    'Time Taken (seconds)',
                    'Remarks'
                ])
                
                # Write data rows
                total_rows = len(scores)
                for idx, (score, quiz, chapter, subject) in enumerate(scores, 1):
                    writer.writerow([
                        quiz.id,
                        quiz.name,
                        chapter.id,
                        chapter.name,
                        subject.id,
                        subject.name,
                        quiz.date_of_quiz.strftime('%Y-%m-%d') if quiz.date_of_quiz else 'N/A',
                        score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S'),
                        score.total_scored,
                        score.total_possible_score,
                        f"{score.percentage:.2f}%",
                        'Yes' if score.passed else 'No',
                        f"{score.time_taken / 60:.1f}" if score.time_taken else '0.0',
                        score.time_taken if score.time_taken else 0,
                        quiz.remarks or ''
                    ])
                    
                    # Update progress
                    self.update_state(
                        state='PROGRESS',
                        meta={
                            'current': idx,
                            'total': total_rows,
                            'status': f'Processing row {idx} of {total_rows}'
                        }
                    )
            
        logger.info(f"Export completed successfully for user {user_id}")
            
        return {
            'status': 'completed',
            'message': 'Export completed successfully',
            'filename': filename
        }
        
    except Exception as e:
        logger.error(f"Export failed for user {user_id}: {str(e)}")
        raise

@celery.task(bind=True)
def send_daily_reminders(self):
    """
    Send daily reminders to users who haven't logged in recently
    """
    try:
        from flask import Flask
        from application.config import LocalDevelopmentConfig
        from application.simple_email import send_daily_reminder
        
        # Create a Flask app for this task
        app = Flask(__name__)
        app.config.from_object(LocalDevelopmentConfig)
        
        # Explicitly set the database URI
        BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.sqlite3')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
        
        db.init_app(app)
        
        with app.app_context():
            # Define what "inactive" means - users who haven't logged in for more than 2 days
            cutoff_date = datetime.utcnow() - timedelta(days=2)
            
            # Find inactive users
            inactive_users = Users.query.filter(
                Users.is_active == True,
                or_(
                    Users.last_login == None,
                    Users.last_login < cutoff_date
                )
            ).all()
            
            logger.info(f"Found {len(inactive_users)} inactive users to send reminders to")
            
            # Get available quizzes (active quizzes created in the last 7 days)
            recent_cutoff = datetime.utcnow() - timedelta(days=7)
            recent_quizzes = db.session.query(
                Quizzes, Chapters, Subjects
            ).join(
                Chapters, Quizzes.chapter_id == Chapters.id
            ).join(
                Subjects, Chapters.subject_id == Subjects.id
            ).filter(
                Quizzes.is_active == True
            ).all()
            
            available_quizzes = [
                {
                    'id': quiz.id,
                    'name': quiz.name,
                    'subject': subject.name,
                    'chapter': chapter.name
                }
                for quiz, chapter, subject in recent_quizzes
            ]
            
            # Send emails to each inactive user
            success_count = 0
            for user in inactive_users:
                try:
                    # Send reminder email
                    result = send_daily_reminder(
                        user_email=user.email,
                        user_name=user.username,
                        available_quizzes=available_quizzes
                    )
                    
                    if result:
                        success_count += 1
                        logger.info(f"Successfully sent reminder to {user.email}")
                    else:
                        logger.warning(f"Failed to send reminder to {user.email}")
                        
                    # Optional: Update last reminder sent
                    if hasattr(user, 'last_reminder_sent'):
                        user.last_reminder_sent = datetime.utcnow()
                        db.session.commit()
                        
                except Exception as e:
                    logger.error(f"Error sending reminder to {user.email}: {str(e)}")
            
            return {
                'status': 'completed',
                'message': f'Daily reminders sent to {success_count} of {len(inactive_users)} users',
                'timestamp': datetime.utcnow().isoformat()
            }
    
    except Exception as e:
        logger.error(f"Failed to send daily reminders: {str(e)}")
        raise

@celery.task(bind=True)
def send_monthly_reports(self):
    """
    Send monthly activity reports to all users
    """
    try:
        from flask import Flask
        from application.config import LocalDevelopmentConfig
        from application.simple_email import send_monthly_report
        
        # Create a Flask app for this task
        app = Flask(__name__)
        app.config.from_object(LocalDevelopmentConfig)
        
        # Explicitly set the database URI
        BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.sqlite3')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
        
        db.init_app(app)
        
        with app.app_context():
            # Calculate the previous month's date range
            today = datetime.utcnow()
            first_day_of_current_month = datetime(today.year, today.month, 1)
            last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
            first_day_of_previous_month = datetime(last_day_of_previous_month.year, last_day_of_previous_month.month, 1)
            
            previous_month_name = first_day_of_previous_month.strftime('%B')
            previous_month_year = first_day_of_previous_month.year
            
            logger.info(f"Generating monthly reports for {previous_month_name} {previous_month_year}")
            
            # Get all active users
            active_users = Users.query.filter_by(is_active=True).all()
            
            # Generate and send reports for each user
            success_count = 0
            for user in active_users:
                try:
                    # Get quiz attempts for the previous month
                    user_scores = db.session.query(Scores).filter(
                        Scores.user_id == user.id,
                        Scores.time_stamp_of_attempt >= first_day_of_previous_month,
                        Scores.time_stamp_of_attempt < first_day_of_current_month
                    ).all()
                    
                    # Calculate statistics
                    total_quizzes = len(user_scores)
                    
                    if total_quizzes > 0:
                        average_score = sum(score.percentage for score in user_scores) / total_quizzes
                        best_score = max((score.percentage for score in user_scores), default=0)
                    else:
                        average_score = 0
                        best_score = 0
                    
                    # Prepare report data
                    report_data = {
                        'month': previous_month_name,
                        'year': previous_month_year,
                        'total_quizzes': total_quizzes,
                        'average_score': average_score,
                        'best_score': best_score
                    }
                    
                    # Send monthly report email
                    result = send_monthly_report(
                        user_email=user.email,
                        user_name=user.username,
                        report_data=report_data
                    )
                    
                    if result:
                        success_count += 1
                        logger.info(f"Successfully sent monthly report to {user.email}")
                    else:
                        logger.warning(f"Failed to send monthly report to {user.email}")
                
                except Exception as e:
                    logger.error(f"Error generating monthly report for {user.email}: {str(e)}")
            
            return {
                'status': 'completed',
                'message': f'Monthly reports sent to {success_count} of {len(active_users)} users',
                'month': previous_month_name,
                'year': previous_month_year,
                'timestamp': datetime.utcnow().isoformat()
            }
    
    except Exception as e:
        logger.error(f"Failed to send monthly reports: {str(e)}")
        raise