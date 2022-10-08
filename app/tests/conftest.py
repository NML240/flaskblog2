import bcrypt 
import pytest 
import os 
from app.models import User, ConfirmationEmail

from app import create_app, db
from app.config import PytestConfig, TokenPytestConfig 
from flask_migrate import Migrate 


# why do I have to declare the variables outside the fixtures? 
# why does Test_Config take no argumnts?
# Is this the correct way to handle this error by creating Test_app?

# function for tests_models.py
# The scope='module' fixture allows you to pass in the function many times?
# use "@pytest.fixture(scope='module')" when in a different file or folder?


@pytest.fixture()
def new_user(): 
    '''
    Given a User model
    When a new user is being created 
    Check the User database columns
    '''
    # example password
    plaintext_password = 'pojkp[kjpj[pj'
    # converting password to array of bytes
    bytes = plaintext_password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hashed_password = bcrypt.hashpw(bytes, salt)
    current_user = User(username='fkpr[kfkuh',hashed_password=hashed_password, email=os.environ['TESTING_EMAIL_USERNAME'])

    return current_user
    
'''
@pytest.fixture()
def new_confirmation_(): 


    return current_confirmationemail
'''
app = create_app(PytestConfig)
''' 
migrate = Migrate(app, db)
app.config.from_object(PytestConfig)
'''
@pytest.fixture()
# IOW the function is client
# what exactly is a client?
def client():
    # make_app_run_in_test_env = client
    return app.test_client()


# what is the point of this?
@pytest.fixture()
def runner():
    return app.test_cli_runner()







token_app = create_app(TokenPytestConfig)



@pytest.fixture()
# IOW the function is client
# what exactly is a client?
def token_client():
    # make_app_run_in_test_env = client
    return token_app.test_client()


# what is the point of this?
@pytest.fixture()
def token_runner():
    return token_app.test_cli_runner()

# Why can't the code below be located here?
"""
@pytest.fixture() 
def init_database_for_tokens(new_user):
    # Create the database and the database table
    db.create_all(token_app)
    # Insert user data
    db.session.add(new_user)
    # Commit the changes for the users
    db.session.commit()
    ''' 
    yield freezes till the functions ends. 
    This also allows you to create and delete the database 
    while putting code inbetween
    '''
    yield db.drop_all(token_app)
     
    user = User.query.filter_by(username=new_user.id).first()
    token = user.create_token()
    print(token) 
    assert token != None # assert user?
    verify_token = User.verify_token(token)
    print(verify_token)
    assert verify_token != None 
"""
