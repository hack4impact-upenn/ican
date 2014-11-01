from . import db, login_manager
from flask.ext.login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    user_role = db.Column(db.String(15))
    phone = db.Column(db.Integer, unique=True, index=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mentor = db.relationship('User', backref='students', remote_side=[id])
    tasks = db.relationship('Task', backref='student', lazy='dynamic')

    def is_role(self, role):
        return self.user_role == role


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class GeneralTask(db.Model):
    __tablename__ = 'general_tasks'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'))


class University(db.Model):
    __tablename__ = 'universities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    tasks = db.relationship('GeneralTask', backref='university', lazy='dynamic')
