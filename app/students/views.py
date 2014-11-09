from . import students
from flask import render_template, session, redirect, url_for, current_app
from ..decorators import student_required
from flask.ext.login import login_required, current_user
from forms import SignupForm

@students.route('/')
# @login_required
# @student_required
def index():
    return render_template('student/landing.html')

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
