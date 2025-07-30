from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..models import Questions, Quizzes, Chapters, Subjects
from ..database import db
from datetime import datetime
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

def create_question_routes(app):
    
    @app.route('/api/questions', methods=['GET'])
    @jwt_required()
    @admin_required
    def get_questions():
        """Get all questions or filter by quiz_id (Admin only)"""
        try:
            quiz_id = request.args.get('quiz_id', type=int)
            
            query = Questions.query
            
            if quiz_id:
                query = query.filter_by(quiz_id=quiz_id)
            
            questions = query.all()
            
            questions_list = []
            for question in questions:
                question_data = question.serialize()
                # Add quiz and chapter information
                if question.quiz:
                    question_data['quiz_name'] = question.quiz.name
                    if question.quiz.chapter:
                        question_data['chapter_name'] = question.quiz.chapter.name
                        if question.quiz.chapter.subject:
                            question_data['subject_name'] = question.quiz.chapter.subject.name
                questions_list.append(question_data)
            
            return jsonify(questions_list), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/questions/<int:question_id>', methods=['GET'])
    @jwt_required()
    @admin_required
    def get_question(question_id):
        """Get a specific question by ID (Admin only)"""
        try:
            question = Questions.query.get_or_404(question_id)
            
            question_data = question.serialize()
            
            # Add quiz and chapter information
            if question.quiz:
                question_data['quiz_name'] = question.quiz.name
                if question.quiz.chapter:
                    question_data['chapter_name'] = question.quiz.chapter.name
                    if question.quiz.chapter.subject:
                        question_data['subject_name'] = question.quiz.chapter.subject.name
            
            return jsonify(question_data), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/questions', methods=['POST'])
    @jwt_required()
    @admin_required
    def create_question():
        """Create a new question (Admin only)"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['quiz_id', 'question_statement', 'option1', 'option2', 'option3', 'option4', 'correct_option']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'message': f'{field} is required'}), 400
            
            # Validate quiz exists
            quiz = Quizzes.query.get(data['quiz_id'])
            if not quiz:
                return jsonify({'message': 'Quiz not found'}), 404
            
            # Validate correct_option is between 1-4
            correct_option = data['correct_option']
            if not isinstance(correct_option, int) or correct_option < 1 or correct_option > 4:
                return jsonify({'message': 'correct_option must be between 1 and 4'}), 400
            
            # Validate marks if provided
            marks = data.get('marks', 1.0)
            if not isinstance(marks, (int, float)) or marks <= 0:
                return jsonify({'message': 'marks must be a positive number'}), 400
            
            # Create new question
            question = Questions(
                quiz_id=data['quiz_id'],
                question_statement=data['question_statement'],
                option1=data['option1'],
                option2=data['option2'],
                option3=data['option3'],
                option4=data['option4'],
                correct_option=correct_option,
                difficulty_level=data.get('difficulty_level', 'Medium'),
                marks=data.get('marks', 1.0)
            )
            
            db.session.add(question)
            
            # Update quiz total_questions count
            quiz.total_questions = Questions.query.filter_by(quiz_id=quiz.id).count() + 1
            
            db.session.commit()
            
            # Return updated quiz data along with the new question
            return jsonify({
                'message': 'Question created successfully',
                'question': question.serialize(),
                'quiz': {
                    'id': quiz.id,
                    'total_questions': quiz.total_questions
                }
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/questions/<int:question_id>', methods=['PUT'])
    @jwt_required()
    @admin_required
    def update_question(question_id):
        """Update a question (Admin only)"""
        try:
            question = Questions.query.get_or_404(question_id)
            data = request.get_json()
            
            # Validate quiz if being updated
            if 'quiz_id' in data:
                quiz = Quizzes.query.get(data['quiz_id'])
                if not quiz:
                    return jsonify({'message': 'Quiz not found'}), 404
                
                # Update question counts for old and new quiz
                old_quiz = question.quiz
                if old_quiz and old_quiz.id != data['quiz_id']:
                    old_quiz.total_questions = Questions.query.filter_by(quiz_id=old_quiz.id).count() - 1
                    quiz.total_questions = Questions.query.filter_by(quiz_id=data['quiz_id']).count() + 1
                
                question.quiz_id = data['quiz_id']
            
            # Update fields
            if 'question_statement' in data:
                question.question_statement = data['question_statement']
            if 'option1' in data:
                question.option1 = data['option1']
            if 'option2' in data:
                question.option2 = data['option2']
            if 'option3' in data:
                question.option3 = data['option3']
            if 'option4' in data:
                question.option4 = data['option4']
            if 'correct_option' in data:
                correct_option = data['correct_option']
                if not isinstance(correct_option, int) or correct_option < 1 or correct_option > 4:
                    return jsonify({'message': 'correct_option must be between 1 and 4'}), 400
                question.correct_option = correct_option
            if 'difficulty_level' in data:
                question.difficulty_level = data['difficulty_level']
            if 'marks' in data:
                marks = data['marks']
                if not isinstance(marks, (int, float)) or marks <= 0:
                    return jsonify({'message': 'marks must be a positive number'}), 400
                question.marks = marks
            
            db.session.commit()
            
            return jsonify({
                'message': 'Question updated successfully',
                'question': question.serialize()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    @jwt_required()
    @admin_required
    def delete_question(question_id):
        """Delete a question (Admin only)"""
        try:
            question = Questions.query.get_or_404(question_id)
            quiz = question.quiz
            
            db.session.delete(question)
            
            # Update quiz total_questions count
            if quiz:
                quiz.total_questions = Questions.query.filter_by(quiz_id=quiz.id).count() - 1
            
            db.session.commit()
            
            return jsonify({'message': 'Question deleted successfully'}), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/questions/bulk', methods=['POST'])
    @jwt_required()
    @admin_required
    def create_bulk_questions():
        """Create multiple questions for a quiz (Admin only)"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if 'quiz_id' not in data or 'questions' not in data:
                return jsonify({'message': 'quiz_id and questions array are required'}), 400
            
            quiz_id = data['quiz_id']
            questions_data = data['questions']
            
            # Validate quiz exists
            quiz = Quizzes.query.get(quiz_id)
            if not quiz:
                return jsonify({'message': 'Quiz not found'}), 404
            
            if not isinstance(questions_data, list) or len(questions_data) == 0:
                return jsonify({'message': 'questions must be a non-empty array'}), 400
            
            created_questions = []
            
            for i, q_data in enumerate(questions_data):
                # Validate each question
                required_fields = ['question_statement', 'option1', 'option2', 'option3', 'option4', 'correct_option']
                for field in required_fields:
                    if field not in q_data or not q_data[field]:
                        return jsonify({'message': f'{field} is required for question {i+1}'}), 400
                
                # Validate correct_option
                correct_option = q_data['correct_option']
                if not isinstance(correct_option, int) or correct_option < 1 or correct_option > 4:
                    return jsonify({'message': f'correct_option must be between 1 and 4 for question {i+1}'}), 400
                
                # Create question
                question = Questions(
                    quiz_id=quiz_id,
                    question_statement=q_data['question_statement'],
                    option1=q_data['option1'],
                    option2=q_data['option2'],
                    option3=q_data['option3'],
                    option4=q_data['option4'],
                    correct_option=correct_option,
                    difficulty_level=q_data.get('difficulty_level', 'Medium'),
                    marks=q_data.get('marks', 1.0)
                )
                
                db.session.add(question)
                created_questions.append(question)
            
            # Update quiz total_questions count
            quiz.total_questions = Questions.query.filter_by(quiz_id=quiz_id).count() + len(created_questions)
            
            db.session.commit()
            
            return jsonify({
                'message': f'{len(created_questions)} questions created successfully',
                'questions': [q.serialize() for q in created_questions]
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/questions/validate', methods=['POST'])
    @jwt_required()
    @admin_required
    def validate_questions():
        """Validate question data before creation (Admin only)"""
        try:
            data = request.get_json()
            
            if 'questions' not in data:
                return jsonify({'message': 'questions array is required'}), 400
            
            questions_data = data['questions']
            errors = []
            
            for i, q_data in enumerate(questions_data):
                question_errors = []
                
                # Check required fields
                required_fields = ['question_statement', 'option1', 'option2', 'option3', 'option4', 'correct_option']
                for field in required_fields:
                    if field not in q_data or not q_data[field]:
                        question_errors.append(f'{field} is required')
                
                # Validate correct_option
                if 'correct_option' in q_data:
                    correct_option = q_data['correct_option']
                    if not isinstance(correct_option, int) or correct_option < 1 or correct_option > 4:
                        question_errors.append('correct_option must be between 1 and 4')
                
                # Validate marks
                if 'marks' in q_data:
                    marks = q_data['marks']
                    if not isinstance(marks, (int, float)) or marks <= 0:
                        question_errors.append('marks must be a positive number')
                
                if question_errors:
                    errors.append({
                        'question_index': i + 1,
                        'errors': question_errors
                    })
            
            if errors:
                return jsonify({
                    'valid': False,
                    'errors': errors
                }), 400
            
            return jsonify({
                'valid': True,
                'message': 'All questions are valid'
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app 