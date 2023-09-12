from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    email = EmailField(label='Email', validators=[Email()])
    password = PasswordField(label='Password', validators=[Length(min=5)])
    theme = RadioField(label="Select preferred theme", choices=[("Light"), ("Dark")], coerce=bool)
    submit = SubmitField(label="Register")

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember me')
    submit = SubmitField(label="Register")

class CreateCardForm(FlaskForm):
    card_name = StringField(label='Card Name', validators=[DataRequired(), Length(max=50)])
    card_subtitle = TextAreaField(label='Card Subtitle', validators=[DataRequired(), Length(max=150)])
    card_content = TextAreaField(label="Card Content", validators=[DataRequired()])
    submit = SubmitField(label="Add Task")

class CreateBoardForm(FlaskForm):
    board_name = StringField(label='Board Name', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField(label='Create Board')

class AddColForm(FlaskForm):
    col_name = StringField(label='Column Name', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField(label='Add Column')
