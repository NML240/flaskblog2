from flask_migrate import Migrate
# make SQLAlchemy work 
      
from app import create_app, db
app = create_app()
migrate = Migrate(app, db)



# to run the code
'''
$env:FLASK_APP="wsgi"
To use the dubugger use this line.
$env:FLASK_ENV="development"
flask run

'''