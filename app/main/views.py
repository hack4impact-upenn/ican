from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import Student
from ..email import send_email
from . import main
from .forms import SignupForm


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student is None:
            student = Student(email=form.email.data, name=form.name.data)
            db.session.add(student)
            return redirect(url_for('.menu'))
        else:
            #throw some error and rerender form
            return redirect(url_for('.menu'))
    return render_template('index.html',
                           form=form)

@main.route('/menu')
def index():
    return render_template('menu.html')
