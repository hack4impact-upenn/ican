from . import students
from ..models import User, FAQ, Task
from .. import db
from flask import render_template, session, redirect, url_for, current_app
from ..decorators import student_required
from flask.ext.login import login_required, current_user, login_user
from forms import SignupForm, ContactForm

import datetime

@students.route('/')
@login_required
@student_required
def index():
    # name = student.name
    # tasks = student.tasks.all()
    print "*****"
    print current_user.tasks
    print "*****"
    return render_template('student/menu.html', student=current_user, date=datetime.datetime, tasks=[])

@students.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        student = User.query.filter_by(email=form.email.data).first()
        if student is None:
            student = User(email=form.email.data, name=form.name.data, password=form.password.data, user_role='student')
            # student.password(form.password.data)
            student.match_with_mentor()
            db.session.add(student)
            db.session.commit()
            login_user(student)
            return redirect(url_for('.index'))
        else:
            #throw some error and rerender form
            return redirect(url_for('.index'))
    return render_template('student/signup.html',
                            form=form)

@students.route('/tasks')
def tasks():
    ordered_tasks = current_user.tasks.order_by(Task.deadline)
    return render_template('student/tasks.html', student=current_user, tasks=ordered_tasks, date=datetime.datetime.now())

@students.route('/mentor')
def mentor():
    return render_template('student/mentor.html', student=current_user, mentor=current_user.mentor)

@students.route('/faq')
def faq():
    return render_template('student/faq.html', faqs=FAQ.query.all())

@students.route('/profile')
def profile():
    return render_template('student/profile.html', student=current_user)

@students.route('/college')
def college():
    return render_template('student/college.html', student=current_user)

@students.route('/contact')
def contact():
    return render_template('student/contact.html', form=ContactForm())
