import os     

# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 becomes ['MAX_CONTENT_LENGTH']

class Config:
    # Setup CSRF secret key
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
     # what do these lines do?
    DEBUG = False
    TESTING = False
 
 
    # setting UP GMAIL EMAIL
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ['EMAIL_USER']
    MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

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
    # Is the same valie as ['DEBUG'] =  
    Mail_DEBUG = False  
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

    # Makes it so you can't upload a file to big breaking the database. You get a 413 status code.  
    # ['MAX_CONTENT_LENGTH'] = 1024 * 1024  
    # Makes it so you can only upload certain files
    # ['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
    # Where is this located?
    # ['UPLOAD_PATH'] = 'uploads'
