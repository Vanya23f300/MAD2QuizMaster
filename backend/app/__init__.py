from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from celery import Celery
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

def create_app():
    print("create_app() called")
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)

    from .routes import auth, admin, user
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(user.bp)

    with app.app_context():
        from . import models 
        db.create_all()
        from .utils import create_admin_if_not_exists
        create_admin_if_not_exists()

    return app