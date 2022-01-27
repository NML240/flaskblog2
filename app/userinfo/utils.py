from flask import Flask, Blueprint, flash, render_template, request, redirect, url_for, abort, send_from_directory, render_template, session
from flask_login import login_user, login_required, current_user 
from app import db, mail 
# make bcrypt and db work 
import bcrypt
from flask_mail import Message
from app.userinfo.forms import ResetPasswordTokenForm ,UpdateAccountForm  
# itsdangergous... gives a time sensitive message 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.models import User 
from app.userinfo.forms import RegistrationForm

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
    {url_for('userinfo.verified_email', token=token, _external=True)}
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




