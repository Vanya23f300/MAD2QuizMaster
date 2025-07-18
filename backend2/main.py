from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from application.models import *
from dotenv import load_dotenv
import os



from datetime import timedelta
import base64
from flasgger import Swagger


app = None
UPLOAD_FOLDER="static/images"
load_dotenv()



def create_app():
    app=Flask(__name__)
    print("starting local development")
    app.config.from_object(LocalDevelopmentConfig)
    app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER

    
    
    db.init_app(app)
   
   

    
    app.app_context().push()
    return app

app=create_app()

Swagger(app)  # This will serve Swagger UI at /docs

if not os.path.exists(os.path.join(app.instance_path, 'database.sqlite3')):
    db.create_all()    
    # run only once to create admin user 
    b=Bcrypt()
    password=b.generate_password_hash("admin123").decode('utf-8')
    user=Users(email="admin@email.com",username="admin",password=password,is_admin=True)
    
    db.session.add(user)

    db.session.commit()
    

jwt = JWTManager(app)

CORS(app)



# CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

from application.controllers import *

if __name__ == '__main__':
    

    app.run(debug=True,port=8000)
