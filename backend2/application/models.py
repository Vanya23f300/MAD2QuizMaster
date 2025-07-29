from .database import db
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Float, Text, JSON, Time
import re

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    qualification = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_reminder_sent = db.Column(db.DateTime, nullable=True)

    # Relationships
    subjects = relationship("Subjects", back_populates="created_by_user")
    scores = relationship("Scores", back_populates="user")
    preferences = relationship("UserPreferences", back_populates="user", uselist=False, cascade="all, delete-orphan")

    @classmethod
    def create_admin(cls, email='admin@quizmaster.com', username='QuizMaster', password=None):
        """
        Create the single admin user for the application
        Ensures only one admin can exist
        """
        # Check if admin already exists
        existing_admin = cls.query.filter_by(is_admin=True).first()
        if existing_admin:
            return existing_admin
        
        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        
        # Validate username
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        
        # If no password provided, generate a secure default
        from flask_bcrypt import Bcrypt
        if not password:
            import secrets
            password = secrets.token_urlsafe(12)
        
        # Hash the password
        bcrypt = Bcrypt()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create admin user
        admin = cls(
            email=email,
            username=username,
            password=hashed_password,
            is_admin=True,
            is_active=True,
            qualification='Quiz Master Administrator',
            last_login=datetime.utcnow(),
            registration_date=datetime.utcnow()
        )
        
        db.session.add(admin)
        db.session.commit()
        
        return admin
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Serialize user object"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'is_admin': self.is_admin,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'registration_date': self.registration_date.isoformat()
        }

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'dob': str(self.dob),
            'qualification': self.qualification,
            'is_admin': self.is_admin,
            'last_login': str(self.last_login) if self.last_login else None,
            'is_active': self.is_active,
            'registration_date': str(self.registration_date),
            'last_reminder_sent': str(self.last_reminder_sent) if self.last_reminder_sent else None
        }

    def __repr__(self):
        return f'<User {self.username}>'

class UserPreferences(db.Model):
    __tablename__ = "UserPreferences"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False, unique=True)
    # Notification preferences
    daily_reminders = db.Column(db.Boolean, default=True)
    reminder_time = db.Column(db.Time, nullable=True)  # No default - user must choose
    quiz_notifications = db.Column(db.Boolean, default=True)
    monthly_reports = db.Column(db.Boolean, default=True)
    export_notifications = db.Column(db.Boolean, default=True)
    # Display preferences
    theme = db.Column(db.String, default='dark')
    dashboard_layout = db.Column(db.String, default='comfortable')
    show_performance_trends = db.Column(db.Boolean, default=True)
    # Quiz preferences
    auto_save = db.Column(db.Boolean, default=True)
    show_timer = db.Column(db.Boolean, default=True)
    confirm_before_submit = db.Column(db.Boolean, default=True)
    review_mode = db.Column(db.String, default='immediate')
    # Export preferences
    default_export_format = db.Column(db.String, default='csv')
    include_personal_data = db.Column(db.Boolean, default=False)
    auto_delete_days = db.Column(db.String, default='14')
    # Notification channels
    gchat_webhook_url = db.Column(db.String, nullable=True)
    sms_number = db.Column(db.String, nullable=True)
    email_notifications = db.Column(db.Boolean, default=True)
    # Last notification sent
    last_reminder_sent = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = relationship("Users", back_populates="preferences")

    def serialize(self):
        return {
            'notifications': {
                'dailyReminders': self.daily_reminders,
                'reminderTime': self.reminder_time.strftime('%H:%M') if self.reminder_time else None,
                'quizNotifications': self.quiz_notifications,
                'monthlyReports': self.monthly_reports,
                'exportNotifications': self.export_notifications
            },
            'display': {
                'theme': self.theme,
                'dashboardLayout': self.dashboard_layout,
                'showPerformanceTrends': self.show_performance_trends
            },
            'quiz': {
                'autoSave': self.auto_save,
                'showTimer': self.show_timer,
                'confirmBeforeSubmit': self.confirm_before_submit,
                'reviewMode': self.review_mode
            },
            'export': {
                'defaultFormat': self.default_export_format,
                'includePersonalData': self.include_personal_data,
                'autoDeleteDays': self.auto_delete_days
            },
            'notificationChannels': {
                'gchatWebhookUrl': self.gchat_webhook_url,
                'smsNumber': self.sms_number,
                'emailNotifications': self.email_notifications
            }
        }

    @classmethod
    def create_default(cls, user_id):
        """Create default preferences for a new user"""
        preferences = cls(
            user_id=user_id,
            daily_reminders=True,
            reminder_time=None,  # No default time, user must choose
            quiz_notifications=True,
            monthly_reports=True,
            export_notifications=True,
            theme='dark',
            dashboard_layout='comfortable',
            show_performance_trends=True,
            auto_save=True,
            show_timer=True,
            confirm_before_submit=True,
            review_mode='immediate',
            default_export_format='csv',
            include_personal_data=False,
            auto_delete_days='14',
            email_notifications=True
        )
        
        db.session.add(preferences)
        db.session.commit()
        
        return preferences

class Subjects(db.Model):
    __tablename__ = "Subjects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    created_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    created_by_user = relationship("Users", back_populates="subjects")
    chapters = relationship("Chapters", back_populates="subject")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

    def __repr__(self):
        return f'<Subject {self.name}>'

class Chapters(db.Model):
    __tablename__ = "Chapters"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('Subjects.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    order = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    subject = relationship("Subjects", back_populates="chapters")
    quizzes = relationship("Quizzes", back_populates="chapter")

    def serialize(self):
        return {
            'id': self.id,
            'subject_id': self.subject_id,
            'name': self.name,
            'description': self.description,
            'order': self.order,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Chapter {self.name}>'

class Quizzes(db.Model):
    __tablename__ = "Quizzes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('Chapters.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    date_of_quiz = db.Column(db.Date)
    time_duration = db.Column(db.Integer)  # in minutes
    total_questions = db.Column(db.Integer)
    passing_score = db.Column(db.Float)
    remarks = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    chapter = relationship("Chapters", back_populates="quizzes")
    questions = relationship("Questions", back_populates="quiz")
    scores = relationship("Scores", back_populates="quiz")

    def serialize(self):
        return {
            'id': self.id,
            'chapter_id': self.chapter_id,
            'name': self.name,
            'description': self.description,
            'date_of_quiz': str(self.date_of_quiz) if self.date_of_quiz else None,
            'time_duration': self.time_duration,
            'total_questions': len(self.questions),  # Use actual count instead of stored value
            'passing_score': self.passing_score,
            'remarks': self.remarks,
            'is_active': self.is_active
        }

    def __repr__(self):
        return f'<Quiz {self.name}>'

class Questions(db.Model):
    __tablename__ = "Questions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quizzes.id'), nullable=False)
    question_statement = db.Column(db.String, nullable=False)
    option1 = db.Column(db.String, nullable=False)
    option2 = db.Column(db.String, nullable=False)
    option3 = db.Column(db.String, nullable=False)
    option4 = db.Column(db.String, nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)
    difficulty_level = db.Column(db.String)
    marks = db.Column(db.Float, default=1.0)

    # Relationships
    quiz = relationship("Quizzes", back_populates="questions")

    def serialize(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question_statement': self.question_statement,
            'options': [
                self.option1,
                self.option2,
                self.option3,
                self.option4
            ],
            'correct_option': self.correct_option,
            'difficulty_level': self.difficulty_level,
            'marks': self.marks
        }

    def __repr__(self):
        return f'<Question {self.id}>'

class Scores(db.Model):
    __tablename__ = "Scores"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quizzes.id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    total_scored = db.Column(db.Float, nullable=False)
    total_possible_score = db.Column(db.Float, nullable=False)
    time_taken = db.Column(db.Integer)  # in seconds
    percentage = db.Column(db.Float)
    passed = db.Column(db.Boolean)

    # Relationships
    user = relationship("Users", back_populates="scores")
    quiz = relationship("Quizzes", back_populates="scores")

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'quiz_id': self.quiz_id,
            'time_stamp_of_attempt': self.time_stamp_of_attempt.isoformat(),
            'total_scored': self.total_scored,
            'total_possible_score': self.total_possible_score,
            'time_taken': self.time_taken,
            'percentage': self.percentage,
            'passed': self.passed
        }

    def __repr__(self):
        return f'<Score {self.id}>'

