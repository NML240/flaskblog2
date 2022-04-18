from app import create_app


def test_login_page():
    """ 
    GIVEN a Flask application configured for testing
    WHEN the '/login'page requested (GET) 
    THEN check that the response is valid 
    """
    # what is 'flask_test.cfg'?
    flask_app = create_app('flask_test.cfg')
    # The with statemnt allows you to open and close files safely by making sure there is no errors
    # What is test_client?  test_client makes requests to the application without running a live server
    # Use the test_client to check the route which is a get request
    with flask_app.test_client() as test_client: 
        response = test_client.post('/login')
        """
        In Python, the assert statement is used to continue the execute if the given condition evaluates to True. 
        If the assert condition evaluates to False, then it raises the AssertionError exception with the specified error message.
        """
        # Why use a b string? What is response.data? Does it only work if I have a status code like 200?
        assert response.status_code == 405
        
        # checking username 
        assert b'Flask User management Example' in response.data
        ''' 
        # checking email
        assert b' You need an an account' in response.data
        # checking hashed_password
        assert b'The password is plaintext' in response.data
        # checking confirmation_email
        assert b'The registeration email is False' in response.data
        '''