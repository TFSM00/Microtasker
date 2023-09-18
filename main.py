from flask import (flash, redirect, render_template, request,
                   session, url_for, abort)
from flask_login import current_user, login_required, login_user, logout_user

from functools import wraps

from werkzeug.security import check_password_hash, generate_password_hash

from app import create_app
from models import Board, Card, Column, User
from utils.forms import (AddColForm, CreateBoardForm, CreateCardForm,
                         EditCardForm, LoginForm, RegisterForm)

app, db, login_manager = create_app()

# TODO: Add card route and template
# TODO: Change theme function to modify db entry
# TODO: Add user mark to cards
# TODO: Edit board names
# TODO: Edit and Delete boards, columns
# TODO: Add remember me function
# TODO: Add card modal
# TODO: Add color to column top
# TODO: Add color picker to column form and color entry to db
# TODO: Standardize card creation and hours ago func


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if current_user.id == 1:
                return func(*args, **kwargs)
            else:
                return abort(403)
        except AttributeError:
            return abort(403)
    return wrapper

# db.drop_all()
# db.create_all()

@app.route("/theme", methods=["POST"])
def theme():
    """
    Receives a theme string and a path, saves the theme to a cookie
    and redirects back to the page from the post request is made.
    """
    if current_user.is_authenticated:
        current_user.theme = request.args.get('theme')
        db.session.commit()

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
        user = db.session.query(User)\
            .filter_by(username=request.form["username"]).first()
        
        if user:
            if check_password_hash(user.password, request.form["password"]):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Wrong password. Try again.')
                return redirect(url_for('login'))
        else:
            flash('User does not exist.')
            return redirect(url_for('login'))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.session.query(User)\
                .filter_by(email=request.form["email"]).first()

            user_check = db.session.query(User)\
                .filter_by(username=request.form['username']).first()

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
@login_required
def board(id):
    board_object = db.session.get(Board, id)
    if request.method == 'GET':
        return render_template('board.html', board = board_object)

@app.route("/delete/<int:board_id>/<int:card_id>")
@login_required
def delete(card_id, board_id):
    card_data = db.session.get(Card, card_id)
    db.session.delete(card_data)
    db.session.commit()
    return redirect(url_for('board', id=board_id))

@app.route("/card/<int:id>", methods=["GET", "POST"])
@login_required
def card(id):
    print(id)
    form = CreateCardForm()
    return render_template('card.html', form=form)

@app.route("/editcard/<int:card_id>", methods=["GET", "POST"])
@login_required
def editcard(card_id):
    card_data = db.session.get(Card, card_id)
    form = EditCardForm(
            card_name = card_data.card_name,
            card_subtitle = card_data.card_subtitle,
            card_content = card_data.card_content)
    col_data = db.session.get(Column, card_data.column_id)
    if request.method == "POST":
        if form.validate_on_submit():
            card_data.card_name = form.card_name.data
            card_data.card_subtitle = form.card_subtitle.data
            card_data.card_content = form.card_content.data
            card_data.user = current_user
            card_data.column = col_data
            card_data.board = db.session.get(Board, col_data.board_id)
            db.session.commit()
            return redirect(url_for('board', id=col_data.board_id))
    else:
        return render_template('editcard.html', form=form, col=col_data, card=card_data)
    
@app.route("/newcard/<int:col_id>", methods=["GET", "POST"])
@login_required
def newcard(col_id):
    form = CreateCardForm()
    col_object = db.session.get(Column, col_id)
    if request.method == "POST":
        if form.validate_on_submit():
            newCard = Card(
                card_name = form.card_name.data,
                card_subtitle = form.card_subtitle.data,
                card_content = form.card_content.data,
                user = current_user,
                column = col_object,
                board = db.session.get(Board, col_object.board_id)
            )
            db.session.add(newCard)
            db.session.commit()
            return redirect(url_for('board', id=col_object.board_id))
    else:
        return render_template('createcard.html', form=form, col_id=col_id, col_name=col_object.column_name )

@app.route("/createboard", methods=["GET", "POST"])
@login_required
def createboard():
    form = CreateBoardForm()
    if request.method == "POST":
        print(form.errors)
        if form.validate_on_submit():
            board_detect = db.session.query(Board).filter_by(title=request.form['title']).first()
            if board_detect:
                flash("A board already exists with that name. Try again")
                return redirect(url_for('createboard'))
            else:
                new_board = Board(
                    title = form.title.data,
                    user = current_user
                )
                db.session.add(new_board)
                db.session.commit()
                board_id = db.session.query(Board).filter_by(user=current_user, title=form.title.data).all()[-1].id
                return redirect(url_for('addcol', id = board_id))
        else:
            flash("The board name can't be longer than 50 characters")
            return redirect(url_for('createboard'))
    else:
        return render_template('createboard.html', form=form)
    
@app.route("/addcol/<int:id>", methods=["GET", "POST"])
@login_required
def addcol(id):
    form = AddColForm()
    if request.method == "POST":
        if form.validate_on_submit():
            board_object = db.session.get(Board, id)
            col_check = db.session.query(Column).filter_by(column_name=form.col_name.data, board=board_object).first()
            if col_check:
                flash("A column with this name already exists in this board. Try again")
                return redirect(url_for('addcol', id=id))
            else:
                newCol = Column(
                    column_name = form.col_name.data,
                    user = current_user,
                    board = board_object
                )
                db.session.add(newCol)
                db.session.commit()
                return redirect(url_for('addcol', id=id))
        else:
            flash("The column name can't have more than 50 characters")
            return redirect(url_for('addcol', id=id))
    else:
        board_object = db.session.get(Board, id)
        return render_template('addcolumn.html', id = board_object.id, form = form, cols = board_object.columns)
    

@app.route('/update-position', methods=["POST"])
@login_required
def update_position():
    col_id = request.form['col_id']
    card_id = request.form['card_id']
    col_data = db.session.get(Column, col_id)
    board_data = col_data.board
    card_data = db.session.get(Card, card_id)

    new_card = Card(
            card_name = card_data.card_name,
            card_subtitle = card_data.card_subtitle,
            card_content = card_data.card_content,
            user = card_data.user,
            column = col_data,
            board = board_data,
            date_created = card_data.date_created
        )
    db.session.add(new_card)
    db.session.delete(card_data)
    db.session.commit()
    return ('', 204)

if __name__ == "__main__":
    app.run(debug=True)