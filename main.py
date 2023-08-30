from flask import Flask, render_template, redirect, url_for, session, request
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


@app.route("/")
def home():
    return render_template('base.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/board/<int:id>")
def board():
    

if __name__ == "__main__":
    app.run(debug=True)
