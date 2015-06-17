from flask.ext.wtf import Form
from wtforms import SelectField, SubmitField, StringField, TextField, DateField, widgets, SelectMultipleField, TextAreaField
from wtforms.validators import Required

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ReassignForm(Form):
    mentor = SelectField('Which mentor do you want to assign them to', validators=[Required()], coerce=int)
    submit = SubmitField('Reassign')

class EditTaskForm(Form):
    title = StringField('Task Title')
    description = TextField('Task Description')
    deadline = DateField('When is this task due? (YYYY-MM-DD)')
    submit = SubmitField('Update Task')

class TaskCreationForm(Form):
    universities = MultiCheckboxField("Universities", coerce=int)
    title = StringField('Task Title')
    description = TextField('Task Description')
    deadline = DateField('When is this task due? (YYYY-MM-DD)')
    submit = SubmitField('Create Task')

class EditFAQForm(Form):
    question = TextField('Question')
    answer = TextField('Answer')
    submit = SubmitField('Update FAQ')

class FAQCreationForm(Form):
    question = TextField('Question')
    answer = TextField('Answer')
    submit = SubmitField('Create FAQ')

class EditUniversityForm(Form):
    description = TextAreaField('University Description')
    submit = SubmitField('Update University')