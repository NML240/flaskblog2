# Register forms 
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import User


# should I improve wff forms to more modern wtforms stlye?

# Also use Registrationform in verified.html
class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=
    [
    DataRequired(message='Username is required'),
    Length(min=1, max=25),
    ])

    email = StringField('Email', validators=
    [
    DataRequired('Email is required'),
    Length(min=4, max=35, message='Must be between 4 and 25 characters'),
    ])


    password = PasswordField('Password', validators=
    [
    DataRequired('Password is required'), 
    Length(min=8, max=25, message='Must be between 8 and 25 characters'),
    ])

    confirm_password = PasswordField('Repeat Password', validators=
    [
    DataRequired('Does not match password'),
    ])
    
    # could this go in routes.py?
    #self?
    
    # I want an email that does not exist 
    # check if the email does exist so you can throw an error 
    '''
    def validate (self, email):
        email = User.query.filter_by(email=email.data.first())
        if email: 
            # raise ValidationError gives a custom error message?
            raise ValidationError ("You have entered an email that already exists. Please select an original email.")
    '''


class LoginForm(FlaskForm):
    # 'todo implement Username_or_email'
    username = StringField('Username', validators=[DataRequired('Username is required')],)  
    password = PasswordField('Password', validators=[DataRequired('Password is required'),])
    




class UpdateAccountForm(FlaskForm):
    password = PasswordField('Password', validators=
    [
    DataRequired('Password is required'), 
    Length(min=8, max=25, message='Must be between 8 and 25 characters'),
    ])

    confirm_password = PasswordField('Repeat Password', validators=
    [
    DataRequired('Does not match password'),
    ])


class EmptyForm(FlaskForm):
    pass





# todo move later
class FileForm(FlaskForm):
    
    image_filename = FileField('image', validators=
    [FileRequired() ,FileAllowed(['jpg', 'png'], 'Images only!')  ])
    submit = SubmitField('Submit')


 