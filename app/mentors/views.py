from . import mentors
from flask import render_template, session, redirect, url_for, current_app, flash
from flask.ext.login import login_required, current_user, login_user
from ..decorators import mentor_required
from forms import TaskCreationForm, EditProfileForm, ContactForm
from ..models import User
import datetime

@mentors.route('/')
def index():
    return render_template('mentor/menu.html')

@mentors.route('/signup')
# @mentors_required
def signup():
    return render_template('mentor/signup.html')

# TODO: modify - temporarily added by Annie
@mentors.route('/profile')
# @mentors_required
def profile():
    return render_template('mentor/profile.html')

@mentors.route('/tasks')
# @mentors_required
def tasks():
    return render_template('mentor/tasks.html')

@mentors.route('/students')
# @mentors_required
def students():
    return render_template('mentor/students.html')

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
# END OF TEMPORARY ADD

# @mentors.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = SignupForm()
#     if form.validate_on_submit():
#         mentor = Mentors.query.filter_by(email=form.email.data).first()
#         if mentor is None:
#             mentor = Mentor(email=form.email.data, name=form.name.data)
#             db.session.add(mentor)
#             return redirect(url_for('.index'))
#         else:
#             #throw some error and rerender form
#             return redirect(url_for('.index'))
#     return render_template('signup.html',
#                            form=form)

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
