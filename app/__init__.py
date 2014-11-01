from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.scss import Scss
from config import config
from flask.ext.login import LoginManager

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    Scss(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .students import students as students_blueprint
    app.register_blueprint(students_blueprint, url_prefix="/students")

    from .mentors import mentors as mentors_blueprint
    app.register_blueprint(students_blueprint, url_prefix="/mentors")

    from .admin import admin as admin_blueprint
    app.register_blueprint(students_blueprint, url_prefix="/admin")

    return app
