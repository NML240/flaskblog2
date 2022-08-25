# __init__.py in not in users folder

# why is this line here  
from flask import Flask  
 
# make SQLAlchemy work 
from flask_sqlalchemy import SQLAlchemy

# make login work
from flask_login import LoginManager 

from flask_redmail import RedMail 

# imports config from config.py
from app.config import Config

 


# setup databases
db = SQLAlchemy()







# make csrf protection work 
from flask_wtf.csrf import CSRFProtect
# Setup CSRF protection. This allows html forms to work and be secure
csrf = CSRFProtect()

# make mail work?
email = RedMail()


from app.models import User

app = Flask(__name__)

# Make @login_required work
login_manager = LoginManager(app)
# You get a custom login message when @login_required appears in the code.
login_manager.login_message_category = 'Login is required'

# The name you would use is the name in url_for() for the login route.
# Should I use userinfo.login? 
login_manager.login_view = 'login' 


@app.login_manager.user_loader
def load_user(id):
    return User.query.get(id) 




def create_app(Config): 
     
    
    # load function from config file
    # ('config_class')  'Config' is the name of config.py class
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    email.init_app(app)    
    csrf.init_app(app)
 

    

    from app.userinfo.routes import userinfo
    from app.postinfo.routes import postinfo
    from app.mail.routes import mail 

    # why lowercse b in blueprints ?
    app.register_blueprint(mail)
    app.register_blueprint(userinfo)     
    app.register_blueprint(postinfo)

    return app 

  


 