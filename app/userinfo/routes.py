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
    # use a try if the Posts_db is empty then it will skip it
    try: 
        posts = Posts.query.all()
    except:
        posts = None

    return render_template('home.html', posts=posts, title='home')  








@userinfo.route('/profile/<string:username>', methods = ['GET'])
def profile(username): 
    user = User.query.filter_by(username=username).first_or_404()
    # profilepicture = request.files['profilepicture']
    '''
    The line below won't work becauses what if I don't have any posts. 
    posts = Posts.query.filter_by(id=current_user.id).first()
    posts.id
    '''

    return render_template('profile.html', title='profile', user=user)
    


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


def check_if_the_user_is_already_registered(forms_username, forms_email):
    
    # do I need a try?
    # I don't need passwords because people can have the same password
    try:   
        users = User.query.filter_by(username=forms_username).all()
    except: 
        users = None # what if username is None?
    finally:
        # do I want to redirect to register route? 
    
        for all_users in users: 
            if all_users.username == forms_username:
                flash ("The username is already taken. Please select another username.")     
                return redirect(url_for('userinfo.register')) 

        for all_users in users:
            if all_users.email == forms_email:    
                flash("The email is already taken. Please select another email.")
                return redirect(url_for('userinfo.register')) 

@userinfo.route("/register", methods = ['POST', 'GET'])
def register():
    
    # if the user is logged in make so they can't go to the register page. 
    if current_user.is_authenticated:
        return redirect(url_for(('userinfo.home')))
    
    form = RegistrationForm()
    # form.validate_on_submit(): are always the same line of render template to always allow a get request.
    if form.validate_on_submit():
    

        # if NOT NULL do I need this? check wtf forms.
        forms_username = form.username.data
        if forms_username is None:
            flash("Please fill in the username field")
        forms_email = form.email.data
        if forms_email is None:
            flash("Please fill in the email field")
        forms_plaintext_password = form.password.data
        if forms_plaintext_password is None:
            flash("Please fill in the password field")
        forms_confirm_password = form.confirm_password.data
        if forms_confirm_password is None:    
            flash("Please fill in the confirm password field")
        
        # won't work redirect?
        if forms_plaintext_password != forms_confirm_password:
            flash("Please fill in the confirm password field")

        # do I need a try?
        # I don't think I should use for password for security reasons. ?
        check_if_the_user_is_already_registered(forms_username, forms_email)
        ''' 
        make_password_contain_capital(confirm_password)
        make_password_contain_number(confirm_password):
        make_password_contain_special_characters(confirm_password)
        '''
        
        # example password
        plaintext_password = form.password.data
        # converting password to array of bytes
        bytes = plaintext_password.encode('utf-8')
        # generating the salt
        salt = bcrypt.gensalt()
        # Hashing the password
        hashed_password = bcrypt.hashpw(bytes, salt)
        # Use this code if adding code to the database the first time.
        user = User(username=forms_username, email=forms_email, hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        user = User.query.filter_by(email=forms_email).first()
        flash('You have almost registered successfully. Please click the link in your email to complete the registeration.')        
        send_account_registration_email(user) 
        return redirect(url_for('userinfo.login'))
    '''    
    else:
        flash('You have registered unsuccessfully')
    ''' 

    return render_template('register.html',title='register', form=form)



# if the user does not exist then you do not register
def check_if_user_is_not_registered(username):
    if not username:
        flash('You have not registered yet. Please register')
        return redirect(userinfo.register)


@userinfo.route("/login",methods = ['POST', 'GET'])
def login():

    # if the user is logged in make it so they can't go to the login page. 
    if current_user.is_authenticated:
        return redirect(url_for('userinfo.home')) 

    form = LoginForm()
    if form.validate_on_submit():
        
        forms_username = form.username.data           
        user = User.query.filter_by(username=forms_username).first()
        check_if_user_is_not_registered(user.username)

        registration_confirmation_email = user.registration_confirmation_email
        if registration_confirmation_email == False:
            flash('You have almost registered successfully. Please click the link in your email to complete the registeration.')
            flash(registration_confirmation_email)
            return redirect(url_for('userinfo.home'))
 

        if not user.hashed_password and User: 
            flash('You have not typed in your password correctly. Please retype it.')
            return redirect(url_for('userinfo.login'))           
            
        # login_user(user, remember=form.remember.data)
        login_user(user)
        flash('You have logged in successfully') 
        '''           
            
            To determine if the URL is relative or absolute, parse it with Werkzeug's url_parse() function and then check 
            if the netloc component is set or not. What is netloc?
            
            next = '/login?next=/index', index is just a route. 
            The 'next' variable can have 3 values

            1st value)
	        If the login URL does not have a next argument you will be logged in and redirected to the home page.
            iow's next = '/login?next=/'. 
            
            How would the other 2 situations happen?

            2nd value)
            if the user is not logged in and tries to go to a route with @login_required, then for example post/new_post ,
            iow's 'next = login?next=/post/new_post' . (This is relative import).
           
            3rd value)
            To protect from redirect to any other website, in the module it checks if next is relative or full url. 
            if it's full domain then, the user is redirected to home page. 
        '''
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('userinfo.home')
        return redirect(next_page)
 
    return render_template('login.html', title='login', form=form)
         
 





# for some reason I can go to the new post route when logged in? Need to fix
@userinfo.route("/logoff")
@login_required
def logoff():
    logout_user()
    return redirect (url_for('userinfo.home.html'))
                  



