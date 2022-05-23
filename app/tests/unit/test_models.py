
import bcrypt 

def test_new_user_with_fixture(new_user, plaintext_password):
   
    # testing_hashed_password = hashed_password
    assert new_user.username == 'ugbuighiug'
    assert new_user.email == 'sefefo3240@svcache.com'
    assert plaintext_password == 'jotpjgjbgt'
    assert new_user.hashed_password != 'jotpjgjbgt'
    
    

    # make sure password hashed    
    ''' 
    assert new_user.hashed_password == testing_hashed_password 
    # make sure not plaintext password 
    assert new_user.hashed_password != 'jotpjgjbgt'
    '''
    