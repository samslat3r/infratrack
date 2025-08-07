from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect


db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'create-an-environment-variable-for-this'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'create-an-environment-variable-for-this'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    csrf.init_app(app)
    
    with app.app_context():
        from . import routes, models
        db.create_all()
        
    return app 

