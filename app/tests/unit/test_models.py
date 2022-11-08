import os 

from app.models import User, db

def test_new_user_with_fixture(new_user,  plaintext_password = 'pojkp[kjpj[pj'):
    # testing_hashed_password = hashed_password
    # assert new_user.id == 5 
    # assert new_user.id == 0  
    
    
    new_user = User.query.filter_by(username=new_user.username).first()
    assert new_user.username == 'fkpr[kfkuh' 
    assert new_user.email == os.environ['TESTING_EMAIL_USERNAME']
    assert plaintext_password == 'pojkp[kjpj[pj'
    assert new_user.hashed_password != 'pojkp[kjpj[pj'

    # make sure password hashed    
''' 
    assert new_user.hashed_password == testing_hashed_password 
    # make sure not plaintext password 
    assert new_user.hashed_password != 'jotpjgjbgt'
    '''

