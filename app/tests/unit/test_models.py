from app.models import User 
import bcrypt 

def test_new_user():
    ''' 
    Given a User model
    When a new user is being created in
    Check the User database columns
    '''
    # username, hashed_password, email
    
    
    plaintext_password = 'jotpjgjbgt'
    hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())
    
    user = User('ugbuighiug', hashed_password ,'sefefo3240@svcache.com')
    assert user.username == 'ugbuighiug'
    # make sure password hashed
    assert user.hashed_password == hashed_password
    # make sure not plaintext password 
    assert user.hashed_password != plaintext_password 
    assert user.email == 'sefefo3240@svcache.com'

 
