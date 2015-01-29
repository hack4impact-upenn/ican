from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, TextField, DateField,SelectMultipleField, widgets, SelectField
from wtforms.validators import Required, Email, EqualTo

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class TaskCreationForm(Form):
    students = MultiCheckboxField("Students", coerce=int)
    title = StringField('Task Title')
    description = TextField('Task Description')
    deadline = DateField('When is this task due? (YYYY-MM-DD)')
    submit = SubmitField('Create Tasks')

# TODO: TEMPORARY - added by Annie
class EditProfileForm(Form):
    name = StringField('Name:')
    email = StringField('Email:', validators=[Email()])
    current_password = PasswordField('Current Password:')
    new_password = PasswordField('New Password:')
    submit = SubmitField('Save')

class SignupForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    email = StringField('What is your email?', validators=[Required(), Email()])
    university = SelectField('Which college are you currently enrolled?', validators=[Required()], coerce=int)
    bio = StringField('Tell us about yourself:', validators=[Required()])
    password = PasswordField('Enter a password:', validators=[Required(), EqualTo('password2', message='Passwords must match') ])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Sign up')

class ContactForm(Form):
    text = TextField("Send a text")
    submit = SubmitField('Contact')
