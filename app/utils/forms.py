from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, EmailField, SubmitField,
                     BooleanField, TextAreaField)
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets.core import ColorInput


class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    email = EmailField(label='Email', validators=[Email()])
    password = PasswordField(label='Password', validators=[Length(min=5)])
    # theme = RadioField(label="Select preferred theme",
    #                    choices=[("Light"), ("Dark")],
    #                    coerce=bool)
    submit = SubmitField(label="Register")


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember me')
    submit = SubmitField(label="Login")


class CreateCardForm(FlaskForm):
    card_name = StringField(label='Card Name',
                            validators=[DataRequired(), Length(max=50)])
    card_subtitle = TextAreaField(label='Card Subtitle',
                                  validators=[DataRequired(), Length(max=150)])
    card_content = TextAreaField(label="Card Content",
                                 validators=[DataRequired()])
    card_color = StringField(label='Card Color',
                             validators=[DataRequired(), Length(max=20)],
                             widget=ColorInput())
    submit = SubmitField(label="Add Card")


class EditCardForm(CreateCardForm):
    card_name = CreateCardForm.card_name
    card_subtitle = CreateCardForm.card_subtitle
    card_content = CreateCardForm.card_content
    card_color = CreateCardForm.card_color
    submit = SubmitField(label="Edit Card")


class CreateBoardForm(FlaskForm):
    title = StringField(label='Board Name',
                        validators=[DataRequired(), Length(max=50)])
    board_color = StringField(label='Board Color',
                              validators=[DataRequired(), Length(max=20)],
                              widget=ColorInput())
    submit = SubmitField(label='Create Board')


class AddColForm(FlaskForm):
    col_name = StringField(label='Column Name',
                           validators=[DataRequired(), Length(max=50)])
    col_color = StringField(label='Column Color',
                            validators=[DataRequired(), Length(max=20)],
                            widget=ColorInput())
    submit = SubmitField(label='Add Column')


class EditColForm(FlaskForm):
    col_name = StringField(label='Column Name',
                           validators=[DataRequired(), Length(max=50)])
    col_color = StringField(label='Column Color',
                            validators=[DataRequired(), Length(max=20)],
                            widget=ColorInput())
    submit = SubmitField(label='Edit Column')


class EditBoardForm(FlaskForm):
    title = StringField(label='Board Name',
                        validators=[DataRequired(), Length(max=50)])
    board_color = StringField(label='Board Color',
                              validators=[DataRequired(), Length(max=20)],
                              widget=ColorInput())
    submit = SubmitField(label='Edit Board')