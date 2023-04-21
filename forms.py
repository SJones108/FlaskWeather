from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    '''
    set user login variables for the flask app using
    validators to ensure all necessary information is
    input and session is secure
    '''
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()
