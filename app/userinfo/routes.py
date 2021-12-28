# Continue 25:31 https://www.youtube.com/watch?v=803Ei2Sq-Zs
import os
# use variables in routes 
from flask import Flask, Blueprint, flash, render_template, request, redirect, url_for, abort, send_from_directory, render_template, session
# make file uploading possible
from werkzeug.utils import secure_filename
# current_user gets the current User info from the database
from flask_login import login_user, login_required, current_user 
# importing databases 
# import the flaskblog folder and from models.py 
from app.models import User, Posts 
# import db from flaskblog folder in __init__.py
from app import db, mail
# make bcrypt and db work 
import bcrypt
from flask_mail import Message

# why not .forms? Beacuse it is an class and needs "()" brackets
from app.userinfo.forms import (RegistrationForm, LoginForm, UpdateAccountForm )
from werkzeug.utils import secure_filename



from app.userinfo.utils import send_account_registration_email 
# make @userinfo work from userinfo folder 
userinfo = Blueprint('userinfo', __name__)

 


# todo turn into a database why is there no post number like 1st post ever posted in general etc?
posts = {   
    "username": "author",
    "author": "Bobby Bobson",
    "Title": "Hello World",
    "Content": "This is a post content 1",
    "date_posted": "March 17 2021" 
}


# get data from wtf forms 
# username = form.username.data
# read the post
@userinfo.route("/")
@userinfo.route("/home")
def home():
    # .query.all() means I get all info from the database.   
    #if there are no posts in the database
    Posts_db = Posts.query.all() 
    return render_template('home.html', Posts_db=Posts_db, title='home') 
'''     
# Check 1st 512 bytes and makes sure it is the correct extension.
# By extension I just mean .jpg etc
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    # imghdr.what() function starts by looking if it matches the file type and returns the (file type) if not it returns (none). 
    format = imghdr.what(None, header)
    print("print format value",format)
    if not format:
        print("print not format value",format)
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


# create the upload file path and send the file to where the file is saved
@userinfo.route('/uploads/<filename>')
def upload(filename):
    # Send the file to " app.config'UPLOAD_PATH' " where the picture is saved 
    return send_from_directory(['UPLOAD_PATH'], filename)


# The send_to_profile function gets a list of files from os.listdir() and the location of the files is at ['UPLOAD_PATH'].
# Then you pass the files on to profile.html
@userinfo("/profile/<string:username>")
def send_to__profile(username):
    username = User.query.filter_by(username=username).first_or_404()
    files = os.listdir(['UPLOAD_PATH'])
    return render_template('profile.html', files=files)


# check if right filename and extension if wrong extension 400    
@userinfo('/profile/<string:username>', methods=['POST'])
def upload_files(username):
    # Example name = jim's.jpg. Get uploaded file from db and Check if has the correct name 
    # get uploaded file and confirm it has a name.  
    username = User.query.filter_by(username=username).first_or_404()
    uploaded_file = request.files['profilepicture']
    filename = secure_filename(uploaded_file.filename)
    # filename = uploaded_file.filename. uploaded_file.filenam is the filename
    # When you combine uploaded_file with filename you get the filename 
    if filename != '':
        # make sure the extensions are allowed
        # get 400 error if wrong extension
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in ['UPLOAD_EXTENSIONS']:
            abort(400)
        # Make the file publically aviable 
        uploaded_file.save(os.path.join(['UPLOAD_PATH'], filename))
    return redirect(url_for('profile.html')

 '''

@userinfo.route('/profile/<string:username>', methods = ['GET'])
def profile(username): 
    username = User.query.filter_by(username=username).first_or_404()
    # profilepicture = request.files['profilepicture']
    return render_template('profile.html', title='profile', username=username)
    


@userinfo.route("/profile/<string:username>/update_profile", methods = ['POST'])
def update_profile(username):  
    form = UpdateAccountForm 
    
    if form.validate_on_submit():
        password = form.password.data
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        confirm_password = form.confirm_password
        if password != confirm_password:
            # need better phrasing 
            flash("Your passwords fields don't match.") 
        else:
            # Can the line below have a "_" in it?
            # profilepicture = request.files['profilepicture']
            # files = request.files.getlist('images')
            user_db = User(hashed_password=hashed_password)
            db.session.add(user_db)
            db.session.commit()
            return render_template('update_profile.html', title='update_profile', username=username, form=form)





@userinfo.route("/about")
def about():
    return render_template('about.html')



# bcrypt.hashpw vs bcrypt.checkpw Are they correct? 



@userinfo.route("/register", methods = ['POST', 'GET'])
def register():
    
    # if the user is logged in make so they can't go to the register page. 
    if current_user.is_authenticated:
        return redirect(url_for(('userinfo.home')))
    
    form = RegistrationForm()
    if form.validate_on_submit():
       
        username = form.username.data
        if username is None:
            flash("Please fill in the username field")
        email = form.email.data
        if email is None:
            flash("Please fill in the email field")
        password = form.password.data
        if password is None:
            flash("Please fill in the password field")
        confirm_password = form.confirm_password.data
        if confirm_password is None:    
            flash("Please fill in the confirm password field")


    
        '''
        if user is None:
            return print("user is none") 
        '''
        
        
        flash("An email has been sent with instructions to your email to create the password")     
        # didn't I already declare password?
      
        # login user. Should I use next or login?
        # get data form wtf forms iow get user inputted data from the forms
        # password = userInput
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_db = User(username=username, email=email, hashed_password=hashed_password)
        db.session.add(user_db)
        db.session.commit()
    
        user = User.query.filter_by(email=email).first()
        send_account_registration_email(user)
                                        




        flash('You have almost registered successfully. Pleae click the link in your email to complete the registeration.')
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
    if form.validate_on_submit():
        email = form.email.data
        if email is None:    
            flash("Please fill in the email field")
        username = form.username.data
        if username is None:    
            flash("Please fill in the username field")
        password = form.password.data
        if password is None:
            flash("Please fill in the password field")
        # query.filter_by(...).first gets the first result in the database query
        # check if username and password inputted in login forms matches the database
        # db_username = User.query.filter_by(username=username).first()
       
        user = User.query.filter_by(email=email).first()
        

        # Using bcrypt compare password from the form vs the current user's hashed password from the database
        # if user exists and check passwords
        if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            #log the user in remember is a boolean. Where do I get form.remember.data?
            flash('You have logged in successfully') 
            login_user(user, remember=form.remember.data)
            # @login_required redirects to the login page no matter the route in the url. 
            # To prevent seeing the original typing use the code below.
            
            # get the information typed from the url learn more about this line
            words_typed_in_url = request.args.get('next') 
            # else runs when = None
            return redirect(words_typed_in_url) if words_typed_in_url else redirect(url_for('userinfo.home'))
        return render_template('login.html', title='login', form=form)
        
        
        # delete? hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # why won't work db_hashed_password = User.query.filter_by(hashed_password=hashed_password).first()?
        '''

        # User.password is the password in the database ? 
        matching_password_with_db = bcrypt.check_password_hash(User.password, form.password.data)
        # if username and password are already in the database login user
        if db_username and matching_password_with_db:
            user_db = User(db_username=db_username, db_hashed_password=hashed_password)
            login_user(user_db) 
            flash('You have logged in successfully') 
        '''




# for some reason I can go to the new post route when logged in? Need to fix
@userinfo.route("/logoff")
@login_required
def logoff():
    return render_template('home.html')
                  






