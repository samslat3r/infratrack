# infratrack/app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    # Secret + DB URL
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "replace-with-secure-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite+pysqlite:///infratrack.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Optional: quick visibility of what URL SQLAlchemy sees
    # print("DB URL =", app.config["SQLALCHEMY_DATABASE_URI"])

    db.init_app(app)
    csrf.init_app(app)

    # Register blueprint
    from .routes import main as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()
        
    @app.context_processor
    def inject_csrf():
        return dict(csrf_token=csrf.generate_csrf())

    return app
