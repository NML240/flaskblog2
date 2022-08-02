from app.models import User 
import bcrypt 
import pytest 
from app import db
import os 
from flask import Flask  
 
 # make SQLAlchemy work 
from flask_sqlalchemy import SQLAlchemy
# make flask-migrate work
from flask_migrate import Migrate

# make login work
from flask_login import LoginManager 

from flask_redmail import RedMail 

from app.config import Pytest_Config

 
# setup databases
db = SQLAlchemy()


# Make @login_required work
login_manager = LoginManager()
# You get a custom login message when @login_required appears in the code.
login_manager.login_message_category = 'Login is required'

# The name you would use is the name in url_for() for the login route.
# Should I use userinfo.login? 
login_manager.login_view = 'login' 

# make csrf protection work 
from flask_wtf.csrf import CSRFProtect
# Setup CSRF protection. This allows html forms to work and be secure
csrf = CSRFProtect()

# make mail work?
email = RedMail()
# make it so @login_required sends you to the login page. 


@pytest.fixture()
def create_app(config_obj=Pytest_Config):
    app = Flask(__name__)

    app.config.from_object(config_obj)
    
    app.debug = True
    db.init_app(app)
    login_manager.init_app(app)
    email.init_app(app) 

    yield app 
    # unyield here?



# function for tests_models.py
# The scope='module' fixture allows you to pass in the function many times?
# use "@pytest.fixture(scope='module')" when in a different file or folder?
@pytest.fixture()
def new_user():
    
    """
    Given a User model
    When a new user is being created 
    Check the User database columns
    """
    
    # why can't I go plaintext_password() instead of plaintext_password 
    
    plaintext_password = 'pojkp[kjpj[pj'
    hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())  
    current_user = User(username='fkpr[kfkuh', hashed_password=hashed_password, email=os.environ['TESTING_EMAIL_USERNAME'],
    confirmation_email=False)
    return current_user
 
 

 
@pytest.fixture()
def init_database(new_user):
  
    # Create the database and the database table 
    db.create_all()
    # Insert user data
    # fill out the data that is new. ]
    
    db.session.add(new_user)
    # Commit the changes for the users
    db.session.commit()
    yield # this is where the testing happens!
    
    db.drop_all() # delete table after use



# function for test_routes.py 
 
@pytest.fixture()
def make_app_run_in_test_env(create_app):
    flask_app = create_app
    # The with statemnt allows you to open and close files safely by making sure there is no errors
    # What is test_client/.make_app_run_in_test_env?  test_client makes requests to the application without running a live server
    # Use the test_client to check the route which is a get request or post request
    with flask_app.test_client() as testing_client: 
        # What is this line?
        with flask_app.app_context():
            yield testing_client
 
   


    
   










