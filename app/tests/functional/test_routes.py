import email
import os
# from types import new_class 
import bcrypt
from app.models import User
from flask_migrate import Migrate
import pytest


from app import create_app, db
from app.config import PytestConfig, TokenPytestConfig

app = create_app(PytestConfig)

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


app = create_app(PytestConfig)
app.app_context().push()



 
    

#why does normal scope in pytest work if it in the documentation it says it can be only run once?

def test_verified_email(client, new_user):   
    ''' 
    GIVEN a Flask application configured for testing
    WHEN the "/verified_email<token>" request is (GET) Also test the token is created and verified. email is sent
    THEN check that a token works.
    '''   


    response = client.get("/verified_email<token>", follow_redirects=True)
    assert response.status_code == 200
    with app.test_request_context():                   
        # Create the database and the database table
        # Insert user data
        db.session.add(new_user)
        # Commit the changes for the users
        db.session.commit()
        # Why does this work?
        try:
            user = User.query.filter_by(username=new_user.username).first()
            token = user.create_token()

            assert token != None # assert user?
            user = User.verify_token(token)
            assert user == None 
        finally:
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
        '''
        """ 
    
        