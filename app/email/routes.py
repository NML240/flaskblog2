from flask import Blueprint, flash, render_template, request, redirect, url_for, abort, send_from_directory, render_template, session
from flask_login import login_user, login_required, current_user 
from app import db, mail 
# make bcrypt and db work 

import bcrypt

from flask_mail import Message 
# itsdangergous... gives a time sensitive message 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.models import User 
from app.userinfo.forms import RegistrationForm, UpdateAccountForm
from app.email.forms import RequestResetPasswordForm 


email = Blueprint('email', __name__)
# why user in the function?
# because I want a specific user. Shouldn't it be User? No because classes work 
def send_account_registration_email(user):
    # the function creates the randomly generated token
    # why user? Because token needs user to access the class
    token = user.create_token()
    # 'Email registration' the title
    msg = Message ('Email registration',
        sender='noreply@demo.com', 
        recipients=[user.email]) 
    msg.body = f'''To complete the registration please click on the link:
    {url_for('email.verified_email', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made. 
    ''' 
    mail.send(msg)

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




# verify the users email or after you clicked on the email from the recieved email
# better name for function maybe change to verify?
@email.route("/verified_email<token>", methods = ['POST', 'GET'])
def verified_email(token): 
     
    user = User.verify_token(token)
    	
    # if the user is already verified  
    confirmation_email = user.confirmation_email
    if confirmation_email is True:
        # flash is not working here
        flash('You already verified your email!')
        # I don't think I need  redirect below
        return redirect(url_for('userinfo.login'))   
  
    # make confirmation_email True
    # Use this code if adding code to the database that is not the first time  
    email = user.email
    user = User.query.filter_by(email=email).first_or_404() 
    user.confirmation_email = True  
    db.session.add(user)
    db.session.commit()
    
    form = RegistrationForm
    return render_template('verified_email.html', title = 'verified email', form=form)



# creates form for email for your password reset
# better name
@email.route("/request_reset_password", methods = ['POST', 'GET'])
def request_reset_password():

    form = RequestResetPasswordForm()
    if form.validate_on_submit():   
        email = form.email.data
        if email is None:      
            flash("Please fill in the email field")
        
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
@email.route("/reset_password/<token>", methods = ["GET"] )
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

















