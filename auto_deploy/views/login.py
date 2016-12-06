# -*- coding: utf-8 -*-
from urllib.parse import urlparse, urljoin
from flask import Blueprint, request, url_for, redirect, render_template, abort
from flask.views import View, MethodView
from flask_login import login_user, logout_user

from ..forms import LoginForm


bp = Blueprint('login', __name__)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


class LoginView(View):
    def dispatch_request(self):
        # Here we use a class of some kind to represent and validate our
        # client-side form data. For example, WTForms is a library that will
        # handle this for us, and we use a custom LoginForm to validate.
        form = LoginForm()
        if form.validate_on_submit():
            # Login and validate the user.
            # user should be an instance of your `User` class
            login_user(form.user)

            next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('general.index'))

        return render_template('login.html', form=form)


class LogoutView(MethodView):
    def get(self):
        logout_user()
        return 'Logged out'


bp.add_url_rule('/login', view_func=LoginView.as_view('login'),
                methods=['GET', 'POST'])
bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
