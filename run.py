# import __init__.py in the usersinfo folder
from app import create_app
app = create_app()

if __name__ == '__main__': 
    app.run(debug=True)
    