from flask_migrate import Migrate
# make SQLAlchemy work 
      
from app import create_app, db
app = create_app()
migrate = Migrate(app, db)

