from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Board(db.Model):
    __tablename__ = "boards"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates='boards')
    columns = db.relationship('Column', back_populates='board')
    cards = db.relationship('Card', back_populates='board')
    date_created = db.Column(db.DateTime, nullable=False)
    last_edited = db.Column(db.DateTime, nullable=True)
    color = db.Column(db.String(50), default="#212529")


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    username = db.Column(db.String(1000), unique=True, nullable=False)
    boards = db.relationship('Board', back_populates='user')
    columns = db.relationship('Column', back_populates='user')
    cards = db.relationship('Card', back_populates='user')
    date_created = db.Column(db.DateTime, nullable=False)


class Column(db.Model):
    __tablename__ = 'cols'
    id = db.Column(db.Integer, primary_key=True)
    column_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates='columns')
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    board = db.relationship("Board", back_populates='columns')
    cards = db.relationship('Card', back_populates='column')
    date_created = db.Column(db.DateTime, nullable=False)
    last_edited = db.Column(db.DateTime, nullable=True)
    color = db.Column(db.String(50), default="#212529")


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(50), nullable=False)
    card_subtitle = db.Column(db.String(150))
    card_content = db.Column(db.String(4000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates='cards')
    column_id = db.Column(db.Integer, db.ForeignKey('cols.id'))
    column = db.relationship("Column", back_populates='cards')
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    board = db.relationship("Board", back_populates='cards')
    date_created = db.Column(db.DateTime, nullable=False)
    last_edited = db.Column(db.DateTime, nullable=True)
    color = db.Column(db.String(50), default="#212529")
