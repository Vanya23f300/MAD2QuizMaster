#!/usr/bin/env python3
"""
Script to manually trigger Celery tasks for testing.
"""
import os
import sys
import time

# Ensure we're in the correct directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Add current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

# Import the tasks
from application.celery_tasks import send_monthly_reports, send_daily_reminders

if __name__ == "__main__":
    print("Triggering monthly reports task...")
    result1 = send_monthly_reports.delay()
    print(f"Monthly reports task ID: {result1.id}")
    
    # Wait for the first task to complete
    print("Waiting for monthly reports task to complete...")
    try:
        result1_value = result1.get(timeout=60)  # Wait up to 60 seconds
        print(f"Monthly reports completed: {result1_value}")
    except Exception as e:
        print(f"Monthly reports failed: {e}")
    
    print("\n" + "="*50)
    print("Now triggering daily reminders task...")
    
    result2 = send_daily_reminders.delay()
    print(f"Daily reminders task ID: {result2.id}")
    
    # Wait for the second task to complete
    print("Waiting for daily reminders task to complete...")
    try:
        result2_value = result2.get(timeout=60)  # Wait up to 60 seconds
        print(f"Daily reminders completed: {result2_value}")
    except Exception as e:
        print(f"Daily reminders failed: {e}")
    
    print("\nBoth tasks completed!")
    print("Check celery_worker.log for detailed execution logs.") 