# start with making the post work

# use variables in routes 
from flask import Blueprint, flash, session, render_template, redirect,  request, url_for
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
from app.userinfo.forms import (RegistrationForm, LoginForm)
 
  

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
    # use this line.  
    username = User.query.filter_by(username=username).first_or_404()
    profile_title = 'profile/'+'username'
    
    return render_template('profile.html', title=profile_title, username=username)





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
                  



'''
@userinfo.route("/post/new")
@login_required
# why do I need to link to the name of the function in the html. Ex new_post 
def new_post(): 
    form = Postform()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        # current_user variable gives me the current database information of the User.
        # current_user.id gives me the id of the User column id.
        # This works because I am using the user.id for the foreign key in the Post database.                 
        db_post_info = Posts(title=title, content=content, user_id=current_user.id)
        db.session.add(db_post_info)  
        db.session.commit()
        flash('You have posted successfully')
        return redirect(url_for('userinfo.home'))
    return render_template('new_post.html',title='new_post', form=form)

# gives you ability to click on posts from home route and see the posts
# create the post/number route
# gets the posts number
@userinfo.route("/post/<int:post_id>")
def post(post_id):
    # Pass on the Posts database to the post_number variable. If the post doesn't exist get 404 error
    # The reason I don't use Posts.id is because I want a certain "Posts database id". 
    post_id = Posts.query.get_or_404(post_id)
    posts = 'post/'+'post_number'

    return render_template('post.html', post_id=post_id, title=posts)


# The reason you have post_id is because you only want to edit 1 post at a time. 
# If you leave out post_id you would edit every posts. 
@userinfo.route("/post/edit/<int:post_id>", methods = ['POST', 'GET'])
# edit/update posts
@login_required
def edit_post(): 
    form = Postform() 
    if request.method == 'POST' and form.validate(): 
        title = form.tilte.data
        content = form.content.data 
        db.commit()
        # todo make it so only the original poster can edit there post
        return render_template('edit.html', title='edit_post', form=form) 

'''