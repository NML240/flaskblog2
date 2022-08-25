import email
import os
# from types import new_class 
import bcrypt
from app.models import User
from flask_migrate import Migrate



from app import create_app, db
from app.config import Config, TestConfig
# why just TestConfig in the create app function?
app = create_app(TestConfig)
migrate = Migrate(app, db)
app.config.from_object(TestConfig())


def test_register_page_get(client):
    client = client()
    #with client:  
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/register requested (GET) 
    THEN check that the response is valid 
    '''
    response = client.get('/register')
    


    '''
    In Python, the assert statement is used to continue the execute if the given condition evaluates to True. 
    If the assert condition evaluates to False, then it raises the AssertionError exception with the specified error message.
    '''
    # Why use a b string? What is response.data? Answer it only work if I have a status code 200.
    assert response.status_code == 200
    assert b'register' in response.data
        
    

def test_register_page_post(client):
    client = client()
    ''' 
    GIVEN a Flask application configured for testing
    WHEN the '/register requested (POST) 
    THEN check that the response is valid 
    '''   
    response = client.post('/register')
    '''
    In Python, the assert statement is used to continue the execute if the given condition evaluates to True. 
    If the assert condition evaluates to False, then it raises the AssertionError exception with the specified error message.
    '''
    # Why use a b string? What is response.data? Answer it only work if I have a status code 200.
    assert response.status_code == 200
    assert b'register' in response.data



 
 

#why does normal scope in pytest work if it in the documentation it says it can be only run once?
def test_verified_email(client, new_user):
    # making the token work because I can't import methods
    client = client()

    ''' 
    GIVEN a Flask application configured for testing
    WHEN the "/verified_email<token>" request is (GET) Also test the email is sent.
    THEN check that the response is valid and the email is True in the database,
    prior it is false in the database.
    '''   
    
    
    response = client.get("/verified_email<token>", follow_redirects=True)
    assert response.status_code == 200
    
    ''' 
    check if the User/token has a value. If it throws an error then the function
    if User is None is running all the time.
    '''
    
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
        pytesting_email = User.query.filter_by(email=new_user.email).first()
        
        # check if the pytesting_email has a value
        assert pytesting_email!= None
        
        db.session.delete(new_user)
        db.session.commit()
    ''' 
    from redmail import EmailSender
    # Just put something as host and port
    email = EmailSender(host="localhost", port=0)
    
    msg = email.get_message(
        subject='email subject',
        sender="me@example.com",
        receivers=['you@example.com'],
        text="Hi, this is an email.",
    )
    assert str(msg) == """from: me@example.com
    subject: email subject
    to: me@example.com
    Content-Type: text/plain; charset="utf-8"
    Content-Transfer-Encoding: 7bit
    MIME-Version: 1.0

    Hi, this is an email.
 
    assert str(msg) == 'i'
    '''
