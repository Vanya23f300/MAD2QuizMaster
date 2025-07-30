from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Users, Subjects, Chapters, Quizzes, Questions, Scores
from ..database import db
from ..cache import cache_with_expiry
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta, date
import logging

logger = logging.getLogger(__name__)

def create_analytics_routes(app):
    
    @app.route('/api/analytics/summary-charts', methods=['GET'])
    @jwt_required()
    @cache_with_expiry(expiry_seconds=600, key_prefix="summary_charts")
    def get_summary_charts():
        """
        Get comprehensive summary charts data for dashboard
        Available for both admin and users (different data scope)
        """
        try:
            # Get current user's identity (just email string)
            current_user_email = get_jwt_identity()
            current_user = Users.query.filter_by(email=current_user_email).first()
            
            if not current_user:
                return jsonify({
                    'message': 'User not found',
                    'error': 'USER_NOT_FOUND'
                }), 404
            
            # Get time ranges
            today = date.today()
            last_7_days = today - timedelta(days=7)
            last_30_days = today - timedelta(days=30)
            last_6_months = today - timedelta(days=180)
            
            if current_user.is_admin:
                # Admin dashboard charts
                charts_data = {
                    'user_registration_trends': get_user_registration_trends(last_6_months),
                    'quiz_performance_overview': get_quiz_performance_overview(),
                    'subject_popularity': get_subject_popularity(),
                    'daily_activity': get_daily_activity_stats(last_30_days),
                    'top_performers': get_top_performers(),
                    'quiz_difficulty_analysis': get_quiz_difficulty_analysis(),
                    'monthly_stats': get_monthly_stats()
                }
            else:
                # User dashboard charts
                charts_data = {
                    'personal_performance': get_personal_performance(current_user.id, last_6_months),
                    'subject_progress': get_user_subject_progress(current_user.id),
                    'recent_quiz_scores': get_recent_quiz_scores(current_user.id, last_30_days),
                    'performance_comparison': get_performance_comparison(current_user.id),
                    'time_spent_analysis': get_time_spent_analysis(current_user.id, last_30_days)
                }
            
            return jsonify({
                'message': 'Summary charts retrieved successfully',
                'charts': charts_data,
                'generated_at': datetime.utcnow().isoformat(),
                'user_type': 'admin' if current_user.is_admin else 'user'
            })
            
        except Exception as e:
            logger.error(f"Summary charts error: {str(e)}")
            return jsonify({
                'message': 'Failed to retrieve summary charts',
                'error': str(e)
            }), 500
    
    @app.route('/api/analytics/top-performers', methods=['GET'])
    @jwt_required()
    def get_top_performers_api():
        """
        Get leaderboard data of all users for comparison
        ---
        tags:
          - Analytics
        security:
          - bearerAuth: []
        responses:
          200:
            description: Leaderboard data retrieved successfully
          401:
            description: Authentication required
        """
        try:
            # Get current user's identity (just email string)
            current_user_email = get_jwt_identity()
            current_user = Users.query.filter_by(email=current_user_email).first()
            
            if not current_user:
                return jsonify({
                    'message': 'User not found',
                    'error': 'USER_NOT_FOUND'
                }), 404
            
            # Get top performers data (exclude admin users)
            performers = db.session.query(
                Users.id,
                Users.username,
                func.count(Scores.id).label('total_quizzes'),
                func.avg(Scores.percentage).label('avg_score'),
                func.count(func.nullif(Scores.passed, False)).label('passed_quizzes')
            ).join(Scores, Users.id == Scores.user_id, isouter=True)\
             .filter(Users.is_admin == False)\
             .group_by(Users.id, Users.username)\
             .order_by(func.avg(Scores.percentage).desc().nulls_last())\
             .all()
            
            # Process data for frontend
            leaderboard_data = []
            for idx, perf in enumerate(performers):
                # Calculate pass rate
                total_quizzes = perf.total_quizzes or 0
                pass_rate = (perf.passed_quizzes / total_quizzes * 100) if total_quizzes > 0 else 0
                
                # Check if this is the current user
                is_current_user = (perf.id == current_user.id)
                
                # Add to leaderboard data
                leaderboard_data.append({
                    'id': perf.id,
                    'username': perf.username,
                    'total_quizzes': total_quizzes,
                    'avg_score': round(float(perf.avg_score), 2) if perf.avg_score else 0,
                    'pass_rate': round(pass_rate, 2),
                    'rank': idx + 1,  # Add rank (1-based)
                    'isCurrentUser': is_current_user
                })
            
            # If user hasn't taken any quizzes, they might not be in the results
            # Check and add current user if missing
            if not any(entry['id'] == current_user.id for entry in leaderboard_data):
                leaderboard_data.append({
                    'id': current_user.id,
                    'username': current_user.username,
                    'total_quizzes': 0,
                    'avg_score': 0,
                    'pass_rate': 0,
                    'rank': len(leaderboard_data) + 1,
                    'isCurrentUser': True
                })
            
            logger.info(f"Leaderboard data retrieved for user: {current_user.email}")
            
            return jsonify(leaderboard_data), 200
            
        except Exception as e:
            logger.error(f"Leaderboard data error: {str(e)}")
            return jsonify({
                'message': 'Failed to retrieve leaderboard data',
                'error': str(e)
            }), 500
    
    @app.route('/api/analytics/performance-metrics', methods=['GET'])
    @jwt_required()
    @cache_with_expiry(expiry_seconds=300, key_prefix="performance_metrics")
    def get_performance_metrics():
        """
        Get detailed performance metrics for analysis
        """
        try:
            # Get current user's identity (just email string)
            current_user_email = get_jwt_identity()
            current_user = Users.query.filter_by(email=current_user_email).first()
            
            if not current_user:
                return jsonify({
                    'message': 'User not found',
                    'error': 'USER_NOT_FOUND'
                }), 404
            
            # Get query parameters
            days = min(int(request.args.get('days', 30)), 365)
            subject_id = request.args.get('subject_id', type=int)
            
            start_date = date.today() - timedelta(days=days)
            
            if current_user.is_admin:
                # Admin metrics - platform-wide
                metrics = {
                    'platform_performance': get_platform_performance_metrics(start_date),
                    'user_engagement': get_user_engagement_metrics(start_date),
                    'content_analytics': get_content_analytics_metrics(start_date, subject_id)
                }
            else:
                # User metrics - personal
                metrics = {
                    'personal_metrics': get_personal_metrics(current_user.id, start_date),
                    'improvement_trends': get_improvement_trends(current_user.id, start_date),
                    'goal_tracking': get_goal_tracking(current_user.id, start_date)
                }
            
            return jsonify({
                'message': 'Performance metrics retrieved successfully',
                'metrics': metrics,
                'period_days': days,
                'start_date': start_date.isoformat()
            })
            
        except Exception as e:
            logger.error(f"Performance metrics error: {str(e)}")
            return jsonify({
                'message': 'Failed to retrieve performance metrics',
                'error': str(e)
            }), 500

    return app

# Helper functions for chart data generation
def get_user_registration_trends(start_date):
    """Get user registration trends over time"""
    try:
        registrations = db.session.query(
            func.date(Users.registration_date).label('date'),
            func.count(Users.id).label('count')
        ).filter(
            and_(
                Users.registration_date >= start_date,
                Users.is_admin == False
            )
        ).group_by(func.date(Users.registration_date)).all()
        
        return {
            'type': 'line',
            'title': 'User Registration Trends',
            'data': [{'date': reg.date.isoformat(), 'count': reg.count} for reg in registrations]
        }
    except Exception as e:
        logger.error(f"User registration trends error: {str(e)}")
        return {'type': 'line', 'title': 'User Registration Trends', 'data': []}

def get_quiz_performance_overview():
    """Get overall quiz performance statistics"""
    try:
        performance = db.session.query(
            Subjects.name.label('subject'),
            func.count(Scores.id).label('total_attempts'),
            func.avg(Scores.percentage).label('avg_score'),
            func.count(func.nullif(Scores.passed, False)).label('passed_count')
        ).join(Chapters, Subjects.id == Chapters.subject_id)\
         .join(Quizzes, Chapters.id == Quizzes.chapter_id)\
         .join(Scores, Quizzes.id == Scores.quiz_id)\
         .group_by(Subjects.id, Subjects.name).all()
        
        data = []
        for perf in performance:
            pass_rate = (perf.passed_count / perf.total_attempts * 100) if perf.total_attempts > 0 else 0
            data.append({
                'subject': perf.subject,
                'total_attempts': perf.total_attempts,
                'avg_score': round(float(perf.avg_score), 2) if perf.avg_score else 0,
                'pass_rate': round(pass_rate, 2)
            })
        
        return {
            'type': 'bar',
            'title': 'Quiz Performance by Subject',
            'data': data
        }
    except Exception as e:
        logger.error(f"Quiz performance overview error: {str(e)}")
        return {'type': 'bar', 'title': 'Quiz Performance by Subject', 'data': []}

def get_subject_popularity():
    """Get subject popularity based on quiz attempts"""
    try:
        popularity = db.session.query(
            Subjects.name.label('subject'),
            func.count(Scores.id).label('attempts')
        ).join(Chapters, Subjects.id == Chapters.subject_id)\
         .join(Quizzes, Chapters.id == Quizzes.chapter_id)\
         .join(Scores, Quizzes.id == Scores.quiz_id)\
         .group_by(Subjects.id, Subjects.name)\
         .order_by(func.count(Scores.id).desc())\
         .limit(10).all()
        
        return {
            'type': 'pie',
            'title': 'Most Popular Subjects',
            'data': [{'subject': pop.subject, 'attempts': pop.attempts} for pop in popularity]
        }
    except Exception as e:
        logger.error(f"Subject popularity error: {str(e)}")
        return {'type': 'pie', 'title': 'Most Popular Subjects', 'data': []}

def get_daily_activity_stats(start_date):
    """Get daily platform activity statistics"""
    try:
        activity = db.session.query(
            func.date(Scores.time_stamp_of_attempt).label('date'),
            func.count(Scores.id).label('quiz_attempts'),
            func.count(func.distinct(Scores.user_id)).label('active_users')
        ).filter(
            Scores.time_stamp_of_attempt >= start_date
        ).group_by(func.date(Scores.time_stamp_of_attempt)).all()
        
        return {
            'type': 'area',
            'title': 'Daily Platform Activity',
            'data': [{
                'date': act.date.isoformat(),
                'quiz_attempts': act.quiz_attempts,
                'active_users': act.active_users
            } for act in activity]
        }
    except Exception as e:
        logger.error(f"Daily activity stats error: {str(e)}")
        return {'type': 'area', 'title': 'Daily Platform Activity', 'data': []}

def get_top_performers():
    """Get top performing users"""
    try:
        performers = db.session.query(
            Users.username,
            func.count(Scores.id).label('total_quizzes'),
            func.avg(Scores.percentage).label('avg_score'),
            func.count(func.nullif(Scores.passed, False)).label('passed_quizzes')
        ).join(Scores, Users.id == Scores.user_id)\
         .filter(Users.is_admin == False)\
         .group_by(Users.id, Users.username)\
         .having(func.count(Scores.id) >= 3)\
         .order_by(func.avg(Scores.percentage).desc())\
         .limit(10).all()
        
        data = []
        for perf in performers:
            pass_rate = (perf.passed_quizzes / perf.total_quizzes * 100) if perf.total_quizzes > 0 else 0
            data.append({
                'username': perf.username,
                'total_quizzes': perf.total_quizzes,
                'avg_score': round(float(perf.avg_score), 2) if perf.avg_score else 0,
                'pass_rate': round(pass_rate, 2)
            })
        
        return {
            'type': 'table',
            'title': 'Top Performers',
            'data': data
        }
    except Exception as e:
        logger.error(f"Top performers error: {str(e)}")
        return {'type': 'table', 'title': 'Top Performers', 'data': []}

def get_quiz_difficulty_analysis():
    """Analyze quiz difficulty based on performance"""
    try:
        difficulty = db.session.query(
            Quizzes.name.label('quiz_name'),
            func.count(Scores.id).label('attempts'),
            func.avg(Scores.percentage).label('avg_score'),
            func.count(func.nullif(Scores.passed, False)).label('passed_count')
        ).join(Scores, Quizzes.id == Scores.quiz_id)\
         .group_by(Quizzes.id, Quizzes.name)\
         .having(func.count(Scores.id) >= 5)\
         .order_by(func.avg(Scores.percentage)).all()
        
        data = []
        for diff in difficulty:
            pass_rate = (diff.passed_count / diff.attempts * 100) if diff.attempts > 0 else 0
            difficulty_level = 'Hard' if pass_rate < 50 else 'Medium' if pass_rate < 80 else 'Easy'
            
            data.append({
                'quiz_name': diff.quiz_name,
                'attempts': diff.attempts,
                'avg_score': round(float(diff.avg_score), 2) if diff.avg_score else 0,
                'pass_rate': round(pass_rate, 2),
                'difficulty': difficulty_level
            })
        
        return {
            'type': 'scatter',
            'title': 'Quiz Difficulty Analysis',
            'data': data
        }
    except Exception as e:
        logger.error(f"Quiz difficulty analysis error: {str(e)}")
        return {'type': 'scatter', 'title': 'Quiz Difficulty Analysis', 'data': []}

def get_monthly_stats():
    """Get monthly platform statistics"""
    try:
        # Get stats for last 6 months
        monthly_stats = []
        for i in range(6):
            month_start = (date.today().replace(day=1) - timedelta(days=i*30)).replace(day=1)
            next_month = (month_start + timedelta(days=32)).replace(day=1)
            
            stats = {
                'month': month_start.strftime('%Y-%m'),
                'new_users': Users.query.filter(
                    and_(
                        Users.registration_date >= month_start,
                        Users.registration_date < next_month,
                        Users.is_admin == False
                    )
                ).count(),
                'quiz_attempts': Scores.query.filter(
                    and_(
                        Scores.time_stamp_of_attempt >= month_start,
                        Scores.time_stamp_of_attempt < next_month
                    )
                ).count(),
                'avg_score': db.session.query(func.avg(Scores.percentage)).filter(
                    and_(
                        Scores.time_stamp_of_attempt >= month_start,
                        Scores.time_stamp_of_attempt < next_month
                    )
                ).scalar() or 0
            }
            monthly_stats.append(stats)
        
        return {
            'type': 'multi_line',
            'title': 'Monthly Platform Statistics',
            'data': monthly_stats
        }
    except Exception as e:
        logger.error(f"Monthly stats error: {str(e)}")
        return {'type': 'multi_line', 'title': 'Monthly Platform Statistics', 'data': []}

# User-specific chart functions
def get_personal_performance(user_id, start_date):
    """Get personal performance trends for a user"""
    try:
        performance = db.session.query(
            func.date(Scores.time_stamp_of_attempt).label('date'),
            func.avg(Scores.percentage).label('avg_score'),
            func.count(Scores.id).label('attempts')
        ).filter(
            and_(
                Scores.user_id == user_id,
                Scores.time_stamp_of_attempt >= start_date
            )
        ).group_by(func.date(Scores.time_stamp_of_attempt)).all()
        
        return {
            'type': 'line',
            'title': 'Your Performance Trend',
            'data': [{
                'date': perf.date.isoformat(),
                'avg_score': round(float(perf.avg_score), 2) if perf.avg_score else 0,
                'attempts': perf.attempts
            } for perf in performance]
        }
    except Exception as e:
        logger.error(f"Personal performance error: {str(e)}")
        return {'type': 'line', 'title': 'Your Performance Trend', 'data': []}

def get_user_subject_progress(user_id):
    """Get user's progress across different subjects"""
    try:
        progress = db.session.query(
            Subjects.name.label('subject'),
            func.count(Scores.id).label('attempts'),
            func.avg(Scores.percentage).label('avg_score'),
            func.count(func.nullif(Scores.passed, False)).label('passed')
        ).join(Chapters, Subjects.id == Chapters.subject_id)\
         .join(Quizzes, Chapters.id == Quizzes.chapter_id)\
         .join(Scores, Quizzes.id == Scores.quiz_id)\
         .filter(Scores.user_id == user_id)\
         .group_by(Subjects.id, Subjects.name).all()
        
        data = []
        for prog in progress:
            pass_rate = (prog.passed / prog.attempts * 100) if prog.attempts > 0 else 0
            data.append({
                'subject': prog.subject,
                'attempts': prog.attempts,
                'avg_score': round(float(prog.avg_score), 2) if prog.avg_score else 0,
                'pass_rate': round(pass_rate, 2)
            })
        
        return {
            'type': 'radar',
            'title': 'Your Subject Progress',
            'data': data
        }
    except Exception as e:
        logger.error(f"User subject progress error: {str(e)}")
        return {'type': 'radar', 'title': 'Your Subject Progress', 'data': []}

def get_recent_quiz_scores(user_id, start_date):
    """Get recent quiz scores for a user"""
    try:
        scores = db.session.query(
            Quizzes.name.label('quiz_name'),
            Scores.percentage,
            Scores.time_stamp_of_attempt,
            Scores.passed
        ).join(Quizzes, Scores.quiz_id == Quizzes.id)\
         .filter(
            and_(
                Scores.user_id == user_id,
                Scores.time_stamp_of_attempt >= start_date
            )
        ).order_by(Scores.time_stamp_of_attempt.desc())\
         .limit(20).all()
        
        return {
            'type': 'bar',
            'title': 'Recent Quiz Scores',
            'data': [{
                'quiz_name': score.quiz_name,
                'percentage': round(float(score.percentage), 2) if score.percentage else 0,
                'date': score.time_stamp_of_attempt.strftime('%Y-%m-%d'),
                'passed': score.passed
            } for score in scores]
        }
    except Exception as e:
        logger.error(f"Recent quiz scores error: {str(e)}")
        return {'type': 'bar', 'title': 'Recent Quiz Scores', 'data': []}

def get_performance_comparison(user_id):
    """Compare user's performance with platform average"""
    try:
        user_avg = db.session.query(func.avg(Scores.percentage)).filter_by(user_id=user_id).scalar() or 0
        platform_avg = db.session.query(func.avg(Scores.percentage)).scalar() or 0
        
        # Get subject-wise comparison
        comparison = db.session.query(
            Subjects.name.label('subject'),
            func.avg(Scores.percentage).label('user_avg')
        ).join(Chapters, Subjects.id == Chapters.subject_id)\
         .join(Quizzes, Chapters.id == Quizzes.chapter_id)\
         .join(Scores, Quizzes.id == Scores.quiz_id)\
         .filter(Scores.user_id == user_id)\
         .group_by(Subjects.id, Subjects.name).all()
        
        data = []
        for comp in comparison:
            # Get platform average for this subject
            subject_platform_avg = db.session.query(func.avg(Scores.percentage))\
                .join(Quizzes, Scores.quiz_id == Quizzes.id)\
                .join(Chapters, Quizzes.chapter_id == Chapters.id)\
                .join(Subjects, Chapters.subject_id == Subjects.id)\
                .filter(Subjects.name == comp.subject).scalar() or 0
            
            data.append({
                'subject': comp.subject,
                'your_score': round(float(comp.user_avg), 2) if comp.user_avg else 0,
                'platform_avg': round(float(subject_platform_avg), 2)
            })
        
        return {
            'type': 'comparison_bar',
            'title': 'Your Performance vs Platform Average',
            'overall': {
                'your_avg': round(float(user_avg), 2),
                'platform_avg': round(float(platform_avg), 2)
            },
            'data': data
        }
    except Exception as e:
        logger.error(f"Performance comparison error: {str(e)}")
        return {'type': 'comparison_bar', 'title': 'Your Performance vs Platform Average', 'data': []}

def get_time_spent_analysis(user_id, start_date):
    """Analyze time spent on quizzes"""
    try:
        time_analysis = db.session.query(
            func.date(Scores.time_stamp_of_attempt).label('date'),
            func.sum(Scores.time_taken).label('total_time'),
            func.count(Scores.id).label('quiz_count')
        ).filter(
            and_(
                Scores.user_id == user_id,
                Scores.time_stamp_of_attempt >= start_date,
                Scores.time_taken.isnot(None)
            )
        ).group_by(func.date(Scores.time_stamp_of_attempt)).all()
        
        return {
            'type': 'area',
            'title': 'Time Spent on Quizzes',
            'data': [{
                'date': analysis.date.isoformat(),
                'total_minutes': analysis.total_time,
                'quiz_count': analysis.quiz_count,
                'avg_time_per_quiz': round(analysis.total_time / analysis.quiz_count, 2) if analysis.quiz_count > 0 else 0
            } for analysis in time_analysis]
        }
    except Exception as e:
        logger.error(f"Time spent analysis error: {str(e)}")
        return {'type': 'area', 'title': 'Time Spent on Quizzes', 'data': []}

# Additional helper functions for performance metrics
def get_platform_performance_metrics(start_date):
    """Get platform-wide performance metrics"""
    try:
        total_users = Users.query.filter_by(is_admin=False).count()
        active_users = db.session.query(func.count(func.distinct(Scores.user_id)))\
            .filter(Scores.time_stamp_of_attempt >= start_date).scalar() or 0
        
        total_attempts = Scores.query.filter(Scores.time_stamp_of_attempt >= start_date).count()
        avg_platform_score = db.session.query(func.avg(Scores.percentage))\
            .filter(Scores.time_stamp_of_attempt >= start_date).scalar() or 0
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'engagement_rate': round((active_users / total_users * 100), 2) if total_users > 0 else 0,
            'total_attempts': total_attempts,
            'avg_platform_score': round(float(avg_platform_score), 2)
        }
    except Exception as e:
        logger.error(f"Platform performance metrics error: {str(e)}")
        return {}

def get_user_engagement_metrics(start_date):
    """Get user engagement metrics"""
    try:
        daily_active_users = db.session.query(
            func.date(Scores.time_stamp_of_attempt).label('date'),
            func.count(func.distinct(Scores.user_id)).label('dau')
        ).filter(
            Scores.time_stamp_of_attempt >= start_date
        ).group_by(func.date(Scores.time_stamp_of_attempt)).all()
        
        return {
            'daily_active_users': [{'date': dau.date.isoformat(), 'count': dau.dau} for dau in daily_active_users]
        }
    except Exception as e:
        logger.error(f"User engagement metrics error: {str(e)}")
        return {}

def get_content_analytics_metrics(start_date, subject_id=None):
    """Get content analytics metrics"""
    try:
        query = db.session.query(
            Subjects.name.label('subject'),
            func.count(Scores.id).label('total_attempts'),
            func.avg(Scores.percentage).label('avg_score')
        ).join(Chapters, Subjects.id == Chapters.subject_id)\
         .join(Quizzes, Chapters.id == Quizzes.chapter_id)\
         .join(Scores, Quizzes.id == Scores.quiz_id)\
         .filter(Scores.time_stamp_of_attempt >= start_date)
        
        if subject_id:
            query = query.filter(Subjects.id == subject_id)
        
        results = query.group_by(Subjects.id, Subjects.name).all()
        
        return {
            'subject_performance': [{
                'subject': result.subject,
                'total_attempts': result.total_attempts,
                'avg_score': round(float(result.avg_score), 2) if result.avg_score else 0
            } for result in results]
        }
    except Exception as e:
        logger.error(f"Content analytics metrics error: {str(e)}")
        return {}

def get_personal_metrics(user_id, start_date):
    """Get personal metrics for a user"""
    try:
        user_scores = Scores.query.filter(
            and_(
                Scores.user_id == user_id,
                Scores.time_stamp_of_attempt >= start_date
            )
        ).all()
        
        if not user_scores:
            return {}
        
        total_attempts = len(user_scores)
        passed_attempts = len([s for s in user_scores if s.passed])
        avg_score = sum(s.percentage for s in user_scores if s.percentage) / total_attempts
        total_time = sum(s.time_taken for s in user_scores if s.time_taken) or 0
        
        return {
            'total_attempts': total_attempts,
            'passed_attempts': passed_attempts,
            'pass_rate': round((passed_attempts / total_attempts * 100), 2),
            'avg_score': round(avg_score, 2),
            'total_time_minutes': total_time,
            'avg_time_per_quiz': round(total_time / total_attempts, 2) if total_attempts > 0 else 0
        }
    except Exception as e:
        logger.error(f"Personal metrics error: {str(e)}")
        return {}

def get_improvement_trends(user_id, start_date):
    """Get improvement trends for a user"""
    try:
        # Get scores grouped by week to show improvement over time
        weekly_scores = db.session.query(
            func.extract('week', Scores.time_stamp_of_attempt).label('week'),
            func.avg(Scores.percentage).label('avg_score')
        ).filter(
            and_(
                Scores.user_id == user_id,
                Scores.time_stamp_of_attempt >= start_date
            )
        ).group_by(func.extract('week', Scores.time_stamp_of_attempt))\
         .order_by(func.extract('week', Scores.time_stamp_of_attempt)).all()
        
        return {
            'weekly_progress': [{'week': int(ws.week), 'avg_score': round(float(ws.avg_score), 2)} for ws in weekly_scores]
        }
    except Exception as e:
        logger.error(f"Improvement trends error: {str(e)}")
        return {}

def get_goal_tracking(user_id, start_date):
    """Get goal tracking data for a user"""
    try:
        # Simple goal tracking - you can expand this based on requirements
        recent_scores = Scores.query.filter(
            and_(
                Scores.user_id == user_id,
                Scores.time_stamp_of_attempt >= start_date
            )
        ).order_by(Scores.time_stamp_of_attempt.desc()).limit(10).all()
        
        target_score = 80  # Default target
        achieving_target = len([s for s in recent_scores if s.percentage >= target_score])
        
        return {
            'target_score': target_score,
            'recent_attempts': len(recent_scores),
            'achieving_target': achieving_target,
            'goal_achievement_rate': round((achieving_target / len(recent_scores) * 100), 2) if recent_scores else 0
        }
    except Exception as e:
        logger.error(f"Goal tracking error: {str(e)}")
        return {}