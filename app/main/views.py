from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm
from . import main

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            if user.is_role("admin"):
                return url_for('admin.index')
            elif user.is_role("student"):
                return url_form('students.index')
            else:
                return url_for('mentors.index')
        flash('Invalid username or password.')
    return render_template('login.html', form=form)
