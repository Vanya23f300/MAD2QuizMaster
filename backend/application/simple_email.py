from flask_mail import Mail, Message
from flask import current_app
import logging
import os

logger = logging.getLogger(__name__)

# Global Mail instance
mail = None

def init_mail(app):
    """Initialize Flask-Mail with app"""
    global mail
    
    # Ensure environment variables are loaded
    from dotenv import load_dotenv
    load_dotenv(override=True)
    
    # Log mail configuration for debugging
    logger.info("Initializing Mail with the following configuration:")
    logger.info(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    logger.info(f"MAIL_PORT: {app.config.get('MAIL_PORT')}")
    logger.info(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    logger.info(f"MAIL_USE_SSL: {app.config.get('MAIL_USE_SSL')}")
    logger.info(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    logger.info(f"MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER')}")
    
    # Initialize Mail
    mail = Mail(app)
    return mail

def send_simple_email(to_email, subject, body):
    """Send a simple plain text email"""
    try:
        if not mail:
            logger.error("Mail not initialized")
            return False
            
        # Get configuration values
        sender = current_app.config.get('MAIL_DEFAULT_SENDER')
        username = current_app.config.get('MAIL_USERNAME')
        
        logger.info(f"Sending email using sender: {sender}")
        logger.info(f"SMTP username: {username}")
        
        # Create message
        msg = Message(
            subject=subject,
            recipients=[to_email],
            body=body,
            sender=sender
        )
        
        # Send email
        mail.send(msg)
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False

def send_daily_reminder(user_email, user_name, available_quizzes):
    """Send daily reminder email"""
    subject = "QuizMaster Daily Reminder"
    
    # Create simple quiz list
    quiz_list = ""
    for quiz in available_quizzes[:5]:  # Show max 5 quizzes
        quiz_list += f"- {quiz['name']} ({quiz['subject']})\n"
    
    if not quiz_list:
        quiz_list = "- No new quizzes available\n"
    
    body = f"""Hi {user_name}!

You haven't visited QuizMaster in a while.

Available quizzes:
{quiz_list}

Visit: http://localhost:8080/login

Thanks,
QuizMaster Team"""
    
    return send_simple_email(user_email, subject, body)

def send_monthly_report(user_email, user_name, report_data):
    """Send monthly report email"""
    subject = f"QuizMaster Monthly Report - {report_data['month']} {report_data['year']}"
    
    body = f"""Monthly Report - {report_data['month']} {report_data['year']}

Hi {user_name},

Your quiz activity:
- Quizzes taken: {report_data['total_quizzes']}
- Average score: {report_data['average_score']:.1f}%
- Best score: {report_data['best_score']:.1f}%

Keep it up!

QuizMaster Team"""
    
    return send_simple_email(user_email, subject, body)

def test_email_setup(test_email):
    """Test email configuration"""
    subject = "QuizMaster Email Test"
    body = """This is a test email from QuizMaster.

If you received this, your email configuration is working correctly!

QuizMaster Team"""
    
    return send_simple_email(test_email, subject, body) 