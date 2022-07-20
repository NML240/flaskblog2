import email
import os 
import bcrypt
from app.models import User



def test_register_page_get(make_app_run_in_test_env):
    """ 
    GIVEN a Flask application configured for testing
    WHEN the '/register requested (GET) 
    THEN check that the response is valid 
    """
    response = make_app_run_in_test_env.get('/register')
    """
    In Python, the assert statement is used to continue the execute if the given condition evaluates to True. 
    If the assert condition evaluates to False, then it raises the AssertionError exception with the specified error message.
    """
    # Why use a b string? What is response.data? Answer it only work if I have a status code 200.
    assert response.status_code == 200
    assert b'register' in response.data
   

def test_register_page_post(make_app_run_in_test_env):

    """ 
    GIVEN a Flask application configured for testing
    WHEN the '/register requested (POST) 
    THEN check that the response is valid 
    """    
    response = make_app_run_in_test_env.post('/register')
    """
    In Python, the assert statement is used to continue the execute if the given condition evaluates to True. 
    If the assert condition evaluates to False, then it raises the AssertionError exception with the specified error message.
    """
    # Why use a b string? What is response.data? Answer it only work if I have a status code 200.
    assert response.status_code == 200
    assert b'register' in response.data



 
 


def test_verified_email(make_app_run_in_test_env, new_user):
    # making the token work because I can't import methods
    
    
    '''
    example uid is a variable in the function
    response = make_app_run_in_test_env.get(f'/user/{uid}')
    '''
    response = make_app_run_in_test_env.get("/verified_email<token>", follow_redirects=True)
    # user = User.query.filter_by(email=new_user.email).first()
    #token = user.create_token() 
    assert response.status_code == 200

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
    """
    assert str(msg) == 'i'

# Each function needs test infront of it to work
def test_valid_login(make_app_run_in_test_env,init_database, new_user):
    """
    Given a flask app tests if it runs  
    When I check to make valid login and logout (POST) request
    Then I should be able to check login and logout using pytest
    """
 
    # If an endpoint which redirects needs to be tested, then follow_redirects=True is useful because it lets the client go to the redirected location.
    # let me check
    # can I just ask a very stupid question in my redirect route in the post request I redirected to the home page. 
    # So response == 200 is fron the home page? 
    
    # hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())
 
    # hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())
   
    response = make_app_run_in_test_env.post('/login', 
    data = dict(username=new_user.username, hashed_password=new_user.hashed_password, email=new_user.email),
    # dict(username='fjrofjfjrbtt', hashed_password=hashed_password, email='dibapav117@runqx.com'),
    # The reason I use "follow_redirects=True" is because I am being redirected in the login route.
    # iow's i use redirect in the POST request?
    follow_redirects=True)
    assert response.status_code == 200
 
    response = make_app_run_in_test_env.get('/logout', 
    data = dict(username=new_user.username, hashed_password=new_user.hashed_password, email=new_user.email),
    follow_redirects=True)
    assert response.status_code == 200
    
    
#data=dict(username=new_user.username, hashed_password=new_user.hashed_password, email=new_user.email), 
""" 
def test_invalid_login(init_database, make_app_run_in_test_env):
    
    init_database
    new_user = None
    # the passwords don't match
    data = new_user(email= 'fijhrpihnp' ,password='FlaskIsGreat', confirm='FlskIsGreat')
    response = make_app_run_in_test_env.post('/login', data, follow_redirects=True)
    assert response.status_code == 200
"""





""" 
# what is the point of this function should it not always return an error.
# this should throw an error because I logged in twice
def test_duplicate_registration(make_app_run_in_test_env, init_database, new_user):
    init_database
    data = new_user 

    # use post because I want the data
    response = response.make_app_run_in_test_env.post('/login',data, follow_redirect=True)
    assert response.status_code == 200

    response = response.make_app_run_in_test_env.post('/login',data, follow_redirect=True)
    assert response.status_code == 200
"""


''' 
def test_register_page_post(test_client):
    """ 
    GIVEN a Flask application configured for testing
    WHEN the '/register'page requested (post) 
    THEN check that the response is valid 
    """

    response = test_client.post('/register')
    """
    In Python, the assert statement is used to continue the execute if the given condition evaluates to True. 
    If the assert condition evaluates to False, then it raises the AssertionError exception with the specified error message.
    """
    # Why use a b string? What is response.data? Answer it only work if I have a status code 405.
    assert response.status_code == 200
    # checking html for the term register
    assert b'register' in response.data
    """ 
'''






#data=dict(username=new_user.username, hashed_password=new_user.hashed_password, email=new_user.email), 
""" 
def test_invalid_login(init_database, make_app_run_in_test_env):
    
    init_database
    new_user = None
    # the passwords don't match
    data = new_user(email= 'fijhrpihnp' ,password='FlaskIsGreat', confirm='FlskIsGreat')
    response = make_app_run_in_test_env.post('/login', data, follow_redirects=True)
    assert response.status_code == 200
"""





""" 
# what is the point of this function should it not always return an error.
# this should throw an error because I logged in twice
def test_duplicate_registration(make_app_run_in_test_env, init_database, new_user):
    init_database
    data = new_user 

    # use post because I want the data
    response = response.make_app_run_in_test_env.post('/login',data, follow_redirect=True)
    assert response.status_code == 200

    response = response.make_app_run_in_test_env.post('/login',data, follow_redirect=True)
    assert response.status_code == 200
"""


''' 
def test_register_page_post(test_client):
    """ 
    GIVEN a Flask application configured for testing
    WHEN the '/register'page requested (post) 
    THEN check that the response is valid 
    """

    response = test_client.post('/register')
    """
    In Python, the assert statement is used to continue the execute if the given condition evaluates to True. 
    If the assert condition evaluates to False, then it raises the AssertionError exception with the specified error message.
    """
    # Why use a b string? What is response.data? Answer it only work if I have a status code 405.
    assert response.status_code == 200
    # checking html for the term register
    assert b'register' in response.data
    """ 
'''

