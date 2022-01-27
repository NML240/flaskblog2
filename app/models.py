# from flaskblog folder in __init__.py
from enum import unique
from datetime import datetime

from flask_login.utils import _secret_key, decode_cookie
from app import db, app
from sqlalchemy import Column, Integer, String, LargeBinary
from flask_login import UserMixin, LoginManager
# itsdangergous... gives a time sensitive message 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import flash 
 

# https://stackoverflow.com/questions/63231163/what-is-the-usermixin-in-flask

# one to many relationship between both databases



# The One relationship
class User(UserMixin, db.Model):
    # The primary key creates an unique value automatically each time starting at 1-infinity.   
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #recieved_confirmation email
    confirmation_email = db.Column(db.Boolean, default=False, nullable=False) 
    # I think I can link the User database to the Posts. I can go User.user.id. I get the Posts id. 
    # If I want to link the Posts database to the User database I can go Posts.user.id
    
    # name this column afer the database from the many. 
    # Backref is = the current database I am using except lowercase except 
    
    # backref allows you to get the "user" object from a "posts" object (posts.user).
    posts = db.relationship('Posts', backref='user', lazy=True)
    # 1800 sec = 30 min 
    # Could this be in routes.py?
    #profilepicture = db.Column(db.LargeBinary, nullable=False)
    # profilepicture = db.Column(db.LargeBinary, nullable=False, default='default.jpg')
  


  
    # get_reset_token = create_token
    # def verify_reset_token(token) = verify_token 
    def create_token(self, expires_sec=1800):
        # Serializer passes in SECRET_KEY 30 min beacuse of expir_sec.
        s = Serializer(app.config['SECRET_KEY'], expires_sec) 
        # Creates randomly assigned token as long as less then 30 min   
        return s.dumps({'user_id': self.id}).decode('utf-8')
        

        
    # why @staticmethod?
    @staticmethod
    def verify_token(token):
        # Serializer passes in SECRET_KEY
        # Why isn't there a time limit?
        s = Serializer(app.config['SECRET_KEY'])
        try:
            ''' 
            get user_id by running s.loads(token).if this line works  
             If it does not work returns error and return none in the except block
            '''
            user_id = s.loads(token)['user_id']   
        except:
            flash('That is an invalid or expired token') 
            return None 
            # why query.get? Because  "u = User.query.get(1)" gives the current user.
        return User.query.get(user_id)    
    

    # what does this do?
    def __repr__(self):
        return '<User %r>' % self.username 

# The foreign key is a many relationship 
class Posts(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    # need a better name then content
    content = db.Column(db.String(120), unique=True, nullable=False) 
    # gives a time of when the post is posted. Everyone sees the same time based on daylight savings  
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # always create the name of the column of the other database except lowercase and end it with _id
    # The foreign key creates the an psuedo column called user.id. This links the two tables.
    # user.id represents the id from the User database. 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # what does this do?
    def __repr__(self):
        return '<Posts %r>' % self.title


from app import login_manager
# Use User.query.get instead of User.get because of sqlalchemy
# what is this function?
@login_manager.user_loader
def load_user(user_id):
   return User.query.get(user_id)

 