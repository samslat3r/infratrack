import os
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app() -> Flask:
    app = Flask(__name__)

    # Config
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("SECRET_KEY environment variable must be set for security")
    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///infratrack.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init 
    db.init_app(app)
    csrf.init_app(app)

    # Enable SQLite FK constraints so ON DELETE CASCADE works
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):

        if isinstance(dbapi_connection, sqlite3.Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    # Register Blueprints
    with app.app_context():
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from . import models 
        db.create_all()

    return app
