from application.models import *
from flask import jsonify, request
from application.database import db
from main import app
from flask_bcrypt import Bcrypt
from application.auth import admin_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

@app.route('/signup', methods=['POST'])
def signup():
    """
    User signup endpoint
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: User's email address
              example: user@example.com
            username:
              type: string
              description: Unique username
              example: johndoe
            password:
              type: string
              description: User's password
              example: securepassword123
            dob:
              type: string
              format: date
              description: Date of Birth
              example: "1990-01-15"
            qualification:
              type: string
              description: User's educational qualification
              example: "Bachelor's Degree"
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            token:
              type: string
              description: JWT access token
            user:
              type: string
              description: Username of the created user
      409:
        description: User already exists
      500:
        description: Something went wrong
    """
    try:
        data = request.get_json()
        user = Users.query.filter_by(email=data['email']).first()
        if user:
            return jsonify({'message': 'User already exists'}), 409
        else:
            b=Bcrypt()
            hashed_password = b.generate_password_hash(data['password'])
            dob_date = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            new_user = Users(email=data['email'], username=data['username'] ,password=hashed_password, dob=dob_date, qualification=data['qualification'])
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(
                identity={"email": data['email']}, additional_claims={"is_administrator": False}
            )
            return jsonify({"token": access_token, "user": new_user.username}), 201
            
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = Users.query.filter_by(email=data['email']).first()
        if user:
            b=Bcrypt()
            if b.check_password_hash(user.password, data['password']):
                #check if admin and pass admin to frontend
                access_token = create_access_token(
                identity={"email":user.email}, additional_claims={"is_administrator": user.is_admin}
                    )
                print(user.is_admin)
                return jsonify({"token": access_token, "user": user.username, "is_admin": user.is_admin }), 200
            else:
                return jsonify({'message': 'Invalid password'}), 401
        else:
            return jsonify({'message': 'User does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = Users.query.all()
        return jsonify([user.serialize() for user in users]), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    try:
        user = Users.query.get(id)
        if user:
            return jsonify({'user': user.serialize()}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/current_user', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user = Users.query.filter_by(email=get_jwt_identity()['email']).first()
        return jsonify({'user': user.serialize()}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500