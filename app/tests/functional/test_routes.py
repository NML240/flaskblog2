from flask import Flask, Blueprint
from app import create_app
from app.config import Config
from app import CSRFProtect
from app.userinfo.routes import userinfo
from app import csrf





def test_register_page_get():
    """ 
    GIVEN a Flask application configured for testing
    WHEN the '/page requested (GET) 
    THEN check that the response is valid 
    """
 
    flask_app = create_app()
    # The with statemnt allows you to open and close files safely by making sure there is no errors
    # What is test_client?  test_client makes requests to the application without running a live server
    # Use the test_client to check the route which is a get request
    with flask_app.test_client() as test_client: 
        response = test_client.get('/register')
        """
        In Python, the assert statement is used to continue the execute if the given condition evaluates to True. 
        If the assert condition evaluates to False, then it raises the AssertionError exception with the specified error message.
        """
        # Why use a b string? What is response.data? Answer it only work if I have a status code 200.
        assert response.status_code == 200
        assert b'register' in response.data






def test_register_page_post():
    """ 
    GIVEN a Flask application configured for testing
    WHEN the '/register'page requested (post) 
    THEN check that the response is valid 
    """
   

    flask_app = create_app()
    # The with statemnt allows you to open and close files safely by making sure there is no errors
    # What is test_client?  test_client makes requests to the application without running a live server
    # Use the test_client to check the route which is a get request
    with flask_app.test_client() as test_client: 
        response = test_client.post('/register')
        """
        In Python, the assert statement is used to continue the execute if the given condition evaluates to True. 
        If the assert condition evaluates to False, then it raises the AssertionError exception with the specified error message.
        """
        # Why use a b string? What is response.data? Answer it only work if I have a status code 405.
        assert response.status_code == 200
        # checking html for the term register
        assert b'register' in response.data
        