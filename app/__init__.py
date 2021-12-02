# __init__.py in not in users folder

# for setting up environment variables
import os
# why is this line here 
from flask import Flask  
 
# make SQLAlchemy work 
from flask_sqlalchemy import SQLAlchemy
# make login work
from flask_login import LoginManager# user_loaded_from_header



from flask_mail import Mail

app = Flask(__name__)
# setup databases
db = SQLAlchemy()
# Make Login user variable work ?
login_manager = LoginManager()

#You get a custom login message when @login_required appears in the code.
login_manager.login_message_category = 'Login is required'

# make csrf protection work 
from flask_wtf.csrf import CSRFProtect
# Setup CSRF protection. This allows html forms to work and be secure
csrf = CSRFProtect()

# make mail work?
mail = Mail()

# imports config from config.py
from app.config import Config

def create_app(config_class=Config): 
    
    # what does this do?
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    # add mail = Mail(app) to .init_app
    mail.init_app(app)

    # add environment variables 27:25 https://www.youtube.com/watch?v=vutyTx7IaAI
    
   
   
    from app.userinfo.routes import userinfo
    from app.postinfo.routes import postinfo
    # why lowercse b in blueprints ?
    app.register_blueprint(userinfo)     
    app.register_blueprint(postinfo)
    return app 
 
# from app.models import User 

