from datetime import datetime as dt

from flask import (Flask, flash, make_response, redirect, render_template,
                   request, session, url_for, get_flashed_messages)
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.dialects.sqlite import JSON
from werkzeug.security import check_password_hash, generate_password_hash

from flask_session import Session
from utils.forms import CreateCardForm, LoginForm, RegisterForm, CreateBoardForm, AddColForm
from utils.funcs import taskTimeAgo

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///micro.db'
app.config['SECRET_KEY'] = 'key'    
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Bootstrap(app)
app.app_context().push()
db.init_app(app)
Session(app)
ckeditor = CKEditor(app)
login_manager = LoginManager()
login_manager.init_app(app)

#TODO: Add dropdown functionality to cards
#TODO: Add card route and template
#TODO: Figure out drag-and-drop
#TODO: Add user login and show user boards in a dropdown in sidebar
#TODO: Change theme function to modify db entry
#TODO: Add user mark to cards
#TODO: Create boards
#TODO: Edit board names
#TODO: Edit and Delete boards, columns and cards


class Board(db.Model):
    __tablename__="boards"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), nullable = False)
    # tdd = db.Column(JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates='boards')
    columns = db.relationship('Column', back_populates='board')
    cards = db.relationship('Card', back_populates='board')

class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    username = db.Column(db.String(1000), unique=True, nullable=False)
    boards = db.relationship('Board', back_populates='user')
    columns = db.relationship('Column', back_populates='user')
    cards = db.relationship('Card', back_populates='user')
    # False is Dark, True is Light
    theme = db.Column(db.String(10), default='light')

class Column(db.Model):
    __tablename__='cols'
    id = db.Column(db.Integer, primary_key=True)
    column_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates='columns')
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    board = db.relationship("Board", back_populates='columns')
    cards = db.relationship('Card', back_populates='column')

class Card(db.Model):
    __tablename__='cards'
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

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

# db.drop_all()
# db.create_all()

# newBoard = Board(
#     title = "Main",
#     tdd =  {
#         "todo": ["Task 1"],
#         "doing":["Task 2"],
#         "done": ["Task 3"]
#     }
# )
# db.session.add(newBoard)
# db.session.commit()



# daboard = db.session.get(Board, 1)
# daboard.tdd = {
#     "To Do": {
#         "Task 1": ["Do something", f"{dt.now()}"],
#         "Task 2": ["Do other thing", f"{dt.now()}"]
#     },
#     "Doing": {"Task 3": ["Doing thing", f"{dt.now()}"]},
#     "Review": {"Task 4": ["Review this", f"{dt.now()}"]},
#     "Done": {"Task 5": ["Done this", f"{dt.now()}"]}
# }

# db.session.commit()

@app.route("/theme", methods=["POST"])
def theme():
    """
    Receives a theme string and a path, saves the theme to a cookie
    and redirects back to the page from the post request is made.
    """

    session['theme'] = request.args.get('theme')
    
    path = request.args.get('path')
    return redirect(path)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        user = db.session.query(User).filter_by(username=request.form["username"]).first()
        if user:
            if check_password_hash(user.password, request.form["password"]):
                login_user(user)
                flash('Logged in successfully.')

                return redirect(url_for('home'))
            else:
                flash('Wrong password. Try again.')
                return redirect(url_for('login'))
        else:
            flash('User does not exist.')
            return redirect(url_for('login'))
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.session.query(User).filter_by(email=request.form["email"]).first()
            user_check = db.session.query(User).filter_by(username=request.form['username']).first()
            if user:
                flash("Email is already registered. Login instead.")
                return redirect(url_for('login'))
            elif user_check:
                flash("Username is taken. Use a different one.")
                return redirect(url_for('register'))
            else:
                hashed_password = generate_password_hash(request.form["password"], "pbkdf2:sha256", 8)
                new_user = User(
                    username = request.form["username"],
                    email = request.form["email"],
                    password = hashed_password,
                    theme = request.form['theme']
                )
                db.session.add(new_user)
                db.session.commit()
                
                login_user(new_user)
                return redirect(url_for('home'))

    return render_template("register.html", form=form)

@app.route("/board/<int:id>", methods=["GET"])
def board(id):
    boardData = db.session.get(Board, id)
    formattedTDD = taskTimeAgo(boardData.tdd)
    keysTDD = list(formattedTDD.keys())
    if request.method == 'GET':
        return render_template('board.html', tdd = formattedTDD, keys = keysTDD)

@app.route("/delete/<int:id>/<task>", methods=["GET"])
def delete(id, task):
    boardData = db.session.get(Board, id)
    data = boardData.tdd.copy()
    for col in data:
        if task in data[col]:
            del data[col][task]
    db.session.query(Board).filter_by(id=id).update({'tdd': data})
    db.session.commit()
    return redirect(url_for('board', id=1))

@app.route("/next/<int:id>/<task>")
def nextcol(id, task):
    boardData = db.session.get(Board, id)
    data = boardData.tdd.copy()
    for index, col in enumerate(data):
        if task in data[col]:
            try:
                next_col = list(data.keys())[index + 1]
                data[next_col][task] = data[col][task]
                del data[col][task]
            except IndexError:
                pass
            break
    db.session.query(Board).filter_by(id=id).update({'tdd': data})
    db.session.commit()
    return redirect(url_for('board', id=1))

@app.route("/previous/<int:id>/<task>")
def previouscol(id, task):
    boardData = db.session.get(Board, id)
    data = boardData.tdd.copy()
    for index, col in enumerate(data):
        if task in data[col]:
            try:
                prev_col = list(data.keys())[index - 1]
                data[prev_col][task] = data[col][task]
                del data[col][task]
            except IndexError:
                pass
            break
    db.session.query(Board).filter_by(id=id).update({'tdd': data})
    db.session.commit()
    return redirect(url_for('board', id=1))

@app.route("/card/<int:id>", methods=["GET", "POST"])
def card(id):
    form = CreateCardForm()
    return render_template('card.html', form=form)

@app.route("/createboard", methods=["GET", "POST"])
def createboard():
    form = CreateBoardForm()
    if request.method == "POST":
        if form.validate_on_submit():
            board_detect = db.session.query(Board).filter_by(title=request.form['title']).first()
            if board_detect:
                flash("A board already exists with that name. Try again")
                return redirect(url_for('createboard'))
            else:
                new_board = Board(
                    title = form.board_name.data,
                    user = current_user
                )
                db.session.add(new_board)
                db.session.commit()
                board_id = db.session.query(Board).filter_by(user=current_user, title=form.board_name.data).all()[-1].id
                return redirect(url_for('addcol', id = board_id))
        else:
            flash("The board name can't be longer than 50 characters")
            return redirect(url_for('createboard'))
    else:
        return render_template('createboard.html', form=form)
    
@app.route("/addcol/<int:id>", methods=["GET", "POST"])
def addcol(id):
    form = AddColForm()
    if request.method == "POST":
        pass
    else:
        board_cols = db.session.get(Board, id).columns
        print(board_cols)
        return render_template('addcolumn.html', form = form, cols = board.columns)
    





if __name__ == "__main__":
    app.run(debug=True)
