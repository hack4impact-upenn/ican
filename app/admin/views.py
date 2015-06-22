import datetime

from . import admin
from ..models import User, University, GeneralTask, FAQ, Task
from flask import render_template, session, redirect, url_for, current_app, flash
from .. import db
from forms import ReassignForm, EditTaskForm, TaskCreationForm, EditFAQForm, FAQCreationForm, EditUniversityForm
from ..decorators import admin_required
from ..email import send_text

from flask.ext.login import login_required

@admin.route('/')
@login_required
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/mentors')
@login_required
@admin_required
def mentors():
    mentors = User.query.filter_by(user_role="mentor").all()
    return render_template('admin/mentors.html', mentors=mentors)

@admin.route('/students')
@login_required
@admin_required
def students():
    students = User.query.filter_by(user_role="student").all()
    return render_template('admin/students.html', students=students)

@admin.route('/reassign/<student_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def reassign(student_id):
    form = ReassignForm()
    student = User.query.get(student_id)
    form.mentor.choices = [(m.id,m.name) for m in User.query.filter_by(user_role="mentor").all()]
    if form.validate_on_submit():
        mentor = User.query.get(form.mentor.data)
        student.mentor = mentor
        db.session.add(student)
        db.session.commit()
        flash("Reassigned " + student.name)
        return redirect(url_for('.index'))

    return render_template('admin/reassign.html', form=form, student=student)

@admin.route('/universities')
@login_required
@admin_required
def universities():
    universities = University.query.all()
    return render_template('admin/universities.html', universities=universities)

@admin.route('/universities/edit/<university_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_universities(university_id):
    university = University.query.filter_by(id=university_id).first()
    form = EditUniversityForm(obj=university)
    if form.validate_on_submit():
        description = form.description.data
        university.description = description
        db.session.add(university)
        db.session.commit()
        flash("Edited description for " + university.name)
        return redirect(url_for('.index'))
    return render_template('admin/edit_universities.html', university=university, form=form)

@admin.route('/tasks')
@login_required
@admin_required
def tasks():
    tasks = GeneralTask.query.all()
    return render_template('admin/tasks.html', tasks=tasks)

@admin.route('/tasks/edit/<task_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_task(task_id):
    task = GeneralTask.query.get(task_id)
    form = EditTaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.deadline = form.deadline.data
        db.session.add(task)
        db.session.commit()
        flash("Successfully edited task")
        return redirect(url_for('.index'))
    return render_template('admin/edit_task.html', form=form)

@admin.route('/tasks/delete/<task_id>')
@login_required
@admin_required
def delete_task(task_id):
    task = GeneralTask.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Deleted task")
    return redirect(url_for('.tasks'))

@admin.route('/tasks/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_task():
    form = TaskCreationForm()
    form.universities.choices = [(university.id, university.name) for university in University.query.all()]
    form.universities.choices.append((-1, "All"))
    if form.validate_on_submit():
        if -1 in form.universities.data:
            new_task = GeneralTask()
            new_task.title = form.title.data
            new_task.description = form.description.data
            new_task.deadline = form.deadline.data
            db.session.add(new_task)
            db.session.commit()
        else:
            for university in form.universities.data:
                new_task = GeneralTask()
                new_task.title = form.title.data
                new_task.description = form.description.data
                new_task.deadline = form.deadline.data
                new_task.university_id = university
                db.session.add(new_task)
                db.session.commit()
        flash("Successfully created task")
        return redirect(url_for(".tasks"))
    return render_template('admin/create_task.html', form=form)

@admin.route('/faqs')
@login_required
@admin_required
def faqs():
    faqs = FAQ.query.all()
    return render_template('admin/faqs.html', faqs=faqs)

@admin.route('/faqs/edit/<faq_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_faq(faq_id):
    faq = FAQ.query.get(faq_id)
    form = EditFAQForm(obj=faq)
    if form.validate_on_submit():
        faq.question = form.question.data
        faq.answer = form.answer.data
        db.session.add(faq)
        db.session.commit()
        flash("Successfully edited FAQ")
        return redirect(url_for('.index'))
    return render_template('admin/edit_faq.html', form=form)

@admin.route('/faqs/delete/<faq_id>')
@login_required
@admin_required
def delete_faq(faq_id):
    faq = FAQ.query.get(faq_id)
    db.session.delete(faq)
    db.session.commit()
    flash("Deleted FAQ")
    return redirect(url_for('.faqs'))

@admin.route('/faqs/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_faq():
    form = FAQCreationForm()
    if form.validate_on_submit():
        new_faq = FAQ()
        new_faq.question = form.question.data
        new_faq.answer = form.answer.data
        db.session.add(new_faq)
        db.session.commit()
        flash("Successfully created FAQ")
        return redirect(url_for(".faqs"))
    return render_template('admin/create_faq.html', form=form)


@admin.route('/send_reminders')
def send_reminders():

    for student in User.query.filter_by(user_role="student").all():
        tasks = student.tasks.filter_by(completed=False).order_by(Task.deadline).all()
        for task in tasks:
            deadline_now_diff = task.deadline - datetime.datetime.now()
            if deadline_now_diff < datetime.timedelta(1):
                send_text(student.phone, "Hello there! " + task.title + " is due in less than 24 hours!")
    return 'Reminders sent.'

