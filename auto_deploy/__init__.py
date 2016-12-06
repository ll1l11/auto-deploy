# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap

from .helpers import register_blueprints
from .core import db, login_manager
from .models import User


def create_app(conf=None):
    app = Flask(__name__)
    if not conf:
        conf = 'auto_deploy.config'
    app.config.from_object(conf)

    Bootstrap(app)
    db.init_app(app)

    # init flask_login
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'
    register_auth(app)

    # register blueprints
    module_prefix = __name__ + '.views.'
    package_path = app.root_path + '/views'
    register_blueprints(app, module_prefix, package_path)

    return app


def register_auth(app):
    @login_manager.user_loader
    def load_user(user_name):
        return User()
