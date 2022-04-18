from app.models import User 

def test_new_user():
    ''' 
    Given a User model
    When a new user is being logged in
    Check the User database columns
    '''
   
   # username  hashed_password  emai  confirmation_email  reset_email_password 
    user = User('aiohrgihrtg', 'jotpjgjbgt','nojafa5998@royins.com', True, False)
    # Just for testing ?
    assert user.username == 'aiohrgihrtg'
    ''' 
    # check if the user exists in the other file by checking if email exists
    assert user.email == 'nojafa5998@royins.com'
    # check to make sure the hashed password doesn't contain plaintext.
    assert user.hashed_password!= 'jotpjgjbgt'
    # check if the email is registered
    assert user.confirmation_email == True
    '''


