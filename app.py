import datetime as dt

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from flask_session import Session
from models import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///micro.db'
    app.config['SECRET_KEY'] = 'key'    
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(hours=5)
    Bootstrap(app)
    app.app_context().push()
    Session(app)
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    return app, db, login_manager