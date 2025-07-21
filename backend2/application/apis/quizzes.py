from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..models import Quizzes, Chapters, Subjects, Questions, Scores, Users
from ..database import db
from datetime import datetime, date
import re

def admin_required(f):
    """Decorator to ensure only admin users can access certain endpoints"""
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        
        if not claims.get('is_admin', False):
            return jsonify({'message': 'Admin access required'}), 403
            
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def create_quiz_routes(app):
    
    @app.route('/api/quizzes', methods=['GET'])
    @jwt_required()
    def get_quizzes():
        """Get all quizzes or filter by chapter"""
        try:
            chapter_id = request.args.get('chapter_id', type=int)
            
            query = Quizzes.query
            
            if chapter_id:
                query = query.filter_by(chapter_id=chapter_id)
            
            # Only show active quizzes to regular users
            claims = get_jwt()
            if not claims.get('is_admin', False):
                query = query.filter_by(is_active=True)
            
            quizzes = query.all()
            
            quiz_list = []
            for quiz in quizzes:
                quiz_data = quiz.serialize()
                # Add chapter and subject information
                if quiz.chapter:
                    quiz_data['chapter_name'] = quiz.chapter.name
                    if quiz.chapter.subject:
                        quiz_data['subject_name'] = quiz.chapter.subject.name
                quiz_list.append(quiz_data)
            
            return jsonify(quiz_list), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/quizzes/<int:quiz_id>', methods=['GET'])
    @jwt_required()
    def get_quiz(quiz_id):
        """Get a specific quiz by ID"""
        try:
            quiz = Quizzes.query.get_or_404(quiz_id)
            
            # Regular users can only see active quizzes
            claims = get_jwt()
            if not claims.get('is_admin', False) and not quiz.is_active:
                return jsonify({'message': 'Quiz not found'}), 404
            
            quiz_data = quiz.serialize()
            
            # Add chapter and subject information
            if quiz.chapter:
                quiz_data['chapter_name'] = quiz.chapter.name
                if quiz.chapter.subject:
                    quiz_data['subject_name'] = quiz.chapter.subject.name
            
            # Add questions count
            quiz_data['questions_count'] = len(quiz.questions)
            
            return jsonify(quiz_data), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/quizzes', methods=['POST'])
    @jwt_required()
    @admin_required
    def create_quiz():
        """Create a new quiz (Admin only)"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['name', 'chapter_id']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'message': f'{field} is required'}), 400
            
            # Validate chapter exists
            chapter = Chapters.query.get(data['chapter_id'])
            if not chapter:
                return jsonify({'message': 'Chapter not found'}), 404
            
            # Validate date format if provided
            date_of_quiz = None
            if data.get('date_of_quiz'):
                try:
                    date_of_quiz = datetime.strptime(data['date_of_quiz'], '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
            
            # Create new quiz
            quiz = Quizzes(
                name=data['name'],
                description=data.get('description', ''),
                chapter_id=data['chapter_id'],
                date_of_quiz=date_of_quiz,
                time_duration=data.get('time_duration', 60),  # Default 60 minutes
                total_questions=data.get('total_questions', 0),
                passing_score=data.get('passing_score', 60.0),  # Default 60%
                remarks=data.get('remarks', ''),
                is_active=data.get('is_active', True)
            )
            
            db.session.add(quiz)
            db.session.commit()
            
            return jsonify({
                'message': 'Quiz created successfully',
                'quiz': quiz.serialize()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/quizzes/<int:quiz_id>', methods=['PUT'])
    @jwt_required()
    @admin_required
    def update_quiz(quiz_id):
        """Update a quiz (Admin only)"""
        try:
            quiz = Quizzes.query.get_or_404(quiz_id)
            data = request.get_json()
            
            # Validate chapter if being updated
            if 'chapter_id' in data:
                chapter = Chapters.query.get(data['chapter_id'])
                if not chapter:
                    return jsonify({'message': 'Chapter not found'}), 404
                quiz.chapter_id = data['chapter_id']
            
            # Update fields
            if 'name' in data:
                quiz.name = data['name']
            if 'description' in data:
                quiz.description = data['description']
            if 'date_of_quiz' in data:
                if data['date_of_quiz']:
                    try:
                        quiz.date_of_quiz = datetime.strptime(data['date_of_quiz'], '%Y-%m-%d').date()
                    except ValueError:
                        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
                else:
                    quiz.date_of_quiz = None
            if 'time_duration' in data:
                quiz.time_duration = data['time_duration']
            if 'total_questions' in data:
                quiz.total_questions = data['total_questions']
            if 'passing_score' in data:
                quiz.passing_score = data['passing_score']
            if 'remarks' in data:
                quiz.remarks = data['remarks']
            if 'is_active' in data:
                quiz.is_active = data['is_active']
            
            db.session.commit()
            
            return jsonify({
                'message': 'Quiz updated successfully',
                'quiz': quiz.serialize()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/quizzes/<int:quiz_id>', methods=['DELETE'])
    @jwt_required()
    @admin_required
    def delete_quiz(quiz_id):
        """Delete a quiz (Admin only)"""
        try:
            quiz = Quizzes.query.get_or_404(quiz_id)
            
            # Check if quiz has any attempts
            if quiz.scores:
                return jsonify({
                    'message': 'Cannot delete quiz with existing attempts. Deactivate instead.'
                }), 400
            
            # Delete associated questions first
            Questions.query.filter_by(quiz_id=quiz_id).delete()
            
            db.session.delete(quiz)
            db.session.commit()
            
            return jsonify({'message': 'Quiz deleted successfully'}), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/quizzes/<int:quiz_id>/questions', methods=['GET'])
    @jwt_required()
    def get_quiz_questions(quiz_id):
        """Get all questions for a quiz"""
        try:
            quiz = Quizzes.query.get_or_404(quiz_id)
            
            # Regular users can only see active quizzes
            claims = get_jwt()
            if not claims.get('is_admin', False) and not quiz.is_active:
                return jsonify({'message': 'Quiz not found'}), 404
            
            questions = Questions.query.filter_by(quiz_id=quiz_id).all()
            
            questions_data = []
            for question in questions:
                question_data = question.serialize()
                # For regular users taking quiz, don't include correct answer
                if not claims.get('is_admin', False):
                    question_data.pop('correct_option', None)
                questions_data.append(question_data)
            
            return jsonify(questions_data), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/quizzes/<int:quiz_id>/start', methods=['POST'])
    @jwt_required()
    def start_quiz(quiz_id):
        """Start a quiz attempt"""
        try:
            current_user_id = get_jwt_identity()
            quiz = Quizzes.query.get_or_404(quiz_id)
            
            # Check if quiz is active
            if not quiz.is_active:
                return jsonify({'message': 'Quiz is not available'}), 400
            
            # Check if quiz has questions
            if not quiz.questions:
                return jsonify({'message': 'Quiz has no questions'}), 400
            
            # Get questions for the quiz (without correct answers)
            questions = Questions.query.filter_by(quiz_id=quiz_id).all()
            questions_data = []
            for question in questions:
                q_data = question.serialize()
                q_data.pop('correct_option', None)  # Remove correct answer
                questions_data.append(q_data)
            
            quiz_data = quiz.serialize()
            quiz_data['questions'] = questions_data
            quiz_data['start_time'] = datetime.utcnow().isoformat()
            
            return jsonify(quiz_data), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/quizzes/<int:quiz_id>/submit', methods=['POST'])
    @jwt_required()
    def submit_quiz(quiz_id):
        """Submit quiz answers and calculate score"""
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            quiz = Quizzes.query.get_or_404(quiz_id)
            
            if not quiz.is_active:
                return jsonify({'message': 'Quiz is not available'}), 400
            
            answers = data.get('answers', {})  # {question_id: selected_option}
            start_time = data.get('start_time')
            submit_time = datetime.utcnow()
            
            # Calculate time taken
            time_taken = 0
            if start_time:
                try:
                    start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    time_taken = int((submit_time - start_dt).total_seconds())
                except:
                    pass
            
            # Get all questions for the quiz
            questions = Questions.query.filter_by(quiz_id=quiz_id).all()
            
            if not questions:
                return jsonify({'message': 'Quiz has no questions'}), 400
            
            # Calculate score
            total_scored = 0
            total_possible_score = 0
            correct_answers = 0
            
            for question in questions:
                total_possible_score += question.marks
                user_answer = answers.get(str(question.id))
                
                if user_answer and int(user_answer) == question.correct_option:
                    total_scored += question.marks
                    correct_answers += 1
            
            # Calculate percentage
            percentage = (total_scored / total_possible_score * 100) if total_possible_score > 0 else 0
            passed = percentage >= quiz.passing_score
            
            # Save score
            score = Scores(
                user_id=current_user_id,
                quiz_id=quiz_id,
                time_stamp_of_attempt=submit_time,
                total_scored=total_scored,
                total_possible_score=total_possible_score,
                time_taken=time_taken,
                percentage=percentage,
                passed=passed
            )
            
            db.session.add(score)
            db.session.commit()
            
            return jsonify({
                'message': 'Quiz submitted successfully',
                'score': score.serialize(),
                'correct_answers': correct_answers,
                'total_questions': len(questions),
                'percentage': percentage,
                'passed': passed
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/quizzes/<int:quiz_id>/attempts', methods=['GET'])
    @jwt_required()
    def get_quiz_attempts(quiz_id):
        """Get quiz attempts (admin sees all, users see their own)"""
        try:
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            
            quiz = Quizzes.query.get_or_404(quiz_id)
            
            query = Scores.query.filter_by(quiz_id=quiz_id)
            
            # Regular users can only see their own attempts
            if not claims.get('is_admin', False):
                query = query.filter_by(user_id=current_user_id)
            
            attempts = query.order_by(Scores.time_stamp_of_attempt.desc()).all()
            
            attempts_data = []
            for attempt in attempts:
                attempt_data = attempt.serialize()
                # Add user information for admin
                if claims.get('is_admin', False):
                    user = Users.query.get(attempt.user_id)
                    if user:
                        attempt_data['username'] = user.username
                        attempt_data['email'] = user.email
                attempts_data.append(attempt_data)
            
            return jsonify(attempts_data), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app 