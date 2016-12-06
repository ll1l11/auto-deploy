# -*- coding: utf-8 -*-
from werkzeug.local import LocalProxy
from flask import current_app

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


logger = LocalProxy(lambda: current_app.logger)
db = SQLAlchemy()
login_manager = LoginManager()
