from flask import render_template, session, redirect, url_for, current_app
from .. import db
# from ..models import Student
from ..email import send_email
from . import main

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

