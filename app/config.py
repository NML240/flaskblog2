# for setting up environment variables
import os      
# This gives me the file which is represented by __file__ path as an absolute import. 
basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 becomes ['MAX_CONTENT_LENGTH']

# what is object ?
class Config: 
    # Setup CSRF secret key
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # why can't I use the below for flask-migrate
    # SQLALCHEMY_DATABASE_URI ='sqlite:///db.sqlite3'
    # EMAIL_SENDER = 

    # I get 'DATABASE_URI' sqlite:///app.db or I get os.path.join(basedir, 'app.db') gives me test.db route
    # "\" is used as newline 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
         
   
    DEBUG = True
    # Is this for pytest?
    TESTING = True
    # When False this disables wtf forms. This useful for pytests that are POST request.
    WTF_CSRF_ENABLED = False
    
    
    
    # setting UP Outlook email  

    from redmail import outlook
    outlook.username = os.environ['EMAIL_USERNAME']
    outlook.password  = os.environ['EMAIL_PASSWORD']
    EMAIL_HOST = 'smtp.office365.com'
    EMAIL_PORT = '587'   
    # need this to prevent error in redmail. 
    SECURITY_EMAIL_SENDER = os.environ['EMAIL_USERNAME']
    
    
    
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

    
    
    
    # Makes it so you can't upload a file to big breaking the database. You get a 413 status code.  
    # ['MAX_CONTENT_LENGTH'] = 1024 * 1024  
    # Makes it so you can only upload certain files
    # ['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
    # Where is this located?
    # ['UPLOAD_PATH'] = 'uploads'
