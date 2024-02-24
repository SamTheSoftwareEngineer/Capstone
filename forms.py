"""Contains forms for the application."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileAllowed, FileField
class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Username"})
    password = PasswordField('Password', render_kw={"placeholder": "Password"})


class RegisterForm(FlaskForm):
    """Form for registering a user."""
    username = StringField('Username')
    password = PasswordField('Password')

class PhotoForm(FlaskForm):
    photo = FileField("Upload Photo", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'heic'], 'Images only!')])
    submit = SubmitField('Upload')