from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class SignupForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    email = StringField('What is your email?', validators=[Required()])
    submit = SubmitField('Submit')
