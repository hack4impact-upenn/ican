from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import Student
from ..email import send_email
from . import main
from .forms import SignupForm


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student is None:
            student = Student(email=form.email.data, name=form.name.data)
            db.session.add(user)
            return redirect(url_for('.index'))
        else:
            #throw some error and rerender form
            return redirect(url_for('.index'))
    return render_template('signup.html',
                           form=form)

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')
