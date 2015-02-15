#!/usr/bin/env python
import datetime
import os

from app import create_app, db
from app.models import User, Task, GeneralTask, University, FAQ
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Task=Task, GeneralTask=GeneralTask, University=University, FAQ=FAQ)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def populate():
  db.drop_all()
  db.create_all()

  #create university
  temple = University(name="Temple University")

  #create general tasks for temple
  gt_1 = GeneralTask(title="FAFSA", description="Max loves Hackuna Matata", deadline=datetime.datetime(2014,5,5), university=temple)
  gt_2 = GeneralTask(title="Housing Application", description="I love comic sans", deadline=datetime.datetime(2014,6,6), university=temple)
  gt_3 = GeneralTask(title="Scholarship Application", description="Ali is the best!!!!", deadline=datetime.datetime(2014,12,5), university=temple)
  gt_4 = GeneralTask(title="Speak to Advisor", description="WOOOOOOOOOO!!!!!", deadline=datetime.datetime(2014,12,7), university=temple)

  #create mentor
  annie = User(name="Annie Meng", email="anniezmeng@gmail.com", phone='1234567890', password="password", user_role="mentor", university=temple, bio="Lorem ipsum dolor sit amet praesent. Libero vehicula turpis. Neque fermentum augue rutrum accumsan eget pretium sapien eu. Sed sed similique sed turpis suscipit rhoncus justo sapien faucibus commodo nibh. Velit aliquet pellentesque turpis eget in. Arcu eu nec. Nulla sollicitudin quis. In placerat eleifend vestibulum animi nullam amet ipsum lorem et a habitant. Feugiat pellentesque inceptos. Nulla vel cursus. Pulvinar pede augue amet nibh tempus. Leo at sollicitudin. Sit amet quo. Viverra integer nullam felis bibendum lectus. Nulla accumsan ut curabitur velit sollicitudin nam nisl felis. Aliquam aenean exercitation diam facilisis mauris. Nulla sit sollicitudin morbi sit commodo arcu.")

  #create students
  max_mc = User(name="Max McCarthy", email="maxllmcc@icloud.com", password="password", phone='2234567890', user_role="student",university=temple)
  max_mc.mentor = annie

  maya = User(name="Maya Ebsworth", email="maya.ebsworth@gmail.com", password="password", phone='3234567890', user_role="student", university=temple)
  maya.mentor = annie

  ayush = User(name="Ayush Goyal", email="ayush.goy01@gmail.com", password="password", phone='4234567890', user_role="student", university=temple)
  ayush.mentor = annie

  ali = User(name="Ali Altaf", email="admin@gmail.com", password="password", user_role="admin")

  #assign tasks to students
  max_1 = Task(title="FAFSA", description="Max loves Hackuna Matata", deadline=datetime.datetime(2014,5,5), student=max_mc, completed=True)
  max_2 = Task(title="Housing Application", description="I love comic sans", deadline=datetime.datetime(2014,6,6), student=max_mc, completed=True)
  max_3 = Task(title="Scholarship Application", description="Ali is the best!!!!", deadline=datetime.datetime(2014,12,5), student=max_mc)
  max_4 = Task(title="Speak to Advisor", description="WOOOOOOOOOO!!!!!", deadline=datetime.datetime(2014,12,7), student=max_mc)

  maya_1 = Task(title="FAFSA", description="maya loves Hackuna Matata", deadline=datetime.datetime(2014,5,5), student=maya)
  maya_2 = Task(title="Housing Application", description="I love comic sans", deadline=datetime.datetime(2014,6,6), student=maya)
  maya_3 = Task(title="Scholarship Application", description="Ali is the best!!!!", deadline=datetime.datetime(2014,12,5), student=maya)
  maya_4 = Task(title="Speak to Advisor", description="WOOOOOOOOOO!!!!!", deadline=datetime.datetime(2014,12,7), student=maya)

  ayush_1 = Task(title="FAFSA", description="ayush loves Hackuna Matata", deadline=datetime.datetime(2014,5,5), student=ayush)
  ayush_2 = Task(title="Housing Application", description="I love comic sans", deadline=datetime.datetime(2014,6,6), student=ayush, completed=True)
  ayush_3 = Task(title="Scholarship Application", description="Ali is the best!!!!", deadline=datetime.datetime(2014,12,5), student=ayush)
  ayush_4 = Task(title="Speak to Advisor", description="WOOOOOOOOOO!!!!!", deadline=datetime.datetime(2014,12,7), student=ayush)

  faq_1 = FAQ(question="Hello?", answer="Hello.")
  faq_2 = FAQ(question="Sup?", answer="Sup.")
  faq_3 = FAQ(question="???", answer="...")

  db.session.add(temple)

  db.session.add(annie)

  db.session.add(max_mc)
  db.session.add(maya)
  db.session.add(ayush)
  db.session.add(ali)

  db.session.add(gt_1)
  db.session.add(gt_2)
  db.session.add(gt_3)
  db.session.add(gt_4)

  db.session.add(max_1)
  db.session.add(max_2)
  db.session.add(max_3)
  db.session.add(max_4)

  db.session.add(maya_1)
  db.session.add(maya_2)
  db.session.add(maya_3)
  db.session.add(maya_4)

  db.session.add(ayush_1)
  db.session.add(ayush_2)
  db.session.add(ayush_3)
  db.session.add(ayush_4)

  db.session.add(faq_1)
  db.session.add(faq_2)
  db.session.add(faq_3)

@manager.command
def deploy():
  from flask.ext.migrate import upgrade

  upgrade()

if __name__ == '__main__':
    manager.run()
