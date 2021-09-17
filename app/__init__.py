# __init__.py in not in users folder
 

# why is this line here 
from flask import Flask  
# make SQLAlchemy work 
from flask_sqlalchemy import SQLAlchemy
# make login work
from flask_login import LoginManager# user_loaded_from_header
# make crf protection work 
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)





# setup databases
db = SQLAlchemy()
# Make Login user variable work ?
login_manager = LoginManager()
# Setup CSRF protection. This allows html forms to work and be secure.  
csrf = CSRFProtect()


# imports config from config.py
from app.config import Config



def create_app(config_class=Config): 
     
    
    
    
    
    # what does this do?
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    

    from app.userinfo.routes import userinfo
    from app.postinfo.routes import postinfo
    # why lowercse b in blueprints ?
    app.register_blueprint(userinfo) 
     
    app.register_blueprint(postinfo)
    return app 
 
# from app.models import User 

