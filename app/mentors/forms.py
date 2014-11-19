from flask.ext.wtf import Form
from wtforms import SubmitField, TextField, DateField
from wtforms.validators import Required, Email

class TaskCreationForm(Form):
    description = TextField('Task Description', validators=[Required()])
    deadline = DateField('When is this task due?', validators=[Required()])
    submit = SubmitField('Create Tasks')
