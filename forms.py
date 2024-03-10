from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email

class RegisterUserForm(FlaskForm):
    """Form for registering a new user"""
    username = StringField('Username',
                           validators=[InputRequired()])
    password = PasswordField('Password',
                             validators=[InputRequired()])
    email = StringField('Email Address',
                        validators = [InputRequired(), Email()])
    first_name = StringField('First Name',
                             validators=[InputRequired()])
    last_name = StringField('Last Name',
                             validators=[InputRequired()])
    

class LoginForm(FlaskForm):
    """Form for logging in"""
    username = StringField('Username',
                           validators=[InputRequired()])
    password = PasswordField('Password',
                             validators=[InputRequired()])
    
class FeedbackForm(FlaskForm):
    """ Form for adding feedback to a user"""
    title = StringField('Title',
                        validators=[InputRequired()])

    content = TextAreaField('Content',
                            validators=[InputRequired()])
    
    