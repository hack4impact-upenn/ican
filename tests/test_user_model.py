import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import User, University


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_match_mentor_basic(self):
        ''' tests match_with_mentor() with 1 simple student object and 1 simple mentor object '''
        s = User()
        s.user_role = 'student'
        s.name = 'studentName'
        db.session.add(s)
        m = User()
        m.user_role = 'mentor'
        m.name = 'mentorName'
        db.session.add(m)
        db.session.commit()
        s.match_with_mentor()
        self.assertTrue(s.mentor.name == m.name)

    def test_match_mentor_university(self):
        ''' 
        tests match_with_mentor() with 1 student and 2 mentors, 
        one of whom shares a university with student. 
        Expected output: s should match with m2
        '''
        s = User()
        s.user_role = 'student'
        s.name = 'studentName'
        db.session.add(s)
        m1 = User()
        m1.user_role = 'mentor'
        m1.name = 'mentor1'
        db.session.add(m1)
        m2 = User()
        m2.user_role = 'mentor'
        m2.name = 'mentor2'
        db.session.add(m2)
        u = University()
        u.name = 'Temple'
        u.users.append(s)
        u.users.append(m2)
        db.session.add(u)
        db.session.commit()
        s.match_with_mentor()
        self.assertTrue(s.mentor.name == m2.name)

    def test_match_mentor_fewestStudents(self):
        ''' 
        tests match_with_mentor() with 1 student and 2 mentors, 
        who all share a university, but mentor2 has fewer
        students than mentor1. 
        Expected output: s should match with m2
        '''
        s = User()
        s.user_role = 'student'
        s.name = 'studentName'
        m3 = User()
        m3.user_role = 'mentor'
        m3.name = 'mentor3'
        m4 = User()
        m4.user_role = 'mentor'
        m4.name = 'mentor4'
        u = University(name='Temple')
        u.users.append(s)
        u.users.append(m3)
        u.users.append(m4)
        m3.students.append(User())
        s.match_with_mentor()
        self.assertTrue(s.mentor.name == m4.name)

    