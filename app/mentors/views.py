from . import mentors
from flask import render_template, session, redirect, url_for, current_app
from flask.ext.login import login_required, current_user, login_user
from ..decorators import mentor_required
from forms import TaskCreationForm, EditProfileForm, SignupForm, ContactForm
from ..models import User, University

import datetime

@mentors.route('/')
def index():
    return render_template('mentor/menu.html')


@mentors.route('/signup', methods=['GET', 'POST'])
# @mentors_required
def signup():
    form = SignupForm()
    form.university.choices = [(u.id,u.name) for u in University.query.all()]
    if form.validate_on_submit():
        userTest = User.query.filter_by(email=form.email.data).first()
        if userTest is None:
            u = University.query.get(form.university.data)
            user = User(email=form.email.data,
                        username=form.username.data,
                        university=u,
                     password=form.password.data)
            db.session.add(user)
            db.session.commit()
        else:
            flash("This Username/Password is already in use.")
            return redirect(url_for('.index'))
    return render_template('mentor/signup.html', form = form)

# TODO: modify - temporarily added by Annie
@mentors.route('/profile')
# @mentors_required
def profile():
    return render_template('mentor/profile.html')

@mentors.route('/tasks')
# @mentors_required
def tasks():
    taskList = self.get_all_tasks_list()
    return render_template('mentor/tasks.html', tasks = taskList, date=datetime.datetime.now())

@mentors.route('/students')
# @mentors_required
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

@mentors.route('/students/<student_id>')
def student(student_id):
    form = ContactForm()
    student = User.query.get(student_id)
    if form.validate_on_submit():
        name = student.name
        flash(name + ' has been sent a message!')
        #TODO Send text to user
        return render_template('mentor/students.html')
    return render_template('mentor/overview.html', form=form, student=student, date=datetime.datetime)

@mentors.route('/profile-edit', methods=['GET', 'POST'])
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
    return render_template('mentor/profile-edit.html', student=current_user, form=form)



@mentors.route('/create_tasks', methods=['GET', 'POST'])
@login_required
@mentor_required
def create_tasks():
    form = TaskCreationForm()
    form.students.choices = [(student.id, student.name) for student in current_user.students]
    if form.validate_on_submit():
        pass
        print form.students.data
    else:
       pass
    return render_template('mentor/task_creation.html', form=form)
