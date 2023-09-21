import datetime as dt
import uuid
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_session import Session

from models import db
from os import environ
from config import DEV_DB, PROD_DB
from utils.funcs import time_ago


def create_app():
    app = Flask(__name__)
    if environ.get('DEBUG') == '1':
        app.config['SQLALCHEMY_DATABASE_URI'] = DEV_DB
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = PROD_DB
    app.config['SECRET_KEY'] = uuid.uuid4()
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(hours=6)

    app.jinja_env.globals['timeago'] = time_ago

    Bootstrap(app)
    app.app_context().push()
    Session(app)
    db.init_app(app)
    db.create_all()
    login_manager = LoginManager()
    login_manager.init_app(app)

    return app, db, login_manager
