from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, EqualTo


class SignupForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    email = StringField('What is your email?', validators=[Required(), Email()])
    password = PasswordField('Enter a password:', validators=[Required(), EqualTo('password2', message='Passwords must match') ])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Sign up')
