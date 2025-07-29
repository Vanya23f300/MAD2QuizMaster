# Ultra-Simple Scheduled Tasks Plan

## Overview
**GOAL: Implement with MINIMAL changes and MAXIMUM simplicity**

Two basic features:
1. **Daily Email Reminders** - Simple text emails for inactive users
2. **Monthly Reports** - Basic email with quiz stats

**🎯 ULTRA-SIMPLE PRINCIPLE: Use what we have, add almost nothing!**

---

## 📧 Feature 1: Daily Email Reminders

### **What It Does**
- Sends plain text email to users who haven't logged in for 3+ days
- Lists available quizzes
- Runs once per day at 6 PM

### **How It Works (Super Simple)**
1. Check `Users.last_login` (field already exists!)
2. Find users inactive for 3+ days
3. Send basic text email
4. Done!

### **Database Changes**
```sql
-- NO NEW TABLES! Just use existing Users table
-- Maybe add ONE optional field:
ALTER TABLE Users ADD COLUMN last_reminder_sent DATE;
```

### **Email Template (Plain Text)**
```
Hi [USER_NAME],

You haven't visited QuizMaster in a while!

Available quizzes:
- Quiz 1
- Quiz 2 
- Quiz 3

Visit: http://localhost:8080/login

Thanks,
QuizMaster Team
```

---

## 📊 Feature 2: Monthly Reports

### **What It Does**
- Sends basic email with quiz stats on 1st of month
- Plain text format
- Simple statistics only

### **Database Changes**
```sql
-- NO NEW TABLES! Use existing data
-- Query existing Scores table for stats
```

### **Email Template (Plain Text)**
```
Monthly Report - [MONTH] [YEAR]

Hi [USER_NAME],

Your quiz activity:
- Quizzes taken: 5
- Average score: 78%
- Best score: 95%

Keep it up!

QuizMaster Team
```

---

## 🔧 Ultra-Simple Implementation

### **Option 1: Add to Flask App (Simplest)**
```python
# In main.py - add background thread
import threading
import time
from datetime import datetime, timedelta

def daily_reminder_job():
    while True:
        now = datetime.now()
        if now.hour == 18:  # 6 PM
            send_daily_reminders()
        time.sleep(3600)  # Check every hour

# Start background thread when app starts
thread = threading.Thread(target=daily_reminder_job)
thread.daemon = True
thread.start()
```

### **Option 2: Use Python Schedule Library (Alternative)**
```python
import schedule
import time

def job():
    send_daily_reminders()

schedule.every().day.at("18:00").do(job)
schedule.every().month.do(send_monthly_reports)

# Run in background
```

### **Option 3: Simple Celery Beat (If needed)**
```python
# Only 2 tasks, minimal config
@celery.task
def send_daily_reminders():
    # Simple email sending logic
    pass

@celery.task  
def send_monthly_reports():
    # Simple report generation
    pass
```

---

## 📝 Implementation Steps

### **Day 1: Daily Reminders (4-6 hours)**
1. Add `send_daily_reminders()` function
2. Query inactive users from existing `Users.last_login` 
3. Send plain text emails using existing Flask-Mail
4. Add simple scheduling (background thread or schedule)
5. Test

### **Day 2: Monthly Reports (4-6 hours)**  
1. Add `send_monthly_reports()` function
2. Query user stats from existing `Scores` table
3. Generate plain text email
4. Schedule for 1st of month
5. Test

### **Total Time: 1-2 days maximum**

---

## 🔧 Configuration (Minimal)

### **Use Existing Email Setup**
```python
# Use current Flask-Mail configuration
# No new environment variables needed
```

### **Dependencies**
```python
# Option 1: No new dependencies (use threading)
# Option 2: Add schedule==1.2.0 (if using schedule library)  
# Option 3: Use existing celery (if preferred)
```

---

## 💡 Core Functions (Ultra-Simple)

### **Daily Reminder Function**
```python
def send_daily_reminders():
    from datetime import datetime, timedelta
    from flask_mail import Message
    
    # Find inactive users (3+ days)
    cutoff = datetime.now() - timedelta(days=3)
    inactive_users = Users.query.filter(Users.last_login < cutoff).all()
    
    # Send simple email to each
    for user in inactive_users:
        send_simple_reminder_email(user.email, user.username)
```

### **Monthly Report Function**  
```python
def send_monthly_reports():
    from datetime import datetime
    
    # Get all users
    users = Users.query.all()
    
    # Generate simple stats for each
    for user in users:
        stats = get_simple_user_stats(user.id)
        send_simple_report_email(user.email, user.username, stats)
```

### **Email Sending (Reuse Existing)**
```python  
def send_simple_email(to_email, subject, body):
    # Use existing Flask-Mail setup
    msg = Message(subject, recipients=[to_email])
    msg.body = body
    mail.send(msg)
```

---

## 🎯 Success Criteria (Minimal)

- [ ] Daily emails sent to inactive users
- [ ] Monthly emails sent with basic stats  
- [ ] Uses existing database tables
- [ ] Uses existing email configuration
- [ ] No complex UI needed initially
- [ ] Works reliably

---

## 🚀 User Experience

### **No UI Changes Initially**
- Users automatically get reminders (no settings needed)
- Can add simple enable/disable later if needed

### **Progressive Enhancement**
- **Phase 1**: Just send emails (no user control)
- **Phase 2**: Add simple enable/disable toggle later
- **Phase 3**: Add time preferences later (if needed)

---

## 📈 Optional Enhancements (Later)

### **If Users Want More Control:**
1. Add simple checkbox: "Send me reminders" (default: yes)
2. Add basic time selection (default: 6 PM)  
3. Add unsubscribe link in emails

### **If Reports Need Enhancement:**
1. Add simple HTML formatting
2. Add more statistics
3. Add user ranking

---

## 🔍 Monitoring (Basic)

### **Simple Logging**
```python
import logging
logger = logging.getLogger(__name__)

def send_daily_reminders():
    try:
        # Send emails
        logger.info(f"Sent reminders to {count} users")
    except Exception as e:
        logger.error(f"Reminder error: {e}")
```

### **Basic Metrics**
- Count emails sent
- Log any errors
- Track in application logs

---

## 🎉 Why This Is Ultra-Simple

✅ **Uses existing database tables**
✅ **Uses existing email setup** 
✅ **No new dependencies required**
✅ **No UI changes needed initially**
✅ **Plain text emails (no HTML complexity)**
✅ **Simple background threading or basic scheduling**
✅ **Minimal code changes**
✅ **1-2 day implementation**
✅ **Easy to understand and debug**
✅ **Can enhance later if needed**

**This is the simplest possible implementation that still provides the core functionality!** 