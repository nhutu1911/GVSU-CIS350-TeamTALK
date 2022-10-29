import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from dotenv import load_dotenv

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    load_dotenv()
    if os.getenv('SECRET_KEY') is None:
        raise ValueError('SECRET_KEY is not set in .env')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        # blueprint for non-auth parts of app
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        db.create_all()

        return app


