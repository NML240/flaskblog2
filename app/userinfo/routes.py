# Continue 25:31 https://www.youtube.com/watch?v=803Ei2Sq-Zs
import os
# use variables in routes 
from flask import Blueprint, flash, session, render_template, redirect,  request, url_for
# make file uploading possible
from werkzeug.utils import secure_filename
# current_user gets the current User info from the database
from flask_login import login_user, login_required, current_user 
# importing databases 
# import the flaskblog folder and from models.py 
from app.models import User, Posts 
# import db from flaskblog folder in __init__.py
from app import db 
# make bcrypt and db work 
import bcrypt
# make @userinfo work from userinfo folder 
userinfo = Blueprint('userinfo', __name__)
# why not .forms? Beacuse it is an class and needs "()" brackets
from app.userinfo.forms import (RegistrationForm, LoginForm, UpdateProfileForm)

'''
# todo turn into a database why is there no post number like 1st post ever posted in general etc?
posts = {   
    "username": "author",
    "author": "Bobby Bobson",
    "Title": "Hello World",
    "Content": "This is a post content 1",
    "date_posted": "March 17 2021" 
}
'''

# get data from wtf forms 
# username = form.username.data
# read the post
@userinfo.route("/")
@userinfo.route("/home")
def home():
    # .query.all() means I get all info from the database.
    Posts_db = Posts.query.all() 
    # All databases are an list    
    return render_template('home.html', Posts_db=Posts_db, title='home')

@userinfo.route("/profile/<string:username>", methods = ['POST', 'GET'])
def profile(username):  
        username = User.query.filter_by(username=username).first_or_404()
        # Why can't I use "profilepicture = form.profilepicture.data" for the line below?
        # Taking current_user image in the database from my folder and storing it as a variable. profile pic is from the database.
        image_file = url_for('static', filename='profile_pics/' + current_user.profilepicture)
        return render_template('profile.html', title='profile', username=username, image_file=image_file)

@userinfo.route("/profile/<string:username>/update_profile", methods = ['POST', 'GET'])
def profile(username):  
    form = UpdateProfileForm 
    if request.method == 'POST' and form.validate(): 
            password = form.password.data
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # Can the line below have a _ in it?
            profilepicture = form.profilepicture.data
            user_db = User(hashed_password=hashed_password,profilepicture=profilepicture)
            db.session.add(user_db)
            db.session.commit()
            return render_template('update_profile.html', title='update_profile', username=username, form=form)


@userinfo.route("/about")
def about():
    return render_template('about.html')



@userinfo.route("/register", methods = ['POST', 'GET'])
def register():
    
    # if the user is logged in make so they can't go to the register page. 
    if current_user.is_authenticated:
        return redirect(url_for(('userinfo.home')))
    
    form = RegistrationForm()
    # if form.validate_on_submit():?
    if request.method == 'POST' and form.validate():
        # get data from wtf forms 
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
     
        user_db =  User(username=username, email=email, hashed_password=hashed_password)
        
        db.session.add(user_db)
        # session commit what does this do
        db.session.commit()
        # todo make it so user can't input no username or password in flask important or is what if request.method == 'POST' and form.validate(): does that  etc  
        # login user Should I use next or login
        login_user(user_db)                                         
        flash('You have registered successfully')
        return redirect(url_for('userinfo.login'))
    else:
        flash('You have registered unsuccessfully')
    return render_template('register.html',title='register', form=form)

@userinfo.route("/login",methods = ['POST', 'GET'])
def login():
   
    # if the user is logged in make it so they can't go to the login page. 
    if current_user.is_authenticated:
        return redirect(url_for(('userinfo.home')))    
    form = LoginForm()
    if request.method == 'POST' and form.validate():
         
        username = form.username.data
        # do I need first()?
        # check if username and password inputted in login forms matches the database
        db_username = User.query.filter_by(username=username).first()
        
        password = form.password.data
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # why won't work db_hashed_password = User.query.filter_by(hashed_password=hashed_password).first()?


        # User.password is the password in the database ? 
        matching_password_with_db = bcrypt.check_password_hash(User.password, form.password.data)
        # if username and password are already in the database login user
        if db_username and matching_password_with_db:
            user_db = User(db_username=db_username, db_hashed_password=hashed_password)
            login_user(user_db) 
            flash('You have logged in successfully') 
    else:
        flash('You have logged in unsuccessfully')     
    return render_template('login.html',title='login', form=form)



# for some reason I can go to the new post route when loggerd in? Need to fix
@userinfo.route("/logoff")
@login_required
def logoff():
    return render_template('home.html')
                  


