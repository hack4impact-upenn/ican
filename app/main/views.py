from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import Student
from ..email import send_email
from . import main
from .forms import SignupForm, LoginForm


# @backend TODO check
@main.route('/')
def landing():
    return render_template('index.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form_signup = SignupForm()
    if form_signup.validate_on_submit():
        student = Student.query.filter_by(email=form_signup.email.data).first()
        if student is None:
            student = Student(email=form_signup.email.data, name=form_signup.name.data)
            db.session.add(student)
            return redirect(url_for('.menu'))
        else:
            #throw some error and rerender form
            return redirect(url_for('.menu'))
    return render_template('index.html',
                           form=form_signup)

# @backend TODO check
@main.route('/login', methods=['GET', 'POST'])
def login():
    form_login = LoginForm()
    if form_login.validate_on_submit():
        student = Student.query.filter_by(email=form_login.email.data).first()
        if student is None:
            student = Student(email=form_login.email.data, name=form_login.name.data)
            db.session.add(student)
            return redirect(url_for('.menu'))
        else:
            #throw some error and rerender form
            return redirect(url_for('.menu'))
    return render_template('index.html',
                           form=form_login)

@main.route('/menu')
def index():
    return render_template('menu.html')
