# posts form  
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length



class Postform(FlaskForm):
    title = StringField('title', validators=[DataRequired('title is required')],)  
    content = TextAreaField('content', validators=[DataRequired('content is required')],) # need better phrasing then 'content is required'
    