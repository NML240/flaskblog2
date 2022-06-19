
# Register forms 
from flask_wtf import FlaskForm
from wtforms import TextAreaField, BooleanField, PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired, Length , ValidationError
from flask_wtf.file import FileField, FileAllowed 


class RequestResetPasswordForm(FlaskForm):
    
    email = EmailField('Email', validators=
    [
    DataRequired('Email is required'),
    # Is the line below useful
    Length(min=4, max=25, message='Must be between 4 and 25 characters'),
    ])
       
    reset_password = PasswordField('Password', [validators.Length(min=4, max=25)]) 
    # does 'profilepicture' below need to match the database?
    #update_picture = FileField('profilepicture', validators=[FileAllowed(['jpg', 'png'])])  
    
    # Could the function below be in routes.py?

    # I want an email that does exist
    '''
    # check if the email does not exist so you can throw an error 
    def validate (self, email):
        email = User.query.filter_by(email=email.data.first())
        # is None just checks if it is none
        if email is None: 
            raise ValidationError ("You have entered a email that does not exist. Please register a valid email.")
    ''' 


    class EmptyForm2(FlaskForm):
        pass 
