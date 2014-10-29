from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import Required, EqualTo, Email


# @backend TODO check
class SignupForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    email = StringField('What is your email?', validators=[Required(), Email()])
    number = StringField('What is your phone number?', validators=[Required()])
    school = SelectField(u'What college are you going attend?',
     choices=[('temple', 'Temple University'), ('ccp', 'Community College of Philadelphia')], default=None)
    password = PasswordField('New Password', [Required(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    submit = SubmitField('Submit')


# @backend TODO check
class LoginForm(Form):
    email = StringField('Email', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Submit')