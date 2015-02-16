import datetime

from . import mentors
from ..decorators import mentor_required
from ..models import User, Task, University
from forms import TaskCreationForm, EditProfileForm, SignupForm, ContactForm
from ..import db
from ..email import send_text

from flask import render_template, session, redirect, url_for, flash, current_app
from flask.ext.login import login_required, current_user, login_user
from twilio.rest import TwilioRestClient


@mentors.route('/')
@login_required
@mentor_required
def index():
    return render_template('mentor/menu.html')


@mentors.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    form.university.choices = [(u.id,u.name) for u in University.query.all()]
    if form.validate_on_submit():
        userTest = User.query.filter_by(email=form.email.data).first()
        if not userTest:
            u = University.query.get(form.university.data)
            user = User(email=form.email.data,
                        name=form.name.data,
                        university=u,
                        bio=form.bio.data,
                        password=form.password.data,
                        user_role = "mentor",
                        phone=form.phone.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('.index'))
        else:
            flash("This Username/Password is already in use.")
            return redirect(url_for('.signup'))
    return render_template('mentor/signup.html', form = form)

@mentors.route('/profile')
@login_required
@mentor_required
def profile():
    return render_template('mentor/profile.html')


@mentors.route('/tasks')
@login_required
@mentor_required
def tasks():
    taskList = [i for i in current_user.get_all_tasks_list() if i.completed is False]
    students = current_user.students
    return render_template('mentor/tasks.html', students=students, User=User, tasks=taskList, date=datetime.datetime.now())


@mentors.route('/students')
@login_required
@mentor_required
def students():
    students = current_user.students
    student_data = []
    for student in students:
        dic = {}
        total_tasks = len(student.tasks.all())
        completed_tasks = len(student.tasks.filter_by(completed=True).all())
        dic['name'] = student.name
        dic['id'] = student.id
        dic['percentage'] = 1.0*completed_tasks/total_tasks
        student_data.append(dic)
    return render_template('mentor/students.html', students=student_data)


@mentors.route('/students/<student_id>', methods=['GET','POST'])
@login_required
@mentor_required
def student(student_id):
    form = ContactForm()
    student = User.query.get(student_id)
    if student.user_role != 'student' or student.mentor != current_user:
        flash("You are not authorized to view this user!")
        return redirect(url_for('.students'))
    tasks = student.tasks.order_by(Task.deadline)
    overdue = []
    upcoming = []
    completed = []
    for task in tasks:
        if task.completed:
            completed.append(task)
        elif datetime.datetime.now() > task.deadline:
            overdue.append(task)
        else:
            upcoming.append(task)

    if form.validate_on_submit():
        name = student.name
        flash(name + ' has been sent a message!')
        send_text(student.phone, form.text.data)
        return redirect(url_for('.students'))
    return render_template('mentor/overview.html', form=form, student=student, date=datetime.datetime, completed=completed, overdue=overdue, upcoming=upcoming)


@mentors.route('/profile-edit', methods=['GET', 'POST'])
@login_required
@mentor_required
def profile_edit():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
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
    form.phone.data = current_user.phone
    return render_template('mentor/profile-edit.html', student=current_user, form=form)


@mentors.route('/create_tasks', methods=['GET', 'POST'])
@login_required
@mentor_required
def create_tasks():
    form = TaskCreationForm()
    form.students.choices = [(student.id, student.name) for student in current_user.students]
    if form.validate_on_submit():
        for student_id in form.students.data:
            student = User.query.get(student_id)
            deadline = datetime.datetime(form.deadline.data.year, form.deadline.data.month, form.deadline.data.day)
            student.add_task(deadline=deadline, description=form.description.data, title=form.title.data)
        flash('Added the new tasks!')
        return redirect(url_for('.index'))
    return render_template('mentor/task_creation.html', form=form)


@mentors.route('/forum')
@login_required
@mentor_required
def forum():
    return render_template('mentor/forum.html')
