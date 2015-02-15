import os
basedir = os.path.abspath(os.path.dirname(__file__))


from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager
from flask.ext import assets

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

    # Set up SASS compilation
    # NB: you may need to `sudo gem install sass` locally
    env = assets.Environment(app)
    # env.config['SASS_STYLE'] = 'compressed'
    # Tell assets where to look for scss files
    env.load_path = [os.path.join(basedir, 'assets/scss')]
    sass_bundle = assets.Bundle('main.scss', filters='scss', output='css/main.css')
    env.register('css_main', sass_bundle)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .students import students as students_blueprint
    app.register_blueprint(students_blueprint, url_prefix="/student")

    from .mentors import mentors as mentors_blueprint
    app.register_blueprint(mentors_blueprint, url_prefix="/mentor")

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/admin")

    return app
