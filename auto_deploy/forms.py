# -*- coding: utf-8 -*-
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, TextAreaField)
from wtforms.validators import DataRequired, ValidationError

from .core import db
from .models import User, DeployScript


class LoginForm(FlaskForm):
    password = PasswordField('密码', [DataRequired()])
    submit = SubmitField('登录')

    def validate_password(self, field):
        if field.data != current_app.config['ADMIN_PASSWORD']:
            raise ValidationError('密码错误')
        self.user = User()


class DeployScriptForm(FlaskForm):
    alias = StringField('别名', [DataRequired()])
    desc = TextAreaField('描述')
    cwd = StringField('脚本路径')
    command = StringField('执行的命令', [DataRequired()],
                          render_kw={'placeholder': './deploy.sh'})
    enabled = BooleanField('启用')
    submit = SubmitField('提交')

    def put(self, alias):
        item = DeployScript.get_by_alias(alias)
        if not item:
            item = DeployScript(alias=alias)
        item.desc = self.desc.data
        item.cwd = self.cwd.data
        item.command = self.command.data
        item.enabled = self.enabled.data

        db.session.add(item)
        db.session.commit()
        return item
