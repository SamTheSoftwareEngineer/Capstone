"""Contains models for the application."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    
class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    
    @classmethod
    def register(cls, username, password):
        """Register user with hashed password and return user."""
        
        hashed_pwd = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed_pwd.decode('utf8')
        
        user = cls(username=username, password=hashed_utf8)
        
        db.session.add(user)
        return user
    
    @classmethod
    def authentication(cls, username, password):

        print(f"Authenticating user: {username}")
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            print(f"Authentication successful for user: {username}")
            return user
        else:
            print(f"Authentication failed for user: {username}")
            return False 
        

class Activity(db.Model):
    
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.Text, nullable=False)
    participants = db.Column(db.Integer, nullable=False)
    kidFriendly = db.Column(db.Boolean, nullable=False)
    accessibility = db.Column(db.Float, nullable=False)

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, activity, user_id):
        self.activity = activity
        self.user_id = user_id


# class Feedback(db.Model):
#     __tablename__ = 'feedback'
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.Text, nullable=False)
#     email = db.Column(db.Text, nullable=False)
#     message = db.Column(db.Text, nullable=False)
    
    
    
    
    