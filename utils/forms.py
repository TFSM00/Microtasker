from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from flask_ckeditor import CKEditorField

class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    email = EmailField(label='Email', validators=[Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    theme = SelectField(label="Select preferred theme (can be changed later)", choices=[(True, "Light"), (False, "Dark")], validate_choice=True)
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