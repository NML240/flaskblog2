from flask import Flask, Blueprint, flash, render_template, request, redirect, url_for, abort, send_from_directory, render_template, session
from flask_login import login_user, login_required, current_user 
from app import db, mail, app
# make bcrypt and db work 
import bcrypt
from flask_mail import Message
from app.userinfo.forms import ResetPasswordTokenForm ,UpdateAccountForm  
# itsdangergous... gives a time sensitive message 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# import for the function verify_token
from app.models import User 


userinfo = Blueprint('userinfo', __name__)

# get_reset_token = create_token
# def verify_reset_token(token) = verify_token 
def create_token(self, expires_sec=1800):
    # Serializer gives 
    s = Serializer(app.conf['secret_key'], expires_sec) 
    #gives randomly assigned token as long as less then 30 min   
    return s.dumps({'user_id': self.id}).decode('utf-8')
    

    
# why @staticmethod?
@staticmethod
def verify_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None 
        # return print("testing")
    return User.query.get(user_id)




# why user in the function?\
# because I want a specific user. Shouldn't it be User?
def send_account_registration_email(users_email):
    # the function creates the randomly generated token
    # why user? 
    token = users_email.create_token()
    # 'Email registration' the title
    msg = Message ('Email registration',
        sender='noreply@demo.com', 
        recipients=[users_email.email]) 
    msg.body = f'''To complete the registration please click on the link:
    {url_for('userinfo.verified_email', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made. 
    ''' 
    mail.send(msg)






# verify the users email or after you clicked on the email from thev recieved email
# better name for function?
@userinfo.route("/verified_email<token>", methods = ['POST', 'GET'])
def verify_email(token):
    # Why User?
    # checks for errors  
    user = User.verify_token(token)
    # explain the code 
    if user is None:
        flash('That is an invalid or expired token')
        # correct?
        return redirect(url_for('userinfo.home'))
    # make confirmation_email True
    confirmation_email = True  
    db_info = User(confirmation_email=confirmation_email)  
    db.session.add(db_info)
    db.session.commit()
    return render_template('verified_email.html', title = 'verified email')

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
    {url_for('userinfo.verified_email', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made. 
    '''
    mail.send(msg)


# Code below resets your email
# email the resetted password
#better name
@userinfo.route("/request_reset_password", methods = "POST, GET" )
def request_reset_password():
    # if the user is logged in make so they can't go to the register page. 
    if current_user.is_authenticated:
        return redirect(url_for(('userinfo.home')))
    form = ResetPasswordTokenForm
    if form.validate_on_submit():
        # get email from the database , better name?
        email = form.email.data
        if email is None:      
            flash("Please fill in the email field")
              
        user = User.query.filter_by(email=email).first()
        send_reset_password_email(user)
        flash("An email has been sent with instructions to your email to reset the password")    
        return render_template('request_reset_password_token.html', title='request reset password', form=form)


# reset password after recieved the token in a email
@userinfo.route("/reset_password/<token>", methods = "POST, GET" )
def reset_password_token(token):
    # if the user is logged in make so they can't go to the register page. 
    # take a lot of the cod from register.
    
    if current_user.is_authenticated:
        return redirect(url_for(('userinfo.home')))
    form = UpdateAccountForm
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
        db_info = User(hashed_password=hashed_password)
        db.session.add(user_password=db_info)
        db.session.commit()
        # login user. Should I use next or login?                                      
        flash('Your password has been reset. You can now login Successfully.')
        return redirect(url_for('userinfo.login'))
    return render_template('reset_password.html', title='reset password', form=form) 