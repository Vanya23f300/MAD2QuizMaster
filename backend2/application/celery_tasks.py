from celery import Celery
from application.celery_config import celery
from application.database import db
from application.models import Users, Scores, Quizzes, Chapters, Subjects
from flask import current_app
from datetime import datetime, timedelta, date
import os
import logging
import csv
import io
import requests
import json

logger = logging.getLogger(__name__)

@celery.task
def send_daily_reminders():
    """
    Scheduled Job - Daily reminders to users
    Check if users haven't visited or new quizzes are created
    Send reminders via email/webhook
    """
    try:
        logger.info("Starting daily reminders task")
        
        # Get all active users who haven't logged in today
        today = date.today()
        users_to_remind = Users.query.filter(
            Users.is_admin == False,
            Users.is_active == True,
            db.or_(
                Users.last_login.is_(None),
                db.func.date(Users.last_login) < today
            )
        ).all()
        
        # Get recent quizzes (created in last 7 days)
        week_ago = today - timedelta(days=7)
        recent_quizzes = Quizzes.query.filter(
            Quizzes.created_date >= week_ago
        ).count()
        
        reminder_count = 0
        for user in users_to_remind:
            try:
                # Check if user has any pending quizzes
                user_subjects = get_user_relevant_subjects(user.id)
                
                message = f"""
                Hi {user.username},
                
                You haven't visited the Quiz Master platform recently. 
                """
                
                if recent_quizzes > 0:
                    message += f"\nWe have {recent_quizzes} new quiz(es) that might interest you!"
                
                message += f"""
                
                Visit now to attempt quizzes and improve your knowledge!
                
                Best regards,
                Quiz Master Team
                """
                
                # Send reminder (email or webhook)
                success = send_reminder_notification(user, message)
                if success:
                    reminder_count += 1
                    
            except Exception as e:
                logger.error(f"Failed to send reminder to user {user.email}: {str(e)}")
                continue
        
        logger.info(f"Daily reminders sent to {reminder_count} users")
        return {
            'status': 'completed',
            'reminders_sent': reminder_count,
            'total_users_checked': len(users_to_remind)
        }
        
    except Exception as e:
        logger.error(f"Daily reminders task failed: {str(e)}")
        return {'status': 'failed', 'error': str(e)}

@celery.task
def send_monthly_activity_reports():
    """
    Scheduled Job - Monthly Activity Report
    Generate and send monthly reports to users via email
    """
    try:
        logger.info("Starting monthly activity reports task")
        
        # Get previous month date range
        today = date.today()
        first_day_current_month = today.replace(day=1)
        last_day_prev_month = first_day_current_month - timedelta(days=1)
        first_day_prev_month = last_day_prev_month.replace(day=1)
        
        # Get all active users
        active_users = Users.query.filter(
            Users.is_admin == False,
            Users.is_active == True
        ).all()
        
        reports_sent = 0
        for user in active_users:
            try:
                # Generate user's monthly report
                report_data = generate_monthly_report(user.id, first_day_prev_month, last_day_prev_month)
                
                if report_data['quizzes_taken'] > 0:
                    # Send report via email
                    success = send_monthly_report_email(user, report_data, last_day_prev_month.strftime('%B %Y'))
                    if success:
                        reports_sent += 1
                        
            except Exception as e:
                logger.error(f"Failed to send monthly report to user {user.email}: {str(e)}")
                continue
        
        logger.info(f"Monthly reports sent to {reports_sent} users")
        return {
            'status': 'completed',
            'reports_sent': reports_sent,
            'total_users_checked': len(active_users),
            'month': last_day_prev_month.strftime('%B %Y')
        }
        
    except Exception as e:
        logger.error(f"Monthly reports task failed: {str(e)}")
        return {'status': 'failed', 'error': str(e)}

@celery.task
def generate_user_csv_export(user_id, export_type='quiz_details'):
    """
    User Triggered Async Job - Generate CSV export
    This makes CSV export asynchronous for better user experience
    """
    try:
        logger.info(f"Starting CSV export for user {user_id}, type: {export_type}")
        
        user = Users.query.get(user_id)
        if not user:
            return {'status': 'failed', 'error': 'User not found'}
        
        if export_type == 'quiz_details':
            file_path = generate_quiz_details_csv(user)
        else:
            return {'status': 'failed', 'error': 'Invalid export type'}
        
        # Optionally, send notification to user that export is ready
        send_export_ready_notification(user, file_path)
        
        return {
            'status': 'completed',
            'file_path': file_path,
            'user_id': user_id,
            'export_type': export_type
        }
        
    except Exception as e:
        logger.error(f"CSV export task failed for user {user_id}: {str(e)}")
        return {'status': 'failed', 'error': str(e)}

@celery.task
def cleanup_old_export_files():
    """
    Cleanup old export files to save disk space
    """
    try:
        logger.info("Starting cleanup of old export files")
        
        # Define export directory (you might want to create this)
        export_dir = os.path.join(os.getcwd(), 'exports')
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        
        # Delete files older than 7 days
        cutoff_date = datetime.now() - timedelta(days=7)
        deleted_count = 0
        
        for filename in os.listdir(export_dir):
            file_path = os.path.join(export_dir, filename)
            if os.path.isfile(file_path):
                file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_modified < cutoff_date:
                    os.remove(file_path)
                    deleted_count += 1
        
        logger.info(f"Cleaned up {deleted_count} old export files")
        return {
            'status': 'completed',
            'files_deleted': deleted_count
        }
        
    except Exception as e:
        logger.error(f"Cleanup task failed: {str(e)}")
        return {'status': 'failed', 'error': str(e)}

# Helper functions
def get_user_relevant_subjects(user_id):
    """Get subjects relevant to user based on their quiz history"""
    return db.session.query(Subjects).join(Chapters).join(Quizzes).join(Scores).filter(
        Scores.user_id == user_id
    ).distinct().all()

def send_reminder_notification(user, message):
    """Send reminder notification via webhook or console log"""
    try:
        # For development, just log the message
        # In production, you can implement email/webhook sending
        logger.info(f"Reminder for {user.email}: {message}")
        return True
    except Exception as e:
        logger.error(f"Failed to send reminder notification: {str(e)}")
        return False

def generate_monthly_report(user_id, start_date, end_date):
    """Generate monthly activity report data for a user"""
    try:
        # Get quiz attempts in the date range
        scores = Scores.query.filter(
            Scores.user_id == user_id,
            Scores.time_stamp_of_attempt >= start_date,
            Scores.time_stamp_of_attempt <= end_date + timedelta(days=1)
        ).all()
        
        if not scores:
            return {
                'quizzes_taken': 0,
                'average_score': 0,
                'best_score': 0,
                'total_time_spent': 0,
                'subjects_covered': 0
            }
        
        # Calculate statistics
        total_score = sum(score.percentage for score in scores if score.percentage)
        average_score = total_score / len(scores) if scores else 0
        best_score = max((score.percentage for score in scores if score.percentage), default=0)
        total_time = sum(score.time_taken for score in scores if score.time_taken)
        
        # Get unique subjects
        subject_ids = set()
        for score in scores:
            quiz = Quizzes.query.get(score.quiz_id)
            if quiz:
                chapter = Chapters.query.get(quiz.chapter_id)
                if chapter:
                    subject_ids.add(chapter.subject_id)
        
        return {
            'quizzes_taken': len(scores),
            'average_score': round(average_score, 2),
            'best_score': round(best_score, 2),
            'total_time_spent': total_time or 0,
            'subjects_covered': len(subject_ids)
        }
        
    except Exception as e:
        logger.error(f"Failed to generate monthly report for user {user_id}: {str(e)}")
        return {'quizzes_taken': 0}

def send_monthly_report_email(user, report_data, month_name):
    """Send monthly activity report via log (for development)"""
    try:
        message = f"""
        Monthly Report for {user.username} - {month_name}:
        Quizzes Taken: {report_data['quizzes_taken']}
        Average Score: {report_data['average_score']:.1f}%
        Best Score: {report_data['best_score']:.1f}%
        Subjects Covered: {report_data['subjects_covered']}
        """
        
        logger.info(f"Monthly report for {user.email}: {message}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send monthly report email: {str(e)}")
        return False

def generate_quiz_details_csv(user):
    """Generate CSV file for user's quiz details"""
    try:
        # Create exports directory
        export_dir = os.path.join(os.getcwd(), 'exports')
        os.makedirs(export_dir, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"quiz_details_{user.username}_{timestamp}.csv"
        file_path = os.path.join(export_dir, filename)
        
        # Get user's quiz data
        scores = db.session.query(Scores, Quizzes, Chapters, Subjects)\
            .join(Quizzes, Scores.quiz_id == Quizzes.id)\
            .join(Chapters, Quizzes.chapter_id == Chapters.id)\
            .join(Subjects, Chapters.subject_id == Subjects.id)\
            .filter(Scores.user_id == user.id)\
            .order_by(Scores.time_stamp_of_attempt.desc())\
            .all()
        
        # Write CSV
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Headers
            writer.writerow([
                'Quiz ID', 'Quiz Name', 'Chapter', 'Subject',
                'Date Attempted', 'Score', 'Percentage', 'Passed'
            ])
            
            # Data rows
            for score, quiz, chapter, subject in scores:
                writer.writerow([
                    quiz.id,
                    quiz.name,
                    chapter.name,
                    subject.name,
                    score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M'),
                    f"{score.total_scored}/{score.total_possible_score}",
                    f"{score.percentage:.1f}%",
                    'Yes' if score.passed else 'No'
                ])
        
        return file_path
        
    except Exception as e:
        logger.error(f"Failed to generate CSV for user {user.email}: {str(e)}")
        return None

def send_export_ready_notification(user, file_path):
    """Send notification when export is ready (via log for development)"""
    try:
        filename = os.path.basename(file_path)
        logger.info(f"Export ready for {user.email}: {filename}")
        return True
    except Exception as e:
        logger.error(f"Failed to send export notification: {str(e)}")
        return False