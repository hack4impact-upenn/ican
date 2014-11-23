from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, TextField, DateField
from wtforms.validators import Required, Email

class TaskCreationForm(Form):
    description = TextField('Task Description', validators=[Required()])
    deadline = DateField('When is this task due?', validators=[Required()])
    submit = SubmitField('Create Tasks')

# TODO: TEMPORARY - added by Annie
class EditProfileForm(Form):
    name = StringField('Name:')
    email = StringField('Email:', validators=[Email()])
    current_password = PasswordField('Current Password:')
    new_password = PasswordField('New Password:')
    submit = SubmitField('Save')
    from wtforms.validators import Required, Email, EqualTo