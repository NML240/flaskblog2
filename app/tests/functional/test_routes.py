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
   




def valid_login( init_database, new_user, make_app_run_in_test_env,):
    """ 
    Given a flask app tests if it runs  
    When I check to make valid login and logout (POST) request
    Then I should be able to check login and logout using pytest
    """
    init_database
    # new user is a dict
    data = new_user 
    # If an endpoint which redirects needs to be tested, then follow_redirects=True is useful because it lets the client go to the redirected location.
    # let me check
    # can I just ask a very stupid question in my redirect route in the post request I redirected to the home page. 
    # So response == 200 is fron the home page?
    response = make_app_run_in_test_env.post('/login', data, follow_redirects=True)
    assert response.status_code == 200
    
    response = make_app_run_in_test_env.get('/logout', data, follow_redirects=True)
    assert response.status_code == 200
    assert b'ttttttttttttttttt' in response.data
     


# How do I fix this?
'''' 
def test_invalid_login(init_database, make_app_run_in_test_env):
    
    init_database
    new_user = None
    # the passwords don't match
    data = new_user(email= 'fijhrpihnp' ,password='FlaskIsGreat', confirm='FlskIsGreat')
    response = make_app_run_in_test_env.post('/login', data, follow_redirects=True)
    assert response.status_code == 200
'''





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
'''




