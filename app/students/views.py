from . import students
from flask import render_template, session, redirect, url_for, current_app
from ..decorators import student_required
from flask.ext.login import login_required, current_user
from forms import SignupForm
import datetime

@students.route('/')
# @login_required
# @student_required
def index():
    name = current_user.name # string
    email = current_user.email # string
    mentor = current_user.mentor # mentor object
    tasks = current_user.tasks.all() # list of tasks
    return render_template('student/menu.html', name=name, email=email, mentor=mentor, tasks=tasks, date=datetime.date)

@students.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        student = Students.query.filter_by(email=form.email.data).first()
        if student is None:
            student = Student(email=form.email.data, name=form.name.data)
            db.session.add(student)
            return redirect(url_for('.index'))
        else:
            #throw some error and rerender form
            return redirect(url_for('.index'))
    return render_template('student/signup.html',
                            form=form)
