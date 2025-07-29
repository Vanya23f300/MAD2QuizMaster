# Celery Scheduler Implementation Plan

## Overview
Implement scheduled tasks using Celery Beat for:
1. **Daily Email Reminders** - Send to inactive users
2. **Monthly Activity Reports** - Send monthly statistics via email

## Current Status
✅ **Already Working:**
- Celery worker running for CSV export
- Redis as message broker
- Email system configured and tested
- Basic Celery configuration in place

## Implementation Plan

### Phase 1: Celery Beat Setup

#### 1.1 Dependencies
- Add `celery[redis]` (already in requirements.txt)
- No additional dependencies needed

#### 1.2 Celery Configuration Updates
**File:** `application/celery_config.py`

Need to add back:
- Import `crontab` for scheduling
- Beat schedule configuration
- Task routing configuration

**Schedule Configuration:**
```python
# Daily reminders at 6 PM every day
'daily-reminders': {
    'task': 'application.celery_tasks.send_daily_reminders',
    'schedule': crontab(hour=18, minute=0),  # 6 PM daily
},

# Monthly reports on 1st of every month at 9 AM
'monthly-reports': {
    'task': 'application.celery_tasks.send_monthly_reports',
    'schedule': crontab(day_of_month=1, hour=9, minute=0),  # 1st of month, 9 AM
}
```

### Phase 2: Scheduled Tasks Implementation

#### 2.1 Daily Reminders Task
**File:** `application/celery_tasks.py`

**Function:** `send_daily_reminders()`

**Logic:**
1. Find users who haven't logged in recently (e.g., > 2 days)
2. Get available quizzes for each user
3. Send reminder email using `simple_email.py`
4. Update user's last reminder sent timestamp (optional)

**Database Queries:**
- Query `Users` table for inactive users
- Query `Quizzes` table for available quizzes
- Optional: Update `Users.last_reminder_sent` field

#### 2.2 Monthly Reports Task
**File:** `application/celery_tasks.py`

**Function:** `send_monthly_reports()`

**Logic:**
1. Get all active users
2. Calculate monthly statistics for each user:
   - Total quizzes taken
   - Average score
   - Best score
   - Ranking (optional)
3. Send monthly report email using `simple_email.py`

**Database Queries:**
- Query `Users` table for all users
- Query `QuizAttempts` table for monthly statistics
- Calculate aggregated data per user

### Phase 3: Database Schema (Optional)

#### 3.1 User Table Enhancement
**File:** `application/models.py`

**Optional columns to add:**
```python
# Add to Users model
last_reminder_sent = db.Column(db.DateTime, nullable=True)
email_preferences = db.Column(db.String(50), default='enabled')  # enabled/disabled
```

**Migration:** Simple ALTER TABLE commands

### Phase 4: Celery Beat Process

#### 4.1 Beat Scheduler Setup
**New Process Required:**
- Celery Beat scheduler (separate from worker)
- Runs alongside existing Celery worker
- Manages scheduled task execution

**Commands:**
```bash
# Start Celery Worker (existing)
celery -A application.celery_tasks worker --loglevel=info

# Start Celery Beat (new)
celery -A application.celery_tasks beat --loglevel=info
```

#### 4.2 Process Management Scripts
**Create scripts:**
- `start_celery_beat.sh` - Start beat scheduler
- `stop_celery_beat.sh` - Stop beat scheduler
- Update existing `start_celery.sh` to include beat option

### Phase 5: Testing Strategy

#### 5.1 Development Testing
1. **Immediate Testing:**
   - Manually trigger tasks using `celery call`
   - Test email sending functions
   - Verify database queries

2. **Schedule Testing:**
   - Use shorter intervals for testing (every minute)
   - Verify tasks execute at correct times
   - Check Celery Beat logs

#### 5.2 Production Testing
1. **Gradual Rollout:**
   - Start with daily reminders only
   - Add monthly reports after verification
   - Monitor email delivery and logs

### Phase 6: Configuration Management

#### 6.1 Environment Variables
**File:** `.env`

**Add configuration:**
```
# Scheduler settings
DAILY_REMINDER_HOUR=18
MONTHLY_REPORT_DAY=1
MONTHLY_REPORT_HOUR=9

# Email settings (already configured)
MAIL_DEFAULT_SENDER=QuizMaster <tentiwalavanya26@gmail.com>
```

#### 6.2 Task Configuration
- Email templates in `simple_email.py` (already done)
- Task retry configuration
- Error handling and logging

### Phase 7: Monitoring and Maintenance

#### 7.1 Logging
- Celery Beat logs for schedule execution
- Task execution logs
- Email delivery status logs

#### 7.2 Error Handling
- Retry failed email sends
- Handle database connection issues
- Graceful degradation if Redis unavailable

## Implementation Timeline

### Day 1: Core Setup
- [ ] Update `celery_config.py` with beat schedule
- [ ] Implement `send_daily_reminders()` task
- [ ] Create beat management scripts
- [ ] Test manual task execution

### Day 2: Enhancement & Testing
- [ ] Implement `send_monthly_reports()` task
- [ ] Add optional database fields
- [ ] Test scheduled execution
- [ ] Documentation and README updates

## File Changes Required

### New Files:
- `start_celery_beat.sh`
- `stop_celery_beat.sh`

### Modified Files:
- `application/celery_config.py` - Add beat schedule
- `application/celery_tasks.py` - Add new tasks
- `application/models.py` - Optional new fields
- `README.md` - Update with beat instructions

### No Changes Needed:
- `application/simple_email.py` - Already ready
- `main.py` - Already configured
- `.env` - Already configured
- `requirements.txt` - Already has dependencies

## Testing Commands

```bash
# Test daily reminders manually
celery -A application.celery_tasks call application.celery_tasks.send_daily_reminders

# Test monthly reports manually
celery -A application.celery_tasks call application.celery_tasks.send_monthly_reports

# Check scheduled tasks
celery -A application.celery_tasks inspect scheduled

# Monitor beat scheduler
celery -A application.celery_tasks events
```

## Success Criteria

1. **Daily Reminders:**
   - Emails sent to inactive users at 6 PM daily
   - No duplicate emails
   - Proper error handling

2. **Monthly Reports:**
   - Reports sent on 1st of every month
   - Accurate statistics calculation
   - Professional email formatting

3. **System Stability:**
   - Celery worker and beat running reliably
   - Proper logging and monitoring
   - Easy start/stop management

## Advantages of This Approach

1. **Reuses Existing Infrastructure:**
   - Same Celery + Redis setup
   - Same email system
   - Minimal new dependencies

2. **Scalable:**
   - Can add more scheduled tasks easily
   - Tasks run in background
   - Can distribute across multiple workers

3. **Reliable:**
   - Celery handles retries automatically
   - Beat scheduler ensures tasks run on time
   - Redis provides persistence

4. **Maintainable:**
   - Clear separation of concerns
   - Easy to test individual components
   - Standard Celery patterns

---

**Ready to implement this plan?** 
The implementation will be straightforward since we already have most components in place. 