import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue(True) # change to some condition true for main.index

    def test_register_mentor(self):

        # register a new account
        response = self.client.post(url_for('mentors.signup'), data={
            'email': 'john@example.com',
            'password': 'cat'
        })
        self.assertTrue(response.status_code == 302)
        u = User.query.first()
        self.assertTrue(u.email == 'john@example.com')

    def test_login_student(self):
        u = User(email="alialtaf@gmail.com", password="hello", user_role="student")
        db.session.add(u)
        db.session.commit()
        u = User.query.first()
        # login with the new account
        response =self.client.post(url_for('main.login'), data={
            'email': 'alialtaf@gmail.com',
            'password': 'hello',
            'remember_me' : True
        }, follow_redirects=True)
        self.assertTrue('student' in response.data)
