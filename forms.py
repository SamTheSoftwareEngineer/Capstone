"""Contains forms for the application."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Username"})
    password = PasswordField('Password', render_kw={"placeholder": "Password"})


class RegisterForm(FlaskForm):
    """Form for registering a user."""
    username = StringField('Username')
    password = PasswordField('Password')

class FeedbackForm(FlaskForm):
    """Form for the user to send feedback to devs."""
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email, validators=[InputRequired()])')
    message = TextAreaField('Message', validators=[InputRequired()])