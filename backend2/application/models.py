from .database import db
from datetime import datetime
from pytz import timezone
from flask import url_for




class Users(db.Model):
    __tablename__="Users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=True)
    qualification = db.Column(db.String, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            'email': self.email,
            'username': self.username,
            'dob': self.dob,
            'qualification': self.qualification,
            'is_admin': self.is_admin
        }

