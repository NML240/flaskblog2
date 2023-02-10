


# for setting up environment variables
import os
 
import stripe

# This gives me the filename which is represented by __file__ path as an absolute import. 
# I should probably create a folder 
basedir_for_database = os.path.abspath(os.path.dirname(__file__))

#delete below
# This gives me the filename which is represented by __file__ path as an absolute import. 
#basedir_for_uploads = os.path.abspath(os.path.profilepictures(__file__))



# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 becomes ['MAX_CONTENT_LENGTH']

# app.config['SECRET_KEY'] ,is removed in the class config's and becomes just SECRET_KEY
# what is object ?
class Config(object): 
    # Setup CSRF secret key
    # change to environment variable
    SECRET_KEY = 'temp_secret_key'
    # this is the test key for stripe
    stripe.api_key = os.environ['STRIPE_SECRET_KEY']
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # why can't I use the below for flask-migrate
    # SQLALCHEMY_DATABASE_URI ='sqlite:///db.sqlite3'
    # EMAIL_SENDER = 

    # I get 'DATABASE_URI' sqlite:///app.db or I get os.path.join(basedir, 'app.db') gives me app.db route
    # "\" is used as newline 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
    'sqlite:///' + os.path.join(basedir_for_database, 'app.db')
         
    # should it be False?
    DEBUG = True
    #  for pytest?
    TESTING = True
    # When False this disables wtf forms. This makes POST request work for pytest when False.
    WTF_CSRF_ENABLED = True
  
    
    # setting UP Outlook email  

    from redmail import outlook
    outlook.username = os.environ['EMAIL_USERNAME']
    outlook.password  = os.environ['EMAIL_PASSWORD']
    EMAIL_HOST = 'smtp.office365.com'
    EMAIL_PORT = '587'   
    # need this to prevent error in redmail. 
    SECURITY_EMAIL_SENDER = os.environ['EMAIL_USERNAME']
    
    # need this to prevent error in redmail. 
    SECURITY_EMAIL_SENDER = "no-reply@example.com"
    
    
    
    # Is the same valie as ['DEBUG'] =  
    Mail_DEBUG = True  
  

    # connect to your mail server not your email address
    # confused by localhost
    # MAIL_SERVER = 'localhost' 
    
    '''
    #depends on email provider
    MAIL_PORT =  None 
    # used for security purposes depend on email provider
    
    MAIL_USE_TLT = False
    MAIL_USE_SSL = False 
    ''' 
    '''
    # username of the linked mail account  
    MAIL_USERNAME = None
    # password of the linked mail account
    MAIL_PASSWORD = None
    '''
    # default email a user recieves when a email is sent unless you make a value
    MAIL_DEFAULT_SENDER = None  
    # Make so you can only send x amount of emails at one time. Can also set to none.
    MAIL_MAX_EMAILS = 5  
    # same value ['TESTING'] =. If you are testing your app if you don't want to send emails make it True?
    # ['MAIL_SUPRESS_SEND'] = False 
    # converts file name to ascii. ascii characters are english characters.
    MAIL_ASCII_ATTACHMENTS = False 

    # why does this need env vcariable?
    ELASTICSEARCH_URL = 'http://localhost:9200'

    UPLOAD_FOLDER = r"C:\Users\nmyle\OneDrive\Desktop\flaskcodeusethis\flaskblog2\app\static\profilepictures"
    # max a file can be is 1 megabyte is that big enough? Todo add warning
    MAX_CONTENT_LENGTH = 1024 * 1024
class PytestConfig(Config): 
    DEBUG = False
    # Is the same value as ['DEBUG'] =  
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = '0' 
    Mail_DEBUG = True  
    # for pytest
    TESTING = True	   
    # same value ['TESTING'] =. If you are testing your app if you don't want to send emails make it True?
    MAIL_SUPRESS_SEND = True  
    # When False this disables wtf forms. This makes POST request work for pytest when False.
    WTF_CSRF_ENABLED = False 
    SQLALCHEMY_TRACK_MODIFICATIONS = True 
    # I get 'DATABASE_URI' sqlite:///app.db or I get os.path.join(basedir, 'app.db') gives me app.db route
    # "\" is used as newline 

'''
class TokenPytestConfig(Config): 
    
    # When False this disables wtf forms. This makes POST request work for pytest when False.
    WTF_CSRF_ENABLED = False
    TESTING = True	
    #Debug needs to = False or I will get an error caused by create_all(...) vs delete_all(...).
    DEBUG = False
'''



'''
    from redmail import outlook
    outlook.username = os.environ['EMAIL_USERNAME']
    outlook.password  = os.environ['EMAIL_PASSWORD']
    '''