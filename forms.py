"""Contains forms for the application."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Username"})
    password = PasswordField('Password', render_kw={"placeholder": "Password"})


class RegisterForm(FlaskForm):
    """Form for registering a user."""
    username = StringField('Username')
    password = PasswordField('Password')

class FeedbackForm(FlaskForm):
    """Form for adding feedback."""
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    content = StringField('Content', validators=[InputRequired()])
    submit = SubmitField('Submit')