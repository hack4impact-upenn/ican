from . import mentors
from flask import render_template, session, redirect, url_for, current_app
from flask.ext.login import login_required
from ..decorators import mentor_required
from forms import TaskCreationForm

@mentors.route('/')
def index():
    return render_template('mentor/menu.html')

@mentors.route('/signup')
# @mentors_required
def signup():
    return render_template('mentor/signup.html')




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
# @login_required
# @mentor_required
def create_tasks():
    form = TaskCreationForm()
    return render_template('mentor/task_creation.html', form=form)
