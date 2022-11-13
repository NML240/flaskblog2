from flask import Blueprint, flash, render_template, redirect, url_for, render_template, request
from flask_login import login_user, login_required, current_user 
from app import db, mail, email 
# make bcrypt and db work 

import bcrypt

# from flask_mail import Message 
# itsdangergous... gives a time sensitive message 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.models import User
from app.mail.forms import RequestResetPasswordForm, EmptyForm, ResetPasswordForm


from redmail import outlook


import os
# make the email variable below work. 
 

mail = Blueprint('mail', __name__)











#from redmail import EmailSender
# email = EmailSender(host="smtp.mail.com", port=587)
 
# why user.create_token(), because it is an method? 
def send_account_registration_email(user):
    # should I use a form?
    form = EmptyForm()
    # the function creates the randomly generated token
    token = user.create_token() # don't need to import methods just the class. Confirm?
    # needed for outlook.send for outlook
    outlook.send(
            subject="register account",
            sender=os.environ['EMAIL_USERNAME'], 
            receivers=[user.email],
            # remember url for won't work for some reason.
            html = render_template('verify_email.html', title='verify email', token=token, form=form, _external=True) 
    )
 




  


# This route is always a get request!!!
# verify the users email or after you clicked on the email from the recieved email
# better name for function maybe change to verify?
@mail.route("/verified_email<token>", methods = ['GET']) 
def verified_email(token):      
    user = User.verify_token(token)
    if user is None: # why does this not work pytest later??
        flash('This is an invalid or expired token')
        return redirect(url_for('userinfo.home'))   
    

    # Prevents you from registering twice. Is this needed?
    if user.registration_confirmation_email == True:
        flash('You have already clicked on the confirmation email. You can now login')
        return redirect(url_for('userinfo.home'))

    user.registration_confirmation_email = True 
    db.session.commit()
    
    form = EmptyForm()
    return render_template('verified_email.html', title='verified email', form=form)







def send_reset_password_email(user):
    # get the function from models.py
    token = user.create_token()
    # _external – if set to True, an absolute URL is generated. Server address can be changed via 
    # Absolute import is  https://example.com/my-page relative URL is  /my-page 
    form = EmptyForm()
    outlook.send(        
        subject='Password Reset Request', 
        sender=os.environ['EMAIL_USERNAME'],  # change to noreply...?
        receivers=[user.email],   
        html = render_template('send_reset_password_email.html', title='send reset password email', token=token, form=form, _external=True)
    )
    
# creates form for email for your password reset
# better name
@mail.route("/request_reset_password", methods = ['POST', 'GET'])
def request_reset_password():
    form = RequestResetPasswordForm()
    if form.validate_on_submit():   
        
        # do i need? this check wtf forms
        forms_email = form.email.data
        try: 
            user = User.query.filter_by(email=forms_email).first()
        except:
            user = None
        
        # I think I should combine this into 2 . Do I need "not user.registration_confirmation_email"?
        # if the user is not registered and you have not clicked on the registration email.  
        if not user.email and not user.registration_confirmation_email:
            flash('Your email is not registered')
            return redirect(url_for('mail.request_reset_password')) 


        flash("An email has been sent with instructions to your email to reset the password") 
        send_reset_password_email(user)
        return redirect(url_for('userinfo.home'))
    return render_template('request_reset_password.html', title='request reset password', form=form)




# reset password after recieved the token in a email
# create form for password field and confirm password
@mail.route("/reset_password/<token>", methods = ['GET', 'POST'] )
def reset_password(token):
 
    form = ResetPasswordForm()

    if form.validate_on_submit():   
        user = User.verify_token(token)
        if user is None:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('request_reset_password'))    
        
        # do I need this? check wtf forms
        forms_plaintext_password = form.password.data
        forms_confirm_password = form.confirm_password.data
        
        if forms_plaintext_password != forms_confirm_password:
            flash("The passwords fields do not match" ) # I need better phrases. 
         
        # example password
        plaintext_password = form.password.data
        # converting password to array of bytes
        bytes = plaintext_password.encode('utf-8')
        # generating the salt
        salt = bcrypt.gensalt()
        # Hashing the password
        hashed_password = bcrypt.hashpw(bytes, salt)        
        

        user = User(hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('you have changed your password successfully')
        return redirect(url_for('userinfo.home')) 


    # why does render_template need to go not in the POST if statement?? Confirm
    return render_template('reset_password.html', title='reset password', token=token, form=form) 

















