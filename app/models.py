from . import db

'''
    Mentor has id, name, email, phone #, and list of students
'''
class Mentor(db.Model):
    __tablename__ = 'mentors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    phone = db.Column(db.Integer, unique=True, index=True)

    students = db.relationship('Student', backref='mentor', lazy='dynamic')

    def __repr__(self):
        return '<Mentor %r>' % self.email

    # def get_students(self):
    #     return self.students.all()

    # def add_student(self, s):
    #     self.students.append(s)

'''
    Student has id(Integer), name(String), email(String), phone(Integer), 
    mentor(Mentor), and list of tasks[(Task)]
'''
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    phone = db.Column(db.Integer, unique=True, index=True)

    tasks = db.relationship('Task', backref='student', lazy='dynamic')

    mentor_id = db.Column(db.Integer, db.ForeignKey('mentors.id'))

    def __repr__(self):
        return '<Student %r>' % self.email

'''
    University has name(String), tasks([(Task)]), students([Student])
'''
class University(db.Model):
    name = db.Column(db.String(64))
    tasks = db.relationship('Task')

'''
    Task has description(Text), deadline(DateTime), student(Student), completed(Boolean)
'''
class Task(db.Model):
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

'''
    General Task has a description(Text), deadline(DateTime), university(String)
'''
class General_Task(db.Model):
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    university = db.Column(db.String(64))
    # if university is None, task is general & will be assigned to all students
    # else task will be specific and assigned to students going to university



