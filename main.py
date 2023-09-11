from flask import Flask, render_template, redirect, url_for, session, request, make_response
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import JSON
from flask_session import Session
from datetime import datetime as dt
from utils.funcs import *

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


#TODO: Add user database
#TODO: Add user theme variable
#TODO: Add dropdown functionality to cards
#TODO: Add card route and template
#TODO: Change board route to reflect database
#TODO: Add new buttons to sidebar
#TODO: Figure out drag-and-drop
#TODO: Add functionality to change card column

class Board(db.Model):
    __tablename__="boards"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), nullable = False)
    tdd = db.Column(JSON, nullable = False)

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


# daboard = db.session.query(Board).get(1)
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

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/board/<int:id>", methods=["GET", "POST"])
def board(id):
    if request.method == 'GET':
        boardData = db.session.get(Board, id)
        formattedTDD = taskTimeAgo(boardData.tdd)
        return render_template('board.html', tdd = formattedTDD)
    

if __name__ == "__main__":
    app.run(debug=True)
