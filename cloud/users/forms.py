from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired


class RegistrationForm(FlaskForm):
    ''' User registration form '''
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
    Length(min=3, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
    Length(min=3, max=20), EqualTo('password')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    ''' User login form '''
    username = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])
    email    = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
