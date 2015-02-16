import datetime

from . import students
from ..models import User, FAQ, Task, University, GeneralTask
from .. import db
from ..decorators import student_required
from forms import SignupForm, ContactForm, EditProfileForm, CompletedTaskForm, \
    UncompletedTaskForm
from ..email import send_email

from flask import render_template, redirect, url_for, flash
from flask.ext.login import login_required, current_user, login_user

@students.route('/')
@login_required
@student_required
def index():
    ordered_tasks = current_user.tasks.filter_by(completed=False).order_by(
        Task.deadline).all()
    return render_template('student/menu.html', student=current_user,
                           date=datetime.datetime, tasks=ordered_tasks)


@students.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    form.university.choices = [(u.id, u.name) for u in University.query.all()]
    if form.validate_on_submit():
        student = User.query.filter_by(email=form.email.data).first()
        if student is None:
            u = University.query.get(form.university.data)
            student = User(email=form.email.data, name=form.name.data,
                           university=u, password=form.password.data,
                           phone=form.phone.data,
                           user_role='student')
            general_tasks = GeneralTask.query.all()
            for gt in general_tasks:
                if (gt.university_id == u.id) or (gt.university_id is None):
                    new_task = Task(title=gt.title, description=gt.description,
                                    deadline=gt.deadline, user_id=student.id)
                    student.tasks.append(new_task)

            student.match_with_mentor()
            db.session.add(student)
            db.session.commit()
            login_user(student)
            return redirect(url_for('.index'))
        else:
            # throw some error and rerender form
            return redirect(url_for('.index'))
    return render_template('student/signup.html', form=form)


@students.route('/tasks')
@login_required
@student_required
def tasks():
    ordered_tasks = current_user.tasks.filter_by(completed=False).order_by(
        Task.deadline).all()
    num_completed = current_user.tasks.filter_by(completed=True).count()
    days_until_due = map(lambda t: (t.deadline - datetime.datetime.now()).days,
                         ordered_tasks)
    task_list = zip(ordered_tasks, days_until_due)
    print days_until_due
    return render_template('student/tasks.html',
                           student=current_user,
                           tasks=task_list,
                           num_completed=num_completed,
                           date=datetime.datetime.now())


@students.route('/tasks/completed')
@login_required
@student_required
def completed_tasks():
    ordered_tasks = current_user.tasks.filter_by(completed=True).order_by(
        Task.deadline).all()
    return render_template('student/tasks-completed.html', tasks=ordered_tasks,
                           student=current_user)


@students.route('/task/<task_id>', methods=['GET', 'POST'])
@login_required
@student_required
def task_view(task_id):
    task = Task.query.get(task_id)
    form = CompletedTaskForm()
    if form.validate_on_submit():
        task.complete_task()
        flash('You have completed ' + task.title)
        return redirect(url_for('.index'))
    return render_template('student/task-edit.html', task=task, form=form)


@students.route('/tasks/completed/<task_id>', methods=['GET', 'POST'])
@login_required
@student_required
def completed_view(task_id):
    task = Task.query.get(task_id)
    form = UncompletedTaskForm()
    if form.validate_on_submit():
        task.uncomplete_task()
        flash(task.title + ' has been marked as incomplete')
        return redirect(url_for('.index'))
    return render_template('student/task-edit.html', task=task, form=form)


@students.route('/mentor')
@login_required
@student_required
def mentor():
    return render_template('student/mentor.html', student=current_user,
                           mentor=current_user.mentor)


@students.route('/faq')
@login_required
@student_required
def faq():
    return render_template('student/faq.html', faqs=FAQ.query)


@students.route('/profile')
@login_required
@student_required
def profile():
    return render_template('student/profile.html', student=current_user)


@students.route('/profile-edit', methods=['GET', 'POST'])
@login_required
@student_required
def profile_edit():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        if form.new_password.data and form.current_password.data:
            if current_user.verify_password(form.current_password.data):
                current_user.password = form.new_password.data
                db.session.add(current_user)
                db.session.commit()
                flash('Your profile has been updated')
            else:
                flash('Invalid current password; password not updated')
        else:
            db.session.add(current_user)
            db.session.commit()
            flash('Your profile has been updated')
        return redirect(url_for('.index'))
    form.name.data = current_user.name
    form.email.data = current_user.email
    form.phone.data = current_user.phone
    return render_template('student/profile-edit.html', student=current_user,
                           form=form)


@students.route('/college')
@login_required
@student_required
def college():
    return render_template('student/college.html',
                           college=current_user.university)


@students.route('/contact', methods=['GET', 'POST'])
@login_required
@student_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_email("sarsimon@sas.upenn.edu", 'An iCAN student has reached out!',
                   'email/contact', email_body=form.message)
        flash('Your email has been sent to iCAN! They\'ll respond shortly!')
        return redirect(url_for('.index'))
    return render_template('student/contact.html', form=form)

@students.route('/forum')
def forum():
    return render_template('student/forum.html')
