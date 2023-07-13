from flask import Flask, render_template, redirect, session, flash, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Activity, Favorites
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
import requests
import os 
from sqlalchemy.orm.attributes import InstrumentedAttribute
import json
import os

DATABASE_URL = os.getenv('DATABASE_URL', "postgresql+psycopg2://khbddhaa:POp_X4nCJdP-vl8pTXZgE__fsIHJlaa6@mahmud.db.elephantsql.com/khbddhaa")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL 
# Render 
# 'postgresql:///funseeker' --> Local 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = bool(os.getenv('SQLALCHEMY_ECHO',False))
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', "please-work")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug_toolbar = DebugToolbarExtension(app)


with app.app_context():
    connect_db(app)
    db.create_all()


# Root route
@app.route('/')
def homepage():
    """Show homepage."""
    # Render the welcome page 
    return render_template('base.html')

# Login and logout routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show login page."""
    
    # Create an instance of the login form and validate it
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
    
        # Check if user exists in the database and if the password is correct
        user = User.authentication(username, password)
        
        # If the user exists, add the user to the session and redirect them.
        if user:
            session['user_id'] = user.id
            return redirect('/activity')
        else:
            # Otherwise, display an error message and re-render the login form. 
            form.username.errors = ['Invalid username/password. Please try again.']
            
    # Render the login form and pass the form to the template.
    return render_template('login.html', form=form)

    
@app.route('/logout')
def logout():
    """Logout user."""
    print("Logging out user")
    session.pop('user_id')
    print("User successfully logged out")
    return redirect('/')

#  Registration route
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Register a user."""

    form = RegisterForm()
    
    if request.method == 'POST' and form.validate():
        # Get the username and password from the form
        user = User()
        user.username = form.username.data
        user.password = form.password.data
        
    # Hash the user's password to store in the database 
    # using the register method from the User class
        new_user = User.register(user.username, user.password)

    # Save the user to the database
        db.session.add(new_user)
        db.session.commit()

    # Add the user to the session
        session['user_id'] = new_user.id

        print('User created successfully')
        return redirect('/activity')
    
    else:
        
        return render_template('register.html', form=form)

# Activities routes 
@app.route('/activity', methods=['GET', 'POST'])
def find_activity():
    
    if request.method == 'POST':
        print("Attempting to find activities")
        
        response = requests.get('https://www.boredapi.com/api/activity')
        data = response.json()

        # Extract the type of the recommended activity
        activity_type = data['type']

        # Make two additional GET requests to BoredAPI with the same type (for recommendations)
        recommended_activity1 = requests.get(f'https://www.boredapi.com/api/activity?type={activity_type}')
        recommended_activity2 = requests.get(f'https://www.boredapi.com/api/activity?type={activity_type}')
        data1 = recommended_activity1.json()
        data2 = recommended_activity2.json()
        
        # Extract the recommended activity and additional activities
        activity = data['activity']
        recommended_activities = [data1['activity'], data2['activity']]
        
        return render_template('activity.html', activity=activity, recommended_activities=recommended_activities)
    
    return render_template('activity.html')
    
     
# Favorite routes 
@app.route('/favorites')
def show_favorites():
    """Show user's favorites."""
    user_id = session['user_id']
    
    if user_id != session['user_id']:
        print('You are not authorized to view this page.')
        return redirect('/')
    
    user = User.query.get_or_404(user_id)
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    
    return render_template('favorites.html', user=user, favorites=favorites)

@app.route('/save_favorite', methods=['GET','POST'])
def save_favorite():
    """Save activity to user favorites."""
    if 'user_id' not in session:
        print('You must be logged in to view this page.')
        return redirect('/login')

    if request.method == 'POST':
        print("Attempting to add activity to favorites")
        
        # Get the activity and user id from the form
        activity = request.form['activity']
        user_id = session['user_id']
        
        # Create a new favorite
        favorite = Favorites(activity=activity, user_id=user_id)
        
        # Add the favorite to the database
        db.session.add(favorite)
        db.session.commit()
        
        print("Activity successfully saved to favorites.")
        
    return redirect('/favorites')
    
    
    
# @app.route('/remove_favorite', methods=['POST'])
# def delete_favorite():
#     """Remove an activity from a user's favorites."""
#     activity = request.form.get('activity')

#     if activity:
#         favorite = Favorites.query.filter_by(activity=activity).first()
#         if favorite:
#             db.session.delete(favorite)
#             db.session.commit()
#             print('Favorite successfully deleted!')
#         else:
#             print('Favorite not found.')

#     return redirect('/favorites/')

    
