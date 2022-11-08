from flask_migrate import Migrate
   

from app import create_app, db

from app.config import Config

app = create_app(Config)

# render_as_batch generates a brand new table with the new schema and copy all the data. 
# This is used in flask-migrate to downgrade
migrate = Migrate(app, db, render_as_batch=True)
app.config.from_object(Config)


# to run the code
'''
To setup the app to run from a specif file type the below line. Only do Once.
$env:FLASK_APP="wsgi"
To use the dubugger use this line.
$env:FLASK_ENV="development"
flask run

'''