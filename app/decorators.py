from functools import wraps
from flask import abort
from flask.ext.login import current_user

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_role(role):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def student_required(f):
    return role_required("student")(f)

def mentor_required(f):
    return role_required("mentor")(f)

def admin_required(f):
    return role_required("admin")(f)
