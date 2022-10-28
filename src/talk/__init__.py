import os

from flask import Flask

from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY'),
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'


    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app