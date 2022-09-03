# Continue 25:31 https://www.youtube.com/watch?v=803Ei2Sq-Zs
import os
# use variables in routes 
from flask import  Blueprint, flash, render_template, request, redirect, url_for, render_template 

from flask_login import login_user, login_required, current_user ,logout_user
  
from app.models import User, Posts

from werkzeug.urls import url_parse
# import db from flaskblog folder in __init__.py
from app import db
# make bcrypt and db work 
import bcrypt
 

# why not .forms? Beacuse it is an class and needs "()" brackets
from app.userinfo.forms import (RegistrationForm, LoginForm, EmptyForm)

from werkzeug.utils import secure_filename



from app.mail.routes import send_account_registration_email
# make @userinfo work from userinfo folder 
userinfo = Blueprint('userinfo', __name__)

 

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


''' IMPORTANT flash not working before a redirect why? '''



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
    user = User.query.filter_by(username=username).first_or_404()
    # profilepicture = request.files['profilepicture']
    '''
    The line below won't work becauses what if I don't have any posts. 
    posts = Posts.query.filter_by(id=current_user.id).first()
    posts.id
    '''

    return render_template('profile.html', title='profile', username=user.username)
    


'''move to different route.py keep with profile.'''
@userinfo.route("/followers/<string:username>", methods = ['Get', 'Post'])
# can if user is None be replaced by @login_required
@login_required
def followers(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first_or_404() 	
        # methods from models.py don't need self
        is_following = is_following(user)
        if (is_following == False):
            current_user.follow(user)
            db.session.commit()	
            return render_template( 'followers.html', title='follow', form=form, is_following=is_following, username=user.username)
        
        else:
            current_user.unfollow(user)
            db.session.commit()
            return render_template( 'followers.html', title='unfollow', form=form, is_following=is_following, username=user.username )

    return render_template( 'profile.html', title='followers', form=form, username=user.username)


# I am resetting a passoword differently.
'''
@login_required 
@userinfo.route("/update_profile/<string:username>", methods = ['POST','GET'] )
def update_profile(username):  
    form = UpdateAccountForm 
    
    if form.validate_on_submit():
        # do I need this line? Yes to make sure the username exists
        username = User.query.filter_by(username=username).first_or_404()
        password = form.password.data
        confirm_password = form.confirm_password
        # should I get the hashed passwords before checking them? 
        if password != confirm_password:
            # need better phrasing 
            flash("Your passwords fields don't match.") 
        else:

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user = User.query.filter_by(hashed_password='hashed_password').first()
            user = User(hashed_password=hashed_password)
            db.session.add(user)
            db.session.commit()
        return render_template('update_profile.html', title='update_profile', username=username, form=form)
'''




@userinfo.route("/about")
def about():
    return render_template('about.html')



# bcrypt.hashpw vs bcrypt.checkpw Are they correct? 


# should i include lower case?

def make_password_contain_capital(confirm_password):
    word = confirm_password
    if not word.isupper(): 
      flash("Please include a capital letter in the password field")  
      # what should I return, return redirect?
      return make_password_contain_capital 

def make_password_contain_number(confirm_password):
    word = confirm_password
    if not word.isnumeric():
      flash("Please include a number in the password field")  
      # what should I return, return redirect?
      return make_password_contain_number
 
def make_password_contain_special_characters(confirm_password):
    word = confirm_password
    if word.isalpha() or word.isnumeric():
      flash("Please include a special character in the password field")  
      # what should I return, return redirect?
      return make_password_contain_special_characters



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
        plaintext_password = form.password.data
        if plaintext_password is None:
            flash("Please fill in the password field")
        confirm_password = form.confirm_password.data
        if confirm_password is None:    
            flash("Please fill in the confirm password field")
        
        # won't work redirect?
        if plaintext_password != confirm_password:
            flash("Please fill in the confirm password field")

        # don't do this for passwords because this can reveal passwords. WHat about emails?
        all_usernames = User.query.filter_by(username=form.username.data).all()
        all_emails = User.query.filter_by(username=form.username.data).all()

        # if value other then None iow you have a username or email in the database
        if all_usernames:
            flash ("The usesrname is already taken. Please select another username.")
            return redirect(url_for('userinfo.register')) 
        if all_emails:    
            flash("The email is already taken. Please select another email.")
            return redirect(url_for('userinfo.register')) 
        ''' 
        make_password_contain_capital(confirm_password)
        make_password_contain_number(confirm_password):
        make_password_contain_special_characters(confirm_password)
        '''
        # didn't I already declare password?
      
        # login user. Should I use next or login?
        # get data form wtf forms iow get user inputted data from the forms
        # password = userInput
        hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())


        # Use this code if adding code to the database the first time.

 

        user = User(username=username, email=email, hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        user = User.query.filter_by(email=email).first()
        flash('You have almost registered successfully. Please click the link in your email to complete the registeration.')        
        send_account_registration_email() 
        return redirect(url_for('userinfo.login'))
    '''    
    else:
        flash('You have registered unsuccessfully')
    ''' 

    return render_template('register.html',title='register', form=form)


# flash(You have almost registered successfully. Please click the link in your email to complete the registeration.) appears after I click on the registraation email?



@userinfo.route("/login",methods = ['POST', 'GET'])
def login():

    # if the user is logged in make it so they can't go to the login page. 
    if current_user.is_authenticated:
        return redirect(url_for('userinfo.home')) 

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data  
        user = User.query.filter_by(username=username).first()


        # why does this execute even if true?
       
        confirm_email = user.confirmation_email
        flash(confirm_email)
        if confirm_email == False:
            flash('You have almost registered successfully. Please click the link in your email to complete the registeration.')  
            return redirect(url_for('userinfo.home'))


 
 
        password = form.password.data
 
        # query.filter_by(...).first gets the first result in the database query
        # check if username and password inputted in login forms matches the database
        # db_username = User.query.filter_by(username=username).first()
       

        # Using bcrypt compare password from the form vs the current user's hashed password from the database
        # if user exists and check passwords
        if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
           
            
            # login_user(user, remember=form.remember.data)
            login_user(user)
            # log the user in remember it is a boolean. Where do I get form.remember.data?
            flash('You have logged in successfully') 
            '''           
            The 'next' variable can have 3 values
            To determine if the URL is relative or absolute, parse it with Werkzeug's url_parse() function and then check 
            if the netloc component is set or not.
            
            1st)
	        If the login URL does not have a next argument, this is when you go to the login page and login. 
            You you will be redirected to the home page.

            2nd)
            if the user is not logged in and tries to go to a route with @login_required, then for example post/new_post ,
            next is = login?next=/post/upload . (This is relative import).
           
            3rd)
            To protect from redirect to any other website, in the module it checks if next is relative or full url. 
            if it's full domain then, the user is redirected to home page 
            
            '''
       
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('userinfo.home')
            return redirect(next_page)

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
    logout_user()
    return redirect('home.html')
                  



