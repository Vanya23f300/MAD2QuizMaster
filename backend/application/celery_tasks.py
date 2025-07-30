from main import app, celery, mail, db
from application.models import Users, Quizzes, Chapters, Subjects, Scores
from flask_mail import Message
from datetime import datetime, timedelta
from sqlalchemy import desc, func, and_, or_
import csv
import os
import logging
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

# Create a function to get a safe session for worker processes
def get_safe_session():
    # Get database URI from app config
    with app.app_context():
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    
    # Create a new engine and session just for this worker task
    engine = create_engine(db_uri, connect_args={'check_same_thread': False, 'timeout': 30})
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Session = scoped_session(session_factory)
    return Session()

@celery.task(bind=True)
def generate_user_quiz_export(self, user_id, filename):
    """
    Generate CSV export of user's quiz attempts
    """
    try:
        logger.info(f"Starting quiz export for user {user_id}")
        
        # Create a safe database session (like other tasks)
        session = get_safe_session()
        
        try:
            # First get the user's email - since Scores.user_id contains emails, not IDs
            user = session.query(Users).filter(Users.id == user_id).first()
            if not user:
                logger.error(f"User with ID {user_id} not found")
                return {
                    'status': 'completed',
                    'message': 'User not found',
                    'filename': None
                }
            
            user_email = user.email
            logger.info(f"Found user {user.username} with email {user_email}")
            
            # Get all quiz attempts by the user with related data
            # NOTE: Scores.user_id contains email addresses, not user IDs
            scores = session.query(Scores, Quizzes, Chapters, Subjects)\
                .join(Quizzes, Scores.quiz_id == Quizzes.id)\
                .join(Chapters, Quizzes.chapter_id == Chapters.id)\
                .join(Subjects, Chapters.subject_id == Subjects.id)\
                .filter(Scores.user_id == user_email)\
                .order_by(Scores.time_stamp_of_attempt.desc())\
                .all()
            
            if not scores:
                logger.warning(f"No quiz attempts found for user {user_id} (email: {user_email})")
                return {
                    'status': 'completed',
                    'message': 'No quiz attempts found',
                    'filename': None
                }
            
            logger.info(f"Found {len(scores)} quiz attempts for user {user_id}")
            
            # Use consistent path with API (app.instance_path/exports)
            with app.app_context():
                export_dir = os.path.join(app.instance_path, 'exports')
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
                        
                        # Update progress (only if running in Celery context)
                        if hasattr(self, 'request') and self.request.id:
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
        finally:
            # Always close the session
            session.close()
            
    except Exception as e:
        logger.error(f"Export failed for user {user_id}: {str(e)}")
        raise

@celery.task
def send_daily_reminders():
    """
    Send daily reminders to all active users
    """
    try:
        # Create a safe database session
        session = get_safe_session()
        
        try:
            # Find all active users
            active_users = session.query(Users).filter(
                Users.is_active == True
            ).all()
            
            logger.info(f"Found {len(active_users)} active users to send reminders to")
            
            # Get available quizzes (active quizzes created in the last 7 days)
            recent_quizzes = session.query(
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
            
            # Send emails to each active user
            success_count = 0
            for user in active_users:
                try:
                    # Prepare email content
                    subject = "Daily Quiz Reminder - QuizMaster"
                    
                    # Create quiz list HTML
                    quiz_list_html = ""
                    for quiz in available_quizzes[:5]:  # Show first 5 quizzes
                        quiz_list_html += f"""
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;">
                                <strong>{quiz['name']}</strong><br>
                                <small style="color: #666;">{quiz['subject']} - {quiz['chapter']}</small>
                            </td>
                        </tr>"""
                    
                    # HTML email template
                    html_body = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Daily Quiz Reminder</title>
                    </head>
                    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                            <h1 style="margin: 0; font-size: 28px; font-weight: 300;">📚 QuizMaster</h1>
                            <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Daily Quiz Reminder</p>
                        </div>
                        
                        <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                            <h2 style="color: #4a5568; margin-top: 0;">Hello {user.username}! 👋</h2>
                            
                            <p style="font-size: 16px; color: #4a5568; margin-bottom: 25px;">
                                This is a friendly reminder to visit QuizMaster and challenge yourself with some quizzes!
                            </p>
                            
                            <div style="background: #f7fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                                <h3 style="color: #2d3748; margin-top: 0; font-size: 18px;">🎯 Available Quizzes</h3>
                                <table style="width: 100%; border-collapse: collapse;">
                                    {quiz_list_html}
                                </table>
                            </div>
                            
                            <div style="background: #e6fffa; border-left: 4px solid #38b2ac; padding: 15px; margin: 20px 0;">
                                <p style="margin: 0; color: #234e52;">
                                    <strong>📊 Total Available:</strong> {len(available_quizzes)} quizzes ready for you to attempt!
                                </p>
                            </div>
                            
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="#" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; font-weight: 500; display: inline-block; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);">
                                    🚀 Start Quiz Now
                                </a>
                            </div>
                            
                            <div style="border-top: 1px solid #e2e8f0; padding-top: 20px; margin-top: 30px; text-align: center;">
                                <p style="color: #718096; font-size: 14px; margin: 0;">
                                    Best regards,<br>
                                    <strong style="color: #4a5568;">QuizMaster Team</strong>
                                </p>
                            </div>
                        </div>
                        
                        <div style="text-align: center; margin-top: 20px; color: #a0aec0; font-size: 12px;">
                            <p>© 2025 QuizMaster. Keep learning, keep growing! 🌟</p>
                        </div>
                    </body>
                    </html>
                    """
                    
                    # Plain text fallback
                    plain_text = f"""Hello {user.username},

This is a reminder to visit QuizMaster and take some quizzes!

Available Quizzes:
"""
                    for quiz in available_quizzes[:5]:
                        plain_text += f"- {quiz['name']} ({quiz['subject']} - {quiz['chapter']})\n"
                    
                    plain_text += f"""

We have {len(available_quizzes)} quizzes available for you to attempt.

Visit QuizMaster now and challenge yourself!

Best regards,
QuizMaster Team"""

                    # Send email using Flask-Mail
                    with app.app_context():  # Need app context for mail
                        msg = Message(
                            subject=subject,
                            recipients=[user.email],
                            body=plain_text,
                            html=html_body
                        )
                        mail.send(msg)
                    
                        success_count += 1
                        logger.info(f"Successfully sent reminder to {user.email}")
                        
                    # Optional: Update last reminder sent
                    if hasattr(user, 'last_reminder_sent'):
                        user.last_reminder_sent = datetime.utcnow()
                        session.commit()
                    
                except Exception as e:
                    logger.error(f"Error sending reminder to {user.email}: {str(e)}")
            
            return {
                'status': 'completed',
                'message': f'Daily reminders sent to {success_count} of {len(active_users)} users',
                'timestamp': datetime.utcnow().isoformat()
            }
        finally:
            # Always close the session
            session.close()
        
    except Exception as e:
        logger.error(f"Failed to send daily reminders: {str(e)}")
        raise

@celery.task
def send_monthly_reports():
    """
    Send monthly activity reports to all users
    """
    try:
        # Create a safe database session
        session = get_safe_session()
        
        try:
            # Calculate the previous month's date range
            today = datetime.utcnow()
            first_day_of_current_month = datetime(today.year, today.month, 1)
            last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
            first_day_of_previous_month = datetime(last_day_of_previous_month.year, last_day_of_previous_month.month, 1)
            
            previous_month_name = first_day_of_previous_month.strftime('%B')
            previous_month_year = first_day_of_previous_month.year
            
            logger.info(f"Generating monthly reports for {previous_month_name} {previous_month_year}")
            
            # Test simple count query first
            try:
                user_count = session.query(Users).count()
                logger.info(f"Worker process - SQLAlchemy Users count: {user_count}")
            except Exception as e:
                logger.error(f"Worker process - SQLAlchemy count query failed: {e}")
                raise
            
            # Get all active users
            active_users = session.query(Users).filter_by(is_active=True).all()
            
            # Generate and send reports for each user
            success_count = 0
            for user in active_users:
                try:
                    # Get quiz attempts for the previous month
                    user_scores = session.query(Scores).filter(
                        Scores.user_id == user.id,
                        Scores.time_stamp_of_attempt >= first_day_of_previous_month,
                        Scores.time_stamp_of_attempt < first_day_of_current_month
                    ).all()
                    
                    # Calculate statistics
                    total_quizzes = len(user_scores)
                    
                    if total_quizzes > 0:
                        average_score = sum(score.percentage for score in user_scores) / total_quizzes
                        best_score = max((score.percentage for score in user_scores), default=0)
                        passed_quizzes = sum(1 for score in user_scores if score.passed)
                    else:
                        average_score = 0
                        best_score = 0
                        passed_quizzes = 0
                    
                    # Prepare email content
                    subject = f"Monthly Quiz Report - {previous_month_name} {previous_month_year}"
                    
                    # Calculate pass rate and performance message
                    if total_quizzes > 0:
                        pass_rate = (passed_quizzes / total_quizzes) * 100
                        
                        if average_score >= 80:
                            performance_message = "🎉 Excellent performance! Keep up the great work!"
                            performance_color = "#10b981"
                            performance_bg = "#d1fae5"
                        elif average_score >= 60:
                            performance_message = "👍 Good job! There's room for improvement."
                            performance_color = "#f59e0b"
                            performance_bg = "#fef3c7"
                        else:
                            performance_message = "📚 Consider reviewing the topics and practicing more."
                            performance_color = "#ef4444"
                            performance_bg = "#fee2e2"
                    else:
                        pass_rate = 0
                        performance_message = "We noticed you didn't attempt any quizzes this month. Why not give it a try?"
                        performance_color = "#6b7280"
                        performance_bg = "#f9fafb"
                    
                    # HTML email template
                    html_body = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Monthly Quiz Report</title>
                    </head>
                    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                            <h1 style="margin: 0; font-size: 28px; font-weight: 300;">📊 QuizMaster</h1>
                            <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Monthly Performance Report</p>
                            <p style="margin: 5px 0 0 0; font-size: 20px; font-weight: 500;">{previous_month_name} {previous_month_year}</p>
                        </div>
                        
                        <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                            <h2 style="color: #4a5568; margin-top: 0;">Dear {user.username}! 👋</h2>
                            
                            <p style="font-size: 16px; color: #4a5568; margin-bottom: 25px;">
                                Here is your monthly quiz performance report for <strong>{previous_month_name} {previous_month_year}</strong>:
                            </p>
                            
                            <div style="background: #f7fafc; padding: 25px; border-radius: 12px; margin: 25px 0;">
                                <h3 style="color: #2d3748; margin-top: 0; font-size: 20px; text-align: center; margin-bottom: 20px;">📈 Quiz Statistics</h3>
                                
                                <div style="display: flex; flex-wrap: wrap; gap: 15px;">
                                    <div style="flex: 1; min-width: 140px; background: white; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #e2e8f0;">
                                        <div style="font-size: 24px; font-weight: bold; color: #667eea;">{total_quizzes}</div>
                                        <div style="font-size: 12px; color: #718096; margin-top: 5px;">Total Attempted</div>
                                    </div>
                                    
                                    <div style="flex: 1; min-width: 140px; background: white; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #e2e8f0;">
                                        <div style="font-size: 24px; font-weight: bold; color: #10b981;">{passed_quizzes}</div>
                                        <div style="font-size: 12px; color: #718096; margin-top: 5px;">Quizzes Passed</div>
                                    </div>
                                    
                                    <div style="flex: 1; min-width: 140px; background: white; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #e2e8f0;">
                                        <div style="font-size: 24px; font-weight: bold; color: #f59e0b;">{average_score:.1f}%</div>
                                        <div style="font-size: 12px; color: #718096; margin-top: 5px;">Average Score</div>
                                    </div>
                                    
                                    <div style="flex: 1; min-width: 140px; background: white; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #e2e8f0;">
                                        <div style="font-size: 24px; font-weight: bold; color: #8b5cf6;">{best_score:.1f}%</div>
                                        <div style="font-size: 12px; color: #718096; margin-top: 5px;">Best Score</div>
                                    </div>
                                    
                                    {f'<div style="flex: 1; min-width: 140px; background: white; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #e2e8f0;"><div style="font-size: 24px; font-weight: bold; color: #06b6d4;">{pass_rate:.1f}%</div><div style="font-size: 12px; color: #718096; margin-top: 5px;">Pass Rate</div></div>' if total_quizzes > 0 else ""}
                                </div>
                            </div>
                            
                            <div style="background: {performance_bg}; border-left: 4px solid {performance_color}; padding: 20px; margin: 25px 0; border-radius: 8px;">
                                <p style="margin: 0; color: {performance_color}; font-weight: 500; font-size: 16px;">
                                    {performance_message}
                                </p>
                            </div>
                            
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="#" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; font-weight: 500; display: inline-block; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);">
                                    📚 Continue Learning
                                </a>
                            </div>
                            
                            <div style="border-top: 1px solid #e2e8f0; padding-top: 20px; margin-top: 30px; text-align: center;">
                                <p style="color: #718096; font-size: 14px; margin: 0;">
                                    Best regards,<br>
                                    <strong style="color: #4a5568;">QuizMaster Team</strong>
                                </p>
                            </div>
                        </div>
                        
                        <div style="text-align: center; margin-top: 20px; color: #a0aec0; font-size: 12px;">
                            <p>© 2025 QuizMaster. Keep learning, keep growing! 🌟</p>
                        </div>
                    </body>
                    </html>
                    """
                    
                    # Plain text fallback
                    plain_text = f"""Dear {user.username},

Here is your monthly quiz performance report for {previous_month_name} {previous_month_year}:

📊 QUIZ STATISTICS:
- Total Quizzes Attempted: {total_quizzes}
- Quizzes Passed: {passed_quizzes}
- Average Score: {average_score:.1f}%
- Best Score: {best_score:.1f}%
"""
                    if total_quizzes > 0:
                        plain_text += f"- Pass Rate: {pass_rate:.1f}%\n\n"
                        
                        if average_score >= 80:
                            plain_text += "🎉 Excellent performance! Keep up the great work!\n"
                        elif average_score >= 60:
                            plain_text += "👍 Good job! There's room for improvement.\n"
                        else:
                            plain_text += "📚 Consider reviewing the topics and practicing more.\n"
                    else:
                        plain_text += "We noticed you didn't attempt any quizzes this month. Why not give it a try?\n"
                    
                    plain_text += """
Visit QuizMaster to continue your learning journey!

Best regards,
QuizMaster Team"""

                    # Send monthly report email using Flask-Mail
                    with app.app_context():  # Need app context for mail
                        msg = Message(
                            subject=subject,
                            recipients=[user.email],
                            body=plain_text,
                            html=html_body
                        )
                        mail.send(msg)
                    
                    success_count += 1
                    logger.info(f"Successfully sent monthly report to {user.email}")
                    
                except Exception as e:
                    logger.error(f"Error generating monthly report for {user.email}: {str(e)}")
            
            return {
                'status': 'completed',
                'message': f'Monthly reports sent to {success_count} of {len(active_users)} users',
                'month': previous_month_name,
                'year': previous_month_year,
                'timestamp': datetime.utcnow().isoformat()
            }
        finally:
            # Always close the session
            session.close()
        
    except Exception as e:
        logger.error(f"Failed to send monthly reports: {str(e)}")
        raise 