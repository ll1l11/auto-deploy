# -*- coding: utf-8 -*-
from datetime import datetime

from flask_login import UserMixin
from .core import db
from .helpers import JSONSerializer


class User(UserMixin):
    def __init__(self):
        self.id = 1


class DeployScript(db.Model, JSONSerializer):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(191), unique=True)
    desc = db.Column(db.Text)
    cwd = db.Column(db.String(191))
    command = db.Column(db.String(191))
    enabled = db.Column(db.Boolean, default=True, server_default='1')
    insert_time = db.Column(db.DateTime, default=datetime.now)

    @classmethod
    def get_by_alias(cls, alias):
        return DeployScript.query.filter_by(alias=alias).first()
