from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, IntegerField
from wtforms.validators import Required, Email, EqualTo, NumberRange

class SignupForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    email = StringField('What is your email?', validators=[Required(), Email()])
    university = SelectField('Which college are you going to?', validators=[Required()], coerce=int)
    phone = IntegerField('Phone: ', validators=[NumberRange(min=1000000000,max=9999999999)])
    password = PasswordField('Enter a password:', validators=[Required(), EqualTo('password2', message='Passwords must match') ])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Sign up')

class ContactForm(Form):
    message = TextAreaField('Enter your message', validators=[Required()])
    submit = SubmitField('Send')

class EditProfileForm(Form):
    name = StringField('Name:')
    email = StringField('Email:', validators=[Email()])
    phone = IntegerField('Phone: ', validators=[NumberRange(min=1000000000,max=9999999999)])
    current_password = PasswordField('Current Password:')
    new_password = PasswordField('New Password:')
    submit = SubmitField('Save')

class CompletedTaskForm(Form):
    completed = SubmitField('Mark as completed')

class UncompletedTaskForm(Form):
    completed = SubmitField('Mark as incomplete')
