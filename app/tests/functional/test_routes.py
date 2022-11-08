import email
import os
# from types import new_class 
import bcrypt
from app.models import User#, ConfirmationEmail
from flask_migrate import Migrate
import pytest


from app import create_app, db
from app.config import PytestConfig#, TokenPytestConfig


from flask import flash
from sqlalchemy import exc

app = create_app(PytestConfig)

from redmail import EmailSender

 






''''
token_app = create_app(PytestConfig)
token_app.app_context().push()
'''

app = create_app(PytestConfig)
app.app_context().push()




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
    # checks the html for the string register
    assert b'register' in response.data
        

def check_if_the_username_is_already_taken(forms_username):     
    # do I need a try?
    # I don't need passwords because people can have the same password  
    
    users = User.query.filter_by(username=forms_username).all()
    assert users != None
    for all_users in users:
        assert all_users != None 
        if all_users.username == forms_username:
            flash ("The username is already taken. Please select another")
            return all_users.username 


def check_if_the_email_is_already_taken(forms_email):
    
    # do I need a try?
    # I don't need passwords because people can have the same password
    users = User.query.filter_by(username=forms_email).all()
    for all_users in users:
        if all_users.email == forms_email:    
            flash("The email is already taken. Please select another") 
            return all_users.email

def test_register_page_post(client, new_user):
    
    ''' 
    GIVEN a Flask application configured for testing
    WHEN the '/register requested (POST) 
    THEN check that the response is valid 
    '''   
    response = client.post('/register')
    
    assert response.status_code == 200
    assert b'register' in response.data

    with app.test_request_context():                   

        try:
            assert new_user != None   
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
        finally:
            try:
                users = User.query.filter_by(username=new_user.username).all()
                assert users == None
                for all_users in users:
                    assert all_users == None 
                    if all_users.username == new_user.username:
                        flash ("The username is already taken. Please select another")
                        assert all_users.username == None
                #assert check_if_the_username_is_already_taken(new_user.username) != None 
                #assert check_if_the_email_is_already_taken(user.email) != None   
            finally:
                db.session.rollback()        
       
     
    





# why does this need to be a fixture and not a function?
 







 
    

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
        # add try
         

        # if the new_user is already added delete the user  
        # This is try is if an error occurs in the try below.
        # Else the new_user is eventually added outside the try
        
        
        
        # Why does this work?    
        #Is this to convulted?
        try:   
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
        finally:
            try:
                user = User.query.filter_by(username=new_user.username).first()
                token = user.create_token()
                assert token != None # assert user?
                user = User.verify_token(token)
                assert user != None
                
                user.registration_confirmation_email = True 
                registration_confirmation_email = user.registration_confirmation_email  
                
                user.reset_email_password = True
                reset_email_password = user.reset_email_password
                # test the line below with user and new_user while deleting
                new_user = User(registration_confirmation_email=registration_confirmation_email, 
                                            reset_email_password=reset_email_password)
                db.session.add(new_user)
                db.session.commit()

                user = User.query.filter_by(registration_confirmation_email=registration_confirmation_email).first()
                assert user.registration_confirmation_email == False

            finally:
                db.session.delete(new_user)
                db.session.commit()
       
       
 
 
 
 
 
 
 
 
 
 
 
 
 
 
       








        ''' 
        try:   
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
        finally:
            try:
                user = User.query.filter_by(username=new_user.username).first()
                user != None 
                user.id != None 
                token = user.create_token()
                assert token != None # assert user?
                user = User.verify_token(token)
                assert user != None
                
                # testing ConfirmationEmail 
                confirmation_email = ConfirmationEmail(email=user.email)
                assert confirmation_email != None 

                db.session.add(confirmation_email)
                db.session.commit()
                
                
                confirm_email = ConfirmationEmail.query.filter_by(user_id=user.id)

                registration_confirmation_email = confirm_email.registration_confirmation_email 
                assert registration_confirmation_email == False
                
                registration_confirmation_email = True 
                assert registration_confirmation_email == True

                confirmation_email = ConfirmationEmail(registration_confirmation_email=registration_confirmation_email)
                db.session.add(confirmation_email)
                db.session.commit()
                

            finally:
                db.session.rollback()

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
    
        