import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "replace-with-secure-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite+pysqlite:///infratrack.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    csrf.init_app(app)

    # Make {{ csrf_token() }} available in all templates
    @app.context_processor
    def inject_csrf():
        return dict(csrf_token=generate_csrf)  

    from .routes import main as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
