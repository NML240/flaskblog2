from flask import Blueprint, flash, render_template, redirect, url_for, render_template, request
from flask_login import login_user, login_required, current_user 
from app import db, mail 
# make bcrypt and db work 

import bcrypt

# from flask_mail import Message 
# itsdangergous... gives a time sensitive message 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.models import User 
from app.userinfo.forms import (RegistrationForm, UpdateAccountForm, EmptyForm)
from app.mail.forms import  (RequestResetPasswordForm)




import os
# make the email variable below work. 
 

mail = Blueprint('mail', __name__)




"""

def send_account_registration_email(user):

    # 'Email registration' the title
    msg = Message ('Email registration',
        sender='noreply@demo.com', 
        recipients=[user.email]) 
    msg.body = f'''To complete the registration please click on the link:
    {url_for('email.verified_email', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made. 
    ''' 
    mail.send(msg)
""" 




from redmail import outlook

 

# why user in 'the function?
# because I want a specific user. Shouldn't it be User? No because classes work differently
# verify token
def send_account_registration_email(user):
    form = EmptyForm()
    # should I use a form?
    # the function creates the randomly generated token
    # why user? Because token needs user to access the class
    token = user.create_token() # don't need to import methods just the class. Confirm?
    # needed for outlook.send for outlook
    outlook.send(
            subject="register account",
            sender="testingifjnf@outlook.com", # any way to change this to testingifjnf@outlook.com?
            receivers=[user.email],
            # remember url for won't work for some reason.
            html = render_template('verify_email.html', title='verify email',token=token, form=form, _external=True) 
    )
""" 

def send_reset_password_email(user):  
    # get the function from models.py
    token = user.create_token()
    # What is Message and sender and recipients mssg.body? and f''' ''' string and _external=True?
    # when passing into a f string use 1 "{}" curly brace instead of 2 "{{}}"
    msg = Message('Password Reset Request', 
        sender='noreply@demo.com', 
        recipients=[user.email])             
    # _external – if set to True, an absolute URL is generated. Server address can be changed via 
    # Absolute import is  https://example.com/my-page relative URL is  /my-page 
    # body gives the body of the message, iow the entire message 
    # link to reset_password.html               
    msg.body = f'''To reset your password, visit the following link:
    {url_for('userinfo.request_reset_password', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made. 
    '''
    mail.send(msg)

""" 


# This route is always a get request!!!
# verify the users email or after you clicked on the email from the recieved email
# better name for function maybe change to verify?
@mail.route("/verified_email<token>", methods = ['POST', 'GET']) 
def verified_email(token):    
    # why if I put a empty form in the app.mail.forms doesn't work? 
    form = EmptyForm()
    if request.method == 'GET' : # and form.validate():
        user = User.verify_token(token)
        if user is None: # why does this not work pytest later??
            flash('That is an invalid or expired token')
            return redirect(url_for('userinfo.home'))
        confirmation_email =  user.confirmation_email
        # why does this never execute?
        if confirmation_email is True:
            flash('You have already clicked on the confirmation email. You can now login')
            return redirect(url_for('userinfo.home'))
        # make confirmation_email True
        confirmation_email = True  
        user = User(confirmation_email=confirmation_email)  
        db.session.add(user)
        db.session.commit()
        
        return render_template('verified_email.html', title='verified email', form=form)



""" 

# creates form for email for your password reset
# better name
@mail.route("/request_reset_password", methods = ['POST', 'GET'])
def request_reset_password():

    form = RequestResetPasswordForm()
    if form.validate_on_submit():   
        email = form.email.data
        if email is None:      
            flash("Please fill in the email field"
        
        user = User.query.filter_by(email=email).first()
        
        # if the user is already verified.  
        confirmation_email = user.confirmation_email
        if confirmation_email is True:
            # flash is not working here
            flash('You already verified your email!')
            return redirect(url_for('userinfo.home')) 

        # should I check if the email exists? Or should I not for security purposes?
        send_reset_password_email(user)
        flash("An email has been sent with instructions to your email to reset the password") 
        return redirect(url_for('userinfo.home'))
    return render_template('request_reset_password.html', title='request reset password', form=form)




# reset password after recieved the token in a email
# create form for password field and confirm password
@mail.route("/reset_password/<token>", methods = ["GET"] )
def reset_password(token):
 
    form = UpdateAccountForm()
    if form.validate_on_submit():   
        # confused by adding User?
        # User is the name of the 1st database
        user = User.verify_token(token)
        if user is None:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('request_reset_password'))    
        password = form.password.data
        if password is None: 
            flash("Please fill in the password field")
        confirm_password = form.confirm_password.data
        if confirm_password is None:    
            flash("Please fill in the confirm password field")
        # get data from wtf forms iow get user inputted data from the forms
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gesalt())
        # update information already in the database 
        # do I need add?





        # make confirmation_email True
        # Use this code if adding code to the database that is not the first time  
        user.confirmation_email = True 
        db.session.add(user)
        db.session.commit()
    

        db_info = User(hashed_password=hashed_password)
        db.session.add(user_password=db_info)
        db.session.commit()
        
    # why does render_template need to go not in the POST if statement?? 
    return render_template('reset_password.html', title='reset password', token=token, form=form) 

"""















