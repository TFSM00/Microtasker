from flask import Flask, render_template, redirect, url_for, session, request, make_response
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import JSON
from flask_session import Session

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

@app.route("/board/<int:id>")
def board(id):
    return render_template('board.html')
    

if __name__ == "__main__":
    app.run(debug=True)
