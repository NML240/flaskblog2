import email
import os
# from types import new_class 
import bcrypt
from app.models import User
from flask_migrate import Migrate
import pytest


from app import create_app, db
from app.config import PytestConfig, TokenPytestConfig
# why just TestConfig in the create app function?

 

app = create_app(PytestConfig)
''' 
migrate = Migrate(app, db)
app.config.from_object(PytestConfig)
'''
from redmail import EmailSender

def test_register_page_get(client):
    
    #with client:  
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/register requested (GET) 
    THEN check that the response is valid 
    '''
    response = client.get('/register')
    '''
    In Python, the assert statement is used to continue the execute if the given condition evaluates to True. 
    If the assert condition evaluates to False, then it raises the AssertionError exception with the specified error message.
    '''
    # Why use a b string? What is response.data? Answer it only work if I have a status code 200.
    assert response.status_code == 200
    assert b'register' in response.data
        
    

def test_register_page_post(client):
    
    ''' 
    GIVEN a Flask application configured for testing
    WHEN the '/register requested (POST) 
    THEN check that the response is valid 
    '''   
    response = client.post('/register')
    '''
    In Python, the assert statement is used to continue the execute if the given condition evaluates to True. 
    If the assert condition evaluates to False, then it raises the AssertionError exception with the specified error message.
    '''
    # Why use a b string? What is response.data? Answer it only work if I have a status code 200.
    assert response.status_code == 200
    assert b'register' in response.data






# why does this need to be a fixture and not a function?
 




token_app = create_app(TokenPytestConfig)
token_app.app_context().push()
''' 
migrate = Migrate(token_app, db)
token_app.config.from_object(TokenPytestConfig)
'''

''' 
def create_token(new_user):
    # select user after adding new user new_user is like form.username email
    user = User.query.filter_by(email=new_user.username).first()  
    # if token: # not none or iow some value 
    token = user.create_token()
    assert token != None # assert user?
    print(token) 
    return token 
''' 
''' 
# user is where I select the email 
def verify_token(new_user, create_token):
    # select user after adding new user new_user is like form.username email
    user = User.query.filter_by(email=new_user.username).first()
    token = create_token(user)
    verify_token = user.verify_token(token)
    assert token != None 
    print(verify_token)
    return verify_token 


def add_and_delete_database_try(new_user, create_token, verify_token):            
    try:
        db.session.add(new_user)
        db.session.commit()  
        # select user after adding new user   
        create_token(new_user)
        verify_token(new_user, create_token)
    except:
        db.session.rollback()



def foo():
    raise ValueError('foo')
    raise ValueError('boo')


def test_passes():
    with pytest.raises(ValueError) as e_info:
        n = len(e_info.value.args[-1])
        for element in range (len(e_info.value.args[n])):    
            assert e_info.value.args[element] == 'foo'
 
'''     
def test_try():
    try:
        a = 1
        b = 2 
        raise Exception( a != b)
    except Exception:
        print("do nothing")
    



''' 
def test_passes():
    with pytest.raises(ValueError) as e_info:
        test_try()
    assert e_info.value == 'foo'

'''

'''
def test_try_prints():
    with pytest.raises(Exception): 
        test_try()
        # assert add_and_delete_database_try == 
        assert 4  ==  pytest.raises(Exception).value.args[0]  
'''

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

 

#why does normal scope in pytest work if it in the documentation it says it can be only run once?
def test_verified_email(token_client, new_user):   
    ''' 
    GIVEN a Flask application configured for testing
    WHEN the "/verified_email<token>" request is (GET) Also test the token is created and verified. email is sent
    THEN check that a token works.
    '''   

    
    response = token_client.get("/verified_email<token>", follow_redirects=True)
    assert response.status_code == 200
    with token_app.test_request_context():                   
        init_database_for_tokens(new_user)  
    

        
# assert user?
        # if asserts work this will run.    
        
 


 
 
 
  
    

  
       

    '''            
            raise Exception('value must be 0 or None')


        If I get an assertion error,
        the code will work the firt time and the code runs. 
        The next time the code runs I will have added the username etc 2 times.
        This will cause the except block to run due to a database error. 
    '''
        
            #db.session.delete(new_user)
            #db.session.commit()          
            # db.session.rollback()        
''' 
        check if the User/token has a value. If it throws an error then the function
        if User is None is running all the time.
        '''
    

                



        
""" 
        # Just put something as host and port
        email = EmailSender(host="localhost", port=0)
       
        msg = email.get_message(
            subject='email subject',
            sender="me@example.com",
            receivers=['you@example.com'],
            text="Hi, this is an email.",
        )
        assert str(msg) == '''from: me@example.com
        subject: email subject
        to: me@example.com
        Content-Type: text/plain; charset="utf-8"
        Content-Transfer-Encoding: 7bit
        MIME-Version: 1.0
        Hi, this is an email.'''
              
        assert str(msg) == 'i'
        '''
        """ 
    
        