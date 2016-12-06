# -*- coding: utf-8 -*-
"""manage deploy scirpts"""
from flask import Blueprint, jsonify, render_template, abort
from flask.views import MethodView
from flask_login import login_required

from ..core import db
from ..models import DeployScript
from ..forms import DeployScriptForm


bp = Blueprint('script', __name__)


class ItemView(MethodView):

    decorators = [login_required]

    def get(self, alias):
        if alias:
            item = DeployScript.get_by_alias(alias)
            if not item:
                abort(404)
            form = DeployScriptForm(obj=item)
        else:
            form = DeployScriptForm()
            form.enabled.data = True
        return render_template('put.html', form=form)

    def put(self, alias):
        form = DeployScriptForm()
        if form.validate_on_submit():
            item = form.put(alias)
            return jsonify(item.to_json())
        else:
            return jsonify(
                errcode=1,
                errmsg='form validation error',
                errors=form.errors
            )

    def delete(self, alias):
        item = DeployScript.get_by_alias(alias)
        if not item:
            abort(404)
        db.session.delete(item)
        db.session.commit()
        return '', 204


view_func = ItemView.as_view('item')
bp.add_url_rule(
    '/scripts/',
    defaults={'alias': None},
    view_func=view_func,
    methods=['GET']
)
bp.add_url_rule(
    '/scripts/<alias>',
    view_func=view_func,
    methods=['GET', 'PUT', 'DELETE']
)
