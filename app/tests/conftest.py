from app.models import User 
import bcrypt 
import pytest 
from app import create_app
from app import db

 
# function for tests_models.py
# The scope='module' fixture allows you to pass in the function many times

@pytest.fixture(scope='module')
def plaintext_password():
    plaintext_password = 'jotpjgjbgt'
    return plaintext_password 

@pytest.fixture(scope='module')
def new_user(plaintext_password):
    
    ''' 
    Given a User model
    When a new user is being created 
    Check the User database columns
    '''
    
    # why can't I go plaintext_password() instead of plaintext_password 
   
    # username, hashed_password, email
    hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())
    user = User(username='ugbuighiug' ,email='sefefo3240@svcache.com', hashed_password=hashed_password)
    return user
 


# function for test_routes.py 

@pytest.fixture(scope='module')
def make_app_run_in_test_env():
    flask_app = create_app()
    # The with statemnt allows you to open and close files safely by making sure there is no errors
    # What is test_client/.make_app_run_in_test_env?  test_client makes requests to the application without running a live server
    # Use the test_client to check the route which is a get request
    with flask_app.test_client() as testing_client: 
        # What is this line?
        with flask_app.app_context():
            yield testing_client

   
# function for test/routes.py
@pytest.fixture(scope='module')
def init_database(make_app_run_in_test_env, new_user):

    make_app_run_in_test_env
    # Create the database and the database table 
    db.create_all()
    # Insert user data
    # fill out the data that is new.  

    user = new_user
    db.session.add(user)
    # Commit the changes for the users
    db.session.commit()
    yield  # this is where the testing happens!

    db.drop_all() # delete table after use



