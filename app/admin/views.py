from . import admin
from flask import render_template, session, redirect, url_for, current_app

@admin.route('/')
def index():
    return render_template('index.html')
