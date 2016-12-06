# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.views import MethodView
from flask_login import login_required

from ..models import DeployScript


bp = Blueprint('general', __name__)


class IndexView(MethodView):
    decorators = [login_required]

    def get(self):
        items = DeployScript.query.order_by(DeployScript.id.desc()).all()
        return render_template('index.html', items=items)


bp.add_url_rule('/', view_func=IndexView.as_view('index'))
