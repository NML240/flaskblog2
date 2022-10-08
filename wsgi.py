from flask_migrate import Migrate
   




from app import create_app, db

from app.config import Config

app = create_app(Config)
migrate = Migrate(app, db)
app.config.from_object(Config)


# to run the code
'''
To setup the app to run from a specif file type the below line. Only do Once.
$env:FLASK_APP="wsgi"
To use the dubugger use this line.
$env:FLASK_ENV="development"
flask run

'''