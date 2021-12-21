# from flaskblog folder in __init__.py
from enum import unique
from datetime import datetime

from flask_login.utils import _secret_key, decode_cookie
from app import db
from sqlalchemy import Column, Integer, String, LargeBinary
from flask_login import UserMixin, LoginManager
# itsdangergous... gives a time sensitive message 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

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
    
    #profilepicture = db.Column(db.LargeBinary, nullable=False)
    # profilepicture = db.Column(db.LargeBinary, nullable=False, default='default.jpg')
    # If I want to link the Posts database to the User database I can go Posts.user.id
    # I think I need a column from the Posts database. 
    # I think I can link the User database to the Posts. I can go User.user.id. I get the Posts id. 
    posts = db.relationship('Posts', backref='user', lazy=True)
    # 1800 sec = 30 min 
    # Could this be in routes.py?

  
    
    

    # what does this do?
    def __repr__(self):
        return '<User %r>' % self.username 

# The many relationship 
class Posts(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    # need a better name then content
    content = db.Column(db.String(120), unique=True, nullable=False) 
    date_posted = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
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



 