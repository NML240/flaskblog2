# from flaskblog folder in __init__.py
from datetime import date, datetime
from sqlalchemy import Column, Integer, String, LargeBinary
from flask_login import UserMixin, LoginManager
# itsdangergous... gives a time sensitive message 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import flash 
import bcrypt 
import os
   
from flask_login import login_manager

from app import db 

# https://stackoverflow.com/questions/63231163/what-is-the-usermixin-in-flask











# many to many relationship
Followers = db.Table('followers',
    # I have 2 foreign keys from the User table.  
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')) )

# one to many relationship between both databases
# The One relationship
# Why is the database class different then most? It just the type of class.
class User(UserMixin, db.Model):
    # The primary key creates an unique value automatically each time starting at 1-infinity.   
    id = db.Column(db.Integer, primary_key=True)
    #check if unique blocks 2 same usernames
    # I can't have Nullable=False because it will make me add the columns everytime I add a column in user
    username = db.Column(db.String(80), unique=True)
    hashed_password = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    registration_confirmation_email = db.Column(db.Boolean, default=False) 
    reset_email_password = db.Column(db.Boolean, default=False)        
    # relationship connects the tables. I can get the user id by going User.id.
    # If I want to link the Posts database to the User database I can go Posts.user.id.
    
    # name this column afer the database from the many. 
    # Backref is = the current database I am using except lowercase except  
    # backref allows you to get the "user" object from a "posts" object (posts.user).
    # relationship creates the connection between the 2 databases.
    # lazy?
    posts = db.relationship('Posts', backref='user', lazy=True)
    # uselist=False creates a one to one relationship instead of a 1 to many when using a foreign key etc
    # relationship creates a connection between the foreign key table and the primary key table 
    # is it okay as the same name as the table?
    # confirmation_email = db.relationship('ConfirmationEmail', backref='user', uselist=False, lazy=True)
    
    

    '''
    Create Many to many relationship
    '''
    
    # relationship creates the connection by the database? 
    followed = db.relationship(
        # 'User' is the right table and left table
        # secondary - configures the association followers table? 
        # child table has 2 foreign keys in one table.
        'User', secondary=Followers,
        # primaryjoin links the followers_id with the the user_id.
        primaryjoin=(Followers.c.follower_id == id),
        # secondaryjoin links the followed_id with the user_id.
        secondaryjoin=(Followers.c.followed_id == id),
        # backref - defines how the right and left side entity will be accessed. 
        # get the right and left side entity from the followers table 
        # lazy?
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
  
        
    # why functions like this and here?
    def follow(self, user):
        #  .is_following(user) is False. IOW I am not following an user
        if not self.is_following(user):
            self.followed.append(user)
            return self
        
    def unfollow(self, user):
        # .is_following(user) is True. IOW I am following an user
        if self.is_following(user):
            self.followed.remove(user)
            return self
        # check if it is_following
    def is_following(self, user):
        # followers_id = user_id if it is already following an user_id. 
        # Instead of followers.c.followed_id == user.id I am saying user.id == user.id.
        # 1 > 0 returns True and  0 > 0 returns False. 
        return self.followed.filter(Followers.c.followed_id == user.id).count() > 0
    
    
    
    
    
    
    
    
    
    # show blog posts written by all the people that are followed by the logged in user. 
    # The query scales well and allows pagination and the correct date vs going user.followed.all().          
    def followed_posts(self):
        # The join condition creates a temporary table that combines data from the Posts table and the followers table. It gives me all the Posts I am following/followed! 
        # followers.c.followed_id == Posts.user_id. If it is not True then you are not following an user and you want to be following an user. 
        # I can create a table that has more then one user who follows using followers.c.followed_id == Posts.user_id.      
        followed = Posts.query.join(
            # filter followers.c.follower_id == self.id selects me all the posts of one user! self.id?
            Followers, (Followers.c.followed_id == Posts.user_id)).filter(
                Followers.c.follower_id == self.id)
        # The query above works except it does not include the users own posts in the timeline. Use the line below to do that. 
        own = Posts.query.filter_by(user_id=self.id)
        # combines the followed query with the own query using union
        # Posts.timestamp.desc lists the posts in order in desc order of when they were posted.
        return followed.union(own).order_by(Posts.timestamp.desc())


    # get_reset_token = create_token
    # def verify_reset_token(token) = verify_token 
    def create_token(self, expires_sec=1800):
        # Serializer passes in SECRET_KEY 30 min beacuse of expir_sec.
        SECRET_KEY = 'temp_secret_key'
        s = Serializer (SECRET_KEY, expires_sec) 
        # Creates randomly assigned token as long as less then 30 min   
        # might need to be 'user_id'
        return s.dumps({'users_id': self.id}).decode('utf-8')
            


            
    # why @staticmethod? So I don't have to use the self variable 
    @staticmethod
    def verify_token(token):
        # Serializer passes in SECRET_KEY
        SECRET_KEY = 'temp_secret_key'
        s = Serializer(SECRET_KEY)
        
        try:
            ''' 
                get user id by running s.loads(token).if this line works  
                If it does not work returns error and return none in the except block
            '''
                # might need to be 'user_id' not id
            users_id = s.loads(token)['users_id']   
        except:
            flash('This is an invalid or expired token') 
            # why query.get? Because  "u = User.query.get(1)" gives the current user.
            return None
        return User.query.get(users_id)    

    '''
    def __init__ (self ,username: str,  email: str, hashed_password: str, confirmation_email=False, reset_email_password=False): 
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.confirmation_email = confirmation_email 
        self.reset_email_password = reset_email_password  
    '''

    
    # what does this do?
    def __repr__(self):
        return '<User %r>' % self.username


'''
class ConfirmationEmail(UserMixin, db.Model):
    # m primary key = email    
    id = db.Column(db.Integer, primary_key=True)
    # foreign key?
    email = db.Column(db.String(120), unique=True)

    registration_confirmation_email = db.Column(db.Boolean, default=False) 
    reset_email_password = db.Column(db.Boolean, default=False)    
    # The foreign key is the child to the adult relationship/connection
    # if I have a class like SomeTable when using the foreign key use 'some_table' 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<confirmation_email %r>' % self.registartion_confirmation_email
'''


class Posts(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    # need a better name then content
    content = db.Column(db.String(120), nullable=False) 
    # gives a  of when the post is posted. Everyone sees the same time based on daylight savings  
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # always create the name of the column of the other database except lowercase and end it with _id
    # The foreign key creates the an column called user.id. This links the two tables. IOW the foreign key is the primary key just in another table.
    # user.id represents the id from the User database. 
    # foreign key has to be added.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    
    # what does this do?
    def __repr__(self):
        return '<Posts %r>' % self.title










