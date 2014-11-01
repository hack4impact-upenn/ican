from flask import Blueprint

mentors = Blueprint('mentors', __name__)

from . import views
