# Funseeker

To run this app, please follow these instructions:
1. Clone this repository to your local machine
2. Create the database using 'createdb funseeker' in terminal or command prompt (recommended to use PostgresSQL)
2. Run 'python -m venv venv' to create a virtual environment
3. Run 'source venv/bin/activate' to activate the virtual environment
4. Run 'pip install -r requirements.txt' to install the required packages and dependencies
5. Run 'python app.py' to start the app or 'flask run' if you have flask installed (recommended to use flask)

# Project Description
This project is the first in two capstone projects created as part of Springboard's Software Engineering Coursework. The application seeks to connect to the Bored API (located here: https://www.boredapi.com/) and return an activity for the user to do based on preferences and other criteria. 

MVP for this project includes:
* Once a user selects an activity, the application will recommend another activity similar to the one chosen.  
* The user can also save activities to a list of favorites and view them later.
* Users can register to use the application for login/logout functionality.

Some reach goals for this project include:
* Allowing users to add their own activities to the database
* Adding a feature that allows users to add their own activities to the database
* Allowing users to be able to share their completed activities on social media
* Adding a feature that allows users to be able to share their activities with other users
* Adding a feature that allows users to leave reviews and ratings on activities
* Incorporating a 'photo album' feature that allows users to upload photos of their completed activities with date-time stamps

# Technologies Used
* Python
* Flask
* SQLAlchemy
* PostgreSQL
* HTML
* CSS
* Bootstrap
* WTForms 
* Jinja

# Additional Notes
Please note that this project is still a work in progress and is used for educational and portfolio purposes only. I have included a seed.py file that parses and loads the data from the Bored API into the database for use within this appliction. All API related accrediation goes to the Bored API (https://www.boredapi.com/) and its original creators, contributors, and maintainers.
