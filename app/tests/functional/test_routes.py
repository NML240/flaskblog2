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
    client = client()
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
    client = client()
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
 
def check_token(user):
    token = user.create_token() 
    assert token != None # assert user?
    verify_token = user.verify_token(token)
    assert verify_token != None # assert user? 



token_app = create_app(TokenPytestConfig)
''' 
migrate = Migrate(token_app, db)
token_app.config.from_object(TokenPytestConfig)
'''

#why does normal scope in pytest work if it in the documentation it says it can be only run once?
def test_verified_email(token_client, new_user):
     

    token_client = token_client()

    ''' 
    GIVEN a Flask application configured for testing
    WHEN the "/verified_email<token>" request is (GET) Also test the email is sent.
    THEN check that the response is valid and the email is True in the database,
    prior it is false in the database.
    '''   
    


    response = token_client.get("/verified_email<token>", follow_redirects=True)
    assert response.status_code == 200
    

    with token_app.app_context():
        db.session.add(new_user)
        db.session.commit()
        ''' 
        check if the User/token has a value. If it throws an error then the function
        if User is None is running all the time.
        '''

        email_for_pytesting = User.query.filter_by(email=new_user.email).first()

        # check if the pytesting_email has a value
        assert email_for_pytesting != None 
        db.session.delete(new_user)
        db.session.commit() 


        
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
        """  
    
    
        

