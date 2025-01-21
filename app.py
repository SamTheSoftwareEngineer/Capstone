from flask import Flask, render_template, redirect, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Favorites, Photo
from forms import RegisterForm, LoginForm, PhotoForm
from sqlalchemy.exc import IntegrityError
import random
import os 
import json 
from flask_uploads import UploadSet, configure_uploads, IMAGES


DATABASE_URL = os.getenv('DATABASE_URL', "postgresql+psycopg2://khbddhaa:POp_X4nCJdP-vl8pTXZgE__fsIHJlaa6@mahmud.db.elephantsql.com/khbddhaa")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL 
# Render 
# 'postgresql:///funseeker' --> Local database URL 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False 
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', "adnjcuiebewhbsfbdwujhb")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads/photos'


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
    if 'user_id' not in session:
        flash('You are not logged in. Please log in first.')
        return redirect('/login')
    
    # Otherwise, remove the user_id from the session and redirect them to the homepage.
    session.pop('user_id')
    print("User successfully logged out")
    return redirect('/')

#  Registration route
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()

    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, password=form.password.data)
        new_user = User.register(user.username, user.password)
    
    # Error handling for if the username is already taken
        try: 
            db.session.add(new_user)
            db.session.commit()
            print("User successfully registered")
            session['user_id'] = new_user.id
            
            return redirect('/activity')
        
        except IntegrityError:
            db.session.rollback()
            flash("The username is already taken. Please register with a different username.")
            print("Failure to register user")
            return render_template('register.html', form=form)   
             
        finally:
            db.session.close()

    return render_template('register.html', form=form)

# Activities routes 
# Helper function to load activities from the static file
def load_activities():
    json_path = os.path.join(app.static_folder, 'activities.json')
    with open(json_path, 'r') as file:
        return json.load(file)

@app.route('/activity', methods=['GET', 'POST'])
def find_activity():
    # Load all activities from the static JSON file
    all_activities = load_activities()
    
    if request.method == 'POST':
        print("Attempting to find activities")

        # Fetch a random activity
        random_activity = random.choice(all_activities)

        # Extract the activity and its type
        activity = random_activity.get('activity', "No activity found.")
        activity_type = random_activity.get('type', "general")

        # Filter activities of the same type
        recommended_activities_list = [
            act for act in all_activities if act.get('type') == activity_type and act.get('activity') != activity
        ]

        # Extract two unique recommended activities
        recommended_activities = [
            act['activity'] for act in random.sample(recommended_activities_list, min(2, len(recommended_activities_list)))
        ]

        # Render the activity and recommendations
        return render_template(
            'activity.html',
            activity=activity,
            recommended_activities=recommended_activities
        )
    
    # Render the default template for GET requests
    return render_template('activity.html')

    
     
# Favorite routes 
@app.route('/favorites')
def show_favorites():
    """Show user's favorites."""
    
    if 'user_id' not in session:
        flash('You must be logged in to view this page.')
        return redirect('/login')
    

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
        flash('You must be logged in to view this page.')
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

@app.route('/delete_favorite', methods=['POST'])
def delete_favorite():
    """Delete activity from user favorites."""
    if 'user_id' not in session:
        flash('You must be logged in to view that page.')
        return redirect('/login')

    if request.method == 'POST':
        print("Attempting to delete activity from favorites")
        
        # Get the favorite id from the form
        favorite_id = request.form['favorite_id']
        
        # Delete the favorite from the database
        favorite = Favorites.query.get(favorite_id)
        db.session.delete(favorite)
        db.session.commit()
        
        print("Activity successfully deleted from favorites.")
        
    return redirect('/favorites')


# Photo routes 

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
@app.route("/upload", methods=["GET", "POST"])
def upload_photos():

    if 'user_id' not in session:
        flash('You must be logged in to upload photos!')
        return redirect('/login')


    form = PhotoForm()

    # If the form is valid, save the photo to the database, otherwise return an error 
    if form.validate_on_submit():
        try:
            filename = photos.save(form.photo.data)
            user = User.query.get(session['user_id'])
            photo = Photo(filename=filename, user=user)
            db.session.add(photo)
            db.session.commit()
            print('Photo successfully saved to database.')
            flash('Photo uploaded successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while uploading the photo. Please try again later.', 'error')
            app.logger.error(f"Error uploading photo: {e}")

    return render_template("upload.html", form=form)

@app.route("/photos", methods=["GET", "POST"])
def show_photos():
    if 'user_id' not in session:
        flash('You must be logged in to view photos!')
        return redirect('/login')

    # Retrieve photos uploaded by the current user
    user_id = session['user_id']
    user_photos = Photo.query.filter_by(user_id=user_id).all()

    return render_template("photos.html", user_photos=user_photos)



@app.route('/delete_photo/<int:photo_id>', methods=["POST"])
def delete_photo(photo_id):
    """Delete photo from photobooth"""
    if 'user_id' not in session:
        flash('You must be logged in to delete photos!', 'error')
        return redirect('/login')

    # Retrieve the photo from the database
    photo = Photo.query.get_or_404(photo_id)

    # Check if the photo belongs to the current user
    if photo.user_id != session['user_id']:
        flash('You are not authorized to delete this photo!', 'error')
        return redirect('/photos')

    # Delete the photo file from the server
    photo_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], photo.filename)
    if os.path.exists(photo_path):
        os.remove(photo_path)
    else:
        app.logger.warning(f"Photo file '{photo_path}' not found.")

    # Delete the photo from the database
    db.session.delete(photo)
    db.session.commit()

    return redirect('/photos')
