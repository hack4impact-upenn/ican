from . import db, login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    user_role = db.Column(db.String(15))
    phone = db.Column(db.Integer, unique=True, index=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'))
    mentor = db.relationship('User', backref='students', remote_side=[id])
    tasks = db.relationship('Task', backref='student', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # add mentor matching and task addition here

    def is_role(self, role):
        return self.user_role == role

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def match_with_mentor(self):
        '''
        Matches self(role=student) with User(role=mentor)
        1) Tries to match based on shared university
        2) If student.university is None or university.mentors is None:
            matches student with any mentor with fewest students
        '''
        university = self.university
        possible_mentors = []
        if university:
            possible_mentors = [m for m in university.users.all() if m.user_role == 'mentor']
        if (university is None or len(possible_mentors) == 0):
            possible_mentors = [m for m in User.query.all() if m.user_role == 'mentor']
        if (len(possible_mentors) >= 1):
            min_mentor = possible_mentors[0]
            min_students = len(possible_mentors[0].students)
            for m in possible_mentors:
                if len(m.students) < min_students:
                    min_students = len(m.students)
                    min_mentor = m
            self.mentor = min_mentor



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
    #students = db.relationship('User', backref='university', lazy='dynamic')
    #mentors = db.relationship('User', backref='university', lazy='dynamic')
    users = db.relationship('User', backref='university', lazy='dynamic')
