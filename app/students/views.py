from . import students
from ..models import User, FAQ, Task
from .. import db
from flask import render_template, session, redirect, url_for, current_app, flash
from ..decorators import student_required
from flask.ext.login import login_required, current_user, login_user
from forms import SignupForm, ContactForm, EditProfileForm
from ..email import send_email

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
            # TODO Assign tasks to students based on University
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

@students.route('/task/<task_id>')
def task_view(task_id):
    task = Task.query.get(task_id)
    mark_completed_form = None # todo
    return render_template('student/task-edit.html', task=task, form=mark_completed_form)

@students.route('/mentor')
def mentor():
    return render_template('student/mentor.html', student=current_user, mentor=current_user.mentor)

@students.route('/faq')
def faq():
    return render_template('student/faq.html', faqs=FAQ.query)

@students.route('/profile')
def profile():
    return render_template('student/profile.html', student=current_user)

# TODO: add form to confirm student edits -- @Maya
@students.route('/profile-edit', methods=['GET', 'POST'])
def profile_edit():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        if (form.new_password.data and form.current_password.data):
            if current_user.verify_password(form.current_password.data):
                current_user.password = form.new_password.data
                db.session.add(current_user)
                flash('Your profile has been updated')
            else:
                flash('Invalid current password; password not updated')
        else:
            db.session.add(current_user)
            flash('Your profile has been updated')
        return redirect(url_for('.index'))
    form.name.data = current_user.name
    form.email.data = current_user.email
    return render_template('student/profile-edit.html', student=current_user, form=form)

@students.route('/college')
def college():
    return render_template('student/college.html', college=current_user.university)

@students.route('/contact', methods=['GET','POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_email("ali.altaf9@gmail.com", 'A student has reached out!', 'email/contact', email_body=form.message)
        flash('Your email has been sent to iCAN! They\'ll respond shortly!')
        return redirect(url_for('.index'))
    return render_template('student/contact.html', form=form)
