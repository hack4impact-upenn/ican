from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, TextField, DateField,SelectMultipleField, widgets
from wtforms.validators import Required, Email

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
    description = TextField('Task Description')
    deadline = DateField('When is this task due?')
    submit = SubmitField('Create Tasks')

# TODO: TEMPORARY - added by Annie
class EditProfileForm(Form):
    name = StringField('Name:')
    email = StringField('Email:', validators=[Email()])
    current_password = PasswordField('Current Password:')
    new_password = PasswordField('New Password:')
    submit = SubmitField('Save')
