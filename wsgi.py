from flask_migrate import Migrate
# make SQLAlchemy work 
from flask import Config      

# from app.models import User



from app import create_app, db

from app.config import Config

app = create_app(Config)
migrate = Migrate(app, db)
app.config.from_object(Config())



''' 
# Use User.query.get instead of User.get because of sqlalchemy
# This function logs you in and since there is no way of storing in the database I need the function
# Add @app because of the way the app is structured
@app.login_manager.user_loader
def load_user(id):
    return User.query.get(id)
'''

# to run the code
'''
To setup the app to run  from a specif file type the below line. Only do Once.
$env:FLASK_APP="wsgi"
To use the dubugger use this line.
$env:FLASK_ENV="development"
flask run

'''