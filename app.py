from flask import Flask, render_template, redirect, session, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Favorites
from forms import RegisterForm, LoginForm, FeedbackForm
import requests
import os 
import configure_test



DATABASE_URL = os.getenv('DATABASE_URL', "postgresql+psycopg2://khbddhaa:POp_X4nCJdP-vl8pTXZgE__fsIHJlaa6@mahmud.db.elephantsql.com/khbddhaa")

app = Flask(__name__)

if os.environ.get("FLASK_ENV") == "test":
    app.config['SQLALCHEMY_DATABASE_URI'] = configure_test.TEST_DATABASE_URL
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
     
# Render 
# 'postgresql:///funseeker' --> Local 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False 
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
        
        if User.query.filter_by(username=user.username).first():
            flash("That username is already taken. Please choose a different one or log in.", 'warning')
        
    # Hash the user's password to store in the database 
    # using the register method from the User class
        new_user = User.register(user.username, user.password)

    # Save the user to the database
        db.session.add(new_user)
        db.session.commit()

    # Add the user to the session
        session['user_id'] = new_user.id

        flash('User created successfully', 'success')
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
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        flash('You are not authorized to view this page. Please log in or register', 'warning')
        return redirect('/')
    
    user = User.query.get_or_404(user_id)
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    
    return render_template('favorites.html', user=user, favorites=favorites)

@app.route('/save_favorite', methods=['GET','POST'])
def save_favorite():
    """Save activity to user favorites."""
    if 'user_id' not in session:
        flash('You must be logged or registered to view this page.', 'warning')
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
    
# # Feedback routes

# @app.route('/feedback', methods=['GET', 'POST'])
# def feedback_form():
    
#     form = FeedbackForm() 
    
#     if request.method == "POST" and form.validate():
        
#         print("Saving feedback in database...")
        
#         # Get user information and content from the form
#         name = request.form['name']
#         email = request.form['email']
#         message = request.form['message']
        
#         new_feedback = FeedbackForm(name=name, email=email, message=message)
        
#         # Save feedback to database 
#         db.session.add(new_feedback)
#         db.session.commit()
        
#         print(f"Feedback saved successfully. Thank you {name}! ")
        
#         # Redirect to feedback page
#         return redirect(url_for('/feedback'))
        
        
#     else:
#         return render_template('feedback.html', form=form)
