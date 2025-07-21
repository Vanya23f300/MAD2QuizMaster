from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Users, Subjects, Chapters, Quizzes, Questions, Scores
from ..database import db
from ..cache import cache_with_expiry
from sqlalchemy import or_, and_, func
import logging

logger = logging.getLogger(__name__)

def create_search_routes(app):
    
    @app.route('/api/admin/search', methods=['POST'])
    @jwt_required()
    @cache_with_expiry(expiry_seconds=300, key_prefix="admin_search")
    def admin_global_search():
        """
        Global search functionality for admin dashboard
        Search across users, subjects, chapters, quizzes
        """
        try:
            current_user_identity = get_jwt_identity()
            current_user = Users.query.filter_by(email=current_user_identity['email']).first()
            
            if not current_user or not current_user.is_admin:
                return jsonify({
                    'message': 'Unauthorized. Admin access required.',
                    'error': 'ADMIN_REQUIRED'
                }), 403
            
            data = request.get_json()
            query = data.get('query', '').strip()
            search_type = data.get('type', 'all')  # 'all', 'users', 'subjects', 'quizzes'
            limit = min(int(data.get('limit', 50)), 100)  # Max 100 results
            
            if len(query) < 2:
                return jsonify({
                    'message': 'Search query must be at least 2 characters',
                    'error': 'INVALID_QUERY'
                }), 400
            
            results = {}
            
            # Search Users
            if search_type in ['all', 'users']:
                users = Users.query.filter(
                    and_(
                        Users.is_admin == False,
                        or_(
                            Users.username.ilike(f'%{query}%'),
                            Users.email.ilike(f'%{query}%'),
                            Users.qualification.ilike(f'%{query}%')
                        )
                    )
                ).limit(limit).all()
                
                results['users'] = [{
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'qualification': user.qualification,
                    'registration_date': user.registration_date.strftime('%Y-%m-%d') if user.registration_date else None,
                    'last_login': user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Never',
                    'is_active': user.is_active
                } for user in users]
            
            # Search Subjects
            if search_type in ['all', 'subjects']:
                subjects = Subjects.query.filter(
                    or_(
                        Subjects.name.ilike(f'%{query}%'),
                        Subjects.description.ilike(f'%{query}%')
                    )
                ).limit(limit).all()
                
                results['subjects'] = [{
                    'id': subject.id,
                    'name': subject.name,
                    'description': subject.description,
                    'created_date': subject.created_date.strftime('%Y-%m-%d') if subject.created_date else None,
                    'chapters_count': len(subject.chapters) if subject.chapters else 0
                } for subject in subjects]
            
            # Search Quizzes
            if search_type in ['all', 'quizzes']:
                quizzes = db.session.query(Quizzes, Chapters, Subjects)\
                    .join(Chapters, Quizzes.chapter_id == Chapters.id)\
                    .join(Subjects, Chapters.subject_id == Subjects.id)\
                    .filter(
                        or_(
                            Quizzes.name.ilike(f'%{query}%'),
                            Quizzes.description.ilike(f'%{query}%'),
                            Chapters.name.ilike(f'%{query}%'),
                            Subjects.name.ilike(f'%{query}%')
                        )
                    ).limit(limit).all()
                
                results['quizzes'] = [{
                    'id': quiz.id,
                    'name': quiz.name,
                    'description': quiz.description,
                    'chapter_name': chapter.name,
                    'subject_name': subject.name,
                    'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d') if quiz.date_of_quiz else None,
                    'duration_minutes': quiz.duration_minutes,
                    'total_questions': len(quiz.questions) if quiz.questions else 0,
                    'attempts_count': db.session.query(Scores).filter_by(quiz_id=quiz.id).count()
                } for quiz, chapter, subject in quizzes]
            
            # Calculate total results
            total_results = sum(len(results.get(key, [])) for key in results.keys())
            
            logger.info(f"Admin search for '{query}' returned {total_results} results")
            
            return jsonify({
                'message': 'Search completed successfully',
                'query': query,
                'search_type': search_type,
                'total_results': total_results,
                'results': results
            })
            
        except Exception as e:
            logger.error(f"Admin search failed: {str(e)}")
            return jsonify({
                'message': 'Search failed',
                'error': str(e)
            }), 500
    
    @app.route('/api/admin/users/search', methods=['POST'])
    @jwt_required()
    @cache_with_expiry(expiry_seconds=300, key_prefix="admin_user_search")
    def search_users():
        """
        Advanced user search with filters
        """
        try:
            current_user_identity = get_jwt_identity()
            current_user = Users.query.filter_by(email=current_user_identity['email']).first()
            
            if not current_user or not current_user.is_admin:
                return jsonify({
                    'message': 'Unauthorized. Admin access required.',
                    'error': 'ADMIN_REQUIRED'
                }), 403
            
            data = request.get_json()
            query = data.get('query', '').strip()
            filters = data.get('filters', {})
            sort_by = data.get('sort_by', 'registration_date')
            sort_order = data.get('sort_order', 'desc')
            page = max(int(data.get('page', 1)), 1)
            per_page = min(int(data.get('per_page', 20)), 100)
            
            # Build query
            user_query = Users.query.filter(Users.is_admin == False)
            
            # Apply text search
            if query:
                user_query = user_query.filter(
                    or_(
                        Users.username.ilike(f'%{query}%'),
                        Users.email.ilike(f'%{query}%'),
                        Users.qualification.ilike(f'%{query}%')
                    )
                )
            
            # Apply filters
            if filters.get('is_active') is not None:
                user_query = user_query.filter(Users.is_active == filters['is_active'])
            
            if filters.get('qualification'):
                user_query = user_query.filter(Users.qualification.ilike(f'%{filters["qualification"]}%'))
            
            if filters.get('registration_date_from'):
                user_query = user_query.filter(Users.registration_date >= filters['registration_date_from'])
            
            if filters.get('registration_date_to'):
                user_query = user_query.filter(Users.registration_date <= filters['registration_date_to'])
            
            # Apply sorting
            if hasattr(Users, sort_by):
                if sort_order == 'desc':
                    user_query = user_query.order_by(getattr(Users, sort_by).desc())
                else:
                    user_query = user_query.order_by(getattr(Users, sort_by))
            
            # Paginate
            paginated = user_query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            # Get user statistics
            user_stats = {}
            for user in paginated.items:
                quiz_count = db.session.query(Scores).filter_by(user_id=user.id).count()
                avg_score = db.session.query(func.avg(Scores.percentage)).filter_by(user_id=user.id).scalar()
                
                user_stats[user.id] = {
                    'quiz_attempts': quiz_count,
                    'average_score': round(float(avg_score), 2) if avg_score else 0.0
                }
            
            results = [{
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'qualification': user.qualification,
                'registration_date': user.registration_date.strftime('%Y-%m-%d') if user.registration_date else None,
                'last_login': user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Never',
                'is_active': user.is_active,
                'quiz_attempts': user_stats[user.id]['quiz_attempts'],
                'average_score': user_stats[user.id]['average_score']
            } for user in paginated.items]
            
            return jsonify({
                'message': 'User search completed successfully',
                'users': results,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': paginated.total,
                    'pages': paginated.pages,
                    'has_next': paginated.has_next,
                    'has_prev': paginated.has_prev
                },
                'query': query,
                'filters': filters
            })
            
        except Exception as e:
            logger.error(f"User search failed: {str(e)}")
            return jsonify({
                'message': 'User search failed',
                'error': str(e)
            }), 500
    
    @app.route('/api/admin/quizzes/search', methods=['POST'])
    @jwt_required()
    @cache_with_expiry(expiry_seconds=300, key_prefix="admin_quiz_search")
    def search_quizzes():
        """
        Advanced quiz search with performance analytics
        """
        try:
            current_user_identity = get_jwt_identity()
            current_user = Users.query.filter_by(email=current_user_identity['email']).first()
            
            if not current_user or not current_user.is_admin:
                return jsonify({
                    'message': 'Unauthorized. Admin access required.',
                    'error': 'ADMIN_REQUIRED'
                }), 403
            
            data = request.get_json()
            query = data.get('query', '').strip()
            filters = data.get('filters', {})
            page = max(int(data.get('page', 1)), 1)
            per_page = min(int(data.get('per_page', 20)), 100)
            
            # Build query with joins
            quiz_query = db.session.query(Quizzes, Chapters, Subjects)\
                .join(Chapters, Quizzes.chapter_id == Chapters.id)\
                .join(Subjects, Chapters.subject_id == Subjects.id)
            
            # Apply text search
            if query:
                quiz_query = quiz_query.filter(
                    or_(
                        Quizzes.name.ilike(f'%{query}%'),
                        Quizzes.description.ilike(f'%{query}%'),
                        Chapters.name.ilike(f'%{query}%'),
                        Subjects.name.ilike(f'%{query}%')
                    )
                )
            
            # Apply filters
            if filters.get('subject_id'):
                quiz_query = quiz_query.filter(Subjects.id == filters['subject_id'])
            
            if filters.get('chapter_id'):
                quiz_query = quiz_query.filter(Chapters.id == filters['chapter_id'])
            
            if filters.get('date_from'):
                quiz_query = quiz_query.filter(Quizzes.date_of_quiz >= filters['date_from'])
            
            if filters.get('date_to'):
                quiz_query = quiz_query.filter(Quizzes.date_of_quiz <= filters['date_to'])
            
            # Order by creation date (newest first)
            quiz_query = quiz_query.order_by(Quizzes.created_date.desc())
            
            # Get total count
            total = quiz_query.count()
            
            # Apply pagination
            quizzes = quiz_query.offset((page - 1) * per_page).limit(per_page).all()
            
            # Calculate quiz analytics
            results = []
            for quiz, chapter, subject in quizzes:
                # Get quiz statistics
                attempts_count = db.session.query(Scores).filter_by(quiz_id=quiz.id).count()
                avg_score = db.session.query(func.avg(Scores.percentage)).filter_by(quiz_id=quiz.id).scalar()
                pass_rate = db.session.query(func.count(Scores.id)).filter(
                    and_(Scores.quiz_id == quiz.id, Scores.passed == True)
                ).scalar()
                
                pass_percentage = (pass_rate / attempts_count * 100) if attempts_count > 0 else 0
                
                results.append({
                    'id': quiz.id,
                    'name': quiz.name,
                    'description': quiz.description,
                    'chapter_name': chapter.name,
                    'subject_name': subject.name,
                    'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d') if quiz.date_of_quiz else None,
                    'duration_minutes': quiz.duration_minutes,
                    'created_date': quiz.created_date.strftime('%Y-%m-%d') if quiz.created_date else None,
                    'total_questions': len(quiz.questions) if quiz.questions else 0,
                    'attempts_count': attempts_count,
                    'average_score': round(float(avg_score), 2) if avg_score else 0.0,
                    'pass_rate_percentage': round(pass_percentage, 2)
                })
            
            return jsonify({
                'message': 'Quiz search completed successfully',
                'quizzes': results,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page,
                    'has_next': page * per_page < total,
                    'has_prev': page > 1
                },
                'query': query,
                'filters': filters
            })
            
        except Exception as e:
            logger.error(f"Quiz search failed: {str(e)}")
            return jsonify({
                'message': 'Quiz search failed',
                'error': str(e)
            }), 500

    return app