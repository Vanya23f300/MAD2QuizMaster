#!/usr/bin/env python
"""
Test script to manually trigger scheduled tasks
"""
import os
import sys
import argparse
from datetime import datetime

def setup_flask_app():
    """Initialize Flask app and setup environment"""
    from flask import Flask
    from dotenv import load_dotenv
    from application.config import LocalDevelopmentConfig
    from application.database import db
    from application.simple_email import init_mail
    
    # Load environment variables
    load_dotenv(override=True)
    
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    
    # Init database
    db.init_app(app)
    
    # Init mail
    mail = init_mail(app)
    
    return app

def test_daily_reminders(app):
    """Test sending daily reminders"""
    from application.celery_tasks import send_daily_reminders
    
    print(f"[{datetime.now()}] Manually triggering daily reminders task...")
    
    with app.app_context():
        # Run the task directly (not through Celery)
        result = send_daily_reminders()
        print(f"Result: {result}")
        
    print("Daily reminders test complete!")

def test_monthly_reports(app):
    """Test sending monthly reports"""
    from application.celery_tasks import send_monthly_reports
    
    print(f"[{datetime.now()}] Manually triggering monthly reports task...")
    
    with app.app_context():
        # Run the task directly (not through Celery)
        result = send_monthly_reports()
        print(f"Result: {result}")
        
    print("Monthly reports test complete!")

def test_email_config(app, test_email):
    """Test email configuration"""
    from application.simple_email import test_email_setup
    
    print(f"[{datetime.now()}] Testing email configuration...")
    print(f"Sending test email to: {test_email}")
    
    with app.app_context():
        result = test_email_setup(test_email)
        
    if result:
        print("✅ Email sent successfully!")
    else:
        print("❌ Failed to send email. Check the logs.")
        
    print("Email configuration test complete!")

def main():
    parser = argparse.ArgumentParser(description="Test scheduler functionality")
    parser.add_argument("--task", choices=["reminders", "reports", "email"],
                      help="Task to test (reminders, reports, or email)")
    parser.add_argument("--email", help="Email to use for testing")
    
    args = parser.parse_args()
    
    if not args.task:
        parser.print_help()
        return 1
    
    try:
        app = setup_flask_app()
        
        if args.task == "reminders":
            test_daily_reminders(app)
        elif args.task == "reports":
            test_monthly_reports(app)
        elif args.task == "email":
            if not args.email:
                print("Error: --email is required for email testing")
                return 1
            test_email_config(app, args.email)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main()) 