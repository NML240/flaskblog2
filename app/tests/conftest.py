#from cgi import test
from app.models import User 
import bcrypt 
import pytest 
 
import os
 
from app.models import User 
#from app.tests.config import Test_Config 
from app import create_app, db
from app.config import TestConfig
from flask_migrate import Migrate 



# why do I have to declare the variables outside the fixtures? 
# why does Test_Config take no argumnts?
# Is this the correct way to handle this error by creating Test_app?

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
    confirmation_email=False, reset_email_password=False)
    return current_user
    
# TestConfig() takes no arguments why?
app = create_app(TestConfig)
@pytest.fixture()

# IOW the function is client
# what exactly is a client?
def client():
    # make_app_run_in_test_env = client
    return app.test_client


# what is the point of this?
@pytest.fixture()
def runner():
    return app.test_cli_runner()


    
    

